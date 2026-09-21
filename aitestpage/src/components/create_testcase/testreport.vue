<template>
  <div class="report-container">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">测试报告</h2>
      <div class="search-bar">
        <el-input v-model="input" placeholder="请输入id" class="search-input"></el-input>
        <el-button @click="search" type="primary">搜索</el-button>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="table-card chart-card">
      <div class="card-header">
        <span class="card-title">数据统计</span>
      </div>
      <div class="chart-wrapper">
        <el-row :gutter="20" class="graph">
          <el-col :xs="24" :sm="12">
            <!-- 柱状图 -->
            <div class="chart-box">
              <div ref="echarts2" class="chart"></div>
            </div>
          </el-col>
          <el-col :xs="24" :sm="12">
            <!-- 饼状图 -->
            <div class="chart-box">
              <div ref="echarts3" class="chart"></div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- 表格区域 -->
    <div class="table-card table-section">
      <div class="card-header">
        <span class="card-title">测试结果详情</span>
      </div>
      <div class="table-wrapper">
        <el-table :data="testresultList" class="data-table" border :max-height="testresultList.length > 0 ? tableHeight : undefined">
          <el-table-column prop="id" label="id" min-width="20">
            <template slot-scope="scope"> {{ scope.row.id }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('total')" prop="total" label="总运行数量" min-width="100">
            <template slot-scope="scope"> {{ scope.row.total }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('successes')" prop="successes" label="执行成功" min-width="100">
            <template slot-scope="scope"> {{ scope.row.successes }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('failures')" prop="failures" label="执行失败" min-width="100">
            <template slot-scope="scope"> {{ scope.row.failures }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('errors')" prop="errors" label="执行错误" min-width="100">
            <template slot-scope="scope"> {{ scope.row.errors }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('skipped')" prop="skipped" label="跳过执行" min-width="100">
            <template slot-scope="scope"> {{ scope.row.skipped }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('expectedFailures')" prop="expectedFailures" label="期望失败" min-width="100">
            <template slot-scope="scope"> {{ scope.row.expectedFailures }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('unexpectedSuccesses')" prop="unexpectedSuccesses" label="非期望成功" min-width="100">
            <template slot-scope="scope"> {{ scope.row.unexpectedSuccesses }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('passRate')" prop="passRate" label="通过率" min-width="100">
            <template slot-scope="scope"> {{ scope.row.passRate }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('failRate')" prop="failRate" label="失败率" min-width="100">
            <template slot-scope="scope"> {{ scope.row.failRate }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('errorRate')" prop="errorRate" label="报错率" min-width="100">
            <template slot-scope="scope"> {{ scope.row.errorRate }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('skipRate')" prop="skipRate" label="跳过率" min-width="100">
            <template slot-scope="scope"> {{ scope.row.skipRate }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('expectedFailuresRate')" prop="expectedFailuresRate" label="期望失败率" min-width="100">
            <template slot-scope="scope"> {{ scope.row.expectedFailuresRate }} </template>
          </el-table-column>
          <el-table-column v-if="shouldShowColumn('unexpectedSuccessesRate')" prop="unexpectedSuccessesRate" label="非期望成功率" min-width="100">
            <template slot-scope="scope"> {{ scope.row.unexpectedSuccessesRate }} </template>
          </el-table-column>
          <el-table-column prop="execute_time" label="执行时间" min-width="100">
            <template slot-scope="scope"> {{ scope.row.execute_time }} </template>
          </el-table-column>
          <el-table-column prop="edit" label="操作" min-width="180" fixed="right">
            <template slot-scope="scope">
              <el-button @click="checkResultInfo(scope.row)" type="primary" size="small">查看结果日志</el-button>
              <el-button @click="rerunTest(scope.row)" type="success" size="small">重新运行</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- 结果对话框 -->
    <el-dialog class="result-dialog dark-dialog" :visible.sync="resultVisible" :before-close="handleClose" width="90%" title="测试结果详情">
      <el-table :data="testcaseResult" class="data-table" border>
        <el-table-column prop="id" label="id" min-width="20">
          <template slot-scope="scope"> {{ scope.row.id }} </template>
        </el-table-column>
        <el-table-column prop="testpoint" label="测试点" min-width="100">
          <template slot-scope="scope"> {{ scope.row.testpoint }} </template>
        </el-table-column>
        <el-table-column prop="result" label="运行结果" min-width="100">
          <template slot-scope="scope"> {{ scope.row.result }} </template>
        </el-table-column>
        <el-table-column prop="testinfo" label="结果日志" min-width="100">
          <template slot-scope="scope">
            <el-button type="text" class="link-btn" @click="checktestinfo(scope.row)">查看结果日志</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="platform" label="平台" min-width="100">
          <template slot-scope="scope"> {{ scope.row.platform }} </template>
        </el-table-column>
        <el-table-column prop="execute_time" label="执行时间" min-width="100">
          <template slot-scope="scope"> {{ scope.row.execute_time }} </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 日志详情对话框 -->
    <el-dialog class="info-dialog dark-dialog" :visible.sync="resultInfoVisible" :before-close="handleClose" width="80%" title="结果日志">
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
  beforeDestroy () {
    // 组件销毁时释放 ECharts 实例，防止内存泄漏
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
    /**
     * HTML 过滤 - 防止 XSS 攻击
     */
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
            itemStyle: { color: '#22C55E' }
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
            itemStyle: { color: '#A855F7' }
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
            itemStyle: { color: '#94A3B8' }
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
        // 计算数据的通过率，失败率等，并保留两位小数，然后添加百分号
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
/* CSS 变量定义 */
:root {
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
  --radius-2xl: 12px;
  --color-success: #22C55E;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #06B6D4;
}

/* 主容器 */
.report-container {
  min-height: 100vh;
  background-color: var(--bg-base);
  color: var(--text-primary);
  display: flex;
  flex-direction: column;
  padding: 24px;
  gap: 20px;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
}

.page-title {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
}

/* 搜索栏 */
.search-bar {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-input {
  width: 280px;
}

/* 卡片容器 */
.table-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.card-header {
  padding: 16px 24px;
  border-bottom: 1px solid var(--border-default);
  background-color: var(--bg-elevated);
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

/* 图表卡片 */
.chart-card {
  min-height: 420px;
}

.chart-wrapper {
  padding: 20px 24px;
}

.graph {
  width: 100%;
}

.chart-box {
  height: 380px;
}

.chart {
  width: 100%;
  height: 100%;
}

/* 表格区域 */
.table-section {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.table-wrapper {
  padding: 20px 24px;
  flex: 1;
  overflow: auto;
}

/* Element UI 深色主题覆盖 */
:deep(.el-input__inner) {
  background-color: var(--bg-elevated);
  border-color: var(--border-subtle);
  color: var(--text-primary);
}

:deep(.el-input__inner)::placeholder {
  color: var(--text-muted);
}

:deep(.el-input__inner:focus) {
  border-color: var(--color-primary-500);
}

:deep(.el-button--primary) {
  background-color: var(--color-primary-500);
  border-color: var(--color-primary-500);
}

:deep(.el-button--primary:hover) {
  background-color: #2563EB;
  border-color: #2563EB;
}

:deep(.el-button--success) {
  background-color: var(--color-success);
  border-color: var(--color-success);
}

:deep(.el-button--success:hover) {
  background-color: #16A34A;
  border-color: #16A34A;
}

/* 表格样式 */
:deep(.el-table) {
  background-color: transparent;
  color: var(--text-primary);
  border-color: var(--border-default);

  &::before {
    background-color: var(--border-default);
  }

  th.el-table__cell {
    background-color: var(--bg-elevated);
    color: var(--text-secondary);
    border-color: var(--border-default);
    font-weight: 600;
  }

  td.el-table__cell {
    background-color: var(--bg-surface);
    border-color: var(--border-default);
    color: var(--text-primary);
  }

  tr:hover td.el-table__cell {
    background-color: var(--bg-elevated) !important;
  }

  .el-table__empty-block {
    background-color: var(--bg-surface);
    color: var(--text-muted);
  }
}

/* 对话框样式 */
.dark-dialog {
  :deep(.el-dialog) {
    background-color: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-xl);

    .el-dialog__header {
      background-color: var(--bg-elevated);
      border-bottom: 1px solid var(--border-default);
      padding: 16px 20px;

      .el-dialog__title {
        color: var(--text-primary);
        font-weight: 600;
      }

      .el-dialog__close {
        color: var(--text-muted);

        &:hover {
          color: var(--text-primary);
        }
      }
    }

    .el-dialog__body {
      background-color: var(--bg-surface);
      color: var(--text-primary);
      padding: 20px;
    }
  }
}

.result-dialog :deep(.el-dialog__body) {
  max-height: 70vh;
  overflow-y: auto;
}

.info-dialog :deep(.el-dialog__body) {
  max-height: 80vh;
  overflow-y: auto;
}

/* 链接按钮 */
.link-btn {
  color: var(--color-primary-500);
}

.link-btn:hover {
  color: #60A5FA;
}

/* 日志内容 */
.log-content {
  white-space: pre-wrap;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
  background-color: var(--bg-elevated);
  padding: 16px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-subtle);
  max-height: 60vh;
  overflow-y: auto;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .search-bar {
    width: 100%;
  }

  .search-input {
    flex: 1;
  }

  .chart-box {
    height: 300px;
  }

  .report-container {
    padding: 16px;
  }
}
</style>
