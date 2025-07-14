"""
CodeWise AI 后端主应用入口
负责人：组长
作用：FastAPI应用的主入口，配置路由、中间件、CORS等
"""

# 导入FastAPI框架的核心类和异常处理相关模块
from fastapi import FastAPI, HTTPException
# 导入CORS中间件，用于跨域资源共享
from fastapi.middleware.cors import CORSMiddleware
# 导入JSON响应类，用于自定义返回内容
from fastapi.responses import JSONResponse
# 导入uvicorn服务器，用于本地开发启动服务
import uvicorn
# 导入日志模块，用于记录日志信息
import logging
# 导入异步上下文管理器，用于管理应用生命周期
from contextlib import asynccontextmanager

# 导入自定义的配置获取函数
from config.settings import get_settings
# 导入API路由对象
from backend.api.routes import api_router
# 导入日志配置函数
from backend.core.logging_config import setup_logging

# 获取项目的配置信息（如端口、CORS等）
settings = get_settings()

# 定义FastAPI应用的生命周期管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 应用启动时执行的代码
    setup_logging()  # 配置日志
    logging.info("CodeWise AI 后端服务启动")  # 记录启动日志
    
    # 可以在这里初始化向量数据库等资源（如有需要）
    # await init_vector_db()
    
    yield  # 应用运行期间
    
    # 应用关闭时执行的代码
    logging.info("CodeWise AI 后端服务关闭")  # 记录关闭日志

# 创建FastAPI应用实例，配置基本信息和生命周期
app = FastAPI(
    title="CodeWise AI API",  # 文档标题
    description="智能编程学习伙伴与代码审查员的后端API",  # 文档描述
    version="1.0.0",  # 版本号
    docs_url="/docs",  # 文档路径
    redoc_url="/redoc",  # Redoc文档路径
    lifespan=lifespan  # 生命周期管理
)

# 添加CORS中间件，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # 允许的前端域名
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

# 定义全局异常处理器，捕获未处理的异常
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理"""
    logging.error(f"未处理的异常: {str(exc)}")  # 记录异常日志
    return JSONResponse(
        status_code=500,  # 返回500错误
        content={"detail": "内部服务器错误"}  # 返回错误信息
    )

# 健康检查接口，用于检测服务是否正常
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": "CodeWise AI"}

# 根路径接口，返回欢迎信息和文档入口
@app.get("/")
async def root():
    """根路径欢迎信息"""
    return {
        "message": "欢迎使用 CodeWise AI API",
        "docs": "/docs",
        "health": "/health"
    }

# 注册API路由，将所有业务接口挂载到/api/v1路径下
app.include_router(api_router, prefix="/api/v1")

# 如果直接运行本文件，则启动开发服务器
if __name__ == "__main__":
    # 使用uvicorn启动FastAPI应用
    uvicorn.run(
        "main:app",  # 应用入口
        host=settings.host,  # 监听地址
        port=settings.port,  # 监听端口
        reload=settings.debug,  # 是否自动重载（开发环境用）
        log_level=settings.log_level.lower()  # 日志级别
    )