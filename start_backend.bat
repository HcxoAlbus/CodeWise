@echo off
chcp 65001 >nul
echo 🚀 启动 CodeWise AI 后端服务...

REM 进入项目目录
cd /d "d:\sec_semester_code\Industrial_Training\codewise-ai"

@REM REM 检查虚拟环境
@REM if not exist "venv\Scripts\activate.bat" (
@REM     echo ❌ 虚拟环境不存在，正在创建...
@REM     python -m venv venv
@REM )

@REM REM 激活虚拟环境
@REM echo 🔧 激活虚拟环境...
@REM call venv\Scripts\activate.bat

@REM REM 检查Python版本
@REM echo 📋 检查Python环境...
@REM python --version
@REM if errorlevel 1 (
@REM     echo ❌ Python未正确安装或配置
@REM     pause
@REM     exit /b 1
@REM )

@REM REM 安装依赖
@REM echo 📦 安装Python依赖...
@REM pip install -r requirements.txt
@REM if errorlevel 1 (
@REM     echo ❌ 依赖安装失败
@REM     pause
@REM     exit /b 1
@REM )

REM 创建必要目录
echo 📁 创建必要目录...
if not exist "logs" mkdir logs
if not exist "data\vector_db" mkdir data\vector_db
if not exist "data\knowledge_base" mkdir data\knowledge_base

REM 检查环境配置
if not exist ".env" (
    echo ⚠️  .env文件不存在，复制示例配置...
    copy .env.example .env
    echo 请编辑.env文件并配置您的API密钥
    pause
)

REM 启动后端服务
echo 🎯 启动后端服务...
echo 如果出现错误，请查看详细信息...
python backend/main.py

echo.
echo 按任意键退出...
pause >nul