# tasks.py
import os
from celery import shared_task
from aitestapp import models
from zhipuai import ZhipuAI
import json
import logging

logger = logging.getLogger(__name__)

@shared_task(track_started=True)
def generate_testcases(text_values, project_name, version, testcaseid):
    # 从环境变量读取 API Key
    api_key = os.environ.get('ZHIPUAI_API_KEY', '')
    if not api_key:
        logger.error("ZHIPUAI_API_KEY 环境变量未配置")
        return {"code": 1, "msg": "API Key 未配置"}

    client = ZhipuAI(api_key=api_key)

    try:
        fileinfo_id = models.FileInfo.objects.get(id=testcaseid)
    except models.FileInfo.DoesNotExist:
        logger.error(f"文件记录不存在: id={testcaseid}")
        return {"code": 1, "msg": f"文件记录不存在: {testcaseid}"}

    doc_content = models.vectors.objects.filter().values('text')
    text_values = [record['text'] for record in doc_content]
    test_cases = []  # 在外层初始化，避免变量未定义错误

    for index, data in enumerate(text_values):
        
        input_data = [{
                "role": "system", 
                "content": "你是一名软件测试工程师。你的任务是根据需求内容生成测试用例。请注意一定要严谨，要针对指定的需求内容生成测试用例，为了避免重复不要创造需求或者创作多余的测试用例。"
            }, {
                "role": "user",
                "content": "完整需求内容为：{'功能需求':['请假时间默认设置为当前日期。','请假时间必须与当前日期相同。','请假时间不允许小于或大于当前日期。'],'业务规则':['请假时间自动同步至系统当前日期。','请假时间不可手动更改，仅限于当前日期。','系统需验证请假时间是否为当前日期，不符合则不允许提交。'],'界面和交互':['在请假模块中，请假时间字段自动填充为系统当前日期。','用户界面应明确显示请假时间不可更改的提示信息。','当用户尝试更改请假时间为非当前日期时，系统应提供错误提示。'],'异常处理':['当用户尝试提交非当前日期的请假申请时，系统应阻止提交并显示错误信息。','处理可能的系统时间错误，如系统时间与用户本地时间不一致的情况。'],'性能需求':['确保请假时间字段的自动填充功能快速响应。','优化日期验证逻辑，确保系统处理请假申请时的效率。'],'安全需求':['保护用户请假信息的安全，防止未经授权的访问。','确保请假时间字段的验证逻辑不会引入安全漏洞。']}，测试模块为：我要请假，测试方向为：界面和交互，指定需要生成测试用例的需求为：用户界面应明确显示请假时间不可更改的提示信息。。请注意一定要严谨，只需要针对指定的需求内容生成测试用例，为了避免生成重复的测试用例，请不要创造需求和创作多余的测试用例。"
            }, {
                "role": "assistant",
                "content": "[{'testpoint': '谷歌浏览器，用户界面应明确显示请假时间不可更改的提示信息', 'operation': '1、登录成功后\\n2、点击姓名-我要请假，观察界面 ', 'expectedresult': '明确显示请假时间不可更改的提示信息'}, {'testpoint': 'EDGE浏览器，用户界面应明确显示请假时间不可更改的提示信息', 'operation': '1、登录成功后\\n2、点击姓名-我要请假，观察界面 ', 'expectedresult': '明确显示请假时间不可更改的提示信息'}, {'testpoint': '火狐浏览器，用户界面应明确显示请假时间不可更改的提示信息', 'operation': '1、登录成功后\\n2、点击姓名-我要请假，观察界面 ', 'expectedresult': '明确显示请假时间不可更改的提示信息'}, {'testpoint': '不同分辨率情况下界面提示显示正常', 'operation': '1、登录成功后\\n2、点击姓名-我要请假，观察界面 ', 'expectedresult': '明确显示请假时间不可更改的提示信息'}]"
            }, {
                "role": "user",
                "content": f"完整需求内容为：{text_values}。指定需要生成测试用例的需求为：{data}。请注意一定要严谨，只需要针对指定的需求内容生成测试用例，为了避免生成重复的测试用例，请不要创造需求和创作多余的测试用例。"
            }]
        
        try:
            res = client.chat.completions.create(
                model="glm-4-flash:2011843146::wpcubzsg",
                messages=input_data,
                stream=False
            )
            # json_str = res.choices[0].message.content
            # 解析JSON并保存到数据库（同原逻辑）
            print(f'当前为第{index+1}个需求')
            print(input_data)
            result = res.choices[0].message
            try:
            # 提取content中的JSON字符串
                json_str = result.content.split('```json')[1].split('```')[0].strip()
            except:
                # 从result.content中提取JSON字符串
                json_str = result.content.strip("CompletionMessage(content='").strip("')")
                json_str = json_str.replace("'", '"')
            # print(json_str)
            try:
                test_cases = json.loads(json_str)
                # 验证解析结果是否为列表
                if not isinstance(test_cases, list):
                    logger.warning(f"AI返回的测试用例格式不是列表: {type(test_cases)}")
                    test_cases = []
            except json.JSONDecodeError as e:
                logger.warning(f"第{index+1}个需求JSON解析失败: {e}")
                test_cases = []  # 确保变量已定义

            for case in test_cases:
                print(case)
                keys = list(case.keys())
                if len(keys) == 3:
                    testcase_key = keys[0]
                    operation_key = keys[1]
                    expectedresult_key = keys[2]
                
                    testcase = models.testcase.objects.filter(testcase=case[testcase_key], operation=case[operation_key], expectedresult = case[expectedresult_key]).values()
                    if len(testcase) == 0:
                        models.testcase.objects.create(
                            project_name = project_name,
                            version = version,
                            testcase = case[testcase_key],
                            operation = case[operation_key],
                            expectedresult = case[expectedresult_key],
                            testcaseid = fileinfo_id
                        )
                else:
                    pass
        except Exception as e:
            print(f"Error processing data {data}: {str(e)}")
    
    return {"code": 0, "msg": "任务完成"}

