"""
详细诊断脚本 - 检查所有可能的问题
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("🔍 CodeWise AI 详细诊断")
print("=" * 50)

# 1. 检查基础环境
print("1️⃣ 检查基础环境...")
print(f"   Python版本: {sys.version}")
print(f"   项目根目录: {project_root}")
print(f"   当前工作目录: {os.getcwd()}")
print(f"   Python路径: {sys.path[:3]}...")

# 2. 检查必要文件
print("\n2️⃣ 检查必要文件...")
required_files = [
    ".env",
    "config/__init__.py",
    "config/settings.py",
    "backend/__init__.py",
    "backend/main.py"
]

for file_path in required_files:
    full_path = project_root / file_path
    status = "✅" if full_path.exists() else "❌"
    print(f"   {status} {file_path}")

# 3. 检查Python包导入
print("\n3️⃣ 检查Python包导入...")
packages_to_test = [
    ("pydantic", "pydantic"),
    ("pydantic_settings", "pydantic_settings"),
    ("fastapi", "fastapi"),
    ("uvicorn", "uvicorn"),
    ("python-dotenv", "dotenv"),
    ("langchain", "langchain"),
    ("langchain-community", "langchain_community"),
]

for package_name, import_name in packages_to_test:
    try:
        __import__(import_name)
        print(f"   ✅ {package_name}")
    except ImportError as e:
        print(f"   ❌ {package_name}: {e}")

# 4. 测试配置导入
print("\n4️⃣ 测试配置导入...")
try:
    from config.settings import get_settings
    settings = get_settings()
    print("   ✅ 配置模块导入成功")
    print(f"   📍 服务地址: {settings.host}:{settings.port}")
    print(f"   🔧 调试模式: {settings.debug}")
    
    # 检查API密钥
    if hasattr(settings, 'dashscope_api_key') and settings.dashscope_api_key:
        masked_key = settings.dashscope_api_key[:8] + "..." if len(settings.dashscope_api_key) > 8 else "短密钥"
        print(f"   🔑 API密钥: {masked_key}")
    else:
        print("   ⚠️  API密钥未配置或为空")
        
except Exception as e:
    print(f"   ❌ 配置导入失败: {e}")
    import traceback
    traceback.print_exc()

# 5. 测试FastAPI应用导入
print("\n5️⃣ 测试FastAPI应用导入...")
try:
    from backend.main import app
    print("   ✅ FastAPI应用导入成功")
except Exception as e:
    print(f"   ❌ FastAPI应用导入失败: {e}")
    import traceback
    traceback.print_exc()

# 6. 尝试启动服务器
print("\n6️⃣ 尝试启动服务器...")
try:
    if 'app' in locals() and 'settings' in locals():
        print("   🚀 准备启动服务器...")
        print(f"   📍 访问地址: http://{settings.host}:{settings.port}")
        print("   💡 按 Ctrl+C 停止服务")
        
        import uvicorn
        uvicorn.run(
            app,
            host=settings.host,
            port=settings.port,
            log_level="info"
        )
    else:
        print("   ❌ 无法启动: 应用或配置导入失败")
        
except Exception as e:
    print(f"   ❌ 服务器启动失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("诊断完成！如果有错误，请根据上述信息进行修复。")