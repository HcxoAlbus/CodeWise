"""
核心模块初始化
负责人：组长
作用：核心功能包的初始化文件
"""

# 只导入不会产生循环依赖的模块
from .logging_config import setup_logging

# 不要在这里导入 dependencies，因为它会导致循环导入
# dependencies 模块应该单独导入使用

__all__ = ["setup_logging"]