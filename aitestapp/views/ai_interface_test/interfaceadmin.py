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
import os, json
import logging

logger = logging.getLogger(__name__)
from PyPDF2 import PdfReader
from aitestapp.views.AI.sdk import zhipu_ai
from aitestapp.views.AI.config import API_key
# from zhipuai import ZhipuAI

@require_http_methods(['GET'])
def check_interface_info(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)
    

    try:
        checkdata = models.InterfaceFileInfo.objects.filter().values().order_by('-create_time')
        response['code'] = 0
        response['msg'] = list(checkdata)
    except Exception as e:
        response['code'] = 1
        response['msg'] = f'获取接口信息失败: {str(e)}'
    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def upload_interface_file(request):
    response = {}
    UPLOAD_DIRECTORY = 'interface_file'
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)
    
    file = request.FILES.get('file')  # 获取前端通过el-upload上传的文件
    if not file:
        return JsonResponse({'code': 1, 'msg': '未接收到上传文件'})

    # 验证文件类型
    allowed_extensions = ['.docx']
    file_ext = os.path.splitext(file.name)[1].lower()
    if file_ext not in allowed_extensions:
        return JsonResponse({'code': 1, 'msg': '不支持的文件类型，仅支持 .docx 文件'})
    # 通过文件保存的库FileSystemStorage保存文件
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, UPLOAD_DIRECTORY))
    filename = fs.save(file.name, file) # 根据对应文件名生成保存的文件名
    file_path = os.path.join(UPLOAD_DIRECTORY, filename) # 获取文件的保存本地路径
    print(file_path)

    response['path'] = file_path # 返回保存路径给前端
    response['file_name'] = filename # 返回文件名给前端
    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def upload_interface_info(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)
    
    file_path = request.POST.get('file_path')
    prd_name = request.POST.get('file')
    project = request.POST.get('project_name')
    version = request.POST.get('version')
    remark = request.POST.get('remark')
    models.InterfaceFileInfo.objects.create( # 根据前端传过来的数据存入数据库中
        project = project,
        version = version,
        remark = remark,
        prd_name = prd_name,
        path = file_path
    )

    response['code'] = 0
    response['msg'] = 'uploaded'  # 返回uploaded信息给前端进行判断
    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def show_interface_content(request):
    response = {}
    file_id = request.POST.get('id') # 获取传过来的id

    # 验证 file_id 是否为纯数字
    if not file_id or not file_id.isdigit():
        return JsonResponse({'code': 1, 'msg': '无效的文件ID'}, status=400)

    try:
        # 在interface_fileinfo表中根据对应id查找file_path
        file_pathcheck = models.InterfaceFileInfo.objects.filter(id=file_id).values('id','path')
        if not file_pathcheck.exists() or len(file_pathcheck) == 0:
            return JsonResponse({'code': 1, 'msg': '文件记录不存在'}, status=404)

        fileinfo_id = models.InterfaceFileInfo.objects.get(id=file_id)
        file_path = file_pathcheck[0]['path']
        file_path = os.path.join(settings.MEDIA_ROOT, file_path)

        doc = Document(file_path) # 读取文档内容
        api_data = {} # 创建空字典
        api_list = [] # 创建空列表
        # 遍历文档中的所有段落
        for _,para in enumerate(doc.paragraphs):
            para_text = para.text.strip()
            if not para_text or ':' not in para_text:
                continue  # 跳过空行或不含冒号的行，防止 ValueError

            j,k = para.text.split(':', 1) # 以"："为分割点分割出key和value
            api_data[j.strip()] = k.strip() # 将分割出来的key和value添加到空字典中

            if len(api_data) == 8: # 当字典长度达到8的时候，将字典添加到空列表中，并且重置字典为空字典，以免重复
                api_list.append(api_data)
                api_data = {}

        for db_data in api_list: # 遍历列表中的字典，通过get_or_create来查询或者创建对应的内容到数据库，避免重复添加
            models.InterfaceApiInfo.objects.get_or_create(
                example = db_data.get('example', ''),
                response = db_data.get('Responses', ''),
                title = db_data.get('title', ''),
                url = db_data.get('url', ''),
                notes = db_data.get('notes', ''),
                params = db_data.get('Params', ''),
                status = db_data.get('status', ''),
                method = db_data.get('Method', ''),
                interface_apiinfo_id = fileinfo_id
            )

        checkdata = models.InterfaceApiInfo.objects.filter(interface_apiinfo_id=fileinfo_id).values()  # 只查询当前文件相关的API信息
        response['code'] = 0
        response['msg'] = list(checkdata)
    except Exception as e:
        logger.error(f"解析接口文件失败: {e}")
        response['code'] = 1
        response['msg'] = f'解析接口文件失败: {str(e)}'

    return JsonResponse(response)


@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def create_interface_testcase(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)
    
    file_id = request.POST.get('id')
    project = request.POST.get('project_name')
    version = request.POST.get('version')

    print(f'id: {file_id}, project: {project}, version: {version}')

    testcaseid_id = models.InterfaceFileInfo.objects.get(id = file_id) # 通过id查的外键的id
    # 查询api接口数据的数据表，得到接口信息，并通过zhipuai的方法生成测试用例
    api_info = models.InterfaceApiInfo.objects.filter(interface_apiinfo_id=testcaseid_id).values()
    print(api_info)
    AI = zhipu_ai(API_key)
    for info in api_info:
        data = AI.msg(info)
        res = AI.start(data)
        result = res.choices[0].message # 获取ai接口返回的测试用例
        print(result)
        try:
        # 提取content中的JSON字符串
            json_str = result.content.split('```json')[1].split('```')[0].strip()
        except:
            # 从result.content中提取JSON字符串
            json_str = result.content.strip("CompletionMessage(content='").strip("')")

    # 将单引号替换为双引号
    # json_str = json_str.replace("'", '"')

    # 解析JSON字符串
        try:
            test_cases = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            # 如果有错误，可以在这里处理或打印原始字符串
            print(json_str)
        
    # 提取返回的测试用例数据，并通过循环添加进测试用例数据表中
        for case in test_cases:
            api_name = case['api_name']
            testpoint = case['testpoint']
            expectedresult = case['expectedresult']
            print(f"API名称: {api_name}, 测试点: {testpoint}, 预期结果: {expectedresult}")
            models.InterfaceTestCase.objects.get_or_create(
                project_name = project,
                version = version,
                api_name = api_name,
                testpoint = testpoint,
                expectedresult = expectedresult,
                testcaseid = testcaseid_id
            )
            models.InterfaceDataConfig.objects.get_or_create(
                data_desc = testpoint,
                interface_api_id = testcaseid_id
            )
    response['code'] = 0
    response['msg'] = '生成测试用例成功'
    
    return JsonResponse(response)
