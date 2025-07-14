"""
代码解释服务
负责人：组长
作用：基于LangChain实现的AI代码解释器，使用通义千问模型解释Python代码
"""

import asyncio  # 导入异步IO库，用于异步操作
import logging  # 导入日志库，用于记录日志信息
from typing import Dict, List, Any  # 导入类型注解，用于类型提示
from langchain.chains import LLMChain  # 导入LangChain的LLMChain，用于构建大模型链
from langchain.prompts import PromptTemplate  # 导入提示模板，用于构建大模型输入模板
from langchain_community.llms import Tongyi  # 导入通义千问模型的LangChain适配器

from config.settings import get_settings  # 导入配置获取函数，用于获取项目配置
from backend.core.prompts import CODE_EXPLANATION_PROMPT  # 导入代码解释提示词模板

logger = logging.getLogger(__name__)  # 获取当前模块的日志记录器
settings = get_settings()  # 获取全局配置对象


class CodeExplainerService:
    """代码解释服务类"""

    def __init__(self):
        """初始化代码解释服务"""
        self.llm = None  # 初始化大模型对象为None
        self.explanation_chain = None  # 初始化解释链对象为None
        self._init_llm()  # 调用内部方法初始化大模型和链

    def _init_llm(self):
        """初始化LLM和链"""
        try:
            # 初始化通义千问模型，传入API密钥、模型名、温度和最大token数
            self.llm = Tongyi(
                dashscope_api_key=settings.dashscope_api_key,
                model_name=settings.model_name,
                temperature=settings.temperature,
                max_tokens=settings.max_tokens
            )

            # 创建代码解释提示模板，指定输入变量和模板内容
            prompt = PromptTemplate(
                input_variables=["code", "language"],
                template=CODE_EXPLANATION_PROMPT
            )

            # 创建LLM链，绑定大模型和提示模板，设置是否输出详细日志
            self.explanation_chain = LLMChain(
                llm=self.llm,
                prompt=prompt,
                verbose=True if settings.debug else False
            )

            logger.info("代码解释服务初始化成功")  # 记录初始化成功日志

        except Exception as e:
            logger.error(f"代码解释服务初始化失败: {str(e)}")  # 记录初始化失败日志
            raise  # 抛出异常

    async def explain_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        解释代码功能和逻辑

        Args:
            code: 待解释的代码
            language: 编程语言

        Returns:
            Dict包含解释结果
        """
        try:
            logger.info(f"开始解释 {language} 代码")  # 记录开始解释日志

            # 异步执行LLM链，避免阻塞主线程
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.explanation_chain.run(
                    code=code,
                    language=language
                )
            )

            # 解析LLM响应，结构化输出
            result = self._parse_explanation_response(response)

            logger.info("代码解释完成")  # 记录解释完成日志
            return result  # 返回结构化解释结果

        except Exception as e:
            logger.error(f"代码解释过程出错: {str(e)}")  # 记录解释出错日志
            raise  # 抛出异常

    def _parse_explanation_response(self, response: str) -> Dict[str, Any]:
        """
        解析LLM的解释响应

        Args:
            response: LLM原始响应

        Returns:
            结构化的解释结果
        """
        try:
            # 简单的响应解析逻辑，将响应按行分割
            # 在实际项目中，可能需要更复杂的解析逻辑或结构化输出
            lines = response.strip().split('\n')

            explanation = response  # 直接将响应作为详细解释
            summary = "此代码的主要功能是..." if len(lines) > 0 else "代码功能摘要"  # 简单生成摘要

            # 提取关键概念（简化版本）
            key_concepts = self._extract_key_concepts(response)

            return {
                "explanation": explanation,  # 详细解释
                "summary": summary,  # 摘要
                "key_concepts": key_concepts  # 关键概念
            }

        except Exception as e:
            logger.error(f"解析LLM响应失败: {str(e)}")  # 记录解析失败日志
            return {
                "explanation": response,  # 返回原始响应
                "summary": "代码解释",  # 默认摘要
                "key_concepts": []  # 空关键概念
            }

    def _extract_key_concepts(self, explanation: str) -> List[str]:
        """
        从解释中提取关键概念

        Args:
            explanation: 代码解释文本

        Returns:
            关键概念列表
        """
        # 简化的关键概念提取
        # 在实际项目中可以使用NLP技术或更复杂的规则
        concepts = []  # 初始化概念列表

        # 常见Python概念关键词
        python_concepts = [
            "函数", "类", "循环", "条件判断", "变量", "列表", "字典",
            "异常处理", "模块导入", "面向对象", "递归", "迭代器", "生成器"
        ]

        for concept in python_concepts:
            if concept in explanation:  # 如果解释中包含该概念
                concepts.append(concept)  # 添加到概念列表

        return concepts[:5]  # 最多返回5个关键概念

    async def health_check(self) -> bool:
        """
        服务健康检查

        Returns:
            服务是否正常
        """
        try:
            test_code = "print('Hello, World!')"  # 定义测试代码
            result = await self.explain_code(test_code)  # 调用解释方法
            return bool(result.get("explanation"))  # 判断解释结果是否有效
        except Exception:
            return False  # 出现异常则返回False