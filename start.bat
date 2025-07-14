@echo off
chcp 65001 >nul
echo 🚀 启动 CodeWise AI 开发环境...

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装，请先安装Python 3.11+
    pause
    exit /b 1
)

REM 检查Node.js环境
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js未安装，请先安装Node.js 18+
    pause
    exit /b 1
)

REM 检查是否在conda环境中
where conda >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到conda，请先安装Anaconda或Miniconda并创建虚拟环境
    pause
    exit /b 1
)

REM 检查当前是否已激活conda环境
if "%CONDA_DEFAULT_ENV%"=="" (
    echo ⚠️  当前未激活conda虚拟环境，请先激活您的conda环境再运行本脚本
    pause
    exit /b 1
)

REM 安装Python依赖
echo 📦 安装Python依赖...
pip install -r requirements.txt

REM 检查环境变量文件
if not exist ".env" (
    echo ⚠️  未找到.env文件，复制示例配置...
    copy .env.example .env
    echo 请编辑.env文件并填入您的API密钥
)

REM 创建必要目录
if not exist "logs" mkdir logs
if not exist "data\vector_db" mkdir data\vector_db
if not exist "data\knowledge_base" mkdir data\knowledge_base

REM 安装前端依赖
echo 📦 安装前端依赖...
cd frontend
call npm install
cd ..

REM 启动后端服务
echo 🎯 启动后端服务...
start "CodeWise AI Backend" cmd /c "cd backend && python main.py"

REM 等待后端启动
echo ⏳ 等待后端服务启动...
timeout /t 10 /nobreak >nul

REM 启动前端服务
echo 🎨 启动前端服务...
cd frontend
start "CodeWise AI Frontend" cmd /c "npm run dev"
cd ..

echo 🎉 CodeWise AI 开发环境启动完成！
echo 📍 前端地址: http://localhost:3000
echo 📍 后端地址: http://localhost:8000
echo 📍 API文档: http://localhost:8000/docs
echo.
echo 按任意键退出...
pause >nul