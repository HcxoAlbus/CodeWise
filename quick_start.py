"""
快速启动脚本 - 解决模块导入问题
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print(f"🔧 设置Python路径: {project_root}")
print(f"🐍 Python版本: {sys.version}")

# 现在导入并启动应用
try:
    print("📦 导入配置模块...")
    from config.settings import get_settings
    
    print("📦 导入FastAPI模块...")
    from backend.main import app
    
    print("🚀 启动服务器...")
    import uvicorn
    
    settings = get_settings()
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
    
except Exception as e:
    print(f"❌ 启动失败: {e}")
    import traceback
    traceback.print_exc()
    input("按Enter键退出...")