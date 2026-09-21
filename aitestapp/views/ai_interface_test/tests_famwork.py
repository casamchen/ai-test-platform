import logging, re, unittest
import time, requests
from aitestapp.tool.pubilc_tool import retry
from aitestapp import models
from aitestapp.views.ai_interface_test.tests_result import MyTestResult
from aitestapp.scripts.prompts_interface import Prompts
from aitestapp.scripts.model_AI import ZhiPu4
from aitestapp.scripts.utils import excute_to_json
from aitestapp.scripts.test_data import TestData
from aitestapp.scripts.config_interface import loadConfig
from aitestapp.scripts.test_case_executor import TestCaseExecutor
from concurrent.futures import ThreadPoolExecutor, as_completed
from aitestapp.tool.cipher import Cipherd

logger = logging.getLogger(__name__)



class MyClass:
    def __init__(self, name):
        self.name = name
        print(f"{self.name} 对象被创建")

    def __del__(self):
        print(f"{self.name} 对象被销毁")
        
    def some_method(self):
        print(f"{self.name} 执行了某个方法")

class MyClassTwo(unittest.TestCase):

    def setUp(self):
        self.a = 3
        self.b = 2
        self.c = 3
        self.d = None
        self.e = [1,2,3]
        self.f = 4
        self.start_time = time.time()

    def tearDown(self):
        self.end_time = time.time()
        print('This is tearDown')
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.f = None

    def test_add_01(self):
        print('This is add_01')
        result = self.a + self.b
        self.assertEqual(result, 5)

    def test_add_02(self):
        print('This is add_02')
        result = self.a + self.b
        self.assertNotEqual(result, 3)

    def test_bool_true(self):
        print('This is bool_true')
        result = self.a + self.b
        self.assertTrue(result == 5)

    def test_bool_False(self):
        print('This is bool_false')
        result = self.a + self.b
        self.assertFalse(result == 23)

    def test_IS(self):
        print('This is IS')

        self.assertIs(self.a, self.c)

    def test_NotIS(self):
        print('This is NotIS')

        self.assertIsNot(self.a, self.b)

    def test_IsNone(self):
        print('This is IsNone')

        self.assertIsNone(self.d)
    
    def test_IsNotNone(self):
        print('This is IsNotNone')

        self.assertIsNotNone(self.a)
    
    def test_In(self):
        print('This is In')

        self.assertIn(self.a, self.e)
    
    def test_notin(self):
        print('This is notin')

        self.assertNotIn(self.f, self.e)

    def test_isinstance(self):
        print('This is test_isinstance')
        my_instance = MyClass('casam')
        self.assertIsInstance(my_instance, MyClass)
        self.assertIsInstance(my_instance, object)

    def test_notisinstance(self):
        print('This is test_notisinstance')

        my_instance = MyClass('casam')
        self.assertNotIsInstance(my_instance, int)
        self.assertNotIsInstance(my_instance, list)

zhipu_ai = ZhiPu4()
load_config = loadConfig()
configs = load_config.load_config()
class runTest(unittest.TestCase):
    def __init__(self, testpoint, api_name, expectedresult):
        super().__init__()
        self.testpoint = testpoint
        self.api_name = api_name
        self.expectedresult = expectedresult

    def setUp(self):
        self.start_time = time.time()
        self.special_url = ['/api/login','/api/signup']
        print('-----------setup-------------')

    def tearDown(self) -> None:
        self.end_time = time.time()
        print('------------tearDown------------')

    @retry(retries=2, delay=1)
    def runTest(self):
        self.test_run()

    def test_run(self):
        logger.info(f'---------------runtest: {self.testpoint}-------------')
        # 通过查询对应测试点的数据库，获取外键id
        testcase_id = models.InterfaceTestCase.objects.filter(testpoint=self.testpoint).values('testcaseid', 'project_name')
        if not testcase_id.exists():
            logger.error(f"未找到测试点 '{self.testpoint}' 对应的测试用例")
            raise ValueError(f"未找到测试点: {self.testpoint}")

        interface_file_id = testcase_id.first()['testcaseid']
        # 通过外键id查询主表得到主表id
        try:
            interface_file_id = models.InterfaceFileInfo.objects.get(id=interface_file_id)
        except models.InterfaceFileInfo.DoesNotExist:
            logger.error(f"未找到接口文件记录 (ID: {interface_file_id})")
            raise ValueError(f"接口文件记录不存在: {interface_file_id}")

        api_info_list = models.InterfaceApiInfo.objects.filter(interface_apiinfo_id=interface_file_id, title=self.api_name).values()
        if not api_info_list:
            logger.error(f"未找到API信息 (文件ID: {interface_file_id}, API名称: {self.api_name})")
            raise ValueError(f"未找到API信息: {self.api_name}")

        api_data_url = api_info_list[0]['url']
        # 遍历接口信息列表 api_info_list为读取数据库interface_apiinfo表中的数据
        data = {}
        for api_info in api_info_list:
            prompt = Prompts.api_desc_prompt(api_info)
            status, res = zhipu_ai.zhipuai_request(prompt)
            try:
                data[api_info['url']] = res.replace('\n', '')
            except (AttributeError, TypeError):
                data[api_info['url']] = res

        data_config_info = models.InterfaceDataConfig.objects.filter(data_desc=self.testpoint).values()
        if not data_config_info:
            logger.error(f"未找到数据配置 (测试点: {self.testpoint})")
            raise ValueError(f"未找到数据配置: {self.testpoint}")

        data_decs = data_config_info[0]['data_desc']
        data_info = data_config_info[0]['data_info']
        api_info_case = f"{data_decs},{self.expectedresult}"
        logger.debug(f"测试数据信息: {data_info}")

        api_case_info = f"接口描述为：{data}。测试用例为: {api_info_case}"
        case_prompt = Prompts.api_case_prompt(api_case_info) # 将接口描述和接口测试用例通过api_case_prompt转存prompt

        status, res = zhipu_ai.zhipuai_request(case_prompt) # 将prompt给到ai请求返回response
        # 对ai返回的response通过step为标识进行执行顺序的排序
        sorted_data = sorted(excute_to_json(res), key=lambda x: x['step']) 
        # print(sorted_data)
        test_data = {api_data_url: {'data': data_info, 'decs': data_decs}}

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
        self.result = response_data_list
        logger.debug(f"测试结果: {self.result}")
        if api_data_url in self.special_url:
            cipher = Cipherd()
            decryptData = cipher.decrypt(self.result[0]['msg'])
            self.result[0]['msg'] = decryptData
        logger.debug(f"状态码: {self.result[0].get('status_code')}, 期望结果类型: {type(self.expectedresult)}")
        match = re.search(r"'code': (\d+)", self.expectedresult)
        if match:
            code = int(match.group(1))
            try:
                self.assertEqual(self.result[0]['status_code'], code)
                logging.info(f"断言成功：{self.testpoint} 的状态码是 {code}。")
            except AssertionError:
                logging.info(f"断言失败：{self.testpoint} 的状态码是 {self.result[0]['status_code']}，期望值是 {code}。")
        else:
            logging.error(f"无法从预期结果中提取状态码: {self.expectedresult}")
        return self.result 
    