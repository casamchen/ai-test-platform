<template>
  <div class="hello-container">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">Web 执行结果</h2>
      <div class="page-actions">
        <el-tag type="success">运行正常</el-tag>
      </div>
    </div>

    <!-- Content Card -->
    <div class="content-card">
      <h1 class="main-title">{{ msg }}</h1>

      <!-- Button Demo Section -->
      <div class="demo-section">
        <h3 class="section-title">按钮组件演示</h3>
        <el-row :gutter="12">
          <el-col :span="8">
            <el-button>默认按钮</el-button>
          </el-col>
          <el-col :span="8">
            <el-button type="primary">主要按钮</el-button>
          </el-col>
          <el-col :span="8">
            <el-button type="success">成功按钮</el-button>
          </el-col>
        </el-row>
        <el-row :gutter="12" style="margin-top: 16px;">
          <el-col :span="8">
            <el-button type="info">信息按钮</el-button>
          </el-col>
          <el-col :span="8">
            <el-button type="warning">警告按钮</el-button>
          </el-col>
          <el-col :span="8">
            <el-button type="danger">危险按钮</el-button>
          </el-col>
        </el-row>
      </div>

      <!-- Status Info -->
      <div class="status-section">
        <h3 class="section-title">系统状态</h3>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="组件状态">
            <el-badge is-dot class="status-dot" type="success"></el-badge>
            正常运行
          </el-descriptions-item>
          <el-descriptions-item label="Element UI 版本">
            2.x
          </el-descriptions-item>
          <el-descriptions-item label="Vue 版本">
            2.x
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloElement',
  data () {
    return {
      msg: '使用 Element UI 测试'
    }
  }
}
</script>

<style scoped>
.hello-container {
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

.content-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 32px;
}

.main-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 32px 0;
  text-align: center;
}

.demo-section,
.status-section {
  margin-bottom: 40px;
}

.status-section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 20px 0;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-subtle);
}

/* Element UI 深色主题覆盖 */
/deep/ .el-button--default {
  background-color: var(--bg-elevated);
  border-color: var(--border-subtle);
  color: var(--text-secondary);
}

/deep/ .el-button--default:hover {
  border-color: var(--color-primary-500);
  color: var(--color-primary-500);
  background-color: rgba(59, 130, 246, 0.08);
}

/deep/ .el-button--primary {
  background-color: var(--color-primary-500);
  border-color: var(--color-primary-500);
}

/deep/ .el-button--success {
  background-color: #22C55E;
  border-color: #22C55E;
}

/deep/ .el-button--warning {
  background-color: #F59E0B;
  border-color: #F59E0B;
}

/deep/ .el-button--danger {
  background-color: #EF4444;
  border-color: #EF4444;
}

/deep/ .el-button--info {
  background-color: var(--text-muted);
  border-color: var(--text-muted);
}

/* Descriptions 深色主题 */
/deep/ .el-descriptions {
  background-color: transparent;
}

/deep/ .el-descriptions__label {
  background-color: var(--bg-elevated) !important;
  color: var(--text-secondary) !important;
}

/deep/ .el-descriptions__content {
  background-color: var(--bg-surface) !important;
  color: var(--text-primary) !important;
}

/deep/ .el-descriptions.is-bordered .el-descriptions-item__cell {
  border-color: var(--border-subtle);
}

/* Badge */
.status-dot /deep/ .el-badge__content.is-fixed {
  top: 0;
  right: 0;
}

/* Tag 深色主题 */
/deep/ .el-tag--success {
  background-color: rgba(34, 197, 94, 0.15);
  border-color: #22C55E;
  color: #22C55E;
}
</style>
