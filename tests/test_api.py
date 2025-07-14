"""
后端API测试文件
负责人：组员C
作用：测试FastAPI接口的功能正确性，包括代码解释和代码审查接口
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from backend.main import app

# 创建测试客户端
client = TestClient(app)


class TestHealthEndpoint:
    """健康检查接口测试"""
    
    def test_health_check(self):
        """测试健康检查接口"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "CodeWise AI"
    
    def test_root_endpoint(self):
        """测试根路径接口"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "CodeWise AI" in data["message"]


class TestCodeExplainEndpoint:
    """代码解释接口测试"""
    
    def test_explain_valid_code(self):
        """测试有效代码的解释"""
        test_code = """
def hello_world():
    print("Hello, World!")
    return "success"
"""
        
        payload = {
            "code": test_code,
            "language": "python",
            "analysis_type": "explain"
        }
        
        response = client.post("/api/v1/explain", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "explanation" in data
        assert "code_summary" in data
        assert "execution_time" in data
        assert isinstance(data["key_concepts"], list)
    
    def test_explain_empty_code(self):
        """测试空代码的处理"""
        payload = {
            "code": "",
            "language": "python",
            "analysis_type": "explain"
        }
        
        response = client.post("/api/v1/explain", json=payload)
        assert response.status_code == 422  # 验证错误
    
    def test_explain_invalid_analysis_type(self):
        """测试错误的分析类型"""
        payload = {
            "code": "print('test')",
            "language": "python",
            "analysis_type": "review"  # 应该是explain
        }
        
        response = client.post("/api/v1/explain", json=payload)
        assert response.status_code == 400


class TestCodeReviewEndpoint:
    """代码审查接口测试"""
    
    def test_review_valid_code(self):
        """测试有效代码的审查"""
        test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
        
        payload = {
            "code": test_code,
            "language": "python",
            "analysis_type": "review"
        }
        
        response = client.post("/api/v1/review", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "overall_score" in data
        assert "summary" in data
        assert "bugs" in data
        assert "style_issues" in data
        assert "optimizations" in data
        assert "execution_time" in data
        assert 0 <= data["overall_score"] <= 100
    
    def test_review_code_with_issues(self):
        """测试有问题的代码审查"""
        # 故意写一个有风格问题的代码
        test_code = """
def badFunction(x,y):
  result=x+y
  return result
"""
        
        payload = {
            "code": test_code,
            "language": "python",
            "analysis_type": "review"
        }
        
        response = client.post("/api/v1/review", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        # 应该能检测到一些风格问题
        assert data["overall_score"] < 100


class TestStatusEndpoint:
    """服务状态检查测试"""
    
    def test_ai_status(self):
        """测试AI服务状态"""
        response = client.get("/api/v1/status")
        assert response.status_code in [200, 503]  # 可能服务未启动
        
        if response.status_code == 200:
            data = response.json()
            assert "ai_service" in data
            assert "timestamp" in data


@pytest.fixture
def sample_python_code():
    """测试用的Python代码样本"""
    return """
def calculate_factorial(n):
    '''计算阶乘'''
    if n < 0:
        raise ValueError("负数没有阶乘")
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# 测试函数
print(calculate_factorial(5))
"""


class TestIntegration:
    """集成测试"""
    
    def test_explain_then_review_workflow(self, sample_python_code):
        """测试完整的工作流程：先解释后审查"""
        
        # 1. 先解释代码
        explain_payload = {
            "code": sample_python_code,
            "language": "python",
            "analysis_type": "explain"
        }
        
        explain_response = client.post("/api/v1/explain", json=explain_payload)
        assert explain_response.status_code == 200
        
        # 2. 再审查代码
        review_payload = {
            "code": sample_python_code,
            "language": "python",
            "analysis_type": "review"
        }
        
        review_response = client.post("/api/v1/review", json=review_payload)
        assert review_response.status_code == 200
        
        # 验证两个响应都有有效内容
        explain_data = explain_response.json()
        review_data = review_response.json()
        
        assert len(explain_data["explanation"]) > 0
        assert review_data["overall_score"] > 0


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])