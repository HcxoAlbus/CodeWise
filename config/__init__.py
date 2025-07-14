"""
配置模块初始化
负责人：组长
作用：配置包的初始化文件
"""

from .settings import get_settings, Settings

__all__ = ["get_settings", "Settings"]