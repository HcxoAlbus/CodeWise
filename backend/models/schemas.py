"""
数据模式定义
负责人：组长
作用：定义API请求和响应的数据结构，使用Pydantic进行数据验证
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class AnalysisType(str, Enum):
    """分析类型枚举"""
    EXPLAIN = "explain"
    REVIEW = "review"


class CodeAnalysisRequest(BaseModel):
    """代码分析请求模型"""
    code: str = Field(..., min_length=1, max_length=10000, description="待分析的代码")
    language: str = Field(default="python", description="编程语言")
    analysis_type: AnalysisType = Field(..., description="分析类型")
    
    class Config:
        schema_extra = {
            "example": {
                "code": "def hello():\n    print('Hello, World!')",
                "language": "python",
                "analysis_type": "explain"
            }
        }


class CodeExplanationResponse(BaseModel):
    """代码解释响应模型"""
    explanation: str = Field(..., description="详细的代码解释")
    code_summary: str = Field(..., description="代码功能摘要")
    key_concepts: List[str] = Field(default=[], description="关键概念列表")
    execution_time: float = Field(..., description="分析耗时（秒）")
    
    class Config:
        schema_extra = {
            "example": {
                "explanation": "这是一个简单的函数定义...",
                "code_summary": "定义了一个打印问候语的函数",
                "key_concepts": ["函数定义", "print语句"],
                "execution_time": 1.23
            }
        }


class BugReport(BaseModel):
    """Bug报告模型"""
    line_number: Optional[int] = Field(None, description="问题所在行号")
    description: str = Field(..., description="Bug描述")
    severity: str = Field(default="medium", description="严重程度")
    suggestion: str = Field(..., description="修复建议")
    
    class Config:
        schema_extra = {
            "example": {
                "line_number": 5,
                "description": "可能存在除零错误",
                "severity": "high",
                "suggestion": "添加输入验证"
            }
        }


class StyleIssue(BaseModel):
    """代码风格问题模型"""
    line_number: Optional[int] = Field(None, description="问题所在行号")
    rule: str = Field(..., description="违反的规则")
    message: str = Field(..., description="问题描述")
    suggestion: str = Field(..., description="改进建议")
    
    class Config:
        schema_extra = {
            "example": {
                "line_number": 3,
                "rule": "E302",
                "message": "函数定义前应有两个空行",
                "suggestion": "在函数定义前添加空行"
            }
        }


class OptimizationSuggestion(BaseModel):
    """优化建议模型"""
    category: str = Field(..., description="优化类别")
    description: str = Field(..., description="优化描述")
    performance_impact: str = Field(..., description="性能影响说明")
    before_code: Optional[str] = Field(None, description="优化前代码")
    after_code: Optional[str] = Field(None, description="优化后代码")
    
    class Config:
        schema_extra = {
            "example": {
                "category": "性能优化",
                "description": "使用列表推导式替代循环",
                "performance_impact": "提升约30%的执行效率",
                "before_code": "result = []\nfor i in range(10):\n    result.append(i*2)",
                "after_code": "result = [i*2 for i in range(10)]"
            }
        }


class CodeReviewResponse(BaseModel):
    """代码审查响应模型"""
    overall_score: int = Field(..., ge=0, le=100, description="总体评分(0-100)")
    summary: str = Field(..., description="审查总结")
    bugs: List[BugReport] = Field(default=[], description="潜在Bug列表")
    style_issues: List[StyleIssue] = Field(default=[], description="代码风格问题列表")
    optimizations: List[OptimizationSuggestion] = Field(default=[], description="优化建议列表")
    execution_time: float = Field(..., description="分析耗时（秒）")
    lines_analyzed: int = Field(..., description="分析的代码行数")
    
    class Config:
        schema_extra = {
            "example": {
                "overall_score": 85,
                "summary": "代码质量良好，有少量改进空间",
                "bugs": [],
                "style_issues": [],
                "optimizations": [],
                "execution_time": 2.45,
                "lines_analyzed": 15
            }
        }


class ErrorResponse(BaseModel):
    """错误响应模型"""
    detail: str = Field(..., description="错误详情")
    error_code: Optional[str] = Field(None, description="错误代码")
    timestamp: Optional[str] = Field(None, description="错误时间戳")
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "代码分析失败",
                "error_code": "ANALYSIS_ERROR",
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }