/**
 * API服务模块
 * 负责人：组员A
 * 作用：封装与后端API的通信，提供代码分析等接口调用
 */

import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 60000, // 60秒超时
  headers: {
    'Content-Type': 'application/json',
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('发送API请求:', config.method?.toUpperCase(), config.url)
    return config
  },
  (error) => {
    console.error('请求配置错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log('收到API响应:', response.status, response.config.url)
    return response
  },
  (error) => {
    console.error('API响应错误:', error.response?.status, error.message)
    
    // 统一错误处理
    const errorMessage = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        error.message || 
                        '网络请求失败'
    
    return Promise.reject(new Error(errorMessage))
  }
)

/**
 * 代码分析API
 * @param {Object} data - 分析请求数据
 * @param {string} data.code - 待分析的代码
 * @param {string} data.language - 编程语言
 * @param {string} data.analysis_type - 分析类型 ('explain' | 'review')
 */
export const analyzeCode = async (data) => {
  const endpoint = data.analysis_type === 'explain' ? '/explain' : '/review'
  return api.post(endpoint, data)
}

/**
 * 检查服务状态
 */
export const checkStatus = async () => {
  return api.get('/status')
}

/**
 * 健康检查
 */
export const healthCheck = async () => {
  return api.get('http://localhost:8000/health')
}

export default api