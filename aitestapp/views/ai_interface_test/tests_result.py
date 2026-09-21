import platform
from typing import TextIO
import unittest
import time
import logging
from PIL import ImageGrab
import threading
from aitestapp import models
from django.conf import settings

# 配置日志格式，指定了日志的级别、格式和日期格式
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def get_platform_info():
     # 获取执行平台信息
    return {
        "platform": platform.platform(),
        "system": platform.system(),
        "python_version": platform.python_version(),
        # "env": dict(os.environ),
    }

class MyTestResult(unittest.TestResult):
    test_id = None
    def __init__(self, stream = None, descriptions = None, verbosity = 1):
        super().__init__(stream, descriptions, verbosity)
        self.log = logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
        # 对父类的默认熟悉做部分修改
        self.testcase_results = []  # 所有用例测试结果对象（TestCaseResult对象）列表
        self.successes = []  # 成功用例对象列表，万一用得着呢
        self.verbosity = verbosity or 1  # 设置默认verbosity为1
        self.buffer = True  # 在本定制方法中强制使用self.buffer=True，缓存用例输出
        self.test_results = []
        self.name = None  # 提供通过修改result对象的name属性为结果提供名称描述
        self.start_at = None
        self.end_at = None
        self.duration = None

        # 由于继承的父类属性中存在failures、errors等属性（存放失败和异常的用例列表），此处加以区分
        self.successes_count = 0  # 成功用例数
        self.failures_count = 0  # 失败用例数
        self.errors_count = 0  # 异常用例数
        self.skipped_count = 0  # 跳过用例数
        self.expectedFailures_count = 0  # 期望失败用例数
        self.unexpectedSuccesses_count = 0  # 非期望成功用例数

        self.know_exceptions = {}  # 已知异常字典，用于通过异常名来映射失败原因
    @property
    def summary(self):
        data = dict(
            name=self.name,
            success=self.wasSuccessful(),  # 用例是否成功，父类unittest.TestResult自带方法
            stat=dict(
                testsRun=self.testsRun,
                successes=self.successes_count,
                failures=self.failures_count,
                errors=self.errors_count,
                skipped=self.skipped_count,
                expectedFailures=self.expectedFailures_count,
                unexpectedSuccesses=self.unexpectedSuccesses_count,
            ),
            time=dict(
                start_at=self.start_at,
                end_at=self.end_at,
                duration=self.duration
            ),
            result = self.test_results,
            platform=get_platform_info(),
            # details=[item.data for item in self.testcase_results]  # 每个测试用例结果对象转为其字典格式的数据
        )
        return data
        
    def time_to_string(timestamp: float) -> str:
        time_array = time.localtime(timestamp)
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        return time_str

    @classmethod
    def set_test_id(cls, test_id):
        cls.test_id = test_id

    def startTestRun(self):
        super().startTestRun()
        self.start_at = time.time()
        self.name = self.__class__.test_id
        if self.verbosity > 1:
            logging.info(f'===== 测试开始, 开始时间: {self.time_to_string(self.start_at)} =====')
        # 开始记录时间戳
        logging.info(f"测试运行开始{self.__class__.test_id}")

    def stopTestRun(self):
        super().stopTestRun()
        self.end_at = time.time()
        self.duration = self.end_at - self.start_at  # 整个执行的持续        
        self.success = self.wasSuccessful()  # 整个执行是否成功
        if self.verbosity > 1:
            logging.info(f'===== 测试结束, 持续时间: {self.duration}秒 =====')
        # 记录结束时间戳，计算运行时间
        logging.info(f"测试运行结束: {self.__class__.test_id}")
        logging.info(f"测试运行时间{self.duration}")
    
    def startTest(self, test):
        super().startTest(test)
        # APP，开始录制视频（abd record）
        test.result = MyTestResult(test)
        self.testcase_results.append(test.result)
        test.result.start_at = time.time()

        self.start_video_recording(test.id(), 26)  # 高分辨率，每秒26张截图
        # WEB, 开始录制视频（每秒截图26----高分辨率，每秒截图3张----低分辨率）---python库
        logging.info(f"开始执行测试:{self.__class__.test_id}")

    def stopTest(self, test):
        super().stopTest(test)
        # APP，结束录制视频
        self.stop_recording = True
        if hasattr(self, '_recording_thread') and self.recording_thread.is_alive(): # 通过hassattr检查线程是否存在，如果存在则往下执行，如果不存在则不会触发报错：AttributeError: 'MyTestResult' object has no attribute 'recording_thread'
            self.recording_thread.join()  # 等待截图线程结束
        # WEB，结束录制视频（将图片合成视频）
        logging.info(f"结束执行测试:{test.id()}")
        logging.info(f"执行了多少用例:{len(self.test_results)}")

    def addError(self, test, err):
        super().addError(test,err)
        # 截图，人工判断
        self.take_screenshot(test.id(), 'error')
        logging.error(f"测试 {test.id()}发生错误:{err}")
        self.errors_count += 1
        test_result = test.result
        # 将结果存储在 TestResult 对象中
        self.test_results.append(test_result)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        # 截图，人工判断
        self.take_screenshot(test.id(), 'failure')
        logging.error(f"测试 {test.id()}失败:{err}")
        self.failures_count += 1
        test_result = test.result
        # 将结果存储在 TestResult 对象中
        self.test_results.append(test_result)

    def addSuccess(self, test):
        super().addSuccess(test)
        self.take_screenshot(test.id(), 'success')
        logging.info(f"测试通过:{test.id()}")
        self.successes_count += 1
        test_result = test.result
        # 将结果存储在 TestResult 对象中
        self.test_results.append(test_result)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        # 截图，人工判断
        self.take_screenshot(test.id(), 'skip')
        logging.info(f"跳过测试{test.id()}，原因:{reason}")
        self.skipped_count += 1
        test_result = test.result
        # 将结果存储在 TestResult 对象中
        self.test_results.append(test_result)

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        # 截图，人工判断
        self.take_screenshot(test.id(), 'ExpectedFailure')
        logging.error(f"预期失败的测试{test.id()}: {err}")
        self.expectedFailures_count += 1
        test_result = test.result
        # 将结果存储在 TestResult 对象中
        self.test_results.append(test_result)

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        # 截图，人工判断
        self.take_screenshot(test.id(), 'UnexpectedSuccess')
        logging.info(f"意外成功的测试:{test.id()}")
        self.unexpectedSuccesses_count += 1
        test_result = test.result
        # 将结果存储在 TestResult 对象中
        self.test_results.append(test_result)

    def take_screenshot(self, test_id, screenshot_type):
        # 捕获屏幕截图
        screenshot = ImageGrab.grab()
        # 保存截图
        screenshot.save(os.path.join(getattr(settings, 'SCREENSHOT_DIR', os.path.join(settings.MEDIA_ROOT, 'screenshot')), f'{test_id}_{screenshot_type}.png'))
        logging.info(f'已保存截图：{test_id}_{screenshot_type}.png')
    
    def start_video_recording(self, test_id, frequency):
        # 启动截图线程
        self.stop_recording = False # 给定false，在结束测试时改为true就停止截图
        self.recording_thread = threading.Thread(target=self.record_video, args=(test_id, frequency))
        self.recording_thread.start()

    def record_video(self, test_id, frequency):
        # 截图录屏方法
        screenshot_count = 0 # 截图次数
        while not self.stop_recording: # 为false时，开始截图录屏
            screenshot = ImageGrab.grab()
            screenshot.save(os.path.join(getattr(settings, 'RECORD_DIR', os.path.join(settings.MEDIA_ROOT, 'record')), f'{test_id}_screenshot_{screenshot_count}.png'))
            screenshot_count += 1 # 根据给定的截图频率进行截图命名
            time.sleep(1 / frequency)  # 根据频率控制截图速度

    def getTestResults(self):
        # 返回所有测试用例的结果
        return self.test_results
