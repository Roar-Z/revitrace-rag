import axios from 'axios'
import { ElMessage } from 'element-plus'

// 后端地址统一从环境变量读取，未配置时回退到本地默认值
const baseURL = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '')
const timeout = Number(import.meta.env.VITE_REQUEST_TIMEOUT || 60000)

const http = axios.create({ baseURL, timeout })

// 同一错误短时间内只提示一次，避免并发请求刷屏
let lastMessage = ''
let lastMessageAt = 0

function notifyError(message) {
  const now = Date.now()
  if (message === lastMessage && now - lastMessageAt < 1500) return
  lastMessage = message
  lastMessageAt = now
  ElMessage.error(message)
}

// 请求拦截：上传文件时移除 Content-Type，让浏览器自动补全 boundary
http.interceptors.request.use(
  (config) => {
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截：拆解后端统一响应体 {code, msg, data}，异常统一提示
http.interceptors.response.use(
  (response) => {
    const body = response.data
    if (body && typeof body.code !== 'undefined' && body.code !== 0) {
      const message = body.msg || '请求失败'
      notifyError(message)
      return Promise.reject(new Error(message))
    }
    return body?.data ?? body
  },
  (error) => {
    let message = '请求失败，请稍后重试'

    if (error.code === 'ECONNABORTED') {
      message = '请求超时，请稍后重试'
    } else if (!error.response) {
      message = `无法连接后端服务（${baseURL}）`
    } else {
      message = error.response.data?.msg || `请求失败（HTTP ${error.response.status}）`
    }

    notifyError(message)
    return Promise.reject(error)
  }
)

export { baseURL }
export default http
