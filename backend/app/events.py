"""
应用事件处理器
负责人：组员C
作用：处理应用启动和关闭事件，管理资源的初始化和清理
"""

import logging
from typing import Dict, Any
from fastapi import FastAPI

from backend.app.application import get_application
from backend.core.logging_config import setup_logging
from config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def startup_event_handler():
    """应用启动事件处理"""
    try:
        logger.info("🚀 CodeWise AI 应用启动事件开始...")
        
        # 设置日志系统
        setup_logging()
        
        # 初始化应用
        app = get_application()
        await app.initialize()
        
        # 创建必要的目录
        import os
        os.makedirs(settings.vector_db_path, exist_ok=True)
        os.makedirs(settings.knowledge_base_path, exist_ok=True)
        os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)
        
        logger.info("✅ CodeWise AI 应用启动完成")
        
    except Exception as e:
        logger.error(f"❌ 应用启动失败: {str(e)}")
        raise


async def shutdown_event_handler():
    """应用关闭事件处理"""
    try:
        logger.info("🛑 CodeWise AI 应用关闭事件开始...")
        
        # 关闭应用
        app = get_application()
        await app.shutdown()
        
        logger.info("✅ CodeWise AI 应用关闭完成")
        
    except Exception as e:
        logger.error(f"❌ 应用关闭过程出错: {str(e)}")


def setup_event_handlers(app: FastAPI):
    """
    设置应用事件处理器
    
    Args:
        app: FastAPI应用实例
    """
    
    @app.on_event("startup")
    async def startup():
        """启动事件"""
        await startup_event_handler()
    
    @app.on_event("shutdown") 
    async def shutdown():
        """关闭事件"""
        await shutdown_event_handler()
    
    logger.info("事件处理器配置完成")