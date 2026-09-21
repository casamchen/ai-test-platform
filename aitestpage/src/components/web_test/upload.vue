<template>
  <div class="upload-container">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">Web 测试用例管理</h2>
      <div class="page-actions">
        <el-button size="small" type="primary" @click="$refs.upload.$el.querySelector('.el-upload').click()">选择文件</el-button>
      </div>
    </div>

    <!-- Upload Card -->
    <div class="upload-card">
      <el-upload
        ref="upload"
        class="upload-demo"
        action="/AItestapp/document"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :before-remove="beforeRemove"
        multiple
        :limit="3"
        :on-exceed="handleExceed"
        :file-list="fileList"
        :auto-upload="false">
        <div slot="trigger" class="upload-trigger">
          <i class="el-icon-upload2"></i>
          <span>点击或拖拽文件到此处上传</span>
        </div>
        <div slot="tip" class="el-upload__tip">只能上传 jpg/png 文件，且不超过 500kb</div>
      </el-upload>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      fileList: []
    }
  },
  methods: {
    handleRemove (file, fileList) {
      // 文件移除处理
    },
    handlePreview (file) {
      // 文件预览处理
    },
    handleExceed (files, fileList) {
      this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
    },
    beforeRemove (file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`)
    }
  }
}
</script>

<style scoped>
.upload-container {
  padding: 24px;
  background-color: var(--bg-base);
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px 24px;
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
}

.page-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.page-actions {
  display: flex;
  gap: 12px;
}

.upload-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
}

.upload-trigger {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 200px;
  background-color: var(--bg-elevated);
  border: 2px dashed var(--border-subtle);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-muted);
  font-size: 14px;
}

.upload-trigger:hover {
  border-color: var(--color-primary-500);
  color: var(--color-primary-500);
  background-color: rgba(59, 130, 246, 0.05);
}

.upload-trigger i {
  font-size: 48px;
  margin-bottom: 16px;
}

/* Upload 深色主题 */
/deep/ .el-upload__tip {
  color: var(--text-muted);
  text-align: center;
  margin-top: 12px;
  font-size: 13px;
}

/deep/ .el-upload-list {
  margin-top: 20px;
}

/deep/ .el-upload-list__item {
  background-color: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  color: var(--text-secondary);
  transition: all 0.3s ease;
}

/deep/ .el-upload-list__item:hover {
  background-color: var(--bg-base);
  border-color: var(--color-primary-500);
}

/deep/ .el-upload-list__item-name {
  color: var(--text-primary);
}

/deep/ .el-upload-list__item .el-icon-close {
  color: var(--text-muted);
}

/deep/ .el-upload-list__item .el-icon-close:hover {
  color: #EF4444;
}
</style>
