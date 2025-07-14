"""
Flake8代码静态分析工具
负责人：组员C
作用：封装flake8工具为LangChain Tool，用于代码风格和语法检查
"""

import subprocess
import tempfile
import os
import logging
from typing import Dict, List, Any
from langchain.tools import BaseTool
from pydantic import Field

logger = logging.getLogger(__name__)


class Flake8Tool(BaseTool):
    """Flake8静态分析工具类"""
    
    name: str = "flake8_analyzer"
    description: str = """
    使用flake8对Python代码进行静态分析，检查代码风格和潜在语法问题。
    输入：Python代码字符串
    输出：flake8分析报告，包含行号、错误类型和错误描述
    """
    
    def _run(self, code: str) -> str:
        """
        运行flake8分析
        
        Args:
            code: 待分析的Python代码
            
        Returns:
            flake8分析结果
        """
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # 运行flake8命令
                result = subprocess.run(
                    ['flake8', '--max-line-length=88', '--ignore=E203,W503', temp_file],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # 处理flake8输出
                if result.returncode == 0:
                    return "✅ 代码风格检查通过，未发现问题"
                else:
                    return self._format_flake8_output(result.stdout, temp_file)
                    
            finally:
                # 清理临时文件
                os.unlink(temp_file)
                
        except subprocess.TimeoutExpired:
            logger.error("Flake8分析超时")
            return "❌ 代码分析超时"
        except FileNotFoundError:
            logger.error("flake8命令未找到，请确保已安装flake8")
            return "❌ flake8工具未安装"
        except Exception as e:
            logger.error(f"Flake8分析出错: {str(e)}")
            return f"❌ 分析过程出错: {str(e)}"
    
    async def _arun(self, code: str) -> str:
        """异步版本的运行方法"""
        return self._run(code)
    
    def _format_flake8_output(self, output: str, temp_file: str) -> str:
        """
        格式化flake8输出结果
        
        Args:
            output: flake8原始输出
            temp_file: 临时文件路径
            
        Returns:
            格式化后的分析报告
        """
        if not output.strip():
            return "✅ 代码风格检查通过"
        
        lines = output.strip().split('\n')
        issues = []
        
        for line in lines:
            if temp_file in line:
                # 解析flake8输出格式: filepath:line:col: code message
                parts = line.replace(temp_file + ':', '').split(':', 3)
                if len(parts) >= 3:
                    line_num = parts[0]
                    col_num = parts[1]
                    error_code_and_msg = parts[2].strip()
                    
                    # 分离错误代码和消息
                    if ' ' in error_code_and_msg:
                        error_code, message = error_code_and_msg.split(' ', 1)
                    else:
                        error_code = error_code_and_msg
                        message = ""
                    
                    # 获取错误类型描述
                    error_type = self._get_error_type(error_code)
                    
                    issues.append({
                        'line': line_num,
                        'column': col_num,
                        'code': error_code,
                        'type': error_type,
                        'message': message
                    })
        
        return self._create_analysis_report(issues)
    
    def _get_error_type(self, error_code: str) -> str:
        """
        根据错误代码获取错误类型描述
        
        Args:
            error_code: flake8错误代码
            
        Returns:
            错误类型描述
        """
        if error_code.startswith('E'):
            return "语法/缩进错误"
        elif error_code.startswith('W'):
            return "代码风格警告"
        elif error_code.startswith('F'):
            return "逻辑错误"
        elif error_code.startswith('C'):
            return "复杂度问题"
        elif error_code.startswith('N'):
            return "命名规范"
        else:
            return "其他问题"
    
    def _create_analysis_report(self, issues: List[Dict]) -> str:
        """
        创建格式化的分析报告
        
        Args:
            issues: 问题列表
            
        Returns:
            格式化的报告
        """
        if not issues:
            return "✅ 代码风格检查通过"
        
        report = f"📋 发现 {len(issues)} 个代码风格问题：\n\n"
        
        # 按错误类型分组
        by_type = {}
        for issue in issues:
            error_type = issue['type']
            if error_type not in by_type:
                by_type[error_type] = []
            by_type[error_type].append(issue)
        
        # 生成报告
        for error_type, type_issues in by_type.items():
            report += f"🔸 {error_type} ({len(type_issues)}个):\n"
            for issue in type_issues:
                report += f"  • 第{issue['line']}行: {issue['code']} - {issue['message']}\n"
            report += "\n"
        
        # 添加改进建议
        report += "💡 改进建议:\n"
        report += "- 遵循PEP 8代码风格规范\n"
        report += "- 保持一致的缩进和空格使用\n"
        report += "- 注意行长度限制\n"
        
        return report


def get_flake8_tool() -> Flake8Tool:
    """获取Flake8工具实例"""
    return Flake8Tool()