<template>
  <div class="menu-container">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">组件导航</h2>
      <div class="page-actions">
        <el-radio-group v-model="isCollapse" size="small">
          <el-radio-button :label="false">展开</el-radio-button>
          <el-radio-button :label="true">收起</el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <!-- Menu Card -->
    <div class="menu-card">
      <el-menu
        default-active="2-5"
        class="el-menu-vertical-demo custom-menu"
        @open="handleOpen"
        @close="handleClose"
        @select="handleSelect"
        :collapse="isCollapse"
        background-color="var(--bg-elevated)"
        text-color="var(--text-secondary)"
        active-text-color="var(--color-primary-500)">
        <el-menu-item index="1">
          <a href="http://localhost:8080/#/button" target="_blank" class="menu-link">
            <i class="el-icon-thumb"></i>
            <span slot="title">Button</span>
          </a>
        </el-menu-item>

        <el-submenu index="2">
          <template slot="title">
            <i class="el-icon-more"></i>
            <span>Form 表单</span>
          </template>
          <el-menu-item-group title="表单组件">
            <el-menu-item index="2-1">
              <a href="http://localhost:8080/#/radio" target="_blank" class="menu-link">
                <i class="el-icon-turn-off"></i>
                <span slot="title">Radio 单选框</span>
              </a>
            </el-menu-item>
            <el-menu-item index="2-2">
              <a href="http://localhost:8080/#/select" target="_blank" class="menu-link">
                <i class="el-icon-chat-line-square"></i>
                <span slot="title">Select 选择器</span>
              </a>
            </el-menu-item>
            <el-menu-item index="2-3">
              <a href="http://localhost:8080/#/form" target="_blank" class="menu-link">
                <i class="el-icon-set-up"></i>
                <span slot="title">Form 表单</span>
              </a>
            </el-menu-item>
            <el-menu-item index="2-4">
              <a href="http://localhost:8080/#/upload" target="_blank" class="menu-link">
                <i class="el-icon-upload"></i>
                <span slot="title">Upload 上传</span>
              </a>
            </el-menu-item>
            <el-menu-item index="2-5">
              <a href="http://localhost:8080/#/input" target="_blank" class="menu-link">
                <i class="el-icon-edit-outline"></i>
                <span slot="title">Input 输入框</span>
              </a>
            </el-menu-item>
          </el-menu-item-group>
        </el-submenu>

        <el-menu-item index="3">
          <a href="http://localhost:8080/#/layout" target="_blank" class="menu-link">
            <i class="el-icon-s-fold"></i>
            <span slot="title">Layout 布局</span>
          </a>
        </el-menu-item>

        <el-menu-item index="4">
          <a href="http://localhost:8080/#/table" target="_blank" class="menu-link">
            <i class="el-icon-s-data"></i>
            <span slot="title">Table 表格</span>
          </a>
        </el-menu-item>

        <el-menu-item index="5">
          <a href="http://localhost:8080/#/container" target="_blank" class="menu-link">
            <i class="el-icon-menu"></i>
            <span slot="title">Container 容器</span>
          </a>
        </el-menu-item>

        <el-menu-item index="6">
          <a href="http://localhost:8080/#/dialog" target="_blank" class="menu-link">
            <i class="el-icon-s-opportunity"></i>
            <span slot="title">Dialog 对话框</span>
          </a>
        </el-menu-item>

        <el-menu-item index="7">
          <a href="http://localhost:8080/#/pagination" target="_blank" class="menu-link">
            <i class="el-icon-s-custom"></i>
            <span slot="title">Pagination 分页</span>
          </a>
        </el-menu-item>

        <el-menu-item index="8">
          <a href="http://localhost:8080/#/progress" target="_blank" class="menu-link">
            <i class="el-icon-loading"></i>
            <span slot="title">Progress 进度条</span>
          </a>
        </el-menu-item>

        <el-menu-item index="9">
          <a href="http://localhost:8080/#/NavMenu" target="_blank" class="menu-link">
            <i class="el-icon-s-management"></i>
            <span slot="title">NavMenu 导航菜单</span>
          </a>
        </el-menu-item>
      </el-menu>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      activeIndex: '',
      isCollapse: false
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      // 菜单选择处理
    },
    handleOpen (key, keyPath) {
      // 菜单展开处理
    },
    handleClose (key, keyPath) {
      // 菜单收起处理
    }
  }
}
</script>

<style scoped>
.menu-container {
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
  align-items: center;
}

.menu-card {
  max-width: 280px;
  border-radius: var(--radius-xl);
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

/* Menu 深色主题 */
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 260px;
  min-height: 500px;
}

.custom-menu /deep/ .el-menu {
  border-right: none;
}

.custom-menu /deep/ .el-menu-item,
.custom-menu /deep/ .el-submenu__title {
  transition: all 0.3s ease;
}

.custom-menu /deep/ .el-menu-item:hover,
.custom-menu /deep/ .el-submenu__title:hover {
  background-color: rgba(59, 130, 246, 0.08) !important;
}

.custom-menu /deep/ .el-menu-item.is-active {
  background-color: rgba(59, 130, 246, 0.15) !important;
  border-right: 3px solid var(--color-primary-500);
}

.custom-menu /deep/ .el-submenu .el-menu-item {
  background-color: var(--bg-base) !important;
}

.custom-menu /deep/ .el-submenu .el-menu-item:hover {
  background-color: rgba(59, 130, 246, 0.08) !important;
}

/* Menu Link */
.menu-link {
  display: flex;
  align-items: center;
  width: 100%;
  height: 100%;
  text-decoration: none;
  color: inherit;
}

.menu-link i {
  color: inherit;
}

/* Radio Group 深色主题 */
/deep/ .el-radio-button__inner {
  background-color: var(--bg-elevated);
  border-color: var(--border-subtle);
  color: var(--text-secondary);
  box-shadow: none;
}

/deep/ .el-radio-button__orig-radio:checked + .el-radio-button__inner {
  background-color: var(--color-primary-500);
  border-color: var(--color-primary-500);
  color: #FFFFFF;
  box-shadow: -1px 0 0 0 var(--color-primary-500), 1px 0 0 0 var(--color-primary-500);
}

/deep/ .el-radio-button:first-child .el-radio-button__inner {
  border-radius: var(--radius-lg) 0 0 var(--radius-lg);
}

/deep/ .el-radio-button:last-child .el-radio-button__inner {
  border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
}
</style>
