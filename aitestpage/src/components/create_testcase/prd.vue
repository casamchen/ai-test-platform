<template>
  <div class="prd-container">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-left">
        <h3 class="section-title">Requirements Management</h3>
        <span class="section-desc">Upload and manage your PRD documents</span>
      </div>
      <div class="header-right">
        <el-button type="primary" icon="el-icon-upload2" @click="dialogVisible = true" class="btn-upload">
          Upload Document
        </el-button>
      </div>
    </div>

    <!-- Upload Dialog -->
    <el-dialog :visible.sync="dialogVisible" :before-close="handleClose" title="Upload PRD Document" width="540px">
      <el-form :model="addprojectdata" label-position="top">
        <el-form-item prop="project_name" label="Project Name">
          <el-input v-model="addprojectdata.project_name" placeholder="Enter project name"></el-input>
        </el-form-item>
        <el-form-item prop="version" label="Version">
          <el-input v-model="addprojectdata.version" placeholder="e.g. v1.0.0"></el-input>
        </el-form-item>
        <el-form-item label="Document File">
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
            action="/api/uploadprd"
            :auto-upload="true"
            drag
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
            <div slot="tip" class="el-upload__tip">Supports .doc, .docx, .pdf, .txt files</div>
          </el-upload>
        </el-form-item>
        <el-form-item prop="function" label="Update Notes (Optional)">
          <el-input type="textarea" v-model="addprojectdata.function" placeholder="Describe the updates in this version..." :rows="3"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelButton">Cancel</el-button>
        <el-button type="primary" @click="addproject()" :loading="uploading">Confirm Upload</el-button>
      </div>
    </el-dialog>

    <!-- Data Table -->
    <div class="table-card">
      <el-table :data="prdDatalist" style="width: 100%" border>
        <el-table-column prop="id" label="ID" min-width="60" align="center">
          <template slot-scope="scope">
            <span class="id-badge">{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="project_name" label="Project Name" min-width="120"></el-table-column>
        <el-table-column prop="version" label="Version" min-width="80" align="center">
          <template slot-scope="scope">
            <el-tag size="mini" type="info">{{ scope.row.version }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="function" label="Description" min-width="150" show-overflow-tooltip></el-table-column>
        <el-table-column prop="prd_name" label="File Name" min-width="160">
          <template slot-scope="scope">
            <el-button type="text" class="file-link" @click="showfile_content(scope.row)">
              <i class="el-icon-document"></i> {{ scope.row.prd_name }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="Created At" min-width="140" sortable></el-table-column>
        <el-table-column label="Actions" min-width="140" align="center">
          <template slot-scope="scope">
            <el-button size="small" type="primary" icon="el-icon-magic-stick" @click="create_testcase(scope.row)">
              Generate Cases
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- File Content Dialog -->
    <el-dialog :visible.sync="file_content_Visible" title="Document Content" width="700px">
      <div class="document-preview" v-html="sanitizedDocumentContent"></div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="file_content_Visible = false">Close</el-button>
      </span>
    </el-dialog>

    <!-- Loading Dialog -->
    <el-dialog :visible.sync="loadingVisible" :close-on-click-modal="false" width="400px" custom-class="loading-dialog">
      <div class="loading-content">
        <i class="el-icon-loading loading-spinner"></i>
        <p class="loading-text">{{ loadingText }}</p>
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
      uploading: false,
      addprojectdata: {
        project_name: '',
        version: '',
        function: ''
      },
      loadingText: '',
      filecontent: '',
      file: '',
      documentContent: '',
      file_path: '',
      fileList: [],
      prdDatalist: [],
      pollingInterval: null,
      taskId: null
    }
  },
  created () {
    this.showprddata()
  },
  beforeDestroy () {
    if (this.pollingInterval) {
      clearInterval(this.pollingInterval)
      this.pollingInterval = null
    }
  },
  computed: {
    sanitizedDocumentContent () {
      return this.sanitizeHtml(this.documentContent)
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
    showprddata () {
      this.axios.get('/api/checkprdinfo')
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
      this.$confirm('Close without saving?')
        .then(_ => { done() })
        .catch(_ => {})
    },
    cancelButton () {
      this.addprojectdata = { project_name: '', version: '', function: '' }
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
        return this.$message.error('Please upload a file')
      }
      this.uploading = true
      let formData = new FormData()
      formData.append('file', this.file)
      formData.append('file_path', this.file_path)
      formData.append('project_name', this.addprojectdata.project_name)
      formData.append('version', this.addprojectdata.version)
      formData.append('function', this.addprojectdata.function)
      this.axios.post('/api/uploadprdinfo', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
        .then((res) => {
          if (res.data.msg === 'uploaded') {
            this.showprddata()
            this.$message.success('Document uploaded successfully!')
            this.addprojectdata = { project_name: '', version: '', function: '' }
            this.fileList = []
            this.file = ''
            this.file_path = ''
            this.dialogVisible = false
          } else {
            this.$message.error('Upload failed, please try again')
          }
        })
        .catch((err) => {
          console.error(err)
          this.$message.error('Network error occurred')
        })
        .finally(() => {
          this.uploading = false
        })
    },
    handleRemove (file, fileList) {},
    handlePreview (file) {},
    handleExceed (files, fileList) {
      this.$message.warning(`Limit is 1 file. Selected ${files.length + fileList.length} files`)
    },
    returnfilepath (response, file, fileList) {
      this.file_path = response.path
      this.file = response.file_name
    },
    showfile_content (row) {
      let formData = new FormData()
      formData.append('id', row.id)
      this.file_content_Visible = true
      this.axios.post('/api/filecontent', formData, { responseType: 'blob' })
        .then(response => {
          const blob = response.data
          const reader = new FileReader()
          reader.onload = (event) => {
            const arrayBuffer = event.target.result
            const decoder = new TextDecoder('utf-8')
            const content = decoder.decode(arrayBuffer)
            this.documentContent = content
          }
          reader.readAsArrayBuffer(blob)
        })
    },
    beforeRemove (file, fileList) {
      return this.$confirm(`Remove ${file.name}?`)
    },
    async create_testcase (row) {
      let formData = new FormData()
      formData.append('prd_name', row.prd_name)
      formData.append('project_name', row.project_name)
      formData.append('version', row.version)
      formData.append('id', row.id)
      this.loadingVisible = true
      await this.axios.post('/api/create_testcase', formData)
        .then(response => {
          let code = response.data.code
          let taskId = response.data.task_id
          if (code === 0) {
            this.startPolling(taskId)
          }
        })
    },
    startPolling (taskId) {
      this.pollingInterval = setInterval(() => {
        let formData = new FormData()
        formData.append('task_id', taskId)
        this.axios.post('/api/check_task_status', formData)
          .then(res => {
            let status = res.data.status
            if (status === 'SUCCESS') {
              clearInterval(this.pollingInterval)
              this.loadingVisible = false
              this.$message({ message: 'Test cases generated successfully!', type: 'success' })
              this.showprddata()
            } else if (status === 'PENDING') {
              this.loadingText = 'Preparing task...'
            } else if (status === 'STARTED') {
              this.loadingText = 'Generating test cases...'
            } else if (status === 'FAILURE') {
              clearInterval(this.pollingInterval)
              this.loadingVisible = false
              this.$message({ message: 'Generation failed', type: 'error' })
            }
          })
      }, 2000)
    }
  }
}
</script>

<style scoped>
.prd-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--space-6);
}

