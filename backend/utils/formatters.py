"""
响应格式化工具
负责人：组员C
作用：提供统一的API响应格式化功能
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


def format_analysis_result(
    result: Dict[str, Any], 
    analysis_type: str, 
    execution_time: float
) -> Dict[str, Any]:
    """
    格式化分析结果
    
    Args:
        result: 原始分析结果
        analysis_type: 分析类型
        execution_time: 执行时间
        
    Returns:
        格式化后的结果
    """
    formatted_result = {
        "timestamp": datetime.now().isoformat(),
        "analysis_type": analysis_type,
        "execution_time": round(execution_time, 3),
        "status": "success"
    }
    
    if analysis_type == "explain":
        formatted_result.update({
            "explanation": result.get("explanation", ""),
            "code_summary": result.get("summary", ""),
            "key_concepts": result.get("key_concepts", [])
        })
    elif analysis_type == "review":
        formatted_result.update({
            "overall_score": result.get("score", 0),
            "summary": result.get("summary", ""),
            "bugs": result.get("bugs", []),
            "style_issues": result.get("style_issues", []),
            "optimizations": result.get("optimizations", []),
            "lines_analyzed": result.get("lines_analyzed", 0)
        })
    
    return formatted_result


def format_error_response(
    error_message: str,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    格式化错误响应
    
    Args:
        error_message: 错误信息
        error_code: 错误代码
        details: 错误详情
        
    Returns:
        格式化的错误响应
    """
    error_response = {
        "timestamp": datetime.now().isoformat(),
        "status": "error",
        "detail": error_message
    }
    
    if error_code:
        error_response["error_code"] = error_code
    
    if details:
        error_response["details"] = details
    
    return error_response


def format_success_response(
    data: Dict[str, Any],
    message: str = "操作成功"
) -> Dict[str, Any]:
    """
    格式化成功响应
    
    Args:
        data: 响应数据
        message: 成功信息
        
    Returns:
        格式化的成功响应
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "status": "success",
        "message": message,
        "data": data
    }


def format_health_check_response(
    service_status: Dict[str, Any]
) -> Dict[str, Any]:
    """
    格式化健康检查响应
    
    Args:
        service_status: 服务状态信息
        
    Returns:
        格式化的健康检查响应
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "service": "CodeWise AI",
        "version": "1.0.0",
        "status": service_status.get("status", "unknown"),
        "services": service_status.get("services", {})
    }


def truncate_large_response(
    response: Dict[str, Any],
    max_length: int = 5000
) -> Dict[str, Any]:
    """
    截断过大的响应内容
    
    Args:
        response: 原始响应
        max_length: 最大长度限制
        
    Returns:
        截断后的响应
    """
    if not response:
        return response
    
    # 检查需要截断的字段
    fields_to_check = ["explanation", "summary", "detail"]
    
    for field in fields_to_check:
        if field in response and isinstance(response[field], str):
            if len(response[field]) > max_length:
                response[field] = response[field][:max_length - 3] + "..."
                response["truncated"] = True
    
    return response