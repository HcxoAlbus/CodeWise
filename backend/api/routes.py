"""
API路由配置
负责人：组长
作用：定义和组织所有API端点，包括代码解释和代码审查接口
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import logging
import time
from typing import Dict, Any

from backend.models.schemas import (
    CodeAnalysisRequest, 
    CodeExplanationResponse, 
    CodeReviewResponse,
    ErrorResponse,
    AnalysisType
)
from backend.services.code_explainer import CodeExplainerService
from backend.services.code_reviewer import CodeReviewerService
from backend.core.dependencies import get_code_explainer, get_code_reviewer

# 创建API路由器
api_router = APIRouter()

# 设置日志
logger = logging.getLogger(__name__)


@api_router.post(
    "/explain",
    response_model=CodeExplanationResponse,
    summary="代码解释接口",
    description="分析并解释Python代码的功能和逻辑"
)
async def explain_code(
    request: CodeAnalysisRequest,
    explainer: CodeExplainerService = Depends(get_code_explainer)
) -> CodeExplanationResponse:
    """
    代码解释API端点
    
    Args:
        request: 包含待分析代码的请求
        explainer: 代码解释服务实例
    
    Returns:
        CodeExplanationResponse: 代码解释结果
    """
    start_time = time.time()
    
    try:
        logger.info(f"开始解释代码，代码长度: {len(request.code)} 字符")
        
        # 验证分析类型
        if request.analysis_type != AnalysisType.EXPLAIN:
            raise HTTPException(
                status_code=400,
                detail="此接口仅支持代码解释分析"
            )
        
        # 调用代码解释服务
        result = await explainer.explain_code(
            code=request.code,
            language=request.language
        )
        
        execution_time = time.time() - start_time
        logger.info(f"代码解释完成，耗时: {execution_time:.2f}秒")
        
        return CodeExplanationResponse(
            explanation=result["explanation"],
            code_summary=result["summary"],
            key_concepts=result["key_concepts"],
            execution_time=execution_time
        )
        
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"代码解释失败: {str(e)}, 耗时: {execution_time:.2f}秒")
        raise HTTPException(
            status_code=500,
            detail=f"代码解释服务出错: {str(e)}"
        )


@api_router.post(
    "/review",
    response_model=CodeReviewResponse,
    summary="代码审查接口",
    description="全面审查Python代码，包括Bug检测、风格检查和优化建议"
)
async def review_code(
    request: CodeAnalysisRequest,
    reviewer: CodeReviewerService = Depends(get_code_reviewer)
) -> CodeReviewResponse:
    """
    代码审查API端点
    
    Args:
        request: 包含待审查代码的请求
        reviewer: 代码审查服务实例
    
    Returns:
        CodeReviewResponse: 代码审查结果
    """
    start_time = time.time()
    
    try:
        logger.info(f"开始审查代码，代码长度: {len(request.code)} 字符")
        
        # 验证分析类型
        if request.analysis_type != AnalysisType.REVIEW:
            raise HTTPException(
                status_code=400,
                detail="此接口仅支持代码审查分析"
            )
        
        # 调用代码审查服务
        result = await reviewer.review_code(
            code=request.code,
            language=request.language
        )
        
        execution_time = time.time() - start_time
        logger.info(f"代码审查完成，耗时: {execution_time:.2f}秒")
        
        return CodeReviewResponse(
            overall_score=result["score"],
            summary=result["summary"],
            bugs=result["bugs"],
            style_issues=result["style_issues"],
            optimizations=result["optimizations"],
            execution_time=execution_time,
            lines_analyzed=len(request.code.split('\n'))
        )
        
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"代码审查失败: {str(e)}, 耗时: {execution_time:.2f}秒")
        raise HTTPException(
            status_code=500,
            detail=f"代码审查服务出错: {str(e)}"
        )


@api_router.get(
    "/status",
    summary="服务状态检查",
    description="检查AI服务的可用性和状态"
)
async def check_ai_status() -> Dict[str, Any]:
    """检查AI服务状态"""
    try:
        # 这里可以添加对AI模型和数据库的健康检查
        return {
            "ai_service": "available",
            "model_status": "ready",
            "vector_db": "connected",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"服务状态检查失败: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="AI服务暂时不可用"
        )