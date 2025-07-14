/**
 * 主应用组件
 * 负责人：组员A
 * 作用：应用的根组件，配置路由和整体布局
 */

import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { Layout } from 'antd'
import HomePage from './pages/HomePage'
import CodeAnalysisPage from './pages/CodeAnalysisPage'
import Header from './components/Header'
import Footer from './components/Footer'
import './styles/index.css'

const { Content } = Layout

function App() {
  return (
    <Layout className="app-layout">
      <Header />
      <Content className="app-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/analysis" element={<CodeAnalysisPage />} />
        </Routes>
      </Content>
      <Footer />
    </Layout>
  )
}

export default App