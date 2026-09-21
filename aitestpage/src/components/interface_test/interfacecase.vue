<template>
  <div class="testcase-container">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h2 class="page-title">接口测试用例</h2>
          <p class="page-description">管理和执行接口测试用例，查看测试结果</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" @click="excute_all_testcase">一键运行</el-button>
        </div>
      </div>
    </div>

    <!-- Search Bar -->
    <div class="search-bar">
      <el-input v-model="input" placeholder="请输入需求文档 ID" clearable></el-input>
      <el-button @click="search">搜索</el-button>
    </div>

    <!-- Table Card -->
    <div class="table-card">
      <el-table :data="testcaseList" style="width: 100%" border>
        <el-table-column prop="id" label="ID" min-width="60">
          <template slot-scope="scope"> {{ scope.row.id }} </template>
        </el-table-column>
        <el-table-column prop="api_name" label="接口名称" min-width="140">
          <template slot-scope="scope"> {{ scope.row.api_name }} </template>
        </el-table-column>
        <el-table-column prop="testpoint" label="测试点" min-width="180">
          <template slot-scope="scope"> {{ scope.row.testpoint }} </template>
        </el-table-column>
        <el-table-column prop="expectedresult" label="预期结果" min-width="200">
          <template slot-scope="scope"> {{ scope.row.expectedresult }} </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" min-width="160">
          <template slot-scope="scope"> {{ scope.row.create_time }} </template>
        </el-table-column>
        <el-table-column prop="edit" label="操作" min-width="180" fixed="right">
          <template slot-scope="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="primary" @click="excute(scope.row)">运行</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- Edit Dialog -->
    <el-dialog class="edit-dialog" :visible.sync="dialogVisible" :before-close="handleClose" title="编辑数据配置" custom-class="dark-dialog">
      <el-form :model="update_data_config" label-position="top">
        <el-form-item label="接口名称">
          <div class="form-display">{{ update_data_config.testpoint }}</div>
        </el-form-item>
        <el-form-item label="数据配置">
          <el-input v-model="update_data_config.data_config" type="textarea" :rows="6"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelButton">取消</el-button>
        <el-button type="primary" @click="update">确定</el-button>
      </div>
    </el-dialog>

    <!-- Result Dialog -->
    <el-dialog :visible.sync="resultVisible" :before-close="handleClose" title="测试执行结果" custom-class="dark-dialog result-dialog">
      <div class="execution-summary">
        <span v-if="testExecutionSummary.total > 0" class="summary-item">总执行: <strong>{{ testExecutionSummary.total }}</strong></span>
        <span v-if="testExecutionSummary.successes > 0" class="summary-item success">成功: <strong>{{ testExecutionSummary.successes }}</strong></span>
        <span v-if="testExecutionSummary.failures > 0" class="summary-item failure">失败: <strong>{{ testExecutionSummary.failures }}</strong></span>
        <span v-if="testExecutionSummary.errors > 0" class="summary-item error">错误: <strong>{{ testExecutionSummary.errors }}</strong></span>
        <span v-if="testExecutionSummary.skipped > 0" class="summary-item skipped">跳过: <strong>{{ testExecutionSummary.skipped }}</strong></span>
        <span v-if="testExecutionSummary.expectedFailures > 0" class="summary-item expected">期望失败: <strong>{{ testExecutionSummary.expectedFailures }}</strong></span>
        <span v-if="testExecutionSummary.unexpectedSuccesses > 0" class="summary-item unexpected">非期望成功: <strong>{{ testExecutionSummary.unexpectedSuccesses }}</strong></span>
      </div>
      <el-table :data="testcaseResult" style="width: 100%" border max-height="400px">
        <el-table-column prop="id" label="ID" min-width="60">
          <template slot-scope="scope"> {{ scope.row.id }} </template>
        </el-table-column>
        <el-table-column prop="testpoint" label="测试点" min-width="150">
          <template slot-scope="scope"> {{ scope.row.testpoint }} </template>
        </el-table-column>
        <el-table-column prop="result" label="运行结果" min-width="100">
          <template slot-scope="scope">
            <el-tag :type="getResultType(scope.row.result)" size="small">{{ scope.row.result }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="testinfo" label="结果日志" min-width="120">
          <template slot-scope="scope">
            <el-button type="text" @click="checktestinfo(scope.row)">查看结果日志</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="platform" label="平台" min-width="100">
          <template slot-scope="scope"> {{ scope.row.platform }} </template>
        </el-table-column>
        <el-table-column prop="execute_time" label="执行时间" min-width="160">
          <template slot-scope="scope"> {{ scope.row.execute_time }} </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- Log Detail Dialog -->
    <el-dialog :visible.sync="resultInfoVisible" :before-close="handleClose" title="结果日志详情" custom-class="dark-dialog info-dialog">
      <div v-html="sanitizedTestinfo" class="log-content"></div>
    </el-dialog>

    <!-- Pagination -->
    <div class="pagination-wrapper">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page.sync="currentPage"
        :page-sizes="[15, 30, 45, 60, 75]"
        :page-size="pageSize"
        layout="sizes, prev, pager, next"
        :total="total">
      </el-pagination>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      input: '',
      dialogVisible: false,
      resultInfoVisible: false,
      currentPage: 1,
      pageSize: 15,
      total: 0,
      testcaseList: [],
      testinfo: '',
      update_data_config: {
        testpoint: '',
        data_config: ''
      },
      resultVisible: false,
      testcaseResult: {},
      testExecutionSummary: {
        total: 0,
        successes: 0,
        failures: 0,
        errors: 0,
        skipped: 0,
        expectedFailures: 0,
        unexpectedSuccesses: 0
      }
    }
  },
  created () {
    this.showtestcase()
  },
  computed: {
    tableHeight () {
      const mainHeight = this.$parent.$el.clientHeight
      return mainHeight - 56 - 46 - 24
    },
    sanitizedTestinfo () {
      return this.sanitizeHtml(this.testinfo)
    }
  },
  methods: {
    sanitizeHtml (html) {
      if (!html) return ''
      return String(html)
        .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
        .replace(/on\w+\s*=\s*"[^"]*"/gi, '')
        .replace(/on\w+\s*=\s*'[^']*'/gi, '')
        .replace(/on\w+\s*=[^\s>]+/gi, '')
        .replace(/javascript:/gi, '')
        .replace(/vbscript:/gi, '')
        .replace(/data:\s*text\/html/gi, '')
    },
    getResultType (result) {
      if (result === 'PASS' || result === 'SUCCESS') return 'success'
      if (result === 'FAIL' || result === 'FAILURE') return 'danger'
      if (result === 'ERROR') return 'warning'
      if (result === 'SKIP') return 'info'
      return 'info'
    },
    showtestcase () {
      let formData = new FormData()
      formData.append('Page', this.currentPage)
      formData.append('limit', this.pageSize)
      this.axios.post('/api/showinterfacetestcase', formData)
        .then((res) => {
          this.testcaseList = Object.values(res.data.msg)
          this.total = res.data.total
        })
        .catch(error => {
          console.error('Error fetching data:', error)
        })
    },
    search () {
      let formData = new FormData()
      formData.append('id', this.input)
      formData.append('Page', this.currentPage)
      formData.append('limit', this.pageSize)
      this.axios.post('/api/searchinterfacetestcase', formData)
        .then((res) => {
          const code = res.data.code
          if (code === 0) {
            this.testcaseList = Object.values(res.data.msg)
            this.total = res.data.total
          } else {
            this.$message({
              message: res.data.msg,
              type: 'warning'
            })
          }
        })
    },
    handleClose (done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {})
    },
    cancelButton () {
      this.dialogVisible = false
      this.update_data_config.data_config = ''
    },
    handleEdit (row) {
      this.dialogVisible = true
      let formData = new FormData()
      formData.append('id', row.id)
      this.axios.post('/api/checkdataconfig', formData)
        .then((res) => {
          const config = res.data.msg
          this.update_data_config.testpoint = row.testpoint
          this.update_data_config.data_config = config
        })
    },
    update () {
      let formData = new FormData()
      formData.append('testpoint', this.update_data_config.testpoint)
      formData.append('data_config', this.update_data_config.data_config)
      this.axios.post('/api/updatedataconfig', formData)
        .then((res) => {
          const code = res.data.code
          if (code === 0) {
            this.dialogVisible = false
            this.update_data_config.data_config = ''
            this.$message({
              message: res.data.msg,
              type: 'success'
            })
          } else {
            this.$message({
              message: res.data.msg,
              type: 'warning'
            })
          }
        })
    },
    excute (row) {
      let formData = new FormData()
      formData.append('testpoint', row.testpoint)
      formData.append('api_name', row.api_name)
      formData.append('expectedresult', row.expectedresult)
      this.axios.post('/api/excute_testcase', formData)
        .then((res) => {
          const code = res.data.code
          if (code === 0) {
            this.resultVisible = true
            this.testcaseResult = Object.values(res.data.msg)
            this.testExecutionSummary = res.data.count
          } else {
            this.$message({
              message: res.data.msg,
              type: 'warning'
            })
          }
        })
    },
    excute_all_testcase () {
      if (this.input === '') {
        let formData = new FormData()
        formData.append('id', 4)
        this.axios.post('/api/excute_all_testcase', formData)
          .then((res) => {
            const code = res.data.code
            if (code === 0) {
              this.resultVisible = true
              this.testcaseResult = Object.values(res.data.msg)
              this.testExecutionSummary = res.data.count
            } else {
              this.$message({
                message: res.data.msg,
                type: 'warning'
              })
            }
          })
      } else {
        let formData = new FormData()
        formData.append('id', this.input)
        this.axios.post('/api/excute_all_testcase', formData)
          .then((res) => {
            const code = res.data.code
            if (code === 0) {
              this.resultVisible = true
              this.testcaseResult = Object.values(res.data.msg)
              this.testExecutionSummary = res.data.count
            } else {
              this.$message({
                message: res.data.msg,
                type: 'warning'
              })
            }
          })
      }
    },
    checktestinfo (row) {
      this.resultInfoVisible = true
      this.testinfo = row.testinfo
    },
    handleSizeChange (val) {
      this.pageSize = val
      this.showtestcase()
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.showtestcase()
    }
  }
}
</script>

