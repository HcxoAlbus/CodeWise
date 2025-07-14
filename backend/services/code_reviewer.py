"""
代码审查服务
负责人：组长
作用：基于LangChain Agent实现的智能代码审查员，集成flake8工具和RAG知识库
"""

import asyncio
import logging
import json
from typing import Dict, List, Any
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms import Tongyi

from config.settings import get_settings
from backend.tools.flake8_tool import Flake8Tool
from backend.tools.rag_tool import RAGTool
from backend.core.prompts import CODE_REVIEW_PROMPT
from backend.models.schemas import BugReport, StyleIssue, OptimizationSuggestion

logger = logging.getLogger(__name__)
settings = get_settings()


class CodeReviewerService:
    """代码审查服务类"""
    
    def __init__(self):
        """初始化代码审查服务"""
        self.llm = None
        self.tools = []
        self.agent_executor = None
        self._init_agent()
    
    def _init_agent(self):
        """初始化Agent和工具"""
        try:
            # 初始化通义千问模型
            self.llm = Tongyi(
                dashscope_api_key=settings.dashscope_api_key,
                model_name=settings.model_name,
                temperature=settings.temperature,
                max_tokens=settings.max_tokens
            )
            
            # 初始化工具
            self.tools = [
                Flake8Tool(),
                RAGTool()
            ]
            
            # 创建代码审查提示模板
            prompt = ChatPromptTemplate.from_template(CODE_REVIEW_PROMPT)
            
            # 创建工具调用代理
            agent = create_tool_calling_agent(
                llm=self.llm,
                tools=self.tools,
                prompt=prompt
            )
            
            # 创建代理执行器
            self.agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True if settings.debug else False,
                max_iterations=5,
                handle_parsing_errors=True
            )
            
            logger.info("代码审查服务初始化成功")
            
        except Exception as e:
            logger.error(f"代码审查服务初始化失败: {str(e)}")
            raise
    
    async def review_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        全面审查代码
        
        Args:
            code: 待审查的代码
            language: 编程语言
            
        Returns:
            Dict包含审查结果
        """
        try:
            logger.info(f"开始审查 {language} 代码")
            
            # 准备Agent输入
            agent_input = {
                "code": code,
                "language": language,
                "task": "进行全面的代码审查，包括Bug检测、风格检查和优化建议"
            }
            
            # 异步执行Agent
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.agent_executor.invoke(agent_input)
            )
            
            # 解析Agent响应
            result = self._parse_review_response(response["output"])
            
            logger.info("代码审查完成")
            return result
            
        except Exception as e:
            logger.error(f"代码审查过程出错: {str(e)}")
            raise
    
    def _parse_review_response(self, response: str) -> Dict[str, Any]:
        """
        解析Agent的审查响应
        
        Args:
            response: Agent原始响应
            
        Returns:
            结构化的审查结果
        """
        try:
            # 尝试解析JSON格式的响应
            if response.strip().startswith('{'):
                parsed = json.loads(response)
                return self._format_review_result(parsed)
            
            # 如果不是JSON格式，使用文本解析
            return self._parse_text_response(response)
            
        except Exception as e:
            logger.error(f"解析审查响应失败: {str(e)}")
            return self._create_fallback_result(response)
    
    def _format_review_result(self, parsed_data: Dict) -> Dict[str, Any]:
        """格式化解析后的审查结果"""
        return {
            "score": parsed_data.get("score", 75),
            "summary": parsed_data.get("summary", "代码审查已完成"),
            "bugs": [
                BugReport(**bug) for bug in parsed_data.get("bugs", [])
            ],
            "style_issues": [
                StyleIssue(**issue) for issue in parsed_data.get("style_issues", [])
            ],
            "optimizations": [
                OptimizationSuggestion(**opt) for opt in parsed_data.get("optimizations", [])
            ]
        }
    
    def _parse_text_response(self, response: str) -> Dict[str, Any]:
        """解析文本格式的响应"""
        # 简化的文本解析逻辑
        lines = response.split('\n')
        
        bugs = []
        style_issues = []
        optimizations = []
        
        # 基本的文本解析（在实际项目中需要更复杂的解析逻辑）
        current_section = None
        for line in lines:
            line = line.strip()
            if "bug" in line.lower() or "错误" in line:
                current_section = "bugs"
            elif "style" in line.lower() or "风格" in line:
                current_section = "style"
            elif "优化" in line or "optimization" in line.lower():
                current_section = "optimization"
        
        return {
            "score": 75,  # 默认分数
            "summary": "代码审查已完成，请查看详细报告",
            "bugs": bugs,
            "style_issues": style_issues,
            "optimizations": optimizations
        }
    
    def _create_fallback_result(self, response: str) -> Dict[str, Any]:
        """创建备用审查结果"""
        return {
            "score": 70,
            "summary": f"代码审查完成。{response[:200]}...",
            "bugs": [],
            "style_issues": [],
            "optimizations": []
        }
    
    async def health_check(self) -> bool:
        """
        服务健康检查
        
        Returns:
            服务是否正常
        """
        try:
            test_code = "def hello():\n    print('Hello')"
            result = await self.review_code(test_code)
            return bool(result.get("summary"))
        except Exception:
            return False