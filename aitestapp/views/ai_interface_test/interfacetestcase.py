from django.shortcuts import render
from django.http import JsonResponse
from aitestapp import models

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt  # API 接口使用 Session 认证，无需 CSRF
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

from aitestapp.views.ai_interface_test.getAllcaseData import getAllData
import logging

logger = logging.getLogger(__name__)


@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def show_interface_testcase(request):
    response = {}

    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    # 安全的类型转换
    try:
        page = int(request.POST.get('Page', '1'))
        limit = int(request.POST.get('limit', '10'))
    except (ValueError, TypeError):
        return JsonResponse({'code': 1, 'msg': '分页参数格式错误'}, status=400)

    if page < 1 or limit < 1:
        return JsonResponse({'code': 1, 'msg': '分页参数必须为正整数'}, status=400)

    offset = (page - 1) * limit

    try:
        file_testcase = models.InterfaceFileInfo.objects.filter().values('project')
        if not file_testcase.exists() or len(file_testcase) == 0:
            return JsonResponse({'code': 1, 'msg': '暂无接口文件数据'}, status=404)

        project_name = file_testcase[0]['project']
        testcase_list = models.InterfaceTestCase.objects.filter(project_name=project_name)[offset:offset + limit].values()
        total = models.InterfaceTestCase.objects.filter(project_name=project_name).count()

        response['code'] = 0
        response['msg'] = list(testcase_list)
        response['total'] = total
    except Exception as e:
        logger.error(f"查询接口测试用例失败: {e}")
        response['code'] = 1
        response['msg'] = f'查询失败: {str(e)}'

    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def search_interface_testcase(request):
    response = {}

    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    params = request.POST.get('id')

    # 安全的类型转换
    try:
        page = int(request.POST.get('Page', '1'))
        limit = int(request.POST.get('limit', '10'))
    except (ValueError, TypeError):
        return JsonResponse({'code': 1, 'msg': '分页参数格式错误'}, status=400)

    if page < 1 or limit < 1:
        return JsonResponse({'code': 1, 'msg': '分页参数必须为正整数'}, status=400)

    offset = (page - 1) * limit

    try:
        testcase_data = models.InterfaceFileInfo.objects.filter(id=params).values('project')
        if testcase_data:

            testcase_search_data = models.InterfaceTestCase.objects.filter(project_name=testcase_data[0]['project'])[offset:offset + limit].values()
            total = models.InterfaceTestCase.objects.filter(project_name=testcase_data[0]['project']).count()
            response['code'] = 0
            response['msg'] = list(testcase_search_data)
            response['total'] = total

        else:
            response['code'] = 1
            response['msg'] = '没有该需求文档id的测试用例，请检查输入的id是否正确并重新输入'

    except Exception as e:
        logger.error(f"搜索接口测试用例失败: {e}")
        response['code'] = 1
        response['msg'] = f'查询失败: {str(e)}'

    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def check_data_config(request):
    response = {}

    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    id = request.POST.get('id') # 获取testpoint参数

    try:
        # 通过查询对应测试点的数据库，获取外键id
        testcase_data = models.InterfaceDataConfig.objects.filter(id=id).values('data_info')
        if not testcase_data.exists() or len(testcase_data) == 0:
            return JsonResponse({'code': 1, 'msg': '数据配置不存在'}, status=404)

        data = testcase_data[0]['data_info']
        response['code'] = 0
        response['msg'] = data
    except Exception as e:
        logger.error(f"查询数据配置失败: {e}")
        response['code'] = 1
        response['msg'] = f'查询失败: {str(e)}'

    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def update_data_config(request):
    response = {}

    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    testpoint = request.POST.get('testpoint') # 获取testpoint参数
    data_config = request.POST.get('data_config') # 获取输入的数据配置参数

    if not testpoint:
        return JsonResponse({'code': 1, 'msg': '缺少测试点参数'}, status=400)

    try:
        # 通过查询对应测试点的数据库，获取外键id
        testcase_list = models.InterfaceTestCase.objects.filter(testpoint=testpoint).values('testcaseid')
        if not testcase_list.exists() or len(testcase_list) == 0:
            return JsonResponse({'code': 1, 'msg': '测试点不存在'}, status=404)

        interface_file_id = testcase_list[0]['testcaseid']
        # 通过update，修改表中的数据配置
        models.InterfaceDataConfig.objects.filter(data_desc=testpoint).update(data_info=data_config)

        response['code'] = 0
        response['msg'] = '添加接口数据配置成功'
    except Exception as e:
        logger.error(f"更新数据配置失败: {e}")
        response['code'] = 1
        response['msg'] = f'更新失败: {str(e)}'

    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def excute_testcase(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    testpoint = request.POST.get('testpoint') # 获取testpoint参数
    api_name = request.POST.get('api_name') # 获取api_name参数
    expectedresult = request.POST.get('expectedresult') # 获取expectedresult参数

    if not all([testpoint, api_name, expectedresult]):
        return JsonResponse({'code': 1, 'msg': '缺少必要参数'}, status=400)

    try:
        # 动态传参
        getdata = getAllData()
        getdata.getData(testpoint, api_name, expectedresult)
        result = getdata.execute()
        response['code'] = 0
        response['count'] = result[0]['count']
        response['msg'] = list(result[1]['test_results'])
    except Exception as e:
        logger.error(f"执行测试用例失败: {e}")
        response['code'] = 1
        response['msg'] = f'执行失败: {str(e)}'

    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def excute_all_testcase(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    id = request.POST.get('id')

    if not id:
        return JsonResponse({'code': 1, 'msg': '缺少文件ID参数'}, status=400)

    try:
        getdata = getAllData()
        getdata.get_All_Data(id)
        result = getdata.execute()
        response['code'] = 0
        response['count'] = result[0]['count']
        response['msg'] = list(result[1]['test_results'])
    except Exception as e:
        logger.error(f"执行所有测试用例失败: {e}")
        response['code'] = 1
        response['msg'] = f'执行失败: {str(e)}'

    return JsonResponse(response)
