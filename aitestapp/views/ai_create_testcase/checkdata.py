from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from aitestapp import models
from aitestapp.tool.cipher import Cipherd
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import json
import datetime

@require_http_methods(['GET'])
def checkprdinfo(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    checkdata = models.FileInfo.objects.filter().values()
    print(checkdata)

    response['code'] = 0
    response['msg'] = list(checkdata)

    return JsonResponse(response)
