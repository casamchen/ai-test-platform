

from aitestapp.scripts.utils import filter_interface
from aitestapp.scripts.utils import excute_to_json
from aitestapp.scripts.prompts_interface import Prompts

class TestData:

    def __init__(self, step_list: list, api_info_desc_list: dict, test_data_dict: dict, ZhiPu4: object, api_info_config_case: str) -> None:
        # 测试用例操作步骤
        self.setp = step_list
        # 测试数据，比如账号那些
        self.test_data = test_data_dict
        # 接口信息描述
        self.api_info_desc = api_info_desc_list
        # 智谱AI Model Object
        self.zhipu_ai = ZhiPu4
        # 功能测试用例
        self.test_case = api_info_config_case

    def run(self):
        # 筛选对应的接口信息
        api_info = filter_interface(self.setp, self.api_info_desc, 1)
        # 筛选对应的测试数据
        test_data_info = filter_interface(self.setp, self.test_data, 2)
        prrmpt_data_info = f"接口信息为：{api_info}。测试数据为：{test_data_info}。测试用例为：{self.test_case}。测试用例对应的执行步骤为：{self.setp}"
        print(f'接口信息为：{api_info}')
        print(f'测试数据为：{test_data_info}')
        prrmpt_data = Prompts.api_operation_prompt(prrmpt_data_info)
        
        status, response = self.zhipu_ai.zhipuai_request(prrmpt_data)
        params_data_info = excute_to_json(response)
        for item in params_data_info:
            if 'params' in item and isinstance(item['params'], dict):
                # 获取嵌套的 'param' 字典
                nested_params = item['params'].get('param', {})
                # 将嵌套的字典更新为扁平的字典
                item['params'] = nested_params
        # 执行步骤和数据，到此就搞定了
        self.run_data = []
        for pr_data in params_data_info:
            pr_data_api_path = pr_data['api_path']
            for api_info_data in self.api_info_desc:
                if api_info_data['url'] == pr_data_api_path:
                    pr_data['api_info'] = api_info_data
                    self.run_data.append(pr_data)
        print(self.run_data)
