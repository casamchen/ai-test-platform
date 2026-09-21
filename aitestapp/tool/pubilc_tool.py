import unittest
import time

def retry(retries, delay):
    def decorator(test_func):
        def wrapper(*args, **kwargs):
            success = False
            exception = None

            for _ in range(retries + 1):
                try:
                    # 执行测试用例
                    test_func(*args, **kwargs)
                except (unittest.SkipTest, AssertionError, Exception) as e:
                    # 如果是跳过测试或者断言失败，记录日志并等待一段时间
                    print(f'Retry: {test_func.__name__} - {str(e)}')
                    time.sleep(delay)
                    exception = e
                else:
                    # 如果测试通过，设置标志变量为True 并退出循环
                    success = True
                    break
            
            if not success:
                # 如果循环结束时标志变量仍然为False， 说明充实次数已经用尽，抛出最后一次失败的异常
                raise exception
        
        return wrapper
    return decorator