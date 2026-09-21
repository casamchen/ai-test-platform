<template>
    <div class="testcase-container">
      <!-- Page Header -->
      <div class="page-header">
        <div class="header-content">
          <div class="header-text">
            <h2 class="page-title">测试用例管理</h2>
            <p class="page-description">管理和查看所有测试用例，支持搜索、编辑和状态更新</p>
          </div>
          <div class="header-actions">
            <el-button @click="showtestcase" class="refresh-btn">刷新列表</el-button>
          </div>
        </div>
      </div>

      <!-- Search Bar -->
      <div class="search-bar">
        <el-input v-model="input" placeholder="请输入需求文档id" prefix-icon="el-icon-search" clearable></el-input>
        <el-button type="primary" @click="search" class="search-btn">搜索</el-button>
      </div>

      <!-- Table Card -->
      <div class="table-card">
        <el-table :data="testcaseList" style="width: 100%" border class="dark-table">
          <el-table-column fixed prop="id" label="ID" min-width="60">
            <template slot-scope="scope">{{ scope.row.id }}</template>
          </el-table-column>
          <el-table-column prop="project_name" label="项目名称" min-width="120">
            <template slot-scope="scope">{{ scope.row.project_name }}</template>
          </el-table-column>
          <el-table-column prop="version" label="版本号" min-width="100">
            <template slot-scope="scope">{{ scope.row.version }}</template>
          </el-table-column>
          <el-table-column prop="testcase" label="测试点" min-width="140">
            <template slot-scope="scope">{{ scope.row.testcase }}</template>
          </el-table-column>
          <el-table-column prop="priority" label="优先级" min-width="90">
            <template slot-scope="scope">
              <span :class="'priority-' + (scope.row.priority ? scope.row.priority.toLowerCase() : 'none')">{{ scope.row.priority || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="operation" label="操作步骤" min-width="160">
            <template slot-scope="scope">{{ scope.row.operation }}</template>
          </el-table-column>
          <el-table-column prop="expectedresult" label="预期结果" min-width="160">
            <template slot-scope="scope">{{ scope.row.expectedresult }}</template>
          </el-table-column>
          <el-table-column prop="actual_results" label="实际结果" min-width="160">
            <template slot-scope="scope">{{ scope.row.actual_results }}</template>
          </el-table-column>
          <el-table-column prop="execution_time" label="执行时间" min-width="150">
            <template slot-scope="scope">{{ scope.row.execution_time }}</template>
          </el-table-column>
          <el-table-column prop="execution_person" label="执行人员" min-width="100">
            <template slot-scope="scope">{{ scope.row.execution_person }}</template>
          </el-table-column>
          <el-table-column fixed="right" prop="edit" label="操作" min-width="100">
            <template slot-scope="scope">
              <el-button size="small" @click="handleEdit(scope.row)" class="edit-btn">编辑</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- Edit Dialog -->
      <el-dialog class="edit-dialog" :visible.sync="dialogVisible" :before-close="handleClose" width="500px" title="编辑实际结果">
        <el-form :model="update_results" label-position="top">
          <el-form-item label="实际结果">
            <el-input v-model="update_results.actual_results" type="textarea" :rows="4"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="cancelButton" class="cancel-btn">取消</el-button>
          <el-button type="primary" @click="update" class="confirm-btn">确定</el-button>
        </div>
      </el-dialog>

      <!-- Pagination -->
      <div class="pagination-wrapper">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page.sync="currentPage"
          :page-sizes="[10, 20, 40, 50]"
          :page-size="pageSize"
          layout="sizes, prev, pager, next"
          :total="total"
          background>
        </el-pagination>
      </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      options: [{
        value: '通过',
        label: '通过'
      },
      {
        value: '失败',
        label: '失败'
      },
      {
        value: '阻塞',
        label: '阻塞'
      }],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      multipleSelection: [],
      input: '',
      dialogVisible: false,
      testcaseList: [],
      state: '',
      update_results: {
        actual_results: ''
      }
    }
  },
  created () {
    this.showtestcase()
  },
  computed: {
    tableHeight () {
      const mainHeight = this.$parent.$el.clientHeight
      return mainHeight - 200
    }
  },
  methods: {
    showtestcase () {
      let formData = new FormData()
      formData.append('Page', this.currentPage)
      formData.append('limit', this.pageSize)
      this.axios.post('/api/showtestcase', formData)
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
      this.axios.post('/api/searchtestcase', formData)
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
    update_state (row) {
      let formData = new FormData()
      formData.append('testcase', row.testcase)
      formData.append('state', row.state)

      this.axios.post('/api/updatetestcase_state', formData)
        .then((res) => {
          const code = res.data.code
          if (code === 0) {
            this.$set(this.testcaseList.findIndex(item => item.testcase === row.testcase), 'state', row.state)
            this.showtestcase()
            this.$message({
              message: res.data.msg,
              type: 'success'
            })
            this.dialogVisible = false
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
      this.update_results = {
        actual_results: ''
      }
      this.dialogVisible = false
    },
    handleEdit (row) {
      this.dialogVisible = true
      this.update_results = { ...row }
    },
    update () {
      let formData = new FormData()
      formData.append('testcase', this.update_results.testcase)
      formData.append('result', this.update_results.actual_results)

      this.axios.post('/api/updatetestcase_result', formData)
        .then((res) => {
          const code = res.data.code
          if (code === 0) {
            this.showtestcase()
            this.$message({
              message: res.data.msg,
              type: 'success'
            })
            this.dialogVisible = false
          } else {
            this.$message({
              message: res.data.msg,
              type: 'warning'
            })
          }
        })
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
.testcase-container {
  height: 100%;
  min-height: calc(100vh - 24px);
  background-color: var(--bg-base);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Page Header */
.page-header {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: var(--text-primary);
}

.page-description {
  margin: 0;
  font-size: 14px;
  color: var(--text-muted);
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
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: 16px;
}

.search-bar .el-input {
  max-width: 360px;
}

/* Table Card */
.table-card {
  flex: 1;
  overflow: auto;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 16px;
}

/* Dark Table Styles */
.dark-table {
  color: var(--text-primary);
}

.dark-table::before {
  background-color: var(--border-default);
}

.dark-table /deep/ .el-table__header-wrapper th {
  background-color: var(--bg-elevated) !important;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-subtle);
}

.dark-table /deep/ .el-table__body-wrapper td {
  background-color: var(--bg-surface) !important;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-default);
}

.dark-table /deep/ .el-table__body-wrapper tr:hover > td {
  background-color: var(--bg-elevated) !important;
}

.dark-table /deep/ .el-table__fixed,
.dark-table /deep/ .el-table__fixed-right {
  background-color: var(--bg-surface);
}

/* Priority Tags */
.priority-high {
  color: #EF4444;
  font-weight: 600;
}

.priority-medium {
  color: #F59E0B;
  font-weight: 600;
}

.priority-low {
  color: #10B981;
  font-weight: 600;
}

/* Pagination */
.pagination-wrapper {
  position: sticky;
  bottom: 0;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: 12px;
  display: flex;
  justify-content: flex-end;
  z-index: 1000;
}

/* Dialog Styles */
.edit-dialog /deep/ .el-dialog {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
}

.edit-dialog /deep/ .el-dialog__title {
  color: var(--text-primary);
}

.edit-dialog /deep/ .el-dialog__headerbtn .el-dialog__close {
  color: var(--text-muted);
}

.edit-dialog /deep/ .el-form-item__label {
  color: var(--text-secondary);
}

.edit-dialog /deep/ .el-textarea__inner {
  background-color: var(--bg-elevated);
  color: var(--text-primary);
  border-color: var(--border-default);
}

.edit-dialog /deep/ .el-textarea__inner:focus {
  border-color: var(--color-primary-500);
}

.edit-dialog /deep/ .el-dialog__body {
  color: var(--text-primary);
}

/* Button Styles */
.refresh-btn,
.search-btn,
.edit-btn,
.cancel-btn,
.confirm-btn {
  border-radius: var(--radius-lg);
}

.refresh-btn {
  background-color: var(--bg-elevated);
  color: var(--text-secondary);
  border-color: var(--border-default);
}

.refresh-btn:hover {
  background-color: var(--border-subtle);
  color: var(--text-primary);
}

.search-btn,
.confirm-btn {
  background-color: var(--color-primary-500);
  border-color: var(--color-primary-500);
}

.search-btn:hover,
.confirm-btn:hover {
  opacity: 0.9;
}

.cancel-btn {
  background-color: var(--bg-elevated);
  color: var(--text-secondary);
  border-color: var(--border-default);
}

.cancel-btn:hover {
  background-color: var(--border-subtle);
  color: var(--text-primary);
}

.edit-btn {
  background-color: var(--bg-elevated);
  border: 1px solid var(--color-primary-500);
  color: var(--color-primary-500) !important;
  opacity: 1;
  transition: all var(--transition-fast);
}

.edit-btn,
.edit-btn span,
.edit-btn i {
  color: var(--color-primary-500) !important;
}

.edit-btn:hover {
  background-color: var(--color-primary-500) !important;
  border-color: var(--color-primary-500) !important;
}

.edit-btn:hover,
.edit-btn:hover span,
.edit-btn:hover i {
  color: #FFFFFF !important;
}

/* Input Styles */
.search-bar /deep/ .el-input__inner {
  background-color: var(--bg-elevated);
  color: var(--text-primary);
  border-color: var(--border-default);
}

.search-bar /deep/ .el-input__inner:focus {
  border-color: var(--color-primary-500);
}

.search-bar /deep/ .el-input__inner::placeholder {
  color: var(--text-muted);
}

/* Table Cell Padding */
.testcase-container /deep/ .el-table td,
.testcase-container /deep/ .el-table th {
  padding: 10px 0;
}

/* Pagination Component */
.testcase-container /deep/ .el-pagination {
  margin-top: 0;
  padding: 0;
}

.testcase-container /deep/ .el-pagination button,
.testcase-container /deep/ .el-pagination li {
  background-color: var(--bg-elevated);
  color: var(--text-secondary);
}

.testcase-container /deep/ .el-pagination .el-pager li.active {
  background-color: var(--color-primary-500);
}
</style>
