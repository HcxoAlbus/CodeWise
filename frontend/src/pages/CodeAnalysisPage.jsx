/**
 * 代码分析页面
 * 负责人：组员A
 * 作用：核心功能页面，提供代码输入、分析选择和结果展示
 */

import React, { useState } from 'react'
import { Row, Col, Button, Radio, message, Typography, Space, Card } from 'antd'
import { PlayCircleOutlined, LoadingOutlined } from '@ant-design/icons'
import CodeEditor from '../components/CodeEditor'
import AnalysisResult from '../components/AnalysisResult'
import { analyzeCode } from '../services/api'

const { Title } = Typography

const CodeAnalysisPage = () => {
  const [code, setCode] = useState('')
  const [analysisType, setAnalysisType] = useState('explain')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [backendStatus, setBackendStatus] = useState('unknown') // 新增后端状态

  // 检查后端服务状态
  const checkBackendStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/health')
      if (response.ok) {
        setBackendStatus('connected')
        message.success('后端服务连接正常')
      } else {
        setBackendStatus('error')
        message.error(`后端服务响应异常: ${response.status}`)
      }
    } catch (error) {
      setBackendStatus('disconnected')
      message.error('无法连接到后端服务，请检查服务是否启动')
    }
  }

  // 组件加载时检查后端状态
  React.useEffect(() => {
    checkBackendStatus()
  }, [])

  // 处理代码分析
  const handleAnalyze = async () => {
    if (!code.trim()) {
      message.warning('请输入要分析的代码')
      return
    }

    setLoading(true)
    try {
      console.log('开始分析，请求数据:', {
        code: code.trim(),
        language: 'python',
        analysis_type: analysisType
      })
      
      const response = await analyzeCode({
        code: code.trim(),
        language: 'python',
        analysis_type: analysisType
      })
      
      console.log('分析成功，响应数据:', response.data)
      setResult(response.data)
      message.success('分析完成！')
    } catch (error) {
      console.error('分析失败，详细错误:', {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        config: error.config
      })
      
      // 更详细的错误信息
      let errorMsg = '分析失败：'
      if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
        errorMsg += '无法连接到后端服务，请确保后端服务已启动 (http://localhost:8000)'
      } else if (error.response?.status === 404) {
        errorMsg += '接口不存在，请检查API路径配置'
      } else if (error.response?.status === 500) {
        errorMsg += `服务器内部错误: ${error.response?.data?.detail || '未知错误'}`
      } else if (error.response?.status === 422) {
        errorMsg += `请求参数错误: ${error.response?.data?.detail || '数据验证失败'}`
      } else {
        errorMsg += error.message || '未知错误'
      }
      
      message.error(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  // 示例代码
  const handleLoadExample = () => {
    const exampleCode = `def fibonacci(n):
    """计算斐波那契数列的第n项"""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# 测试函数
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")`
    
    setCode(exampleCode)
    message.info('已加载示例代码')
  }

  return (
    <div className="code-analysis-page">
      <Title level={2} className="page-title">
        AI 代码分析工具
      </Title>
      
      <Row gutter={[24, 24]}>
        {/* 左侧：代码输入区 */}
        <Col xs={24} lg={12}>
          <Card title="代码输入" className="input-card">
            <Space direction="vertical" style={{ width: '100%' }} size="middle">
              <div className="analysis-options">
                <Radio.Group 
                  value={analysisType} 
                  onChange={(e) => setAnalysisType(e.target.value)}
                  size="large"
                >
                  <Radio.Button value="explain">代码解释</Radio.Button>
                  <Radio.Button value="review">代码审查</Radio.Button>
                </Radio.Group>
              </div>
              
              <CodeEditor 
                value={code}
                onChange={setCode}
                height="500px"
                language="python"
              />
              
              <Space>
                <Button 
                  type="primary" 
                  size="large"
                  icon={loading ? <LoadingOutlined /> : <PlayCircleOutlined />}
                  onClick={handleAnalyze}
                  loading={loading}
                  disabled={!code.trim() || backendStatus !== 'connected'}
                >
                  {loading ? '分析中...' : '开始分析'}
                </Button>
                
                <Button 
                  size="large"
                  onClick={handleLoadExample}
                >
                  加载示例
                </Button>
                
                <Button 
                  size="large"
                  onClick={checkBackendStatus}
                  type={backendStatus === 'connected' ? 'default' : 'dashed'}
                >
                  {backendStatus === 'connected' ? '✅ 后端已连接' : 
                   backendStatus === 'disconnected' ? '❌ 后端未连接' : 
                   backendStatus === 'error' ? '⚠️ 后端异常' : '🔄 检查中...'}
                </Button>
              </Space>
            </Space>
          </Card>
        </Col>

        {/* 右侧：分析结果区 */}
        <Col xs={24} lg={12}>
          <Card title="分析结果" className="result-card">
            <AnalysisResult 
              result={result}
              loading={loading}
              analysisType={analysisType}
            />
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default CodeAnalysisPage