<template>
  <div class="layout-container">
    <!-- Sidebar -->
    <aside class="sidebar" :style="{ width: sidebarWidth + 'px' }">
      <div class="sidebar-header">
        <div class="brand">
          <div class="brand-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 12l2 2 4-4"/>
              <circle cx="12" cy="12" r="10"/>
            </svg>
          </div>
          <span class="brand-text">AI Test</span>
        </div>
      </div>

      <nav class="sidebar-nav">
        <!-- Functional Testing -->
        <div class="nav-group">
          <span class="nav-group-title">Testing</span>
          <el-menu
            :default-active="activeMenu"
            @select="ChangeSelect"
            class="nav-menu"
          >
            <el-menu-item index="/home/prd">
              <i class="el-icon-document"></i>
              <span>Requirements</span>
            </el-menu-item>
            <el-menu-item index="/home/testcase">
              <i class="el-icon-finished"></i>
              <span>Test Cases</span>
            </el-menu-item>
            <el-menu-item index="/home/testreport">
              <i class="el-icon-data-analysis"></i>
              <span>Reports</span>
            </el-menu-item>
          </el-menu>
        </div>

        <!-- API Testing -->
        <div class="nav-group">
          <span class="nav-group-title">API Testing</span>
          <el-menu
            :default-active="activeMenu"
            @select="ChangeSelect"
            class="nav-menu"
          >
            <el-menu-item index="/home/interface_admin">
              <i class="el-icon-connection"></i>
              <span>Interface Mgmt</span>
            </el-menu-item>
            <el-menu-item index="/home/interface_testcase">
              <i class="el-icon-lightning"></i>
              <span>API Testing</span>
            </el-menu-item>
            <el-menu-item index="/home/interface_data">
              <i class="el-icon-setting"></i>
              <span>Data Config</span>
            </el-menu-item>
            <el-menu-item index="/home/interface_testcase_report">
              <i class="el-icon-notebook-2"></i>
              <span>Test Reports</span>
            </el-menu-item>
          </el-menu>
        </div>

        <!-- Automation -->
        <div class="nav-group">
          <span class="nav-group-title">Automation</span>
          <el-menu
            :default-active="activeMenu"
            @select="ChangeSelect"
            class="nav-menu"
          >
            <div class="nav-sub-group">
              <span class="nav-sub-title">App Testing</span>
              <el-menu-item index="/home/app_result">
                <i class="el-icon-monitor"></i>
                <span>Results</span>
              </el-menu-item>
              <el-menu-item index="/home/app_testcase">
                <i class="el-icon-tickets"></i>
                <span>Cases</span>
              </el-menu-item>
            </div>
            <div class="nav-sub-group">
              <span class="nav-sub-title">Web Testing</span>
              <el-menu-item index="/home/web_result">
                <i class="el-icon-monitor"></i>
                <span>Results</span>
              </el-menu-item>
              <el-menu-item index="/home/web_testcase">
                <i class="el-icon-tickets"></i>
                <span>Cases</span>
              </el-menu-item>
            </div>
          </el-menu>
        </div>

        <!-- Performance -->
        <div class="nav-group">
          <span class="nav-group-title">Performance</span>
          <el-menu
            :default-active="activeMenu"
            @select="ChangeSelect"
            class="nav-menu"
          >
            <el-menu-item index="/home/performance_prd">
              <i class="el-icon-document-checked"></i>
              <span>PRD</span>
            </el-menu-item>
            <el-menu-item index="/home/performance_result">
              <i class="el-icon-pie-chart"></i>
              <span>Results</span>
            </el-menu-item>
            <el-menu-item index="/home/execute_record">
              <i class="el-icon-time"></i>
              <span>Records</span>
            </el-menu-item>
          </el-menu>
        </div>

        <!-- CI/CD -->
        <div class="nav-group">
          <span class="nav-group-title">CI/CD</span>
          <el-menu
            :default-active="activeMenu"
            @select="ChangeSelect"
            class="nav-menu"
          >
            <el-menu-item index="/home/a">
              <i class="el-icon-cpu"></i>
              <span>Pipeline A</span>
            </el-menu-item>
            <el-menu-item index="/home/b">
              <i class="el-icon-cpu"></i>
              <span>Pipeline B</span>
            </el-menu-item>
            <el-menu-item index="/home/c">
              <i class="el-icon-cpu"></i>
              <span>Pipeline C</span>
            </el-menu-item>
          </el-menu>
        </div>

        <!-- Config -->
        <div class="nav-group">
          <span class="nav-group-title">Settings</span>
          <el-menu
            :default-active="activeMenu"
            @select="ChangeSelect"
            class="nav-menu"
          >
            <el-menu-item index="/home/project_config_1">
              <i class="el-icon-tools"></i>
              <span>Project Config</span>
            </el-menu-item>
          </el-menu>
        </div>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">{{ userInitial }}</div>
          <div class="user-detail">
            <span class="user-name">{{ userName }}</span>
            <span class="user-role">Administrator</span>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="main-wrapper" :style="{ marginLeft: sidebarWidth + 'px' }">
      <!-- Top Bar -->
      <header class="topbar">
        <div class="topbar-left">
          <h2 class="page-title">{{ pageTitle }}</h2>
          <el-tag v-if="pageTag" size="mini" type="primary">{{ pageTag }}</el-tag>
        </div>
        <div class="topbar-right">
          <div class="topbar-action" title="Notifications">
            <i class="el-icon-bell"></i>
            <span class="action-dot"></span>
          </div>
          <div class="topbar-user" :title="userName">
            {{ userInitial }}
          </div>
        </div>
      </header>

      <!-- Content Area -->
      <main class="main-content">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      sidebarWidth: 220,
      activeMenu: '/home/prd'
    }
  },
  computed: {
    userName () {
      const token = localStorage.getItem('token') || ''
      return token ? 'User' : 'Guest'
    },
    userInitial () {
      return this.userName.charAt(0).toUpperCase()
    },
    pageTitle () {
      const routeMap = {
        'prd': 'Requirements',
        'testcase': 'Test Cases',
        'testreport': 'Test Reports',
        'interface_admin': 'Interface Management',
        'interface_testcase': 'API Test Cases',
        'interface_data': 'Data Configuration',
        'interface_testcase_report': 'API Reports',
        'app_result': 'App Results',
        'app_testcase': 'App Cases',
        'web_result': 'Web Results',
        'web_testcase': 'Web Cases',
        'performance_prd': 'Performance PRD',
        'performance_result': 'Performance Results',
        'execute_record': 'Execution Records'
      }
      const path = this.$route.path.split('/').pop()
      return routeMap[path] || 'Dashboard'
    },
    pageTag () {
      const tagMap = {
        'prd': 'PRD',
        'testcase': 'QA',
        'testreport': 'Report',
        'interface_admin': 'API',
        'interface_testcase': 'API',
        'performance_prd': 'Perf'
      }
      const path = this.$route.path.split('/').pop()
      return tagMap[path] || null
    }
  },
  watch: {
    '$route.path': {
      handler (path) {
        this.activeMenu = path
      },
      immediate: true
    }
  },
  methods: {
    ChangeSelect (path) {
      this.$router.push(path).catch(() => {})
    },
    handleResize () {},
    handleDragStart (event) {
      this.startX = event.clientX
      this.isDragging = true
    },
    handleDrag (event) {
      if (this.isDragging) {
        const currentX = event.clientX
        const deltaX = currentX - this.startX
        this.sidebarWidth = Math.max(this.sidebarWidth + deltaX, 180)
        this.startX = currentX
      }
    },
    handleDragEnd () {
      this.isDragging = false
    }
  },
  mounted () {
    window.addEventListener('resize', this.handleResize)
    this.activeMenu = this.$route.path
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.handleResize)
  }
}
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
  background-color: var(--bg-base);
}

