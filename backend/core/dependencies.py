"""
依赖注入配置
负责人：组长
作用：管理服务依赖，提供单例模式的服务实例
"""

from functools import lru_cache
from backend.services.code_explainer import CodeExplainerService
from backend.services.code_reviewer import CodeReviewerService


@lru_cache()
def get_code_explainer() -> CodeExplainerService:
    """
    获取代码解释服务单例实例
    
    Returns:
        CodeExplainerService: 代码解释服务实例
    """
    return CodeExplainerService()


@lru_cache()
def get_code_reviewer() -> CodeReviewerService:
    """
    获取代码审查服务单例实例
    
    Returns:
        CodeReviewerService: 代码审查服务实例
    """
    return CodeReviewerService()