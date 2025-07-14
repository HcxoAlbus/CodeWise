"""
服务模块初始化
负责人：组长
作用：服务包的初始化文件
"""

# 移除直接导入，避免循环依赖
# 服务类应该在需要时直接从模块导入

__all__ = ["CodeExplainerService", "CodeReviewerService"]

# 使用延迟导入避免循环依赖
def get_code_explainer_service():
    from .code_explainer import CodeExplainerService
    return CodeExplainerService

def get_code_reviewer_service():
    from .code_reviewer import CodeReviewerService
    return CodeReviewerService