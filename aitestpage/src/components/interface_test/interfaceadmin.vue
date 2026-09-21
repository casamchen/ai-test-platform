<template>
  <div class="prd-container">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h2 class="page-title">接口文档管理</h2>
          <p class="page-description">上传和管理 API 接口文档，生成测试用例</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" @click="dialogVisible = true">上传接口文档</el-button>
        </div>
      </div>
    </div>

    <!-- Upload Dialog -->
    <el-dialog :visible.sync="dialogVisible" :before-close="handleClose" title="上传接口文档" custom-class="dark-dialog">
      <el-form :model="addprojectdata" label-position="top">
        <el-form-item prop="project_name" label="项目名称">
          <el-input v-model="addprojectdata.project_name"></el-input>
        </el-form-item>
        <el-form-item prop="version" label="版本号">
          <el-input v-model="addprojectdata.version"></el-input>
        </el-form-item>
        <el-form-item label="上传需求">
          <el-upload
            ref="upload"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            :limit="1"
            :on-exceed="handleExceed"
            :file-list="fileList"
            :before-upload="beforeUpload"
            :on-success="returnfilepath"
            class="upload-demo"
            action="/api/uploadinterfacefile"
            :auto-upload="true">
            <el-button size="small" type="primary">上传</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item prop="remark" label="备注">
          <el-input type="textarea" v-model="addprojectdata.remark"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelButton">取消</el-button>
        <el-button type="primary" @click="addproject()">确定</el-button>
      </div>
    </el-dialog>

    <!-- Table Card -->
    <div class="table-card">
      <el-table :data="prdDatalist" style="width: 100%" border>
        <el-table-column prop="id" label="ID" min-width="80">
          <template slot-scope="scope"> {{ scope.row.id }} </template>
        </el-table-column>
        <el-table-column prop="project" label="项目名称" min-width="120">
          <template slot-scope="scope"> {{ scope.row.project }} </template>
        </el-table-column>
        <el-table-column prop="version" label="版本号" min-width="100">
          <template slot-scope="scope"> {{ scope.row.version }} </template>
        </el-table-column>
        <el-table-column prop="path" label="项目路径" min-width="150">
          <template slot-scope="scope"> {{ scope.row.path }} </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="120">
          <template slot-scope="scope"> {{ scope.row.remark }} </template>
        </el-table-column>
        <el-table-column prop="prd_name" label="文件名称" min-width="140">
          <template slot-scope="scope">
            <el-button type="text" @click="showfile_content(scope.row)">{{ scope.row.prd_name }}</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" min-width="160">
          <template slot-scope="scope"> {{ scope.row.create_time }} </template>
        </el-table-column>
        <el-table-column prop="operation" label="操作" min-width="140" fixed="right">
          <template slot-scope="scope">
            <el-button size="small" type="primary" @click="create_testcase(scope.row)">生成测试用例</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- File Content Dialog -->
    <el-dialog :visible.sync="file_content_Visible" title="API 接口信息" custom-class="dark-dialog">
      <el-table :data="api_info" style="width: 100%" border max-height="500px">
        <el-table-column prop="id" label="ID" min-width="60">
          <template slot-scope="scope"> {{ scope.row.id }} </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" min-width="120">
          <template slot-scope="scope"> {{ scope.row.title }} </template>
        </el-table-column>
        <el-table-column prop="url" label="URL" min-width="180">
          <template slot-scope="scope"> {{ scope.row.url }} </template>
        </el-table-column>
        <el-table-column prop="method" label="方法" min-width="80">
          <template slot-scope="scope"> {{ scope.row.method }} </template>
        </el-table-column>
        <el-table-column prop="params" label="参数" min-width="150">
          <template slot-scope="scope"> {{ scope.row.params }} </template>
        </el-table-column>
        <el-table-column prop="example" label="示例" min-width="150">
          <template slot-scope="scope"> {{ scope.row.example }} </template>
        </el-table-column>
        <el-table-column prop="response" label="响应" min-width="150">
          <template slot-scope="scope"> {{ scope.row.response }} </template>
        </el-table-column>
        <el-table-column prop="notes" label="备注" min-width="120">
          <template slot-scope="scope"> {{ scope.row.notes }} </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" min-width="80">
          <template slot-scope="scope"> {{ scope.row.status }} </template>
        </el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="file_content_Visible = false">关闭</el-button>
      </span>
    </el-dialog>

    <!-- Loading Dialog -->
    <el-dialog :visible.sync="loadingVisible" :close-on-click-modal="false" custom-class="loading-dialog" :show-close="false">
      <div class="loading-content">
        <i class="el-icon-loading"></i>
        <span>{{ loadingText }}</span>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data () {
    return {
      dialogVisible: false,
      file_content_Visible: false,
      loadingVisible: false,
      loadingText: '正在生成测试用例',
      addprojectdata: {
        project_name: '',
        version: '',
        remark: ''
      },
      filecontent: '',
      file: '',
      documentContent: '',
      file_path: '',
      fileList: [],
      prdDatalist: [],
      api_info: []
    }
  },
  created () {
    this.showprddata()
  },
  methods: {
    showprddata () {
      this.axios.get('/api/checkinterfaceinfo')
        .then((res) => {
          this.prdDatalist = Object.values(res.data.msg)
        })
        .catch(error => {
          console.error('Error fetching data:', error)
        })
    },
    open_dialog () {
      this.dialogVisible = true
    },
    handleClose (done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done()
        })
        .catch(_ => {})
    },
    cancelButton () {
      this.addprojectdata = {
        project_name: '',
        version: '',
        remark: ''
      }
      this.fileList = []
      this.file = ''
      this.file_path = ''
      this.dialogVisible = false
    },
    beforeUpload (file) {
      this.file = file
      return true
    },
    addproject () {
      if (!this.file) {
        return this.$message.error('请上传至少一个文件')
      }
      if (!this.addprojectdata.project_name || !this.addprojectdata.version) {
        return this.$message.error('请填写项目名称和版本号')
      }
      let formData = new FormData()
      formData.append('file', this.file)
      formData.append('file_path', this.file_path)
      formData.append('project_name', this.addprojectdata.project_name)
      formData.append('version', this.addprojectdata.version)
      formData.append('remark', this.addprojectdata.remark)
      this.axios.post('/api/uploadinterfaceinfo', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
        .then((res) => {
          if (res.data.msg === 'uploaded') {
            this.showprddata()
            this.$message.success('接口文档上传成功!')
            this.addprojectdata = {
              project_name: '',
              version: '',
              remark: ''
            }
            this.fileList = []
            this.file = ''
            this.file_path = ''
            this.dialogVisible = false
          } else {
            this.$message.error('接口文档上传失败!')
          }
        })
        .catch((err) => {
          return err
        })
    },
    handleRemove (file, fileList) {
      // File removed
    },
    handlePreview (file) {
      // File preview
    },
    handleExceed (files, fileList) {
      this.$message.warning(`当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
    },
    returnfilepath (response, file, fileList) {
      this.file_path = response.path
      this.file = response.file_name
    },
    showfile_content (row) {
      let formData = new FormData()
      formData.append('id', row.id)
      this.file_content_Visible = true
      this.axios.post('/api/showinterfacecontent', formData)
        .then((res) => {
          this.api_info = Object.values(res.data.msg)
        })
        .catch(error => {
          console.error('Error fetching data:', error)
        })
    },
    beforeRemove (file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`)
    },
    create_testcase (row) {
      if (!row || !row.id) {
        this.$message.error('无效的接口文档数据')
        return
      }
      let formData = new FormData()
      formData.append('project_name', row.project)
      formData.append('version', row.version)
      formData.append('id', row.id)
      this.loadingVisible = true
      this.axios.post('/api/createinterfacetesecase', formData, {
        timeout: 900000
      })
        .then(response => {
          let code = response.data.code
          this.loadingVisible = false
          if (code === 0) {
            this.$message({
              message: response.data.msg,
              type: 'success'
            })
          } else {
            this.$message({
              message: response.data.msg || '生成测试用例失败',
              type: 'error'
            })
          }
        })
        .catch(error => {
          this.loadingVisible = false
          this.$message({
            message: '生成测试用例请求失败，请稍后重试',
            type: 'error'
          })
          console.error('Error generating test cases:', error)
        })
    }
  }
}
</script>

