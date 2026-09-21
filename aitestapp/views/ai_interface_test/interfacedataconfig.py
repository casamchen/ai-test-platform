import datetime
from django.shortcuts import render
from django.http import JsonResponse
from aitestapp import models
from aitestapp.tool.cipher import Cipherd
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt  # API 接口使用 Session 认证，无需 CSRF
from django.conf import settings
import json

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def show_interface_data_config(request):
    response = {}

    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)
    
    page = int(request.POST.get('Page'))
    limit = int(request.POST.get('limit'))
    offset = (page - 1) * limit

    testcase_data = models.InterfaceDataConfig.objects.all()[offset:offset + limit].values()
    total = models.InterfaceDataConfig.objects.count()
    print(testcase_data)
    if len(testcase_data) == 0: 
        response['code'] = 1
        response['msg'] = '暂无数据'
    else:
        response['code'] = 0
        response['msg'] = list(testcase_data)
        response['total'] = total
    return JsonResponse(response)