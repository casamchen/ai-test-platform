<template>
  <div class="report-container">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h2 class="page-title">测试报告</h2>
          <p class="page-description">查看接口测试执行结果和统计分析</p>
        </div>
      </div>
    </div>

    <!-- Search Bar -->
    <div class="search-bar">
      <el-input v-model="input" placeholder="请输入 ID" clearable style="max-width: 300px;"></el-input>
      <el-button @click="search">搜索</el-button>
    </div>

    <!-- Chart and Table Container -->
    <div class="chart-table-container">
      <!-- Charts Section -->
      <div class="chart-wrapper">
        <el-row :gutter="20" class="graph-row">
          <el-col :xs="24" :sm="12">
            <!-- 柱状图 -->
            <div class="chart-card">
              <div class="chart-title">执行结果分布</div>
              <div ref="echarts2" class="chart"></div>
            </div>
          </el-col>
          <el-col :xs="24" :sm="12">
            <!-- 饼状图 -->
            <div class="chart-card">
              <div class="chart-title">结果占比</div>
              <div ref="echarts3" class="chart"></div>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- Table Card -->
      <div class="table-card">
        <el-table :data="testresultList" style="width: 100%" border :max-height="testresultList.length > 0 ? tableHeight : undefined">
          <el-table-column prop="id" label="ID" min-width="60">
            <template slot-scope="scope"> {{ scope.row.id }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('total')" prop="total" label="总运行数量" min-width="100">
            <template slot-scope="scope"> {{ scope.row.total }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('successes')" prop="successes" label="执行成功" min-width="90">
            <template slot-scope="scope"> {{ scope.row.successes }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('failures')" prop="failures" label="执行失败" min-width="90">
            <template slot-scope="scope"> {{ scope.row.failures }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('errors')" prop="errors" label="执行错误" min-width="90">
            <template slot-scope="scope"> {{ scope.row.errors }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('skipped')" prop="skipped" label="跳过执行" min-width="90">
            <template slot-scope="scope"> {{ scope.row.skipped }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('expectedFailures')" prop="expectedFailures" label="期望失败" min-width="100">
            <template slot-scope="scope"> {{ scope.row.expectedFailures }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('unexpectedSuccesses')" prop="unexpectedSuccesses" label="非期望成功" min-width="110">
            <template slot-scope="scope"> {{ scope.row.unexpectedSuccesses }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('passRate')" prop="passRate" label="通过率" min-width="80">
            <template slot-scope="scope">
              <span class="rate-success">{{ scope.row.passRate }}</span>
            </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('failRate')" prop="failRate" label="失败率" min-width="80">
            <template slot-scope="scope">
              <span class="rate-failure">{{ scope.row.failRate }}</span>
            </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('errorRate')" prop="errorRate" label="报错率" min-width="80">
            <template slot-scope="scope">
              <span class="rate-error">{{ scope.row.errorRate }}</span>
            </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('skipRate')" prop="skipRate" label="跳过率" min-width="80">
            <template slot-scope="scope">{{ scope.row.skipRate }}</template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('expectedFailuresRate')" prop="expectedFailuresRate" label="期望失败率" min-width="100">
            <template slot-scope="scope">{{ scope.row.expectedFailuresRate }}</template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('unexpectedSuccessesRate')" prop="unexpectedSuccessesRate" label="非期望成功率" min-width="120">
            <template slot-scope="scope">{{ scope.row.unexpectedSuccessesRate }}</template>
          </el-table-column>
          <el-table-column prop="execute_time" label="执行时间" min-width="160">
            <template slot-scope="scope"> {{ scope.row.execute_time }} </template>
          </el-table-column>
          <el-table-column prop="edit" label="操作" min-width="200" fixed="right">
            <template slot-scope="scope">
              <el-button @click="checkResultInfo(scope.row)" type="primary" size="small">查看结果日志</el-button>
              <el-button @click="rerunTest(scope.row)" type="success" size="small">重新运行</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- Result Detail Dialog -->
    <el-dialog class="result-dialog" :visible.sync="resultVisible" :before-close="handleClose" title="测试用例结果详情" custom-class="dark-dialog" width="90%">
      <el-table :data="testcaseResult" style="width: 100%" border max-height="500px">
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

    <!-- Log Info Dialog -->
    <el-dialog class="info-dialog" :visible.sync="resultInfoVisible" :before-close="handleClose" title="日志详情" custom-class="dark-dialog" width="80%">
      <div v-html="sanitizedTestinfo" class="log-content"></div>
    </el-dialog>
  </div>
</template>

<script>
import user from '@/data/user.js'
import video from '@/data/data2.js'
import * as echarts from 'echarts'

export default {
  data () {
    return {
      input: '',
      testresultList: [],
      resultVisible: false,
      resultInfoVisible: false,
      testinfo: '',
      testcaseResult: {}
    }
  },
  computed: {
    tableHeight () {
      return window.innerHeight - 200
    },
    sanitizedTestinfo () {
      return this.sanitizeHtml(this.testinfo)
    }
  },
  mounted () {
    this.initChart()
  },
  beforeDestroy () {
    if (this.$refs.echarts2) {
      echarts.dispose(this.$refs.echarts2)
    }
    if (this.$refs.echarts3) {
      echarts.dispose(this.$refs.echarts3)
    }
  },
  created () {
    this.showtestreport()
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
    initChart (data) {
      var Data = data
      const echarts2 = echarts.init(this.$refs.echarts2)
      var echarts2Option = user
      if (Array.isArray(data)) {
        echarts2Option.xAxis.data = Data.map(item => item.id)
        echarts2Option.series = [
          {
            name: '通过用例数',
            data: Data.map(item => item.successes),
            type: 'bar',
            stack: 'x',
            itemStyle: { color: '#10B981' }
          },
          {
            name: '失败用例数',
            data: Data.map(item => item.failures),
            type: 'bar',
            stack: 'x',
            itemStyle: { color: '#EF4444' }
          },
          {
            name: '错误用例数',
            data: Data.map(item => item.errors),
            type: 'bar',
            stack: 'x',
            itemStyle: { color: '#F59E0B' }
          },
          {
            name: '跳过用例数',
            data: Data.map(item => item.skipped),
            type: 'bar',
            stack: 'x',
            itemStyle: { color: '#8B5CF6' }
          },
          {
            name: '期望失败用例数',
            data: Data.map(item => item.expectedFailures),
            type: 'bar',
            stack: 'x',
            itemStyle: { color: '#6B7280' }
          },
          {
            name: '非期望成功用例数',
            data: Data.map(item => item.unexpectedSuccesses),
            type: 'bar',
            stack: 'x',
            itemStyle: { color: '#06B6D4' }
          }
        ]
        echarts2.setOption(echarts2Option)

        const echarts3 = echarts.init(this.$refs.echarts3)
        var echarts3Option = video
        var pieData = [
          { value: Data.reduce((acc, item) => acc + parseInt(item.successes, 10), 0), name: '通过用例数' },
          { value: Data.reduce((acc, item) => acc + parseInt(item.failures, 10), 0), name: '失败用例数' },
          { value: Data.reduce((acc, item) => acc + parseInt(item.errors, 10), 0), name: '错误用例数' },
          { value: Data.reduce((acc, item) => acc + parseInt(item.skipped, 10), 0), name: '跳过用例数' },
          { value: Data.reduce((acc, item) => acc + parseInt(item.expectedFailures, 10), 0), name: '期望失败用例数' },
          { value: Data.reduce((acc, item) => acc + parseInt(item.unexpectedSuccesses, 10), 0), name: '非期望成功用例数' }
        ]
        echarts3Option.series[0].data = pieData
        echarts3.setOption(echarts3Option)
      } else {
        console.error('yourVariable is not an array:', data)
      }
    },
    showtestreport () {
      this.axios.get('/api/showtestreport')
        .then((res) => {
          const testResultsArray = res.data.msg
          this.testresultList = Object.values(testResultsArray)
          this.countRate(this.testresultList)
          this.initChart(testResultsArray)
        })
        .catch(error => {
          console.error('Error fetching data:', error)
        })
    },
    countRate (data) {
      for (let i = 0; i < data.length; i++) {
        var testResult = data[i]
        var total = parseInt(testResult.total, 10)
        var successes = parseInt(testResult.successes, 10)
        var failures = parseInt(testResult.failures, 10)
        var errors = parseInt(testResult.errors, 10)
        var skipped = parseInt(testResult.skipped, 10)
        var expectedFailures = parseInt(testResult.expectedFailures, 10)
        var unexpectedSuccesses = parseInt(testResult.unexpectedSuccesses, 10)

        testResult.passRate = (successes / total * 100).toFixed(2) + '%'
        testResult.failRate = (failures / total * 100).toFixed(2) + '%'
        testResult.errorRate = (errors / total * 100).toFixed(2) + '%'
        testResult.skipRate = (skipped / total * 100).toFixed(2) + '%'
        testResult.expectedFailuresRate = (expectedFailures / total * 100).toFixed(2) + '%'
        testResult.unexpectedSuccessesRate = (unexpectedSuccesses / total * 100).toFixed(2) + '%'
      }
    },
    search () {
      if (!this.input.trim()) {
        this.$message({
          message: '请输入有效的ID',
          type: 'warning'
        })
        return
      }
      let formData = new FormData()
      formData.append('id', this.input)
      this.axios.post('/api/searchinterfacetestcase', formData)
        .then((res) => {
          const code = res.data.code
          if (code === 0) {
            this.testresultList = Object.values(res.data.msg)
            this.countRate(this.testresultList)
            this.initChart(this.testresultList)
          } else {
            this.$message({
              message: res.data.msg,
              type: 'warning'
            })
          }
        })
        .catch(error => {
          console.error('搜索请求失败:', error)
          this.$message({
            message: '搜索请求失败，请稍后重试',
            type: 'error'
          })
        })
    },
    handleClose (done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {})
    },
    checkResultInfo (row) {
      let formData = new FormData()
      formData.append('id', row.id)
      this.axios.post('/api/getreportlog', formData)
        .then((res) => {
          const code = res.data.code
          if (code === 0) {
            this.resultVisible = true
            this.testcaseResult = Object.values(res.data.msg)
          } else {
            this.$message({
              message: res.data.msg,
              type: 'warning'
            })
          }
        })
    },
    shouldShowColumn (columnName) {
      return this.testresultList.some(item => {
        const value = parseInt(item[columnName], 10)
        return value > 0
      })
    },
    checktestinfo (row) {
      this.resultInfoVisible = true
      this.testinfo = row.testinfo
    },
    rerunTest (row) {
      this.$confirm('确认重新运行该测试?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let formData = new FormData()
        formData.append('id', row.id)
        this.$message({
          type: 'info',
          message: '测试重新运行中，请稍候...'
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消重新运行'
        })
      })
    }
  }
}
</script>

<style scoped>
/* CSS Variables */
.report-container {
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

  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow: hidden;
  background-color: var(--bg-base);
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

/* Search Bar */
.search-bar {
  flex-shrink: 0;
  margin-bottom: 16px;
  display: flex;
  gap: 12px;
  align-items: center;
}

/* Chart Table Container */
.chart-table-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow: hidden;
}

/* Chart Wrapper */
.chart-wrapper {
  flex-shrink: 0;
}

.graph-row {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.chart-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 20px;
  height: 400px;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.chart {
  width: 100%;
  height: calc(100% - 40px);
}

/* Table Card */
.table-card {
  flex: 1;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 20px;
  overflow: auto;
}

/* Rate Colors */
.rate-success {
  color: #10B981;
  font-weight: 500;
}

.rate-failure {
  color: #EF4444;
  font-weight: 500;
}

.rate-error {
  color: #F59E0B;
  font-weight: 500;
}

/* Dark Dialog Styles */
.report-container /deep/ .dark-dialog {
  background-color: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
}

.report-container /deep/ .dark-dialog .el-dialog__header {
  background-color: var(--bg-elevated);
  border-bottom: 1px solid var(--border-subtle);
  padding: 16px 20px;
  margin: 0;
}

.report-container /deep/ .dark-dialog .el-dialog__title {
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 600;
}

.report-container /deep/ .dark-dialog .el-dialog__body {
  background-color: var(--bg-elevated);
  padding: 20px;
  color: var(--text-primary);
  max-height: 70vh;
  overflow-y: auto;
}

.report-container /deep/ .dark-dialog .el-dialog__footer {
  background-color: var(--bg-elevated);
  border-top: 1px solid var(--border-subtle);
  padding: 16px 20px;
}

/* Input Styles */
.report-container /deep/ .el-input__inner {
  background-color: var(--bg-elevated);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.report-container /deep/ .el-input__inner:focus {
  border-color: var(--color-primary-500);
}

/* Table Styles */
.report-container /deep/ .el-table {
  background-color: transparent;
  color: var(--text-primary);
}

.report-container /deep/ .el-table th.el-table__cell {
  background-color: var(--bg-elevated);
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-subtle);
}

.report-container /deep/ .el-table td.el-table__cell {
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--border-default);
  color: var(--text-primary);
}

.report-container /deep/ .el-table--border::after,
.report-container /deep/ .el-table--group::after,
.report-container /deep/ .el-table::before {
  background-color: var(--border-default);
}

.report-container /deep/ .el-table--border {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
}

.report-container /deep/ .el-table__empty-block {
  background-color: var(--bg-surface);
  color: var(--text-muted);
}

/* Button Styles */
.report-container /deep/ .el-button--primary {
  background-color: var(--color-primary-500);
  border-color: var(--color-primary-500);
}

.report-container /deep/ .el-button--primary:hover {
  background-color: #2563EB;
  border-color: #2563EB;
}

.report-container /deep/ .el-button--success {
  background-color: #10B981;
  border-color: #10B981;
}

.report-container /deep/ .el-button--success:hover {
  background-color: #059669;
  border-color: #059669;
}

.report-container /deep/ .el-button--default {
  background-color: var(--bg-elevated);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.report-container /deep/ .el-button--default:hover {
  background-color: var(--bg-surface);
  border-color: var(--border-subtle);
  color: var(--text-primary);
}

.report-container /deep/ .el-button--text {
  color: var(--color-primary-500);
}

.report-container /deep/ .el-button--text:hover {
  color: #2563EB;
}

/* Tag Styles */
.report-container /deep/ .el-tag--success {
  background-color: rgba(16, 185, 129, 0.2);
  border-color: #10B981;
  color: #10B981;
}

.report-container /deep/ .el-tag--danger {
  background-color: rgba(239, 68, 68, 0.2);
  border-color: #EF4444;
  color: #EF4444;
}

.report-container /deep/ .el-tag--warning {
  background-color: rgba(245, 158, 11, 0.2);
  border-color: #F59E0B;
  color: #F59E0B;
}

.report-container /deep/ .el-tag--info {
  background-color: rgba(59, 130, 246, 0.2);
  border-color: #3B82F6;
  color: #3B82F6;
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
