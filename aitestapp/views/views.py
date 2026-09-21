from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from aitestapp import models
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt  # API 接口使用 Session 认证，无需 CSRF
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
import json
import logging

logger = logging.getLogger(__name__)

# Create your views here.

@require_http_methods('GET')
def check_config(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    try:
        check_data = models.project_config.objects.filter().values() # 查询表中所有数据
        response['data'] = list(check_data)
    except Exception as e:
        logger.error(f"查询配置失败: {e}")
        response['error'] = str(e)
        return JsonResponse(response, status=500)
    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def add_config_data(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    try:
        data = request.body.decode()
        data_dict = json.loads(data) # 对数据进行json处理
        # 添加输入校验，防止 KeyError
        config_key = data_dict.get('key')  # 通过字典获取对应值
        config_value = data_dict.get('value')
        config_remarks = data_dict.get('remarks', '')

        if not all([config_key, config_value]):
            return JsonResponse({'code': 1, 'msg': '缺少必要参数: key 和 value'}, status=400)

        # 根据提交的数据在数据库进行创建
        models.project_config.objects.create(key=config_key, value=config_value, remarks=config_remarks)
        response['code'] = 0
        response['msg'] = '创建成功'
    except json.JSONDecodeError:
        return JsonResponse({'code': 1, 'msg': 'JSON格式错误'}, status=400)
    except Exception as e:
        logger.error(f"创建配置失败: {e}")
        return JsonResponse({'code': 1, 'msg': f'创建失败: {str(e)}'}, status=500)

    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def update_config_data(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    try:
        data = request.body.decode()
        data_dict = json.loads(data) # 对数据进行json处理
        config_id = data_dict.get('id') # 通过字典获取对应值
        config_key = data_dict.get('key')
        config_value = data_dict.get('value')
        config_remarks = data_dict.get('remarks', '')

        if not config_id:
            return JsonResponse({'code': 1, 'msg': '缺少必要参数: id'}, status=400)

        # 根据提交的数据在数据库进行更新
        update_params = {}
        if config_key is not None:
            update_params['key'] = config_key
        if config_value is not None:
            update_params['value'] = config_value
        if config_remarks is not None:
            update_params['remarks'] = config_remarks

        models.project_config.objects.filter(id=config_id).update(**update_params)
        response['code'] = 0
        response['msg'] = '修改成功'
    except json.JSONDecodeError:
        return JsonResponse({'code': 1, 'msg': 'JSON格式错误'}, status=400)
    except Exception as e:
        logger.error(f"更新配置失败: {e}")
        return JsonResponse({'code': 1, 'msg': f'更新失败: {str(e)}'}, status=500)

    return JsonResponse(response)

@csrf_exempt  # API 接口使用 Session 认证，无需 CSRF 保护
@require_http_methods(['POST'])
def delete_config_data(request):
    response = {}
    # 检查是否登录
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error' : '用户未登录'}, status=401)

    try:
        data = request.body.decode()
        data_dict = json.loads(data) # 对数据进行json处理
        config_id = data_dict.get('id') # 获取传的id值

        if not config_id:
            return JsonResponse({'code': 1, 'msg': '缺少必要参数: id'}, status=400)

        models.project_config.objects.filter(id=config_id).delete() # 根据提交的id在数据库进行删除
        response['code'] = 0
        response['msg'] = '删除成功'
    except json.JSONDecodeError:
        return JsonResponse({'code': 1, 'msg': 'JSON格式错误'}, status=400)
    except Exception as e:
        logger.error(f"删除配置失败: {e}")
        return JsonResponse({'code': 1, 'msg': f'删除失败: {str(e)}'}, status=500)

    return JsonResponse(response)