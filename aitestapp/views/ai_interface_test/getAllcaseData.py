from aitestapp.scripts.prompts_interface import Prompts
from aitestapp.scripts.model_AI import ZhiPu4
from aitestapp.scripts.utils import excute_to_json
from aitestapp.scripts.test_data import TestData
from aitestapp.scripts.config_interface import loadConfig
from aitestapp.scripts.test_case_executor import TestCaseExecutor
from concurrent.futures import ThreadPoolExecutor, as_completed
from aitestapp.tool.cipher import Cipherd
from aitestapp.views.ai_interface_test.tests_famwork import runTest
from aitestapp.views.ai_interface_test.tests_result import MyTestResult
from aitestapp import models
import unittest

zhipu_ai = ZhiPu4()
load_config = loadConfig()
configs = load_config.load_config()
class getAllData:

    def get_All_Data(self, id):
        # 这是测试用例的信息
        
        self.testcase_info_list = models.InterfaceTestCase.objects.filter(testcaseid=id).values('api_name', 'testpoint','expectedresult')
        return self.testcase_info_list
    
    def getData(self, testpoint, api_name, expectedresult):
        # 这是测试用例的信息
        self.testcase_info_list = [{'testpoint': testpoint,'api_name': api_name,'expectedresult': expectedresult}]
        return self.testcase_info_list

    def execute(self):
        all_results = []  # 创建一个列表来存储所有测试用例的结果
        # 使用 ThreadPoolExecutor 并行处理测试用例
        # 限制最大线程数，防止创建过多线程导致资源耗尽
        max_workers = min(len(self.testcase_info_list), 10)  # 最多10个线程
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.execute_func, case['testpoint'], case['api_name'], case['expectedresult']): case for case in self.testcase_info_list}
            for future in as_completed(futures):
                response_data = future.result()
                print('================')
                print(response_data)
                print('================')
                all_results.append(response_data)
                summary = self.summarize_results(all_results)
        count_num = summary[0]
        testresult = summary[1]['test_results']
        id = models.TestReport.objects.create(
            total = count_num['total'],
            successes= count_num['successes'],
            failures= count_num['failures'],
            errors= count_num['errors'],
            skipped= count_num['skipped'],
            expectedFailures= count_num['expectedFailures'],
            unexpectedSuccesses= count_num['unexpectedSuccesses']
        )
        new_summary = []
        for result in testresult:
            if result['success']:
                execute = models.TestCaseResult.objects.create(
                        testpoint = result['name'],
                        result = '测试通过',
                        testinfo = result['result'][0],
                        platform = result['platform'],
                        testresultid = id
                    )
            else:
                execute = models.TestCaseResult.objects.create(
                        testpoint = result['name'],
                        result = '测试失败',
                        testinfo = result['result'][0],
                        platform = result['platform'],
                        testresultid = id
                    )
        test_result = models.TestCaseResult.objects.filter(testresultid=id).values()
        new_summary.append({'count': summary[0]})
        new_summary.append({'test_results': test_result})
        return new_summary

    def execute_func(self, testpoint, api_name, expectedresult):
        MyTestResult.set_test_id(testpoint)
        my_class_instance = runTest(testpoint=testpoint, api_name=api_name, expectedresult=expectedresult)
        myclass_suite = unittest.TestSuite()
        myclass_suite.addTest(my_class_instance)

        runner = unittest.TextTestRunner(resultclass=MyTestResult)
        test_result = runner.run(myclass_suite)
        result = test_result.summary
        result_count = result['stat']

        return result_count, result

    def summarize_results(self, results):
        summary = [
            {
                'total': 0,
                'successes': 0,
                'failures': 0,
                'errors': 0,
                'skipped': 0,
                'expectedFailures': 0,
                'unexpectedSuccesses': 0
            },
            {
                'test_results': [] # 测试用例结果
            }
        ]
        for result in results:
            stats, queryset = result
            summary[0]['total'] += stats['testsRun']
            summary[0]['successes'] += stats['successes']
            summary[0]['failures'] += stats['failures']
            summary[0]['errors'] += stats['errors']
            summary[0]['skipped'] += stats['skipped']
            summary[0]['expectedFailures'] += stats['expectedFailures']
            summary[0]['unexpectedSuccesses'] += stats['unexpectedSuccesses']
            summary[1]['test_results'].append(queryset)
        
        return summary