<style scoped>
/* CSS Variables */
.testcase-container {
  --bg-base: #09090B;
  --bg-surface: #18181B;
  --bg-elevated: #27272A;
  --text-primary: #F4F4F5;
  --text-secondary: #E4E4E7;
  --text-muted: #A1A1AA;
  --border-default: #27272A;
  --border-subtle: #3F3F46;
  --color-primary-500: #3B82F6;
  --radius-lg: 8px;
  --radius-xl: 10px;

  height: 100%;
  min-height: calc(100vh - 24px);
  display: flex;
  flex-direction: column;
  background-color: var(--bg-base);
  padding: 20px;
  color: var(--text-primary);
}

/* Page Header */
.page-header {
  flex-shrink: 0;
  margin-bottom: 16px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-text {
  flex: 1;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

.page-description {
  font-size: 14px;
  color: var(--text-muted);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* Search Bar */
.search-bar {
  flex-shrink: 0;
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 16px;
}

.search-bar .el-input {
  max-width: 300px;
}

/* Table Card */
.table-card {
  flex: 1;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 20px;
  overflow: auto;
  min-height: 200px;
}

/* Dark Dialog Styles */
.testcase-container /deep/ .dark-dialog {
  background-color: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
}

.testcase-container /deep/ .dark-dialog .el-dialog__header {
  background-color: var(--bg-elevated);
  border-bottom: 1px solid var(--border-subtle);
  padding: 16px 20px;
  margin: 0;
}

.testcase-container /deep/ .dark-dialog .el-dialog__title {
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 600;
}

.testcase-container /deep/ .dark-dialog .el-dialog__body {
  background-color: var(--bg-elevated);
  padding: 20px;
  color: var(--text-primary);
}

.testcase-container /deep/ .dark-dialog .el-dialog__footer {
  background-color: var(--bg-elevated);
  border-top: 1px solid var(--border-subtle);
  padding: 16px 20px;
}

/* Form Styles */
.testcase-container /deep/ .el-form-item__label {
  color: var(--text-secondary);
}

.testcase-container /deep/ .el-input__inner {
  background-color: var(--bg-base);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.testcase-container /deep/ .el-input__inner:focus {
  border-color: var(--color-primary-500);
}

.testcase-container /deep/ .el-textarea__inner {
  background-color: var(--bg-base);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.testcase-container /deep/ .el-textarea__inner:focus {
  border-color: var(--color-primary-500);
}

.form-display {
  padding: 8px 12px;
  background-color: var(--bg-base);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  color: var(--text-muted);
  font-size: 14px;
}

/* Execution Summary */
.execution-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding: 16px;
  background-color: var(--bg-base);
  border-radius: var(--radius-lg);
  margin-bottom: 16px;
}

.summary-item {
  color: var(--text-secondary);
  font-size: 14px;
}

.summary-item strong {
  color: var(--text-primary);
  margin-left: 4px;
}

.summary-item.success strong { color: #10B981; }
.summary-item.failure strong { color: #EF4444; }
.summary-item.error strong { color: #F59E0B; }
.summary-item.skipped strong { color: #8B5CF6; }
.summary-item.expected strong { color: #6B7280; }
.summary-item.unexpected strong { color: #06B6D4; }

/* Table Styles */
.testcase-container /deep/ .el-table {
  background-color: transparent;
  color: var(--text-primary);
}

.testcase-container /deep/ .el-table th.el-table__cell {
  background-color: var(--bg-elevated);
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-subtle);
}

.testcase-container /deep/ .el-table td.el-table__cell {
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--border-default);
  color: var(--text-primary);
}

.testcase-container /deep/ .el-table--border::after,
.testcase-container /deep/ .el-table--group::after,
.testcase-container /deep/ .el-table::before {
  background-color: var(--border-default);
}

.testcase-container /deep/ .el-table--border {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
}

.testcase-container /deep/ .el-table__empty-block {
  background-color: var(--bg-surface);
  color: var(--text-muted);
  min-height: 120px;
  max-height: 200px;
}

/* Button Styles */
.testcase-container /deep/ .el-button--primary {
  background-color: var(--color-primary-500);
  border-color: var(--color-primary-500);
}

.testcase-container /deep/ .el-button--primary:hover {
  background-color: #2563EB;
  border-color: #2563EB;
}

.testcase-container /deep/ .el-button--default {
  background-color: var(--bg-elevated);
  border-color: var(--border-default);
  color: var(--color-primary-500) !important;
}

.testcase-container /deep/ .el-button--default span,
.testcase-container /deep/ .el-button--default i {
  color: var(--color-primary-500) !important;
}

.testcase-container /deep/ .el-button--default:hover {
  background-color: var(--color-primary-500);
  border-color: var(--color-primary-500);
}

.testcase-container /deep/ .el-button--default:hover span,
.testcase-container /deep/ .el-button--default:hover i {
  color: #FFFFFF !important;
}

.testcase-container /deep/ .el-button--text {
  color: var(--color-primary-500);
}

.testcase-container /deep/ .el-button--text:hover {
  color: #2563EB;
}

/* Tag Styles */
.testcase-container /deep/ .el-tag--success {
  background-color: rgba(16, 185, 129, 0.2);
  border-color: #10B981;
  color: #10B981;
}

.testcase-container /deep/ .el-tag--danger {
  background-color: rgba(239, 68, 68, 0.2);
  border-color: #EF4444;
  color: #EF4444;
}

.testcase-container /deep/ .el-tag--warning {
  background-color: rgba(245, 158, 11, 0.2);
  border-color: #F59E0B;
  color: #F59E0B;
}

.testcase-container /deep/ .el-tag--info {
  background-color: rgba(59, 130, 246, 0.2);
  border-color: #3B82F6;
  color: #3B82F6;
}

/* Pagination */
.pagination-wrapper {
  position: sticky;
  bottom: 0;
  z-index: 1000;
  padding: 16px 0;
  background-color: var(--bg-base);
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.3);
}

.testcase-container /deep/ .el-pagination {
  color: var(--text-secondary);
}

.testcase-container /deep/ .el-pagination .el-pager li {
  background-color: var(--bg-elevated);
  color: var(--text-secondary);
  border: 1px solid var(--border-default);
}

.testcase-container /deep/ .el-pagination .el-pager li.active {
  background-color: var(--color-primary-500);
  color: white;
  border-color: var(--color-primary-500);
}

.testcase-container /deep/ .el-pagination button {
  background-color: var(--bg-elevated);
  color: var(--text-secondary);
  border: 1px solid var(--border-default);
}

.testcase-container /deep/ .el-select .el-input__inner {
  background-color: var(--bg-elevated);
  border-color: var(--border-default);
  color: var(--text-primary);
}

/* Log Content */
.log-content {
  white-space: pre-wrap;
  word-break: break-all;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
  background-color: var(--bg-base);
  padding: 16px;
  border-radius: var(--radius-lg);
  max-height: 70vh;
  overflow-y: auto;
}
</style>
