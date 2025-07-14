/**
 * 首页组件
 * 负责人：组员A
 * 作用：项目介绍页面，展示功能特性和使用指南
 */

import React from 'react'
import { Link } from 'react-router-dom'
import { Button, Card, Row, Col, Typography, Space } from 'antd'
import { CodeOutlined, BugOutlined, ThunderboltOutlined, BookOutlined } from '@ant-design/icons'

const { Title, Paragraph } = Typography

const HomePage = () => {
  const features = [
    {
      icon: <CodeOutlined style={{ fontSize: '48px', color: '#1890ff' }} />,
      title: 'AI代码解释器',
      description: '智能解释Python代码逻辑，帮助理解复杂代码结构和设计思想'
    },
    {
      icon: <BugOutlined style={{ fontSize: '48px', color: '#f5222d' }} />,
      title: '潜在Bug检测',
      description: '识别代码中的潜在错误和边界条件问题，提前预防运行时错误'
    },
    {
      icon: <ThunderboltOutlined style={{ fontSize: '48px', color: '#52c41a' }} />,
      title: '性能优化建议',
      description: '提供代码性能优化方案，让您的代码更高效、更Pythonic'
    },
    {
      icon: <BookOutlined style={{ fontSize: '48px', color: '#722ed1' }} />,
      title: '最佳实践指导',
      description: '基于权威知识库，提供符合社区规范的代码风格建议'
    }
  ]

  return (
    <div className="home-page">
      {/* 主标题区域 */}
      <div className="hero-section">
        <Title level={1} className="hero-title">
          CodeWise AI
        </Title>
        <Title level={3} className="hero-subtitle">
          智能编程学习伙伴与代码审查员
        </Title>
        <Paragraph className="hero-description">
          基于大型语言模型的智能代码分析工具，为编程初学者和中级开发者提供即时的代码解释和深度的代码审查服务
        </Paragraph>
        <Space size="large">
          <Link to="/analysis">
            <Button type="primary" size="large">
              开始分析代码
            </Button>
          </Link>
          <Button size="large" href="#features">
            了解更多
          </Button>
        </Space>
      </div>

      {/* 功能特性区域 */}
      <div id="features" className="features-section">
        <Title level={2} className="section-title">
          核心功能
        </Title>
        <Row gutter={[24, 24]}>
          {features.map((feature, index) => (
            <Col xs={24} sm={12} lg={6} key={index}>
              <Card 
                className="feature-card"
                hoverable
                bordered={false}
              >
                <div className="feature-icon">
                  {feature.icon}
                </div>
                <Title level={4}>{feature.title}</Title>
                <Paragraph>{feature.description}</Paragraph>
              </Card>
            </Col>
          ))}
        </Row>
      </div>

      {/* 使用指南区域 */}
      <div className="guide-section">
        <Title level={2} className="section-title">
          使用指南
        </Title>
        <Row gutter={[24, 24]}>
          <Col xs={24} md={8}>
            <Card className="guide-card">
              <Title level={4}>1. 粘贴代码</Title>
              <Paragraph>
                将您的Python代码粘贴到代码编辑器中
              </Paragraph>
            </Card>
          </Col>
          <Col xs={24} md={8}>
            <Card className="guide-card">
              <Title level={4}>2. 选择分析类型</Title>
              <Paragraph>
                选择"代码解释"或"代码审查"功能
              </Paragraph>
            </Card>
          </Col>
          <Col xs={24} md={8}>
            <Card className="guide-card">
              <Title level={4}>3. 获取AI分析</Title>
              <Paragraph>
                获得详细的代码分析报告和改进建议
              </Paragraph>
            </Card>
          </Col>
        </Row>
      </div>
    </div>
  )
}

export default HomePage