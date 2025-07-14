"""
代码分析工具
负责人：组员C
作用：提供代码结构分析和语法检查功能
"""

import ast
import keyword
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class CodeAnalyzer:
    """代码分析工具类"""
    
    @staticmethod
    def parse_python_code(code: str) -> Optional[ast.AST]:
        """
        解析Python代码为AST
        
        Args:
            code: Python代码
            
        Returns:
            AST对象或None（如果解析失败）
        """
        try:
            return ast.parse(code)
        except SyntaxError as e:
            logger.warning(f"代码语法错误: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"代码解析失败: {str(e)}")
            return None
    
    @staticmethod
    def extract_functions(code: str) -> List[Dict[str, Any]]:
        """
        提取代码中的函数定义
        
        Args:
            code: Python代码
            
        Returns:
            函数信息列表
        """
        functions = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_info = {
                        "name": node.name,
                        "line_number": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "has_docstring": ast.get_docstring(node) is not None,
                        "is_async": False
                    }
                    functions.append(func_info)
                elif isinstance(node, ast.AsyncFunctionDef):
                    func_info = {
                        "name": node.name,
                        "line_number": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "has_docstring": ast.get_docstring(node) is not None,
                        "is_async": True
                    }
                    functions.append(func_info)
                    
        except Exception as e:
            logger.error(f"提取函数失败: {str(e)}")
        
        return functions
    
    @staticmethod
    def extract_classes(code: str) -> List[Dict[str, Any]]:
        """
        提取代码中的类定义
        
        Args:
            code: Python代码
            
        Returns:
            类信息列表
        """
        classes = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = []
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            methods.append(item.name)
                    
                    class_info = {
                        "name": node.name,
                        "line_number": node.lineno,
                        "methods": methods,
                        "has_docstring": ast.get_docstring(node) is not None,
                        "base_classes": [base.id if isinstance(base, ast.Name) else str(base) 
                                       for base in node.bases]
                    }
                    classes.append(class_info)
                    
        except Exception as e:
            logger.error(f"提取类失败: {str(e)}")
        
        return classes
    
    @staticmethod
    def extract_imports(code: str) -> List[Dict[str, Any]]:
        """
        提取代码中的导入语句
        
        Args:
            code: Python代码
            
        Returns:
            导入信息列表
        """
        imports = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({
                            "type": "import",
                            "module": alias.name,
                            "alias": alias.asname,
                            "line_number": node.lineno
                        })
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        imports.append({
                            "type": "from_import",
                            "module": node.module,
                            "name": alias.name,
                            "alias": alias.asname,
                            "line_number": node.lineno
                        })
                        
        except Exception as e:
            logger.error(f"提取导入失败: {str(e)}")
        
        return imports
    
    @staticmethod
    def check_syntax_errors(code: str) -> List[Dict[str, Any]]:
        """
        检查代码语法错误
        
        Args:
            code: Python代码
            
        Returns:
            语法错误列表
        """
        errors = []
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append({
                "type": "SyntaxError",
                "message": str(e.msg),
                "line_number": e.lineno,
                "column": e.offset,
                "text": e.text.strip() if e.text else ""
            })
        except Exception as e:
            errors.append({
                "type": "ParseError",
                "message": str(e),
                "line_number": None,
                "column": None,
                "text": ""
            })
        
        return errors
    
    @staticmethod
    def calculate_complexity(code: str) -> Dict[str, int]:
        """
        计算代码复杂度
        
        Args:
            code: Python代码
            
        Returns:
            复杂度指标
        """
        try:
            tree = ast.parse(code)
            
            # 简单的复杂度指标
            complexity = {
                "functions": 0,
                "classes": 0,
                "if_statements": 0,
                "loops": 0,
                "try_except": 0
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity["functions"] += 1
                elif isinstance(node, ast.ClassDef):
                    complexity["classes"] += 1
                elif isinstance(node, ast.If):
                    complexity["if_statements"] += 1
                elif isinstance(node, (ast.For, ast.While)):
                    complexity["loops"] += 1
                elif isinstance(node, ast.Try):
                    complexity["try_except"] += 1
            
            return complexity
            
        except Exception as e:
            logger.error(f"复杂度计算失败: {str(e)}")
            return {"error": str(e)}