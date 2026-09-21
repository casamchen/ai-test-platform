

import requests, json
from aitestapp.scripts.api_request import APIRequester

class TestCaseExecutor:
    def __init__(self, test_data, base_url):
        self.test_data = test_data  # 测试数据列表
        self.base_url = base_url    # API的基础URL
        self.session = requests.Session()  # 创建一个session对象供APIRequester使用
        self.api_requester = APIRequester(base_url=self.base_url, session=self.session)

    def parse_response(self, response):
        # 尝试解析响应内容为JSON
        try:
            response_dict = response.json()
            # print(f'这是17行：{response_dict}')
        except json.JSONDecodeError:
            # 如果响应内容不是JSON，则可能是一个字符串或其他格式
            response_dict = {'content': response.text}
            # print(f'这是21行：{response_dict}')
        
        # 添加响应状态码和头信息到字典中
        response_dict.update({
            'status_code': response.status_code,
            'headers': dict(response.headers)
        })
        
        return response_dict

    def run(self):
        response_data_list = []
        for test_data in self.test_data:
            path = test_data['api_info']['url'].replace('/api', '')
            response = self.api_requester.request(method=test_data['api_info']['method'],
                                                  endpoint=path,
                                                  payload=test_data['params'])
            request_info = self.api_requester.capture_request(response)

            response_data = self.parse_response(response)
            response_data_list.append(response_data)
            response_data_list.append(request_info)
        return response_data_list