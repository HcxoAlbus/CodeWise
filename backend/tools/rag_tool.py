"""
RAG知识库检索工具
负责人：组员B
作用：封装向量数据库检索功能为LangChain Tool，提供代码优化和最佳实践建议
"""

import logging
import os
from typing import List, Dict, Any
from langchain.tools import BaseTool
# 修复 LangChain 导入警告
try:
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import HuggingFaceEmbeddings
except ImportError:
    # 如果新版本导入失败，使用旧版本导入
    from langchain.vectorstores import FAISS
    from langchain.embeddings import HuggingFaceEmbeddings

from langchain.schema import Document
import numpy as np

from config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class RAGTool(BaseTool):
    """RAG知识库检索工具类"""
    
    name: str = "knowledge_retriever"
    description: str = """
    从Python编程知识库中检索相关的最佳实践、优化建议和代码示例。
    输入：代码片段或编程概念关键词
    输出：相关的知识库内容，包括最佳实践和优化建议
    """
    
    def __init__(self):
        super().__init__()
        self.embeddings = None
        self.vector_store = None
        self._init_rag_system()
    
    def _init_rag_system(self):
        """初始化RAG系统"""
        try:
            # 初始化嵌入模型
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            
            # 尝试加载现有的向量数据库
            vector_db_path = settings.vector_db_path
            if os.path.exists(vector_db_path):
                self.vector_store = FAISS.load_local(
                    vector_db_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("已加载现有向量数据库")
            else:
                # 创建新的向量数据库
                self._create_initial_knowledge_base()
                logger.info("已创建新的向量数据库")
                
        except Exception as e:
            logger.error(f"RAG系统初始化失败: {str(e)}")
            self.vector_store = None
    
    def _create_initial_knowledge_base(self):
        """创建初始知识库"""
        try:
            # 基础Python最佳实践文档
            documents = [
                Document(
                    page_content="使用列表推导式代替传统循环可以提高代码性能和可读性。例如：[x*2 for x in range(10)] 比使用for循环更加Pythonic。",
                    metadata={"topic": "列表推导式", "category": "性能优化"}
                ),
                Document(
                    page_content="使用with语句进行文件操作可以确保文件正确关闭，避免资源泄漏。例如：with open('file.txt', 'r') as f: content = f.read()",
                    metadata={"topic": "文件操作", "category": "最佳实践"}
                ),
                Document(
                    page_content="避免在循环中使用字符串拼接，使用join()方法或f-string会更高效。例如：''.join(items) 或 f'{name}_{id}'",
                    metadata={"topic": "字符串操作", "category": "性能优化"}
                ),
                Document(
                    page_content="使用isinstance()而不是type()进行类型检查，这样可以正确处理继承关系。例如：isinstance(obj, str) 而不是 type(obj) == str",
                    metadata={"topic": "类型检查", "category": "最佳实践"}
                ),
                Document(
                    page_content="函数应该遵循单一职责原则，每个函数只做一件事。复杂的函数应该拆分为多个小函数。",
                    metadata={"topic": "函数设计", "category": "代码结构"}
                ),
                Document(
                    page_content="使用异常处理时要捕获具体的异常类型，避免使用裸露的except语句。例如：except ValueError: 而不是 except:",
                    metadata={"topic": "异常处理", "category": "最佳实践"}
                ),
                Document(
                    page_content="使用生成器表达式处理大数据集可以节省内存。例如：sum(x*x for x in range(1000000))",
                    metadata={"topic": "生成器", "category": "内存优化"}
                ),
                Document(
                    page_content="类的命名应该使用帕斯卡命名法(PascalCase)，函数和变量使用蛇形命名法(snake_case)。",
                    metadata={"topic": "命名规范", "category": "代码风格"}
                )
            ]
            
            # 创建向量存储
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
            
            # 保存向量数据库
            os.makedirs(os.path.dirname(settings.vector_db_path), exist_ok=True)
            self.vector_store.save_local(settings.vector_db_path)
            
        except Exception as e:
            logger.error(f"创建知识库失败: {str(e)}")
            raise
    
    def _run(self, query: str) -> str:
        """
        检索相关知识
        
        Args:
            query: 查询内容（代码片段或关键词）
            
        Returns:
            相关的知识库内容
        """
        try:
            if not self.vector_store:
                return "❌ 知识库未初始化"
            
            # 执行相似度搜索
            docs = self.vector_store.similarity_search(
                query, 
                k=3  # 返回最相关的3个结果
            )
            
            if not docs:
                return "💡 未找到相关的最佳实践建议"
            
            # 格式化检索结果
            return self._format_retrieval_results(docs)
            
        except Exception as e:
            logger.error(f"知识库检索失败: {str(e)}")
            return f"❌ 检索过程出错: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """异步版本的运行方法"""
        return self._run(query)
    
    def _format_retrieval_results(self, docs: List[Document]) -> str:
        """
        格式化检索结果
        
        Args:
            docs: 检索到的文档列表
            
        Returns:
            格式化的知识库内容
        """
        if not docs:
            return "💡 未找到相关建议"
        
        result = "📚 从知识库中找到以下相关建议：\n\n"
        
        for i, doc in enumerate(docs, 1):
            metadata = doc.metadata
            topic = metadata.get('topic', '未知主题')
            category = metadata.get('category', '其他')
            
            result += f"🔸 建议 {i} - {topic} ({category}):\n"
            result += f"   {doc.page_content}\n\n"
        
        result += "💡 建议根据以上最佳实践优化您的代码。"
        
        return result
    
    def add_knowledge(self, content: str, topic: str, category: str = "其他"):
        """
        向知识库添加新内容
        
        Args:
            content: 知识内容
            topic: 主题
            category: 分类
        """
        try:
            if not self.vector_store:
                logger.error("向量存储未初始化")
                return False
            
            doc = Document(
                page_content=content,
                metadata={"topic": topic, "category": category}
            )
            
            # 添加到向量存储
            self.vector_store.add_documents([doc])
            
            # 保存更新
            self.vector_store.save_local(settings.vector_db_path)
            
            logger.info(f"已添加新知识: {topic}")
            return True
            
        except Exception as e:
            logger.error(f"添加知识失败: {str(e)}")
            return False
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """获取知识库统计信息"""
        try:
            if not self.vector_store:
                return {"status": "未初始化", "count": 0}
            
            # 获取向量数量（简化的统计）
            index_size = self.vector_store.index.ntotal if hasattr(self.vector_store, 'index') else 0
            
            return {
                "status": "可用",
                "document_count": index_size,
                "embedding_model": "all-MiniLM-L6-v2"
            }
            
        except Exception as e:
            logger.error(f"获取知识库统计失败: {str(e)}")
            return {"status": "错误", "error": str(e)}


def get_rag_tool() -> RAGTool:
    """获取RAG工具实例"""
    return RAGTool()