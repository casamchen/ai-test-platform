from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from aitestapp import models
from aitestapp.tool.cipher import Cipherd
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from docx import Document
from aitestapp.views.ai_interface_test import tests_famwork
from aitestapp.views.ai_interface_test.tests_famwork import MyClass, MyClassTwo, runTest
from aitestapp.views.ai_interface_test.tests_result import MyTestResult
from PyPDF2 import PdfReader
import unittest

@require_http_methods(['GET'])
def test_one(requset):
    response = {}
    # my_class = MyClass(name='casam')
    # my_class.some_method()

    # 第一种实现方式-----------------
    # myclass_suite = unittest.TestSuite()
    # myclass_suite.addTest(MyClassTwo('test_login'))

    # 第二种实现方式-------------------
    # loader = unittest.TestLoader()
    # myclass_suite = loader.loadTestsFromModule(tests_famwork)

    # # 第三种实现方式--------------------
    loader = unittest.TestLoader()
    myclass_suite = loader.loadTestsFromTestCase(MyClassTwo)

    # # 动态传参方式-------------------
    # student_id = 3
    # excepted_results = 200
    # MyTestResult.set_test_id('1.high_resolution')
    # my_class_instance = MyClassThree(student_id=student_id, expected_results=excepted_results)
    # myclass_suite = unittest.TestSuite()
    # myclass_suite.addTest(my_class_instance)


    runner = unittest.TextTestRunner(resultclass=MyTestResult)
    test_result = runner.run(myclass_suite)

    response['code'] = 0
    return JsonResponse(response)
