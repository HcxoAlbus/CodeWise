"""
CodeWise AI 应用模块初始化
负责人：组员B
作用：应用核心模块的初始化文件，定义应用级别的公共接口
"""

__version__ = "1.0.0"
__app_name__ = "CodeWise AI Application Layer"

# 导出主要的应用组件
from .application import CodeWiseApplication
from .middleware import setup_middleware
from .events import setup_event_handlers

__all__ = [
    "CodeWiseApplication",
    "setup_middleware", 
    "setup_event_handlers"
]