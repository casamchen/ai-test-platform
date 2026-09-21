<template>
  <div class="dataconfig-container">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h2 class="page-title">接口数据配置</h2>
          <p class="page-description">管理接口测试数据配置，编辑测试参数</p>
        </div>
      </div>
    </div>

    <!-- Table Card -->
    <div class="table-card">
      <el-table :data="interface_DataConfig_list" style="width: 100%" border>
        <el-table-column prop="id" label="ID" min-width="60">
          <template slot-scope="scope"> {{ scope.row.id }} </template>
        </el-table-column>
        <el-table-column prop="interface_api_id_id" label="关联项目 ID" min-width="120">
          <template slot-scope="scope"> {{ scope.row.interface_api_id_id }} </template>
        </el-table-column>
        <el-table-column prop="data_desc" label="数据描述" min-width="180">
          <template slot-scope="scope"> {{ scope.row.data_desc }} </template>
        </el-table-column>
        <el-table-column prop="data_info" label="数据" min-width="250" show-overflow-tooltip>
          <template slot-scope="scope"> {{ scope.row.data_info }} </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" min-width="160">
          <template slot-scope="scope"> {{ scope.row.create_time }} </template>
        </el-table-column>
        <el-table-column prop="operation" label="操作" min-width="100" fixed="right">
          <template slot-scope="scope">
            <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- Edit Dialog -->
      <el-dialog class="edit-dialog" :visible.sync="dialogVisible" :before-close="handleClose" title="编辑数据配置" custom-class="dark-dialog">
        <el-form :model="update_data_config" label-position="top">
          <el-form-item label="接口名称">
            <div class="form-display">{{ update_data_config.data_desc }}</div>
          </el-form-item>
          <el-form-item label="数据配置">
            <el-input v-model="update_data_config.data_config" type="textarea" :rows="8"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="cancelButton">取消</el-button>
          <el-button type="primary" @click="update">确定</el-button>
        </div>
      </el-dialog>
    </div>

    <!-- Pagination -->
    <div class="pagination-wrapper">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page.sync="currentPage"
        :page-sizes="[15, 30, 45, 60]"
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
      dialogVisible: false,
      interface_DataConfig_list: [],
      update_data_config: {
        data_desc: '',
        data_config: ''
      },
      currentPage: 1,
      pageSize: 15,
      total: 0
    }
  },
  computed: {
    tableHeight () {
      const mainHeight = this.$parent.$el.clientHeight
      return mainHeight - 56 - 46 - 24
    }
  },
  created () {
    this.show_interface_data()
  },
  methods: {
    show_interface_data () {
      let formData = new FormData()
      formData.append('Page', this.currentPage)
      formData.append('limit', this.pageSize)
      this.axios.post('/api/showinterfacedataconfig', formData)
        .then((res) => {
          this.interface_DataConfig_list = Object.values(res.data.msg)
          this.total = res.data.total
        })
        .catch(error => {
          console.error('Error fetching data:', error)
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
      this.update_data_config.data_desc = row.data_desc
      this.update_data_config.data_config = row.data_info
      this.dialogVisible = true
    },
    update (row) {
      let formData = new FormData()
      formData.append('testpoint', this.update_data_config.data_desc)
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
            this.show_interface_data()
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
      this.show_interface_data()
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.show_interface_data()
    }
  }
}
</script>

<style scoped>
/* CSS Variables */
.dataconfig-container {
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

/* Table Card */
.table-card {
  flex: 1;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 20px;
  overflow: auto;
}

/* Dark Dialog Styles */
.dataconfig-container /deep/ .dark-dialog {
  background-color: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
}

.dataconfig-container /deep/ .dark-dialog .el-dialog__header {
  background-color: var(--bg-elevated);
  border-bottom: 1px solid var(--border-subtle);
  padding: 16px 20px;
  margin: 0;
}

.dataconfig-container /deep/ .dark-dialog .el-dialog__title {
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 600;
}

.dataconfig-container /deep/ .dark-dialog .el-dialog__body {
  background-color: var(--bg-elevated);
  padding: 20px;
  color: var(--text-primary);
}

.dataconfig-container /deep/ .dark-dialog .el-dialog__footer {
  background-color: var(--bg-elevated);
  border-top: 1px solid var(--border-subtle);
  padding: 16px 20px;
}

/* Form Styles */
.dataconfig-container /deep/ .el-form-item__label {
  color: var(--text-secondary);
}

.dataconfig-container /deep/ .el-input__inner {
  background-color: var(--bg-base);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.dataconfig-container /deep/ .el-input__inner:focus {
  border-color: var(--color-primary-500);
}

.dataconfig-container /deep/ .el-textarea__inner {
  background-color: var(--bg-base);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.dataconfig-container /deep/ .el-textarea__inner:focus {
  border-color: var(--color-primary-500);
}

.form-display {
  padding: 10px 14px;
  background-color: var(--bg-base);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  color: var(--text-muted);
  font-size: 14px;
  line-height: 1.5;
}

/* Table Styles */
.dataconfig-container /deep/ .el-table {
  background-color: transparent;
  color: var(--text-primary);
}

.dataconfig-container /deep/ .el-table th.el-table__cell {
  background-color: var(--bg-elevated);
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-subtle);
}

.dataconfig-container /deep/ .el-table td.el-table__cell {
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--border-default);
  color: var(--text-primary);
}

.dataconfig-container /deep/ .el-table--border::after,
.dataconfig-container /deep/ .el-table--group::after,
.dataconfig-container /deep/ .el-table::before {
  background-color: var(--border-default);
}

.dataconfig-container /deep/ .el-table--border {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
}

.dataconfig-container /deep/ .el-table__empty-block {
  background-color: var(--bg-surface);
  color: var(--text-muted);
}

/* Button Styles */
.dataconfig-container /deep/ .el-button--primary {
  background-color: var(--color-primary-500);
  border-color: var(--color-primary-500);
}

.dataconfig-container /deep/ .el-button--primary:hover {
  background-color: #2563EB;
  border-color: #2563EB;
}

.dataconfig-container /deep/ .el-button--default {
  background-color: var(--bg-elevated);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.dataconfig-container /deep/ .el-button--default:hover {
  background-color: var(--bg-surface);
  border-color: var(--border-subtle);
  color: var(--text-primary);
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

.dataconfig-container /deep/ .el-pagination {
  color: var(--text-secondary);
}

.dataconfig-container /deep/ .el-pagination .el-pager li {
  background-color: var(--bg-elevated);
  color: var(--text-secondary);
  border: 1px solid var(--border-default);
}

.dataconfig-container /deep/ .el-pagination .el-pager li.active {
  background-color: var(--color-primary-500);
  color: white;
  border-color: var(--color-primary-500);
}

.dataconfig-container /deep/ .el-pagination button {
  background-color: var(--bg-elevated);
  color: var(--text-secondary);
  border: 1px solid var(--border-default);
}

.dataconfig-container /deep/ .el-select .el-input__inner {
  background-color: var(--bg-elevated);
  border-color: var(--border-default);
  color: var(--text-primary);
}
</style>
