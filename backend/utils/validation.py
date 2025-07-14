"""
输入验证工具
负责人：组员C
作用：提供输入数据的验证和清理功能
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

# 支持的编程语言列表
SUPPORTED_LANGUAGES = ["python"]

# 最大代码长度限制
MAX_CODE_LENGTH = 10000


def validate_code_input(code: str) -> Tuple[bool, Optional[str]]:
    """
    验证代码输入
    
    Args:
        code: 待验证的代码
        
    Returns:
        Tuple[bool, Optional[str]]: (是否有效, 错误信息)
    """
    if not code:
        return False, "代码不能为空"
    
    if not isinstance(code, str):
        return False, "代码必须是字符串类型"
    
    if len(code.strip()) == 0:
        return False, "代码不能只包含空白字符"
    
    if len(code) > MAX_CODE_LENGTH:
        return False, f"代码长度不能超过 {MAX_CODE_LENGTH} 字符"
    
    # 检查是否包含潜在的恶意代码
    malicious_patterns = [
        r'import\s+os',
        r'import\s+subprocess',
        r'import\s+sys',
        r'exec\s*\(',
        r'eval\s*\(',
        r'__import__\s*\(',
        r'open\s*\(',
        r'file\s*\(',
    ]
    
    for pattern in malicious_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            logger.warning(f"检测到潜在风险代码: {pattern}")
            # 注意：这里只是警告，不阻止分析
            break
    
    return True, None


def validate_language(language: str) -> Tuple[bool, Optional[str]]:
    """
    验证编程语言
    
    Args:
        language: 编程语言名称
        
    Returns:
        Tuple[bool, Optional[str]]: (是否有效, 错误信息)
    """
    if not language:
        return False, "编程语言不能为空"
    
    if not isinstance(language, str):
        return False, "编程语言必须是字符串类型"
    
    language = language.lower().strip()
    
    if language not in SUPPORTED_LANGUAGES:
        return False, f"暂不支持 {language} 语言，当前支持: {', '.join(SUPPORTED_LANGUAGES)}"
    
    return True, None


def validate_analysis_type(analysis_type: str) -> Tuple[bool, Optional[str]]:
    """
    验证分析类型
    
    Args:
        analysis_type: 分析类型
        
    Returns:
        Tuple[bool, Optional[str]]: (是否有效, 错误信息)
    """
    valid_types = ["explain", "review"]
    
    if not analysis_type:
        return False, "分析类型不能为空"
    
    if analysis_type not in valid_types:
        return False, f"无效的分析类型: {analysis_type}，支持的类型: {', '.join(valid_types)}"
    
    return True, None


def sanitize_code(code: str) -> str:
    """
    清理代码输入
    
    Args:
        code: 原始代码
        
    Returns:
        清理后的代码
    """
    if not code:
        return ""
    
    # 移除BOM标记
    if code.startswith('\ufeff'):
        code = code[1:]
    
    # 统一换行符
    code = code.replace('\r\n', '\n').replace('\r', '\n')
    
    # 移除末尾空白
    code = code.rstrip()
    
    return code


def validate_request_payload(payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    验证完整的请求载荷
    
    Args:
        payload: 请求数据
        
    Returns:
        Tuple[bool, List[str]]: (是否有效, 错误信息列表)
    """
    errors = []
    
    # 检查必需字段
    required_fields = ["code", "language", "analysis_type"]
    for field in required_fields:
        if field not in payload:
            errors.append(f"缺少必需字段: {field}")
    
    if errors:
        return False, errors
    
    # 验证代码
    code_valid, code_error = validate_code_input(payload["code"])
    if not code_valid:
        errors.append(f"代码验证失败: {code_error}")
    
    # 验证语言
    lang_valid, lang_error = validate_language(payload["language"])
    if not lang_valid:
        errors.append(f"语言验证失败: {lang_error}")
    
    # 验证分析类型
    type_valid, type_error = validate_analysis_type(payload["analysis_type"])
    if not type_valid:
        errors.append(f"分析类型验证失败: {type_error}")
    
    return len(errors) == 0, errors