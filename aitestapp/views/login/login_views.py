from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from aitestapp import models
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt  # CSRF 豁免 - API 接口使用 Token 认证
from aitestapp.tool.cipher import Cipherd
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import json
import logging

# 配置日志记录器，替代 print 输出敏感信息
logger = logging.getLogger(__name__)

@csrf_exempt  # 登录接口使用 AES 加密认证，无需 CSRF 保护
@require_http_methods(['POST'])
def sign_in(request):
    response = {}
    cipher = Cipherd() # 创建加密实例
    data = request.body  # 获得通过请求拦截器解密后的数据

    if len(data) == 0:
        encrypData = cipher.encrypt(str({'code': 400, 'msg': '用户名和密码不能为空'}))
        response['msg'] = encrypData
        return JsonResponse(response)  # 统一返回 200 HTTP，用 code 字段表示业务状态

    try:
        raw_data = data.decode('utf-8')
        decryptData = cipher.decrypt(raw_data) # 对加密后的数据进行解密
        dictData = json.loads(decryptData) # 对数据进行json处理
        user = authenticate(request, username=dictData['user'], password=dictData['password']) # 查询登录用户表
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        # 精确捕获特定异常，不再使用裸 except
        logger.warning(f'登录数据解析失败: {e}')
        encrypData = cipher.encrypt(str({'code': 400, 'msg': '数据格式错误'}))
        response['msg'] = encrypData
        return JsonResponse(response)  # 统一返回 200 HTTP
    except Exception as e:
        logger.error(f'登录处理异常: {e}')
        encrypData = cipher.encrypt(str({'code': 500, 'msg': '服务器内部错误'}))
        response['msg'] = encrypData
        return JsonResponse(response)  # 统一返回 200 HTTP

    if user is None: # 如果user不存在，则返回登录失败状态码
        # 统一错误消息，防止用户枚举攻击（不区分"用户不存在"和"密码错误"）
        encrypData = cipher.encrypt(str({'code': 400, 'msg': '用户名或密码错误'}))
        response['msg'] = encrypData
        return JsonResponse(response)  # 统一返回 200 HTTP

    # 删除上次登录的session
    models.Session.objects.filter(usersession__user=user).delete()
    # 实行登录
    login(request, user)
    request.session.save()
    sessionid = request.session.session_key
    models.UserSession.objects.get_or_create(user=user, session_id=sessionid)
    # 对要返回的响应数据进行加密，包含 token（session key）供前端使用
    encrypData = cipher.encrypt(str({'code': 200, 'msg': '登录成功', 'token': sessionid}))
    response['msg'] = encrypData
    return JsonResponse(response)

@csrf_exempt  # 注册接口使用 AES 加密认证，无需 CSRF 保护
@require_http_methods(['POST'])
def sign_up(request):
    response = {}
    cipher = Cipherd() # 创建加密实例
    data = request.body

    if len(data) == 0:
        encrypData = cipher.encrypt(str({'code': 400, 'msg': '注册数据不能为空'}))
        response['msg'] = encrypData
        return JsonResponse(response)

    try:
        decryptData = cipher.decrypt(data.decode()) # 对加密后的数据进行解密
        dictData = json.loads(decryptData) # 对数据进行json处理
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        logger.warning(f'注册数据解析失败: {e}')
        encrypData = cipher.encrypt(str({'code': 400, 'msg': '数据格式错误'}))
        response['msg'] = encrypData
        return JsonResponse(response)

    username = dictData.get('user', '').strip()
    password = dictData.get('password', '')

    # 输入验证
    if not username or not password:
        encrypData = cipher.encrypt(str({'code': 400, 'msg': '用户名和密码不能为空'}))
        response['msg'] = encrypData
        return JsonResponse(response)

    if len(username) < 3 or len(username) > 20:
        encrypData = cipher.encrypt(str({'code': 400, 'msg': '用户名长度必须在3-20个字符之间'}))
        response['msg'] = encrypData
        return JsonResponse(response)

    if len(password) < 6 or len(password) > 128:
        encrypData = cipher.encrypt(str({'code': 400, 'msg': '密码长度必须在6-128个字符之间'}))
        response['msg'] = encrypData
        return JsonResponse(response)

    # 检查用户名是否已存在
    if User.objects.filter(username=username).exists():
        encrypData = cipher.encrypt(str({'code': 400, 'msg': '已经存在相同的用户名，请换个用户名进行注册'}))
        response['msg'] = encrypData
        return JsonResponse(response)

    # 创建用户
    try:
        User.objects.create_user(username=username, password=password)
        logger.info(f'新用户注册成功: {username}')
        encrypData = cipher.encrypt(str({'code': 200, 'msg': '注册成功'}))
        response['msg'] = encrypData
        return JsonResponse(response)
    except Exception as e:
        logger.error(f'用户创建失败: {username}, 错误: {e}')
        encrypData = cipher.encrypt(str({'code': 500, 'msg': '注册失败，请稍后重试'}))
        response['msg'] = encrypData
        return JsonResponse(response)