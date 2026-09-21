"""
URL configuration for aitest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from aitestapp.views import views
from aitestapp.views.login import login_views
from aitestapp.views.ai_create_testcase import uploadprd, testcase, checkdata
from aitestapp.views.ai_interface_test import interfaceadmin, interfacetestcase, interfacedataconfig, test_unittest, interfacereport



urlpatterns = [
    path('admin/', admin.site.urls),
    path('checkconfig', views.check_config),
    path('addconfigdata', views.add_config_data),
    path('updataconfigdata', views.update_config_data),
    path('deleteconfigdata', views.delete_config_data),
    path('login', login_views.sign_in),
    path('signup', login_views.sign_up),
    path('uploadprd', uploadprd.uploadprd),
    path('check_task_status', uploadprd.check_task_status),
    path('uploadprdinfo', uploadprd.uploadprd_info),
    path('checkprdinfo', checkdata.checkprdinfo),
    path('filecontent', uploadprd.showfile_content),
    path('searchtestcase', testcase.search_testcase),
    path('showtestcase', testcase.show_testcase),
    path('updatetestcase_state', testcase.update_state),
    path('updatetestcase_result', testcase.update_result),
    path('create_testcase', uploadprd.create_testcase),
    path('uploadinterfacefile', interfaceadmin.upload_interface_file),
    path('checkinterfaceinfo', interfaceadmin.check_interface_info),
    path('uploadinterfaceinfo', interfaceadmin.upload_interface_info),
    path('showinterfacecontent', interfaceadmin.show_interface_content),
    path('createinterfacetesecase', interfaceadmin.create_interface_testcase),
    path('showinterfacetestcase', interfacetestcase.show_interface_testcase),
    path('checkdataconfig', interfacetestcase.check_data_config),
    path('searchinterfacetestcase', interfacetestcase.search_interface_testcase),
    path('showinterfacedataconfig', interfacedataconfig.show_interface_data_config),
    path('updatedataconfig', interfacetestcase.update_data_config),
    path('test_one', test_unittest.test_one),
    path('excute_testcase', interfacetestcase.excute_testcase),
    path('excute_all_testcase', interfacetestcase.excute_all_testcase),
    path('showtestreport', interfacereport.show_interface_report),
    path('searchtestreport', interfacereport.search_interface_report),
    path('getreportlog', interfacereport.get_interface_report_log),
    path('abc', interfacereport.aaaaa)


]