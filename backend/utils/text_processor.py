"""
文本处理工具
负责人：组员C
作用：提供文本清理、格式化和预处理功能
"""

import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class TextProcessor:
    """文本处理工具类"""
    
    @staticmethod
    def clean_code(code: str) -> str:
        """
        清理代码文本
        
        Args:
            code: 原始代码
            
        Returns:
            清理后的代码
        """
        if not code:
            return ""
        
        # 移除多余的空行
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # 保留有内容的行和必要的空行
            if line.strip() or (cleaned_lines and cleaned_lines[-1].strip()):
                cleaned_lines.append(line.rstrip())
        
        # 移除末尾的空行
        while cleaned_lines and not cleaned_lines[-1].strip():
            cleaned_lines.pop()
        
        return '\n'.join(cleaned_lines)
    
    @staticmethod
    def extract_code_blocks(text: str) -> List[str]:
        """
        从文本中提取代码块
        
        Args:
            text: 包含代码块的文本
            
        Returns:
            代码块列表
        """
        # 匹配 ```python 或 ``` 包围的代码块
        pattern = r'```(?:python)?\s*\n(.*?)\n```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        return [match.strip() for match in matches]
    
    @staticmethod
    def count_code_lines(code: str) -> Dict[str, int]:
        """
        统计代码行数
        
        Args:
            code: 代码文本
            
        Returns:
            行数统计信息
        """
        if not code:
            return {"total": 0, "non_empty": 0, "comments": 0}
        
        lines = code.split('\n')
        total_lines = len(lines)
        non_empty_lines = 0
        comment_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped:
                non_empty_lines += 1
                if stripped.startswith('#'):
                    comment_lines += 1
        
        return {
            "total": total_lines,
            "non_empty": non_empty_lines,
            "comments": comment_lines,
            "code_only": non_empty_lines - comment_lines
        }
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 1000) -> str:
        """
        截断文本到指定长度
        
        Args:
            text: 原始文本
            max_length: 最大长度
            
        Returns:
            截断后的文本
        """
        if len(text) <= max_length:
            return text
        
        return text[:max_length - 3] + "..."
    
    @staticmethod
    def format_markdown_code(code: str, language: str = "python") -> str:
        """
        格式化为Markdown代码块
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            Markdown格式的代码块
        """
        return f"```{language}\n{code}\n```"