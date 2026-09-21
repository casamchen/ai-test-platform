// The Vue Build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'
import CryptoJS from 'crypto-js'
import './styles/dark-theme.css'

Vue.use(ElementUI)
Vue.config.productionTip = false
Vue.prototype.axios = axios

// ============================================
// AES 加密配置 - 密钥需与后端保持一致
// 默认使用与后端相同的密钥，生产环境通过 VUE_APP_AES_KEY 覆盖
// ============================================
const AES_KEY = process.env.VUE_APP_AES_KEY || '1111111111111111'
const AES_IV = process.env.VUE_APP_AES_IV || '1111111111111111'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})

/**
 * AES 加密函数
 * @param {Object} data - 待加密的数据对象
 * @returns {string} Base64编码的密文
 */
function encryptData (data) {
  const key = CryptoJS.enc.Utf8.parse(AES_KEY)
  const iv = CryptoJS.enc.Utf8.parse(AES_IV)
  return encrypt(data, key, iv)
}

/**
 * 内部加密实现
 */
function encrypt (data, key, iv) {
  var jsdata = JSON.stringify(data)
  const encryptedData = CryptoJS.AES.encrypt(jsdata, key, {
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7
  })
  const ciphertext = encryptedData.ciphertext.toString(CryptoJS.enc.Base64)
  return ciphertext
}

/**
 * AES 解密函数
 * @param {string} encryptedData - Base64编码的密文
 * @returns {Object} 解密后的数据对象
 */
function decrypt (encryptedData) {
  const key = CryptoJS.enc.Utf8.parse(AES_KEY)
  const iv = CryptoJS.enc.Utf8.parse(AES_IV)
  const encryptedBytes = CryptoJS.enc.Base64.parse(encryptedData)
  const decryptedData = CryptoJS.AES.decrypt({ciphertext: encryptedBytes}, key, {
    iv: iv,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7})
  const decryptedText = decryptedData.toString(CryptoJS.enc.Utf8)
  // 安全解析JSON，处理单引号兼容
  try {
    const normalizedText = decryptedText.replace(/'/g, '"')
    return JSON.parse(normalizedText)
  } catch (e) {
    console.error('解密数据JSON解析失败:', e)
    return null
  }
}

// 需要加解密的接口列表
const specialEndpoints = ['/api/login', '/api/signup']

// 请求拦截器 - 对敏感接口的请求数据进行加密
axios.interceptors.request.use(config => {
  // 从 localStorage 获取 token 并添加到请求头
  const token = localStorage.getItem('token') || sessionStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  if (specialEndpoints.includes(config.url) && config.data) {
    config.data = encryptData(config.data)
    // 加密后数据是 Base64 字符串，必须阻止 axios 再次 JSON 序列化
    config.transformRequest = [function (data) {
      return data
    }]
    config.headers['Content-Type'] = 'text/plain'
  }
  return config
}, error => {
  return Promise.reject(error)
})

// 响应拦截器 - 对敏感接口的响应数据进行解密
axios.interceptors.response.use(response => {
  if (specialEndpoints.includes(response.config.url) && response.data && response.data.msg) {
    const decryptedData = decrypt(response.data.msg)
    if (decryptedData) {
      response.data = decryptedData
    }
  }
  return response
}, error => {
  if (error.response) {
    const { status } = error.response
    if (status === 401) {
      // Token 过期或无效，清除本地存储并跳转登录页
      localStorage.removeItem('token')
      sessionStorage.removeItem('token')
      router.push('/')
    } else if (status === 403) {
      console.error('无权限访问')
    } else if (status === 500) {
      console.error('服务器内部错误')
    }
  }
  return Promise.reject(error)
})