.section-title {
  font-size: var(--text-lg);
  font-weight: var(--font-medium);
  color: var(--text-primary);
  margin: 0 0 var(--space-1) 0;
}

.section-desc {
  font-size: var(--text-sm);
  color: var(--text-muted);
}

.btn-upload {
  border-radius: var(--radius-lg) !important;
}

/* Table Card */
.table-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: var(--space-4);
  flex: 1;
  overflow: hidden;
}

.id-badge {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-muted);
  background-color: var(--bg-elevated);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
}

.file-link {
  color: var(--color-primary-400) !important;
  font-size: var(--text-sm);
}

.file-link:hover {
  color: var(--color-primary-300) !important;
}

.file-link i {
  margin-right: 4px;
}

/* Document Preview */
.document-preview {
  max-height: 60vh;
  overflow-y: auto;
  padding: var(--space-4);
  background-color: var(--bg-base);
  border-radius: var(--radius-lg);
  font-size: var(--text-base);
  line-height: var(--leading-relaxed);
  color: var(--text-secondary);
}

/* Loading Dialog */
.loading-content {
  text-align: center;
  padding: var(--space-8) 0;
}

.loading-spinner {
  font-size: 32px;
  color: var(--color-primary-400);
}

.loading-text {
  margin-top: var(--space-4);
  font-size: var(--text-md);
  color: var(--text-muted);
}
</style>
