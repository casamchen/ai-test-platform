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
def test_report(request):
    response = {}
    cipher = Cipherd() # 创建加密实例
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)
    
    testcase_id = request.body
    decryptData = cipher.decrypt(testcase_id.decode()) # 对加密后的数据进行解密
    dictData = json.loads(decryptData) # 对数据进行json处理

    update_state = models.testcase.objects.filter(testcase=dictData['testcase']).update(actual_results=dictData['result'])
    print(update_state)
    encrypData = cipher.encrypt(str({'code': 0, 'msg': '更新用例实际结果成功'})) # 对要返回的响应数据进行加密
    response['msg'] = encrypData
    return JsonResponse(response)