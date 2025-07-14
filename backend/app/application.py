"""
CodeWise AI 应用主类
负责人：组员B
作用：应用程序的主要业务逻辑协调器，管理各个服务组件的交互
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from backend.services.code_explainer import CodeExplainerService
from backend.services.code_reviewer import CodeReviewerService
from backend.tools.rag_tool import RAGTool
from backend.tools.flake8_tool import Flake8Tool
from config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class CodeWiseApplication:
    """CodeWise AI 应用主类"""
    
    def __init__(self):
        """初始化应用"""
        self.explainer_service: Optional[CodeExplainerService] = None
        self.reviewer_service: Optional[CodeReviewerService] = None
        self.rag_tool: Optional[RAGTool] = None
        self.flake8_tool: Optional[Flake8Tool] = None
        self.startup_time: Optional[datetime] = None
        self.is_initialized = False
    
    async def initialize(self):
        """异步初始化应用组件"""
        try:
            logger.info("开始初始化 CodeWise AI 应用...")
            
            # 初始化工具
            self.rag_tool = RAGTool()
            self.flake8_tool = Flake8Tool()
            
            # 初始化服务
            self.explainer_service = CodeExplainerService()
            self.reviewer_service = CodeReviewerService()
            
            self.startup_time = datetime.now()
            self.is_initialized = True
            
            logger.info("CodeWise AI 应用初始化完成")
            
        except Exception as e:
            logger.error(f"应用初始化失败: {str(e)}")
            raise
    
    async def shutdown(self):
        """应用关闭清理"""
        try:
            logger.info("开始关闭 CodeWise AI 应用...")
            
            # 清理资源
            self.explainer_service = None
            self.reviewer_service = None
            self.rag_tool = None
            self.flake8_tool = None
            
            self.is_initialized = False
            
            logger.info("CodeWise AI 应用已关闭")
            
        except Exception as e:
            logger.error(f"应用关闭过程出错: {str(e)}")
    
    def get_application_info(self) -> Dict[str, Any]:
        """获取应用信息"""
        return {
            "name": "CodeWise AI",
            "version": "1.0.0",
            "status": "running" if self.is_initialized else "stopped",
            "startup_time": self.startup_time.isoformat() if self.startup_time else None,
            "services": {
                "code_explainer": bool(self.explainer_service),
                "code_reviewer": bool(self.reviewer_service),
                "rag_tool": bool(self.rag_tool),
                "flake8_tool": bool(self.flake8_tool)
            }
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """应用健康检查"""
        if not self.is_initialized:
            return {
                "status": "unhealthy",
                "reason": "应用未初始化"
            }
        
        health_status = {
            "status": "healthy",
            "services": {}
        }
        
        try:
            # 检查代码解释服务
            if self.explainer_service:
                explainer_health = await self.explainer_service.health_check()
                health_status["services"]["explainer"] = "healthy" if explainer_health else "unhealthy"
            
            # 检查代码审查服务
            if self.reviewer_service:
                reviewer_health = await self.reviewer_service.health_check()
                health_status["services"]["reviewer"] = "healthy" if reviewer_health else "unhealthy"
            
            # 检查RAG工具
            if self.rag_tool:
                rag_stats = self.rag_tool.get_knowledge_stats()
                health_status["services"]["rag"] = "healthy" if rag_stats.get("status") == "可用" else "unhealthy"
            
            return health_status
            
        except Exception as e:
            logger.error(f"健康检查失败: {str(e)}")
            return {
                "status": "unhealthy",
                "reason": str(e)
            }


# 全局应用实例
_app_instance: Optional[CodeWiseApplication] = None


def get_application() -> CodeWiseApplication:
    """获取应用实例（单例模式）"""
    global _app_instance
    if _app_instance is None:
        _app_instance = CodeWiseApplication()
    return _app_instance