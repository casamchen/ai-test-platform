<template>
  <div class="progress-container">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">App 测试用例管理</h2>
      <div class="page-actions">
        <el-button type="success" @click="clickButton">更新进度</el-button>
      </div>
    </div>

    <!-- Progress Card -->
    <div class="progress-card">
      <div class="progress-section">
        <h3 class="section-title">线性进度条</h3>
        <el-progress :percentage="50"></el-progress>
      </div>

      <div class="progress-section">
        <h3 class="section-title">内联文字进度</h3>
        <el-progress :text-inside="true" :stroke-width="26" :percentage="70" status="success"></el-progress>
      </div>

      <div class="progress-section circle-progress">
        <h3 class="section-title">环形进度</h3>
        <el-progress type="circle" :percentage="proData" :status="proData === 100 ? 'success' : 'exception'"></el-progress>
      </div>

      <div class="progress-info">
        <p>当前进度: <strong>{{ proData }}%</strong></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      proData: 0
    }
  },
  methods: {
    clickButton () {
      if (this.proData === 100) {
        this.proData = 0
      }
      this.proData = this.proData + 10
    }
  }
}
</script>

<style scoped>
.progress-container {
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

.progress-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 32px;
  max-width: 800px;
  margin: 0 auto;
}

.progress-section {
  margin-bottom: 40px;
}

.progress-section:last-child {
  margin-bottom: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-secondary);
  margin: 0 0 16px 0;
}

.circle-progress {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.progress-info {
  text-align: center;
  padding-top: 24px;
  border-top: 1px solid var(--border-subtle);
  color: var(--text-muted);
  font-size: 14px;
}

.progress-info strong {
  color: var(--color-primary-500);
  font-size: 18px;
}

/* Progress 深色主题 */
/deep/ .el-progress-bar__outer {
  background-color: var(--bg-elevated);
  border-radius: var(--radius-lg);
}

/deep/ .el-progress-bar__inner {
  background-color: var(--color-primary-500);
  border-radius: var(--radius-lg);
}

/deep/ .el-progress__text {
  color: var(--text-primary);
}

/deep/ .el-progress.is-success .el-progress-bar__inner {
  background-color: #22C55E;
}

/deep/ .el-progress.is-exception .el-progress-bar__inner,
/deep/ .el-progress.is-warning .el-progress-bar__inner {
  background-color: #EF4444;
}

/* Circle Progress */
/deep/ .el-progress-circle__track {
  stroke: var(--bg-elevated);
}

/deep/ .el-progress-circle__path {
  stroke: var(--color-primary-500);
}

/deep/ .el-progress.is-success .el-progress-circle__path {
  stroke: #22C55E;
}

/deep/ .el-progress.is-exception .el-progress-circle__path,
/deep/ .el-progress.is-warning .el-progress-circle__path {
  stroke: #EF4444;
}
</style>
