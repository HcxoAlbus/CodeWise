"""
应用中间件配置
负责人：组员C
作用：配置请求处理中间件，包括请求日志、性能监控、错误处理等
"""

import time
import logging
from typing import Callable
from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        
        # 记录请求开始
        logger.info(
            f"请求开始: {request.method} {request.url.path} "
            f"客户端: {request.client.host if request.client else 'unknown'}"
        )
        
        try:
            response = await call_next(request)
            
            # 计算处理时间
            process_time = time.time() - start_time
            
            # 记录请求完成
            logger.info(
                f"请求完成: {request.method} {request.url.path} "
                f"状态码: {response.status_code} "
                f"耗时: {process_time:.3f}s"
            )
            
            # 添加响应头
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"请求异常: {request.method} {request.url.path} "
                f"错误: {str(e)} "
                f"耗时: {process_time:.3f}s"
            )
            raise


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """性能监控中间件"""
    
    def __init__(self, app, slow_request_threshold: float = 5.0):
        super().__init__(app)
        self.slow_request_threshold = slow_request_threshold
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # 记录慢请求
        if process_time > self.slow_request_threshold:
            logger.warning(
                f"慢请求检测: {request.method} {request.url.path} "
                f"耗时: {process_time:.3f}s (阈值: {self.slow_request_threshold}s)"
            )
        
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """安全头中间件"""
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        
        # 添加安全头
        response.headers.update({
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        })
        
        return response


def setup_middleware(app):
    """
    设置应用中间件
    
    Args:
        app: FastAPI应用实例
    """
    
    # 添加性能监控中间件
    app.add_middleware(
        PerformanceMonitoringMiddleware,
        slow_request_threshold=5.0
    )
    
    # 添加请求日志中间件
    app.add_middleware(RequestLoggingMiddleware)
    
    # 添加安全头中间件
    app.add_middleware(SecurityHeadersMiddleware)
    
    logger.info("中间件配置完成")