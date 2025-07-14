#!/bin/bash

# CodeWise AI 项目启动脚本
# 负责人：组员C
# 作用：一键启动开发环境，包括后端和前端服务

set -e

echo "🚀 启动 CodeWise AI 开发环境..."

# 检查Python环境
if ! command -v python &> /dev/null; then
    echo "❌ Python未安装，请先安装Python 3.11+"
    exit 1
fi

# 检查Node.js环境
if ! command -v node &> /dev/null; then
    echo "❌ Node.js未安装，请先安装Node.js 18+"
    exit 1
fi

# 创建Python虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建Python虚拟环境..."
    python -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活Python虚拟环境..."
source venv/bin/activate

# 安装Python依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  未找到.env文件，复制示例配置..."
    cp .env.example .env
    echo "请编辑.env文件并填入您的API密钥"
fi

# 创建必要目录
mkdir -p logs data/vector_db data/knowledge_base

# 安装前端依赖
echo "📦 安装前端依赖..."
cd frontend
npm install
cd ..

# 启动后端服务（后台运行）
echo "🎯 启动后端服务..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

# 等待后端启动
echo "⏳ 等待后端服务启动..."
sleep 10

# 检查后端是否启动成功
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ 后端服务启动成功"
else
    echo "❌ 后端服务启动失败"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# 启动前端服务
echo "🎨 启动前端服务..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "🎉 CodeWise AI 开发环境启动完成！"
echo "📍 前端地址: http://localhost:3000"
echo "📍 后端地址: http://localhost:8000"
echo "📍 API文档: http://localhost:8000/docs"

# 等待用户中断
echo "按 Ctrl+C 停止服务..."
trap 'echo "🛑 停止服务..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true; exit 0' INT
wait