/* Sidebar */
.sidebar {
  width: 220px;
  background-color: var(--bg-surface);
  border-right: 1px solid var(--border-default);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
  transition: width var(--transition-normal);
}

.sidebar-header {
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--border-default);
}

.brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.brand-icon {
  width: 32px;
  height: 32px;
  background: var(--gradient-brand);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.brand-text {
  font-size: var(--text-md);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
}

/* Navigation */
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-3) 0;
}

.nav-group {
  margin-bottom: var(--space-4);
}

.nav-group-title {
  display: block;
  padding: var(--space-2) var(--space-5);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
  color: var(--text-disabled);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.nav-sub-group {
  padding-left: var(--space-4);
}

.nav-sub-title {
  display: block;
  padding: var(--space-1) var(--space-4);
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.nav-menu {
  border-right: none !important;
  background-color: transparent !important;
  padding: 0 !important;
}

.nav-menu .el-menu-item {
  height: 38px;
  line-height: 38px;
  padding: 0 var(--space-5) !important;
  color: var(--text-muted) !important;
  font-size: var(--text-sm);
  border-radius: 0 !important;
  margin: 1px 0;
}

.nav-menu .el-menu-item i {
  color: inherit;
  font-size: 14px;
  margin-right: var(--space-2);
}

.nav-menu .el-menu-item:hover {
  background-color: var(--bg-elevated) !important;
  color: var(--text-primary) !important;
}

.nav-menu .el-menu-item.is-active {
  background-color: var(--bg-elevated) !important;
  color: var(--color-primary-400) !important;
  border-left: 2px solid var(--color-primary-500) !important;
  padding-left: calc(var(--space-5) - 2px) !important;
}

/* Sidebar Footer */
.sidebar-footer {
  padding: var(--space-4) var(--space-5);
  border-top: 1px solid var(--border-default);
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: var(--color-primary-500);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: white;
  flex-shrink: 0;
}

.user-detail {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--text-primary);
  line-height: 1.2;
}

.user-role {
  font-size: var(--text-xs);
  color: var(--text-muted);
}

/* Main Wrapper */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  transition: margin-left var(--transition-normal);
}

/* Top Bar */
.topbar {
  height: var(--topbar-height);
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--border-default);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-6);
  position: sticky;
  top: 0;
  z-index: 50;
}

.topbar-left {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.page-title {
  font-size: var(--text-lg);
  font-weight: var(--font-medium);
  color: var(--text-primary);
  margin: 0;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.topbar-action {
  width: 34px;
  height: 34px;
  background-color: var(--bg-elevated);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  transition: background-color var(--transition-fast);
}

.topbar-action:hover {
  background-color: var(--bg-hover);
}

.topbar-action i {
  font-size: 16px;
  color: var(--text-muted);
}

.action-dot {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 7px;
  height: 7px;
  background-color: var(--color-error);
  border-radius: var(--radius-full);
  border: 1.5px solid var(--bg-surface);
}

.topbar-user {
  width: 34px;
  height: 34px;
  background-color: var(--color-primary-500);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: white;
  cursor: pointer;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: var(--space-6);
  overflow-y: auto;
  background-color: var(--bg-base);
}
</style>
