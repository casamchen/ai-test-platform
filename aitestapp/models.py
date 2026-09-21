from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


class ProjectConfig(models.Model):
    """项目配置表，存储键值对形式的配置信息"""
    key = models.CharField(max_length=20, verbose_name='配置键')
    value = models.CharField(max_length=40, verbose_name='配置值')
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    remarks = models.CharField(max_length=100, verbose_name='备注')

    class Meta:
        db_table = 'aitestapp_project_config'
        verbose_name = '项目配置'
        verbose_name_plural = '项目配置列表'

    def __str__(self):
        return f"{self.key}: {self.value}"


# 保留向后兼容的别名
project_config = ProjectConfig


class UserSession(models.Model):
    """用户会话关联表，用于跟踪和管理用户的登录状态"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    session = models.OneToOneField(Session, on_delete=models.CASCADE, verbose_name='会话')

    class Meta:
        db_table = 'aitestapp_usersession'
        verbose_name = '用户会话'


class FileInfo(models.Model):
    """文件信息表，存储上传的测试文件元数据"""
    project_name = models.CharField(max_length=20, verbose_name='项目名称')
    version = models.CharField(max_length=20, verbose_name='版本')
    function = models.CharField(max_length=300, verbose_name='功能描述')
    prd_name = models.CharField(max_length=30, verbose_name='PRD名称')
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    file_path = models.FileField(upload_to='aitestapp/data', verbose_name='文件路径')

    class Meta:
        db_table = 'aitestapp_fileinfo'
        verbose_name = '文件信息'

    def __str__(self):
        return f"{self.project_name} - {self.prd_name}"

# 向后兼容别名
fileinfo = FileInfo


class TestCase(models.Model):
    """测试用例表，存储AI生成的测试用例"""
    project_name = models.CharField(max_length=20, verbose_name='项目名称')
    version = models.CharField(max_length=20, verbose_name='版本')
    testcase = models.CharField(max_length=300, verbose_name='测试用例')
    priority = models.CharField(max_length=30, null=True, blank=True, verbose_name='优先级')
    operation = models.CharField(max_length=300, verbose_name='操作步骤')
    expectedresult = models.CharField(max_length=300, verbose_name='预期结果')
    actual_results = models.CharField(max_length=300, null=True, blank=True, verbose_name='实际结果')
    execution_time = models.DateField(auto_now_add=True, verbose_name='执行时间')
    execution_person = models.CharField(max_length=30, null=True, verbose_name='执行人')
    state = models.CharField(max_length=30, null=True, blank=True, verbose_name='状态')
    testcaseid = models.ForeignKey(FileInfo, on_delete=models.CASCADE, verbose_name='关联文件', related_name='testcases')

    class Meta:
        db_table = 'aitestapp_testcase'
        verbose_name = '测试用例'
        ordering = ['-id']

# 向后兼容别名
testcase = TestCase


class Requirement(models.Model):
    """需求表，存储产品需求文本和详情"""
    text = models.CharField(max_length=300, verbose_name='需求标题')
    needs = models.CharField(max_length=3000, verbose_name='需求详情')

    class Meta:
        db_table = 'aitestapp_requirements'
        verbose_name = '需求'

    def __str__(self):
        return self.text

# 向后兼容别名
requirements = Requirement


class Vector(models.Model):
    """向量表，存储FAISS向量检索的文本数据"""
    vector_id = models.CharField(max_length=20, verbose_name='向量ID')
    text = models.CharField(max_length=300, verbose_name='文本内容')

    class Meta:
        db_table = 'aitestapp_vectors'
        verbose_name = '向量数据'

# 向后兼容别名
vectors = Vector


class InterfaceFileInfo(models.Model):
    """接口文件信息表，存储接口测试相关的文件"""
    project = models.CharField(max_length=20, verbose_name='项目')
    version = models.CharField(max_length=300, verbose_name='版本')
    prd_name = models.CharField(max_length=300, null=True, verbose_name='PRD名称')
    path = models.FileField(upload_to='aitestapp/interface_file', verbose_name='文件路径')
    remark = models.CharField(max_length=3000, null=True, verbose_name='备注')
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'aitestapp_interface_fileinfo'
        verbose_name = '接口文件'


class InterfaceApiInfo(models.Model):
    """接口API信息表，存储接口的详细定义"""
    example = models.CharField(max_length=300, verbose_name='示例')
    response = models.CharField(max_length=600, verbose_name='响应')
    title = models.CharField(max_length=300, verbose_name='标题')
    url = models.CharField(max_length=300, verbose_name='URL')
    notes = models.CharField(max_length=300, null=True, verbose_name='备注')
    params = models.CharField(max_length=600, verbose_name='参数')
    status = models.CharField(max_length=300, verbose_name='状态')
    method = models.CharField(max_length=30, verbose_name='请求方法')
    interface_apiinfo_id = models.ForeignKey(InterfaceFileInfo, on_delete=models.CASCADE, related_name='api_infos')

    class Meta:
        db_table = 'aitestapp_interface_apiinfo'
        verbose_name = '接口API信息'


class InterfaceDataConfig(models.Model):
    """接口数据配置表，存储接口测试数据"""
    data_desc = models.CharField(max_length=200, verbose_name='数据描述')
    data_info = models.CharField(max_length=600, null=True, verbose_name='数据内容')
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    interface_api_id = models.ForeignKey(InterfaceFileInfo, on_delete=models.CASCADE, related_name='data_configs')

    class Meta:
        db_table = 'aitestapp_interface_data_config'
        verbose_name = '接口数据配置'


class InterfaceTestCase(models.Model):
    """接口测试用例表"""
    project_name = models.CharField(max_length=20, verbose_name='项目名称')
    version = models.CharField(max_length=20, verbose_name='版本')
    api_name = models.CharField(max_length=300, verbose_name='API名称')
    testpoint = models.CharField(max_length=300, verbose_name='测试点')
    expectedresult = models.CharField(max_length=300, verbose_name='预期结果')
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    testcaseid = models.ForeignKey(InterfaceFileInfo, on_delete=models.CASCADE, verbose_name='关联文件', related_name='testcases')

    class Meta:
        db_table = 'aitestapp_interface_testcase'
        verbose_name = '接口测试用例'

# 向后兼容别名
interface_testcase = InterfaceTestCase


class TestLog(models.Model):
    """测试日志表，记录测试执行过程（原名log，避免与stdlib冲突）"""
    test_id = models.CharField(max_length=20, verbose_name='测试ID')
    loginfo = models.CharField(max_length=6000, verbose_name='日志信息')
    vedio_path = models.CharField(max_length=300, verbose_name='视频路径')
    picture_path = models.CharField(max_length=300, verbose_name='截图路径')
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    execute_count = models.CharField(max_length=300, verbose_name='执行次数')

    class Meta:
        db_table = 'aitestapp_log'
        verbose_name = '测试日志'

# 向后兼容别名
log = TestLog


class TestReport(models.Model):
    """测试报告汇总表"""
    total = models.CharField(max_length=20, verbose_name='总数')
    successes = models.CharField(max_length=20, verbose_name='成功数')
    failures = models.CharField(max_length=20, verbose_name='失败数')
    errors = models.CharField(max_length=20, verbose_name='错误数')
    skipped = models.CharField(max_length=20, verbose_name='跳过数')
    expectedFailures = models.CharField(max_length=20, verbose_name='预期失败数')
    unexpectedSuccesses = models.CharField(max_length=20, verbose_name='意外成功数')
    execute_time = models.DateTimeField(auto_now_add=True, verbose_name='执行时间')

    class Meta:
        db_table = 'aitestapp_testreport'
        verbose_name = '测试报告'

# 向后兼容别名
testreport = TestReport


class TestCaseResult(models.Model):
    """测试用例结果详情表"""
    testpoint = models.CharField(max_length=300, verbose_name='测试点')
    result = models.CharField(max_length=20, verbose_name='结果')
    testinfo = models.CharField(max_length=8000, verbose_name='测试信息')
    platform = models.CharField(max_length=200, verbose_name='平台')
    execute_time = models.DateTimeField(auto_now_add=True, verbose_name='执行时间')
    testresultid = models.ForeignKey(TestReport, on_delete=models.CASCADE, verbose_name='关联报告', related_name='results')

    class Meta:
        db_table = 'aitestapp_testcase_result'
        verbose_name = '测试用例结果'

# 向后兼容别名
testcase_result = TestCaseResult
