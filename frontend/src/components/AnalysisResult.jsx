/**
 * 分析结果展示组件
 * 负责人：组员A
 * 作用：展示AI分析结果，支持代码解释和代码审查两种模式
 */

import React from 'react'
import { Empty, Spin, Typography, Divider, Tag, Alert, Progress } from 'antd'
import { ClockCircleOutlined, BugOutlined, ThunderboltOutlined, CheckCircleOutlined } from '@ant-design/icons'
import ReactMarkdown from 'react-markdown'

const { Title, Paragraph, Text } = Typography

const AnalysisResult = ({ result, loading, analysisType }) => {
  // 加载状态
  if (loading) {
    return (
      <div className="loading-container">
        <Spin size="large" />
        <Paragraph style={{ marginTop: 16, textAlign: 'center' }}>
          AI正在分析您的代码，请稍候...
        </Paragraph>
      </div>
    )
  }

  // 无结果状态
  if (!result) {
    return (
      <Empty
        description="请输入代码并点击分析按钮"
        image={Empty.PRESENTED_IMAGE_SIMPLE}
      />
    )
  }

  // 渲染代码解释结果
  const renderExplanationResult = () => (
    <div className="explanation-result">
      <div className="result-header">
        <Title level={4}>
          <CheckCircleOutlined style={{ color: '#52c41a' }} /> 代码解释结果
        </Title>
        <Text type="secondary">
          <ClockCircleOutlined /> 分析耗时: {result.execution_time?.toFixed(2)}秒
        </Text>
      </div>

      <Divider />

      <div className="explanation-content">
        <Title level={5}>功能概述</Title>
        <Alert
          message={result.code_summary}
          type="info"
          showIcon
          style={{ marginBottom: 16 }}
        />

        <Title level={5}>详细解释</Title>
        <div className="markdown-content">
          <ReactMarkdown>{result.explanation}</ReactMarkdown>
        </div>

        {result.key_concepts && result.key_concepts.length > 0 && (
          <>
            <Title level={5}>关键概念</Title>
            <div className="key-concepts">
              {result.key_concepts.map((concept, index) => (
                <Tag key={index} color="blue" style={{ margin: '4px' }}>
                  {concept}
                </Tag>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  )

  // 渲染代码审查结果
  const renderReviewResult = () => (
    <div className="review-result">
      <div className="result-header">
        <Title level={4}>
          <BugOutlined style={{ color: '#f5222d' }} /> 代码审查结果
        </Title>
        <Text type="secondary">
          <ClockCircleOutlined /> 分析耗时: {result.execution_time?.toFixed(2)}秒
        </Text>
      </div>

      <Divider />

      {/* 总体评分 */}
      <div className="overall-score">
        <Title level={5}>总体评分</Title>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <Progress
            type="circle"
            percent={result.overall_score}
            format={(percent) => `${percent}分`}
            strokeColor={percent => 
              percent >= 80 ? '#52c41a' : 
              percent >= 60 ? '#faad14' : '#f5222d'
            }
          />
          <Paragraph>{result.summary}</Paragraph>
        </div>
      </div>

      <Divider />

      {/* Bug分析 */}
      {result.bugs && result.bugs.length > 0 && (
        <div className="bugs-section">
          <Title level={5}>
            <BugOutlined /> 潜在Bug ({result.bugs.length}个)
          </Title>
          {result.bugs.map((bug, index) => (
            <Alert
              key={index}
              type="error"
              message={`第${bug.line_number || '?'}行: ${bug.description}`}
              description={bug.suggestion}
              style={{ marginBottom: 8 }}
            />
          ))}
        </div>
      )}

      {/* 代码风格问题 */}
      {result.style_issues && result.style_issues.length > 0 && (
        <div className="style-issues-section">
          <Title level={5}>
            代码风格问题 ({result.style_issues.length}个)
          </Title>
          {result.style_issues.map((issue, index) => (
            <Alert
              key={index}
              type="warning"
              message={`第${issue.line_number || '?'}行: ${issue.rule}`}
              description={`${issue.message} - ${issue.suggestion}`}
              style={{ marginBottom: 8 }}
            />
          ))}
        </div>
      )}

      {/* 优化建议 */}
      {result.optimizations && result.optimizations.length > 0 && (
        <div className="optimizations-section">
          <Title level={5}>
            <ThunderboltOutlined /> 优化建议 ({result.optimizations.length}个)
          </Title>
          {result.optimizations.map((opt, index) => (
            <Alert
              key={index}
              type="info"
              message={`${opt.category}: ${opt.description}`}
              description={
                <div>
                  <Paragraph>{opt.performance_impact}</Paragraph>
                  {opt.before_code && (
                    <div>
                      <Text strong>优化前:</Text>
                      <pre style={{ background: '#f5f5f5', padding: '8px', borderRadius: '4px' }}>
                        {opt.before_code}
                      </pre>
                    </div>
                  )}
                  {opt.after_code && (
                    <div>
                      <Text strong>优化后:</Text>
                      <pre style={{ background: '#f6ffed', padding: '8px', borderRadius: '4px' }}>
                        {opt.after_code}
                      </pre>
                    </div>
                  )}
                </div>
              }
              style={{ marginBottom: 8 }}
            />
          ))}
        </div>
      )}

      {/* 如果没有问题 */}
      {(!result.bugs || result.bugs.length === 0) && 
       (!result.style_issues || result.style_issues.length === 0) && 
       (!result.optimizations || result.optimizations.length === 0) && (
        <Alert
          type="success"
          message="恭喜！"
          description="您的代码质量很好，没有发现明显的问题。"
          showIcon
        />
      )}
    </div>
  )

  return (
    <div className="analysis-result">
      {analysisType === 'explain' ? renderExplanationResult() : renderReviewResult()}
    </div>
  )
}

export default AnalysisResult