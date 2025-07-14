"""
CodeWise AI 项目配置文件
负责人：组长
作用：管理项目的全局配置，包括API设置、数据库路径、模型参数等
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """项目全局配置类"""
    
    # API配置
    dashscope_api_key: str = Field(..., description="通义千问API密钥")
    debug: bool = Field(True, description="调试模式")
    host: str = Field("0.0.0.0", description="服务器主机地址")
    port: int = Field(8000, description="服务器端口")
    
    # 数据库配置
    vector_db_path: str = Field("./data/vector_db", description="向量数据库路径")
    knowledge_base_path: str = Field("./data/knowledge_base", description="知识库路径")
    
    # 模型配置
    model_name: str = Field("qwen-turbo", description="默认使用的LLM模型")
    max_tokens: int = Field(20000, description="最大token数量")
    temperature: float = Field(0.5, description="模型温度参数")
    
    # 代码分析配置
    max_code_length: int = Field(10000, description="最大代码长度限制")
    analysis_timeout: int = Field(30, description="分析超时时间（秒）")
    
    # CORS配置
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        description="允许的跨域源"
    )
    
    # 日志配置
    log_level: str = Field("INFO", description="日志级别")
    log_file: str = Field("./logs/codewise.log", description="日志文件路径")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 全局配置实例
settings = Settings()


def get_settings() -> Settings:
    """获取配置实例的工厂函数"""
    return settings