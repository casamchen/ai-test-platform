<template>
  <div class="layout-container">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">执行记录</h2>
      <div class="page-actions">
        <el-button type="primary" size="small" icon="el-icon-refresh-right">刷新</el-button>
      </div>
    </div>

    <!-- Layout Card -->
    <div class="layout-card">
      <!-- 基础布局 -->
      <div class="layout-section">
        <h3 class="section-title">基础布局</h3>
        <el-row :gutter="20">
          <el-col :span="24"><div class="grid-content grid-primary"></div></el-col>
        </el-row>

        <el-row :gutter="20" style="margin-top: 16px;">
          <el-col :span="16"><div class="grid-content grid-secondary"></div></el-col>
          <el-col :span="8"><div class="grid-content grid-tertiary"></div></el-col>
        </el-row>

        <el-row :gutter="20" style="margin-top: 16px;">
          <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
          <el-col :span="12"><div class="grid-content grid-tertiary"></div></el-col>
          <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
        </el-row>

        <el-row :gutter="20" style="margin-top: 16px;">
          <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
          <el-col :span="6"><div class="grid-content grid-tertiary"></div></el-col>
          <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
          <el-col :span="6"><div class="grid-content grid-tertiary"></div></el-col>
        </el-row>
      </div>

      <!-- 分栏偏移 -->
      <div class="layout-section">
        <h3 class="section-title">分栏偏移</h3>
        <el-row :gutter="20">
          <el-col :span="16"><div class="grid-content grid-secondary"></div></el-col>
          <el-col :span="2" :offset="6"><div class="grid-content grid-tertiary"></div></el-col>
        </el-row>

        <el-row :gutter="20" style="margin-top: 16px;">
          <el-col :span="4"><div class="grid-content grid-secondary"></div></el-col>
          <el-col :span="8" :offset="4"><div class="grid-content grid-tertiary"></div></el-col>
          <el-col :span="6" :offset="2"><div class="grid-content grid-secondary"></div></el-col>
        </el-row>
      </div>

      <!-- 对齐方式 -->
      <div class="layout-section">
        <h3 class="section-title">对齐方式</h3>

        <div class="alignment-demo">
          <p class="demo-label">左对齐</p>
          <el-row type="flex" class="row-bg">
            <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
            <el-col :span="6"><div class="grid-content grid-tertiary"></div></el-col>
            <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
          </el-row>
        </div>

        <div class="alignment-demo">
          <p class="demo-label">居中</p>
          <el-row type="flex" class="row-bg" justify="center">
            <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
            <el-col :span="6"><div class="grid-content grid-tertiary"></div></el-col>
            <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
          </el-row>
        </div>

        <div class="alignment-demo">
          <p class="demo-label">右对齐</p>
          <el-row type="flex" class="row-bg" justify="end">
            <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
            <el-col :span="6"><div class="grid-content grid-tertiary"></div></el-col>
            <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
          </el-row>
        </div>

        <div class="alignment-demo">
          <p class="demo-label">两端对齐</p>
          <el-row type="flex" class="row-bg" justify="space-between">
            <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
            <el-col :span="6"><div class="grid-content grid-tertiary"></div></el-col>
            <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
          </el-row>
        </div>

        <div class="alignment-demo">
          <p class="demo-label">均匀分布</p>
          <el-row type="flex" class="row-bg" justify="space-around">
            <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
            <el-col :span="6"><div class="grid-content grid-tertiary"></div></el-col>
            <el-col :span="6"><div class="grid-content grid-secondary"></div></el-col>
          </el-row>
        </div>
      </div>

      <!-- 响应式布局 -->
      <div class="layout-section">
        <h3 class="section-title">响应式布局</h3>
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <div class="grid-content grid-responsive">xs=24 sm=12 md=8 lg=6</div>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <div class="grid-content grid-responsive">xs=24 sm=12 md=8 lg=6</div>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <div class="grid-content grid-responsive">xs=24 sm=12 md=8 lg=6</div>
          </el-col>
          <el-col :xs="24" :sm="12" :md="8" :lg="6">
            <div class="grid-content grid-responsive">xs=24 sm=12 md=8 lg=6</div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LayoutDemo'
}
</script>

<style scoped>
.layout-container {
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

.layout-card {
  background-color: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-xl);
  padding: 32px;
}

.layout-section {
  margin-bottom: 48px;
}

.layout-section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 24px 0;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-subtle);
}

.alignment-demo {
  margin-bottom: 24px;
}

.alignment-demo:last-child {
  margin-bottom: 0;
}

.demo-label {
  color: var(--text-muted);
  font-size: 14px;
  margin: 0 0 12px 0;
  font-weight: 500;
}

/* Grid Content 深色主题 */
.grid-content {
  border-radius: var(--radius-lg);
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.grid-content:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.grid-primary {
  background: linear-gradient(135deg, var(--color-primary-500) 0%, #2563EB 100%);
  color: #FFFFFF;
  min-height: 80px;
  font-size: 15px;
  font-weight: 600;
}

.grid-secondary {
  background-color: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  color: var(--color-primary-500);
}

.grid-tertiary {
  background-color: rgba(59, 130, 246, 0.08);
  border: 1px dashed var(--color-primary-500);
  color: var(--text-muted);
}

.grid-responsive {
  background-color: rgba(34, 197, 94, 0.1);
  border: 1px solid #22C55E;
  color: #22C55E;
  font-size: 12px;
}

.el-row {
  margin-bottom: 0;
}
</style>
