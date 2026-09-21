from aitestapp import models
from aitestapp.scripts.prompts_interface import Prompts
from aitestapp.scripts.model_AI import ZhiPu4
from aitestapp.scripts.utils import excute_to_json
from aitestapp.scripts.test_data import TestData
from aitestapp.scripts.config import loadConfig
from aitestapp.scripts.test_case_executor import TestCaseExecutor

zhipu_ai = ZhiPu4()
load_config = loadConfig()
configs = load_config.load_config()

def run_test(testpoint, api_name, expectedresult):

    # 通过查询对应测试点的数据库，获取外键id
    testcase_id = models.InterfaceTestCase.objects.filter(testpoint=testpoint).values('testcaseid')
    interface_file_id = testcase_id[0]['testcaseid']
    # 通过外键id查询主表得到主表id
    interface_file_id = models.InterfaceFileInfo.objects.get(id=interface_file_id)
    api_info_list = models.InterfaceApiInfo.objects.filter(interface_apiinfo_id=interface_file_id, title=api_name).values() # 读取出api_info表中的信息
    # print(api_info_list)
    api_data_url = api_info_list[0]['url']
    # print(api_data_url)
    # 遍历接口信息列表 api_info_list为读取数据库interface_apiinfo表中的数据
    for api_info in api_info_list:
        prompt = Prompts.api_desc_prompt(api_info)
        status, res = zhipu_ai.zhipuai_request(prompt)

        try:
            data = {api_info['url']: res.replace('\n','')}
        except:
            data = {api_info['url']: res}
    # print(data)
    data_config_info = models.InterfaceDataConfig.objects.filter(data_desc=testpoint).values()
    data_decs = data_config_info[0]['data_desc']
    data_info = data_config_info[0]['data_info']
    api_info_case = f"{data_decs},{expectedresult}"
    # print(api_info_case)

    api_case_info = f"接口描述为：{data}。测试用例为: {api_info_case}"
    # print(api_case_info)
    case_prompt = Prompts.api_case_prompt(api_case_info) # 将接口描述和接口测试用例通过api_case_prompt转存prompt

    status, res = zhipu_ai.zhipuai_request(case_prompt) # 将prompt给到ai请求返回response
    # print(res)
    # 对ai返回的response通过step为标识进行执行顺序的排序
    sorted_data = sorted(excute_to_json(res), key=lambda x: x['step']) 
    print(sorted_data)

    test_data_config = f"url: {api_data_url}, api_data: {data_info}, api_case_decs: {data_decs}"
    test_data = {api_data_url: {'data': data_info, 'decs': data_decs}}
    # print(test_data_config)
    print(test_data)

    # sorted_data step排序后的接口执行顺序
    # api_info_list 接口信息数据
    # test_data_config_data 接口测试数据包含：url，decs，data
    # api_info_config_case 接口测试用例
    # 实例化方法，将以上准备的数据集合到testdata中，准备好执行的数据
    test_case_data = TestData(sorted_data, api_info_list, test_data, zhipu_ai, api_info_case)
    test_case_data.run()
    base_url = configs['TEST_URLS'][0]['url']
    # 将测试数据和后台url集合，开始执行测试
    test_case_excutor = TestCaseExecutor(test_case_data.run_data, base_url)
    response_data_list = test_case_excutor.run()

    # print(response_data_list)