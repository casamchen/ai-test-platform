<template>
  <div class="js-container">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">性能需求文档</h2>
      <div class="page-actions">
        <el-tag type="info">JavaScript ES6+</el-tag>
      </div>
    </div>

    <!-- Content Card -->
    <div class="content-card">
      <!-- Introduction -->
      <div class="intro-section">
        <h3 class="section-title">变量声明方式对比</h3>
        <p class="intro-text">
          JavaScript 提供了三种变量声明方式：var、let 和 const。了解它们的区别对于编写高质量的代码至关重要。
        </p>
      </div>

      <!-- Variable Types Demo -->
      <div class="demo-grid">
        <!-- var -->
        <div class="demo-card">
          <div class="card-header">
            <i class="el-icon-warning-outline card-icon warning"></i>
            <h4 class="card-title">var</h4>
          </div>
          <div class="card-body">
            <p class="card-description">函数作用域，存在变量提升</p>
            <code class="code-block">
              var a = 1;<br>
              console.log(a); // 1
            </code>
            <el-button type="warning" size="small" @click="clickButton1" style="width: 100%; margin-top: 16px;">
              测试 var
            </el-button>
          </div>
        </div>

        <!-- let -->
        <div class="demo-card">
          <div class="card-header">
            <i class="el-icon-success card-icon success"></i>
            <h4 class="card-title">let</h4>
          </div>
          <div class="card-body">
            <p class="card-description">块级作用域，可重新赋值</p>
            <code class="code-block">
              let a = 1;<br>
              if (a === 1) {<br>
              &nbsp;&nbsp;let b = 2;<br>
              }
            </code>
            <el-button type="success" size="small" @click="clickButton2" style="width: 100%; margin-top: 16px;">
              测试 let
            </el-button>
          </div>
        </div>

        <!-- const -->
        <div class="demo-card">
          <div class="card-header">
            <i class="el-icon-star-on card-icon primary"></i>
            <h4 class="card-title">const</h4>
          </div>
          <div class="card-body">
            <p class="card-description">块级作用域，不可重新赋值</p>
            <code class="code-block">
              const a = 1;<br>
              // a = 2; // Error!<br>
              console.log(a);
            </code>
            <el-button type="primary" size="small" @click="clickButton3" style="width: 100%; margin-top: 16px;">
              测试 const
            </el-button>
          </div>
        </div>
      </div>

      <!-- Comparison Table -->
      <div class="comparison-section">
        <h3 class="section-title">特性对比</h3>
        <el-table :data="comparisonData" border stripe>
          <el-table-column prop="feature" label="特性" width="180"></el-table-column>
          <el-table-column prop="var" label="var"></el-table-column>
          <el-table-column prop="let" label="let"></el-table-column>
          <el-table-column prop="const" label="const"></el-table-column>
        </el-table>
      </div>

      <!-- Best Practices -->
      <div class="best-practices">
        <h3 class="section-title">最佳实践建议</h3>
        <el-alert
          title="推荐使用 const 和 let"
          type="info"
          description="默认使用 const，只在需要重新赋值时使用 let。避免使用 var 以防止作用域污染和意外行为。"
          show-icon
          :closable="false">
        </el-alert>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      comparisonData: [
        { feature: '作用域', var: '函数作用域', let: '块级作用域', const: '块级作用域' },
        { feature: '变量提升', var: '是', let: '否（暂时性死区）', const: '否（暂时性死区）' },
        { feature: '重复声明', var: '允许', let: '不允许', const: '不允许' },
        { feature: '重新赋值', var: '允许', let: '允许', const: '不允许' },
        { feature: '全局声明', var: '挂载到 window', let: '不挂载', const: '不挂载' }
      ]
    }
  },
  methods: {
    clickButton1 () {
      var a = 1
      this.$message({
        type: 'success',
        message: `var a = ${a}`
      })
    },
    clickButton2 () {
      let a = 1
      if (a === 1) {
        let b = 2
        this.$message({
          type: 'success',
          message: `b: ${b}, a: ${a}`
        })
      }
    },
    clickButton3 () {
      const a = 1
      this.$message({
        type: 'success',
        message: `const a = ${a} (不可变)`
      })
    }
  }
}
</script>

<style scoped>
.js-container {
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

.intro-section,
.comparison-section,
.best-practices {
  margin-bottom: 40px;
}

.intro-section:last-child,
.comparison-section:last-child,
.best-practices:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 16px 0;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-subtle);
}

.intro-text {
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
  font-size: 14px;
}

/* Demo Grid */
.demo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.demo-card {
  background-color: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: all 0.3s ease;
}

.demo-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  border-color: var(--color-primary-500);
}

.card-header {
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid var(--border-subtle);
}

.card-icon {
  font-size: 20px;
}

.card-icon.warning {
  color: #F59E0B;
}

.card-icon.success {
  color: #22C55E;
}

.card-icon.primary {
  color: var(--color-primary-500);
}

.card-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
}

.card-body {
  padding: 20px;
}

.card-description {
  color: var(--text-muted);
  font-size: 13px;
  margin: 0 0 16px 0;
  line-height: 1.5;
}

.code-block {
  display: block;
  background-color: var(--bg-base);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 16px;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 13px;
  line-height: 1.6;
  color: #22C55E;
  overflow-x: auto;
}

/* Table 深色主题 */
/deep/ .el-table {
  background-color: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
}

/deep/ .el-table th,
/deep/ .el-table tr {
  background-color: var(--bg-elevated);
  color: var(--text-primary);
}

/deep/ .el-table td {
  border-bottom: 1px solid var(--border-subtle);
  color: var(--text-secondary);
}

/deep/ .el-table--striped .el-table__body tr.el-table__row--striped td {
  background-color: var(--bg-base);
}

/* Alert 深色主题 */
/deep/ .el-alert--info {
  background-color: rgba(59, 130, 246, 0.08);
  border-color: var(--color-primary-500);
}

/deep/ .el-alert__title {
  color: var(--text-primary);
}

/deep/ .el-alert__description {
  color: var(--text-secondary);
}

/* Tag 深色主题 */
/deep/ .el-tag--info {
  background-color: rgba(161, 161, 170, 0.15);
  border-color: var(--text-muted);
  color: var(--text-muted);
}
</style>
