/**
 * 页头组件
 * 负责人：组员A
 * 作用：应用顶部导航栏，包含Logo、导航菜单和用户操作
 */

import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Layout, Menu, Typography, Space } from 'antd'
import { CodeOutlined, HomeOutlined, ExperimentOutlined } from '@ant-design/icons'

const { Header: AntHeader } = Layout
const { Title } = Typography

const Header = () => {
  const location = useLocation()

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: <Link to="/">首页</Link>
    },
    {
      key: '/analysis',
      icon: <ExperimentOutlined />,
      label: <Link to="/analysis">代码分析</Link>
    }
  ]

  return (
    <AntHeader className="app-header">
      <div className="header-content">
        <div className="logo-section">
          <Link to="/" className="logo-link">
            <Space>
              <CodeOutlined style={{ fontSize: '32px', color: '#1890ff' }} />
              <Title level={3} style={{ margin: 0, color: 'white' }}>
                CodeWise AI
              </Title>
            </Space>
          </Link>
        </div>
        
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[location.pathname]}
          items={menuItems}
          style={{ flex: 1, minWidth: 0 }}
        />
      </div>
    </AntHeader>
  )
}

export default Header