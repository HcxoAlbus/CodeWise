/**
 * 页脚组件
 * 负责人：组员A
 * 作用：应用底部信息栏，包含版权信息和项目说明
 */

import React from 'react'
import { Layout, Typography, Space, Divider } from 'antd'
import { GithubOutlined, TeamOutlined } from '@ant-design/icons'

const { Footer: AntFooter } = Layout
const { Text, Link } = Typography

const Footer = () => {
  const currentYear = new Date().getFullYear()

  return (
    <AntFooter className="app-footer">
      <div className="footer-content">
        <Space split={<Divider type="vertical" />} size="large">
          <Text>
            © {currentYear} CodeWise AI - 智能编程学习伙伴
          </Text>
          <Space>
            <TeamOutlined />
            <Text>团队项目</Text>
          </Space>
          <Text type="secondary">
            基于大型语言模型的代码分析工具
          </Text>
        </Space>
      </div>
    </AntFooter>
  )
}

export default Footer