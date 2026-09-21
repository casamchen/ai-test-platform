import datetime
from django.shortcuts import render
from django.http import JsonResponse
from aitestapp import models
from aitestapp.tool.cipher import Cipherd
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt  # API 接口使用 Session 认证，无需 CSRF
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def search_testcase(request):
    response = {}

    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    params = request.POST.get('id')

    # 安全的类型转换，防止 None 导致 TypeError
    try:
        page = int(request.POST.get('Page', '1'))
        limit = int(request.POST.get('limit', '10'))
    except (ValueError, TypeError):
        return JsonResponse({'code': 1, 'msg': '分页参数格式错误'}, status=400)

    # 参数校验
    if page < 1 or limit < 1:
        return JsonResponse({'code': 1, 'msg': '分页参数必须为正整数'}, status=400)

    offset = (page - 1) * limit

    try:
        testcase_data = models.testcase.objects.filter(testcaseid=params)[offset:offset + limit].values()
        total = models.testcase.objects.filter(testcaseid=params).count()

        if len(testcase_data) == 0:
            response['code'] = 1
            response['msg'] = '没有该需求文档id的测试用例，请检查输入的id是否正确并重新输入'
        else:
            response['code'] = 0
            response['msg'] = list(testcase_data)
            response['total'] = total
    except Exception as e:
        logger.error(f"查询测试用例失败: {e}")
        response['code'] = 1
        response['msg'] = f'查询失败: {str(e)}'

    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def show_testcase(request):
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
        testcase_data = models.testcase.objects.all()[offset:offset + limit].values()
        total = models.testcase.objects.count()

        if len(testcase_data) == 0:
            response['code'] = 1
            response['msg'] = '暂无测试用例数据'
        else:
            response['code'] = 0
            response['msg'] = list(testcase_data)
            response['total'] = total
    except Exception as e:
        logger.error(f"查询所有测试用例失败: {e}")
        response['code'] = 1
        response['msg'] = f'查询失败: {str(e)}'

    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def update_state(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    testcase = request.POST.get('testcase')
    state = request.POST.get('state')

    if not testcase:
        return JsonResponse({'code': 1, 'msg': '缺少测试用例参数'}, status=400)

    try:
        update_state = models.testcase.objects.filter(testcase=testcase).update(state=state)
        logger.info(f"更新用例状态: {testcase} -> {state}, 影响行数: {update_state}")
    except Exception as e:
        logger.error(f"更新用例状态失败: {e}")
        return JsonResponse({'code': 1, 'msg': f'更新失败: {str(e)}'}, status=500)

    response['code'] = 0
    response['msg'] = '更新用例状态成功'
    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def update_result(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    testcase = request.POST.get('testcase')
    result = request.POST.get('result')

    if not testcase:
        return JsonResponse({'code': 1, 'msg': '缺少测试用例参数'}, status=400)

    try:
        update_state = models.testcase.objects.filter(testcase=testcase).update(actual_results=result)
        logger.info(f"更新用例结果: {testcase}")
    except Exception as e:
        logger.error(f"更新用例结果失败: {e}")
        return JsonResponse({'code': 1, 'msg': f'更新失败: {str(e)}'}, status=500)

    response['code'] = 0
    response['msg'] = '更新用例实际结果成功'
    return JsonResponse(response)
