import Vue from 'vue'
import Router from 'vue-router'
import home from '@/components/home'
import prd from '@/components/create_testcase/prd'
import interfaceadmin from '@/components/interface_test/interfaceadmin'
import testcase from '@/components/create_testcase/testcase'
import testreport from '@/components/create_testcase/testreport'
import interfacecase from '@/components/interface_test/interfacecase'
import interfacedataconfig from '@/components/interface_test/interfacedataconfig'
import interfacereport from '@/components/interface_test/interfacereport'
import helloelement from '@/components/app_test/helloelement'
import progress from '@/components/app_test/progress'
import allmenu from '@/components/cicd/allmenu'
import table from '@/components/web_test/table'
import upload from '@/components/web_test/upload'
import js01 from '@/components/performance/js01'
import js02 from '@/components/performance/js02'
import layout from '@/components/performance/layout'
import config from '@/components/project_config/config'
import login from '@/components/login/login'
import nofind from '@/components/nofind'

Vue.use(Router)

// 白名单路由 - 不需要登录即可访问
const whiteList = ['/', '/404']

// 创建路由实例（先赋值给变量，以便添加导航守卫）
const router = new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: login,
      meta: { requiresAuth: false }
    },
    {
      path: '/home',
      name: 'home',
      component: home,
      redirect: {name: 'prd'},
      meta: { requiresAuth: true },
      children:
      [
        {
          path: 'prd',
          name: 'prd',
          component: prd,
          meta: {
            title: '需求文档'
          }
        },
        {
          path: 'testcase',
          name: 'testcase',
          component: testcase,
          meta: {
            title: '测试用例'
          }
        },
        {
          path: 'testreport',
          name: 'testreport',
          component: testreport,
          meta: {
            title: '测试报告'
          }
        },
        {
          path: 'interface_admin',
          name: 'interfaceadmin',
          component: interfaceadmin,
          meta: {
            title: '接口管理'
          }
        },
        {
          path: 'interface_testcase',
          name: 'interfacecase',
          component: interfacecase,
          meta: {
            title: '接口用例'
          }
        },
        {
          path: 'interface_data',
          name: 'interfacedataconfig',
          component: interfacedataconfig,
          meta: {
            title: '数据配置'
          }
        },
        {
          path: 'interface_testcase_report',
          name: 'interfacereport',
          component: interfacereport,
          meta: {
            title: '测试报告'
          }
        },
        {
          path: 'app_result',
          name: 'helloelement',
          component: helloelement,
          meta: {
            title: '选择框'
          }
        },
        {
          path: 'app_testcase',
          name: 'progress',
          component: progress,
          meta: {
            title: '选择框'
          }
        },
        {
          path: 'web_result',
          name: 'table',
          component: table,
          meta: {
            title: '选择框'
          }
        },
        {
          path: 'web_testcase',
          name: 'upload',
          component: upload,
          meta: {
            title: '选择框'
          }
        },
        {
          path: 'performance_prd',
          name: 'js01',
          component: js01,
          meta: {
            title: '选择框'
          }
        },
        {
          path: 'performance_result',
          name: 'js02',
          component: js02,
          meta: {
            title: '选择框'
          }
        },
        {
          path: 'execute_record',
          name: 'layout',
          component: layout,
          meta: {
            title: '选择框'
          }
        },
        {
          path: 'a',
          name: 'allmenu',
          component: allmenu,
          meta: {
            title: '选择框'
          }
        },
        {
          path: 'b',
          name: 'layout-b',
          component: layout,
          meta: {
            title: '选择框'
          }
        },
        {
          path: 'c',
          name: 'layout-c',
          component: layout,
          meta: {
            title: '选择框'
          }
        },
        {
          path: 'project_config_1',
          name: 'config',
          component: config,
          meta: {
            title: '项目配置'
          }
        }
      ]
    },
    {
      path: '/404',
      name: 'nofind',
      component: nofind,
      meta: { requiresAuth: false }
    }
  ]
})

// ============================================
// 全局路由守卫 - 认证检查
// ============================================
router.beforeEach((to, from, next) => {
  // 检查路由是否存在
  if (to.matched.length === 0) {
    next({ path: '/404' })
    return
  }

  // 白名单中的路由直接放行
  if (whiteList.indexOf(to.path) !== -1) {
    next()
    return
  }

  // 获取登录 token
  const token = localStorage.getItem('token') || sessionStorage.getItem('token')

  // 判断目标路由是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false)

  if (requiresAuth && !token) {
    // 需要认证但未登录，跳转到登录页
    next({
      path: '/',
      query: { redirect: to.fullPath } // 保存目标路径，登录后可跳回
    })
  } else if (!requiresAuth && token && to.path === '/') {
    // 已登录用户访问登录页，重定向到首页
    // 使用 replace 避免导航冲突
    next({ path: '/home', replace: true })
  } else {
    next()
  }
})

export default router
