from zhipuai import ZhipuAI
from aitestapp.views.configdir.config import API_key


class zhipu_ai():
    def __init__(self, API_key):
        self.API_key = API_key

    def start(self, msg):
        client = ZhipuAI(api_key=self.API_key) # 创建智普客户端
        res = client.chat.completions.create(
            model='GLM-4-Flash', # 调用glm-4模型
                messages= msg,
                stream=False, # 不调用流式输出
        )
        # for chunk in response: # 如果调用流式输出则用for循环打印
        #     print(chunk.choices[0].delta)
        return res # 如果不调用流失输出则直接打印

    def msg(self, api_info):
        example_info = [{
                    "example": "post /api/login",
                    "url": "/api/login",
                    "Method": "post",
                    "notes": "用户登录",
                    "title": "登录接口",
                    "Params":  [{'description': '登录数据', 'name': 'param', 'in': 'body', 'required': True, 'schema': {'$ref': '#/definitions/request.Login'}}],
                    "Responses": [{'200': {'description': 'OK', 'schema': {'allOf': [{'$ref': '#/definitions/core.Result'}, {'type': 'object', 'properties': {'result': {'$ref': '#/definitions/model.User'}}}]}}, '400': {'description': '失败', 'schema': {'$ref': '#/definitions/model.Error'}}}],
                    "status":  "['200', 'OK'], ['400', '失败']"
                    }]
        example = [
            # {"api_name": "登录接口", "testpoint": "不输入用户名，输入密码", "expectedresult": "{'code': 1, 'msg': '用户名或密码无效'}"},
            # {"api_name": "登录接口", "testpoint": "不输入密码，输入用户名", "expectedresult": "{'code': 1, 'msg': '用户名或密码无效'}"},
            # {"api_name": "登录接口", "testpoint": "用户名和密码不输入", "expectedresult": "{'code': 1, 'msg': '用户名或密码无效'}"},
            {"api_name": "登录接口", "testpoint": "输入正确用户名和密码", "expectedresult": "{'code': 0, 'msg': '登录成功'}"}
            # {"api_name": "登录接口", "testpoint": "输入错误用户名和正确密码", "expectedresult": "{'code': 1, 'msg': '用户名或密码无效'}"},
            # {"api_name": "登录接口", "testpoint": "用户名称输入少于11位", "expectedresult": "{'code': 1, 'msg': '用户名或密码无效'}"},
            # {"api_name": "登录接口", "testpoint": "密码输入小于6位", "expectedresult": "{'code': 1, 'msg': '用户名或密码无效'}"},
            # {"api_name": "登录接口", "testpoint": "密码输入超过12位", "expectedresult": "{'code': 1, 'msg': '用户名或密码无效'}"},
            # {"api_name": "登录接口", "testpoint": "用户名含有非数字字符", "expectedresult": "{'code': 1, 'msg': '用户名或密码无效'}"},
            # {"api_name": "登录接口", "testpoint": "用户名手机号码输入139号段", "expectedresult": "{'code': 0, 'msg': '登录成功'}"},
            # {"api_name": "登录接口", "testpoint": "用户名手机号码输入181号段", "expectedresult": "{'code': 0, 'msg': '登录成功'}"}
        ]
        data = [{
                    "role": "system", 
                    "content": "你是一个专业的测试工程师。你的任务是根据接口文档需求内容生产接口测试用例。"
                }, {
                    "role": "user",
                    "content": """需求：请根据接口文档内容分析并生成对应接口测试的测试点和对应的预期结果,返回的exceptedresult需要跟接口文档响应数据值一样；
                        要求1：生成测试接口用例测试点需要考虑边界值和等价类,正常情况以及异常情况，要全面,期待的结果要返回跟接口文档一样。
                        要求2：内容请用中文生成，要求测试点考虑周全.请严格按照接口文档内容生成测试用例，要输出完整；
                        要求3：生成真实的测试点并用testpoint代替，预期结果用exceptedresult代替，接口名称用api_name代替.
                        重点要求3：生成请严格按照定义的[{“api_name”: "", "testpoint": "", "expectedresult": ""},{“api_name”: "", "testpoint": "", "expectedresult": ""}]的json结构和格式输出；
                        重点要求4：不要生成与测试点及json结构和格式无关的内容，要方便后续代码的处理,生成的exceptedresult要跟文档的响应数据一样，不要有\出现."""
                },{
                    "role": "assistant",
                    "content": "好的，我一定会考虑全面，将细节考虑周全，并严格按照您的要求输出和生成一份完美的接口测试的测试点和预期的结果，请告知您的需求内容"
                },{
                    "role": "user",
                    "content": f"接口内容为：{example_info}"
                },{
                    "role": "assistant",
                    "content": str(example)
                },{
                     "role": "user",
                    "content": api_info
                }]
        return data


