"""
简化的后端测试启动文件
用于快速测试和诊断启动问题
"""

print("🔍 开始诊断 CodeWise AI 后端...")

# 1. 测试基础Python导入
try:
    print("✅ 测试基础模块导入...")
    import os
    import sys
    from pathlib import Path
    print(f"   Python版本: {sys.version}")
    print(f"   当前工作目录: {os.getcwd()}")
except Exception as e:
    print(f"❌ 基础模块导入失败: {e}")
    exit(1)

# 2. 测试环境变量加载
try:
    print("✅ 测试环境变量...")
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if api_key:
        print(f"   API密钥已配置: {api_key[:8]}...")
    else:
        print("⚠️  API密钥未配置")
except Exception as e:
    print(f"❌ 环境变量加载失败: {e}")

# 3. 测试配置加载
try:
    print("✅ 测试配置加载...")
    from config.settings import get_settings
    settings = get_settings()
    print(f"   服务地址: {settings.host}:{settings.port}")
    print(f"   调试模式: {settings.debug}")
except Exception as e:
    print(f"❌ 配置加载失败: {e}")
    print("   可能的解决方案:")
    print("   - 检查.env文件是否存在")
    print("   - 确认pydantic-settings已安装")
    exit(1)

# 4. 测试FastAPI导入
try:
    print("✅ 测试FastAPI模块...")
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    print("   FastAPI模块导入成功")
except Exception as e:
    print(f"❌ FastAPI导入失败: {e}")
    exit(1)

# 5. 测试LangChain导入
try:
    print("✅ 测试LangChain模块...")
    from langchain.llms import LLMChain
    from langchain_community.llms import Tongyi
    print("   LangChain模块导入成功")
except Exception as e:
    print(f"⚠️  LangChain导入失败: {e}")
    print("   这可能影响AI功能，但不会阻止服务启动")

# 6. 创建简化的FastAPI应用
try:
    print("✅ 创建测试服务器...")
    app = FastAPI(title="CodeWise AI Test Server")
    
    @app.get("/")
    def root():
        return {"message": "CodeWise AI 测试服务器运行正常", "status": "ok"}
    
    @app.get("/health")
    def health():
        return {"status": "healthy", "service": "CodeWise AI Test"}
    
    print("   测试服务器创建成功")
except Exception as e:
    print(f"❌ 服务器创建失败: {e}")
    exit(1)

# 7. 启动服务器
try:
    print("🚀 启动测试服务器...")
    print(f"   访问地址: http://localhost:{settings.port}")
    print("   按 Ctrl+C 停止服务")
    
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="info"
    )
except Exception as e:
    print(f"❌ 服务器启动失败: {e}")
    print("   可能的原因:")
    print(f"   - 端口{settings.port}已被占用")
    print("   - 权限不足")
    print("   - 网络配置问题")