<style scoped>
/* CSS Variables */
.prd-container {
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
  display: flex;
  flex-direction: column;
  background-color: var(--bg-base);
  padding: 20px;
  color: var(--text-primary);
}

/* Page Header */
.page-header {
  flex-shrink: 0;
  margin-bottom: 20px;
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

/* Table Card */
.table-card {
  flex: 1;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 20px;
  overflow-y: auto;
}

/* Dark Dialog Styles */
.prd-container /deep/ .dark-dialog {
  background-color: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
}

.prd-container /deep/ .dark-dialog .el-dialog__header {
  background-color: var(--bg-elevated);
  border-bottom: 1px solid var(--border-subtle);
  padding: 16px 20px;
  margin: 0;
}

.prd-container /deep/ .dark-dialog .el-dialog__title {
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 600;
}

.prd-container /deep/ .dark-dialog .el-dialog__body {
  background-color: var(--bg-elevated);
  padding: 20px;
  color: var(--text-primary);
}

.prd-container /deep/ .dark-dialog .el-dialog__footer {
  background-color: var(--bg-elevated);
  border-top: 1px solid var(--border-subtle);
  padding: 16px 20px;
}

/* Form Styles */
.prd-container /deep/ .el-form-item__label {
  color: var(--text-secondary);
}

.prd-container /deep/ .el-input__inner {
  background-color: var(--bg-base);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.prd-container /deep/ .el-input__inner:focus {
  border-color: var(--color-primary-500);
}

.prd-container /deep/ .el-textarea__inner {
  background-color: var(--bg-base);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.prd-container /deep/ .el-textarea__inner:focus {
  border-color: var(--color-primary-500);
}

/* Table Styles */
.prd-container /deep/ .el-table {
  background-color: transparent;
  color: var(--text-primary);
}

.prd-container /deep/ .el-table th.el-table__cell {
  background-color: var(--bg-elevated);
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-subtle);
}

.prd-container /deep/ .el-table td.el-table__cell {
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--border-default);
  color: var(--text-primary);
}

.prd-container /deep/ .el-table--border::after,
.prd-container /deep/ .el-table--group::after,
.prd-container /deep/ .el-table::before {
  background-color: var(--border-default);
}

.prd-container /deep/ .el-table--border {
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
}

.prd-container /deep/ .el-table__empty-block {
  background-color: var(--bg-surface);
  color: var(--text-muted);
}

/* Button Styles */
.prd-container /deep/ .el-button--primary {
  background-color: var(--color-primary-500);
  border-color: var(--color-primary-500);
}

.prd-container /deep/ .el-button--primary:hover {
  background-color: #2563EB;
  border-color: #2563EB;
}

.prd-container /deep/ .el-button--default {
  background-color: var(--bg-elevated);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.prd-container /deep/ .el-button--default:hover {
  background-color: var(--bg-surface);
  border-color: var(--border-subtle);
  color: var(--text-primary);
}

.prd-container /deep/ .el-button--text {
  color: var(--color-primary-500);
}

.prd-container /deep/ .el-button--text:hover {
  color: #2563EB;
}

/* Upload Component */
.prd-container /deep/ .el-upload-list {
  background-color: var(--bg-base);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  padding: 8px;
}

.prd-container /deep/ .el-upload-list__item {
  background-color: var(--bg-surface);
  color: var(--text-primary);
  border-color: var(--border-default);
}

/* Loading Dialog */
.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 40px;
  color: var(--text-primary);
  font-size: 16px;
}

.prd-container /deep/ .loading-dialog {
  background-color: rgba(0, 0, 0, 0.8);
  box-shadow: none;
}

.prd-container /deep/ .loading-dialog .el-dialog__body {
  background-color: transparent;
  padding: 40px;
}

.prd-container /deep/ .el-icon-loading {
  font-size: 32px;
  color: var(--color-primary-500);
}
</style>
