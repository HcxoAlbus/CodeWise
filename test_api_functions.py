"""
API功能测试脚本
测试后端API的基本功能
"""

import requests
import json
import time

# API基础URL
BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 健康检查通过")
            print(f"   响应: {response.json()}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查连接失败: {e}")
        return False

def test_root():
    """测试根路径接口"""
    print("\n🔍 测试根路径接口...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ 根路径访问成功")
            print(f"   响应: {response.json()}")
            return True
        else:
            print(f"❌ 根路径访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 根路径连接失败: {e}")
        return False

def test_code_explanation():
    """测试代码解释接口"""
    print("\n🔍 测试代码解释接口...")
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
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/explain",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ 代码解释测试成功")
            result = response.json()
            print(f"   解释长度: {len(result.get('explanation', ''))}")
            print(f"   摘要: {result.get('code_summary', '')[:50]}...")
            print(f"   执行时间: {result.get('execution_time', 0):.2f}秒")
            return True
        else:
            print(f"❌ 代码解释测试失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 代码解释请求失败: {e}")
        return False

def test_code_review():
    """测试代码审查接口"""
    print("\n🔍 测试代码审查接口...")
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
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/review",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ 代码审查测试成功")
            result = response.json()
            print(f"   总体评分: {result.get('overall_score', 0)}")
            print(f"   摘要: {result.get('summary', '')[:50]}...")
            print(f"   执行时间: {result.get('execution_time', 0):.2f}秒")
            return True
        else:
            print(f"❌ 代码审查测试失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 代码审查请求失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试 CodeWise AI API")
    print("=" * 50)
    
    # 测试基础接口
    health_ok = test_health()
    root_ok = test_root()
    
    if not (health_ok and root_ok):
        print("\n❌ 基础接口测试失败，请检查后端服务是否正常启动")
        return
    
    # 测试AI功能接口
    explain_ok = test_code_explanation()
    review_ok = test_code_review()
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    print(f"   健康检查: {'✅' if health_ok else '❌'}")
    print(f"   根路径: {'✅' if root_ok else '❌'}")
    print(f"   代码解释: {'✅' if explain_ok else '❌'}")
    print(f"   代码审查: {'✅' if review_ok else '❌'}")
    
    if all([health_ok, root_ok, explain_ok, review_ok]):
        print("\n🎉 所有测试通过！后端API工作正常")
        print("💡 现在可以启动前端服务进行完整测试")
    else:
        print("\n⚠️  部分测试失败，请检查相关功能")

if __name__ == "__main__":
    main()