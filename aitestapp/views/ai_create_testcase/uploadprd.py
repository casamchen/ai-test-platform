from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from aitestapp import models
from aitestapp.tool.cipher import Cipherd
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt  # API 接口使用 Session 认证，无需 CSRF
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from docx import Document
import os, json, time
from PyPDF2 import PdfReader
from celery.result import AsyncResult
from django.views.decorators.http import require_http_methods
from aitestapp.views.ai_create_testcase.task import generate_testcases
import logging

logger = logging.getLogger(__name__)

# 允许的文件扩展名白名单，防止上传恶意文件
ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc'}

def is_safe_filename(filename):
    """检查文件名是否安全（防止路径遍历攻击）"""
    if not filename:
        return False
    # 禁止路径遍历字符和特殊字符
    dangerous_chars = ['..', '/', '\\', '\0', '|', ';', '&', '$', '`', '(', ')', '{', '}']
    for char in dangerous_chars:
        if char in filename:
            return False
    return True

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def uploadprd(request):
    response = {}
    UPLOAD_DIRECTORY = 'data'
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)


    file = request.FILES.get('file') # 获取前端通过el-upload上传的文件
    if not file:
        return JsonResponse({'error': '未接收到文件'}, status=400)

    # 验证文件扩展名
    file_ext = os.path.splitext(file.name)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return JsonResponse({'error': f'不支持的文件类型: {file_ext}'}, status=400)

    # 验证文件名安全性
    if not is_safe_filename(file.name):
        return JsonResponse({'error': '文件名包含非法字符'}, status=400)

    # 通过文件保存的库FileSystemStorage保存文件
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, UPLOAD_DIRECTORY))
    filename = fs.save(file.name, file) # 根据对应文件名生成保存的文件名
    file_path = os.path.join(UPLOAD_DIRECTORY, filename) # 获取文件的保存本地路径
    logger.info(f"文件已保存: {file_path}")

    response['path'] = file_path # 返回保存路径给前端
    response['file_name'] = filename # 返回文件名给前端
    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def uploadprd_info(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)
    

    file_path = request.POST.get('file_path')
    prd_name = request.POST.get('file')
    project_name = request.POST.get('project_name')
    version = request.POST.get('version')
    function = request.POST.get('function')
    models.FileInfo.objects.create( # 根据前端传过来的数据存入数据库中
        project_name = project_name,
        version = version,
        function = function,
        prd_name = prd_name,
        file_path = file_path
    )

    response['msg'] = 'uploaded' # 返回uploaded信息给前端进行判断
    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def showfile_content(request):
    response = {}
    file_id = request.POST.get('id') # 获取传过来的id

    # 验证 file_id 是否为纯数字（防止注入）
    if not file_id or not file_id.isdigit():
        return JsonResponse({'error': '无效的文件ID'}, status=400)

    logger.info(f"查看文件内容: id={file_id}")
    # 在fileinfo表中根据对应id查找file_path和prd_name
    try:
        file_pathcheck = models.FileInfo.objects.filter(id=file_id).values('file_path', 'prd_name')
        if not file_pathcheck.exists() or len(file_pathcheck) == 0:
            return JsonResponse({'error': '文件记录不存在'}, status=404)
        file_path = file_pathcheck[0]['file_path']
        file_name = file_pathcheck[0]['prd_name']
    except Exception as e:
        logger.error(f"查询文件信息失败: {e}")
        return JsonResponse({'error': '查询文件信息失败'}, status=500)

    # 初始化content_type变量
    content_type = 'application/octet-stream'  # 默认为通用二进制流类型
    # 使用 settings.MEDIA_ROOT 构建路径，避免硬编码
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)

    if os.path.exists(file_path):
    # 根据文件后缀设置Content-Type
        if file_name.lower().endswith('.pdf'):
            content_type = 'application/pdf'
            try:
                with open(file_path, 'rb') as file_content:
                    file_content_str = PdfReader(file_content)
                    # 获取页面数量
                    num_pages = len(file_content_str.pages)
                    # 初始化HTML内容
                    html_content = '<html><body>'
                    # 遍历每个页面
                    for page_num in range(num_pages):
                        # 获取页面内容
                        page = file_content_str.pages[page_num]
                        # 获取文本内容
                        text = page.extract_text()
                        # 对文本进行 HTML 转义，防止 XSS
                        import html as html_escape
                        safe_text = html_escape.escape(text) if text else ''
                        # 添加到HTML内容中
                        html_content += '<p>{}</p>'.format(safe_text)
                    # 添加结束标签
                    html_content += '</body></html>'
                    response['Content-Disposition'] = f"attachment; filename*=UTF-8''{file_name}"
                    response = HttpResponse(html_content, content_type=content_type)
            except Exception as e:
                logger.error(f"PDF解析失败: {e}")
                return JsonResponse({'error': f'PDF解析失败: {str(e)}'}, status=500)

        elif file_name.lower().endswith(('.docx')):
            content_type = 'application/msword'
            try:
                doc = Document(file_path)
                # 将Word内容转换为HTML
                html_content = '<html><body>'
                for para in doc.paragraphs:
                    # 对文本进行 HTML 转义，防止 XSS
                    import html as html_escape
                    safe_text = html_escape.escape(para.text)
                    html_content += '<p>{}</p>'.format(safe_text)
                html_content += '</body></html>'
                response['Content-Disposition'] = f"attachment; filename*=UTF-8''{file_name}"
                response = HttpResponse(html_content, content_type=content_type)
            except Exception as e:
                logger.error(f"DOCX解析失败: {e}")
                return JsonResponse({'error': f'DOCX解析失败: {str(e)}'}, status=500)

        elif file_name.lower().endswith(('.doc')):
            content_type = 'application/msword'
            # 输出文件路径 - 使用 MEDIA_ROOT 目录，避免硬编码
            output_dir = os.path.join(settings.MEDIA_ROOT, 'document')
            os.makedirs(output_dir, exist_ok=True)  # 确保目录存在
            output_file_path = os.path.join(output_dir, f'{file_id}.docx')

            # 安全地使用 subprocess，禁用 shell 注入
            try:
                # 使用 subprocess.run 并设置 shell=False 防止命令注入
                result = subprocess.run(
                    ['unoconv', '-f', 'docx', '-o', output_file_path, file_path],
                    capture_output=True,
                    text=True,
                    timeout=30  # 设置超时防止挂起
                )
                if result.returncode != 0:
                    logger.error(f"unoconv转换失败: {result.stderr}")
                    return JsonResponse({'error': '文件转换失败'}, status=500)

                # 读取转换后的文件
                with open(output_file_path, 'rb') as f:
                    content_bytes = f.read()

                # 将 Word 内容转换为 HTML（使用 python-docx 解析 bytes）
                from io import BytesIO
                doc = Document(BytesIO(content_bytes))
                import html as html_escape
                html_content = '<html><body>'
                for para in doc.paragraphs:
                    safe_text = html_escape.escape(para.text)
                    html_content += '<p>{}</p>'.format(safe_text)
                html_content += '</body></html>'
                response['Content-Disposition'] = f"attachment; filename*=UTF-8''{file_name}"
                response = HttpResponse(html_content, content_type=content_type)

                # 清理临时文件
                try:
                    os.remove(output_file_path)
                except OSError:
                    pass

            except subprocess.TimeoutExpired:
                logger.error("文件转换超时")
                return JsonResponse({'error': '文件转换超时'}, status=408)
            except Exception as e:
                logger.error(f"DOC处理失败: {e}")
                return JsonResponse({'error': f'文件处理失败: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': '文件不存在'}, status=404)

    return response

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def create_testcase(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)
    
    prd_name = request.POST.get('prd_name')
    project_name = request.POST.get('project_name')
    version = request.POST.get('version')
    testcaseid = request.POST.get('id')
    print(f'prd_name:{prd_name}, project_name:{project_name}, version:{version}, testcaseid: {testcaseid}')

    doc_content = models.vectors.objects.filter().values('text')
    text_values = [record['text'] for record in doc_content]
   # 调用异步任务
    task = generate_testcases.delay(text_values, project_name, version, testcaseid)

    response['code'] = 0
    response['msg'] = '任务已提交，正在处理中'
    response['task_id'] = task.id

    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def check_task_status(request):
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    task_id = request.POST.get('task_id')
    if not task_id:
        return JsonResponse({'error': '缺少 task_id 参数'}, status=400)

    try:
        result = AsyncResult(task_id)
        logger.info(f"查询任务状态: {task_id}, 状态: {result.status}")
        response = {
            'status': result.status,
            'result': result.result if result.ready() else None
        }
    except Exception as e:
        logger.error(f"查询任务状态失败: {e}")
        response = {
            'status': 'FAILURE',
            'result': f'查询失败: {str(e)}'
        }

    return JsonResponse(response)