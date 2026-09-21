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

@require_http_methods(['GET'])
def show_interface_report(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)
    
    testreport = models.TestReport.objects.filter().values()
    response['code'] = 0
    response['msg'] = list(testreport)
    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def search_interface_report(request):
    response = {}

    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)
    
    params = request.POST.get('id')
    # print(params)
    testcase_data = models.TestReport.objects.filter(id=params).values()
    if testcase_data:
        testcase_search_data = models.TestReport.objects.filter(id=params).values()
        response['code'] = 0
        response['msg'] = list(testcase_search_data)
    else:
        response['code'] = 1
        response['msg'] = '没有该id的测试报告，请检查输入的id是否正确并重新输入'
        
    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def get_interface_report_log(request):
    response = {}

    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)
    
    params = request.POST.get('id')
    # print(params)
    testcase_data = models.TestCaseResult.objects.filter(testresultid=params).values()
    if testcase_data:
        response['code'] = 0
        response['msg'] = list(testcase_data)
    else:
        response['code'] = 1
        response['msg'] = '没有该id的测试报告，请检查输入的id是否正确并重新输入'
        
    return JsonResponse(response)

@require_http_methods(['GET'])
def aaaaa(request):
    response = {}

    # print(params)
    aaa = set(models.InterfaceDataConfig.objects.values_list('data_desc', flat=True))
    print(aaa)
    print(len(aaa))
    bbb = list(models.InterfaceTestCase.objects.filter().values())
    c = []
    for b in bbb:
        if b['testpoint'] not in aaa:
            c.append(b)
    print(c)
    response['code'] = 1
    
    return JsonResponse(response)
