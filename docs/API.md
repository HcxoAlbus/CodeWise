# CodeWise AI API 接口文档

## 基础信息
- **基础URL**: `http://localhost:8000`
- **API版本**: v1
- **认证方式**: 无需认证（开发版本）

## 接口列表

### 1. 健康检查

#### GET /health
检查服务运行状态

**响应示例**:
```json
{
  "status": "healthy",
  "service": "CodeWise AI"
}
```

### 2. 代码解释

#### POST /api/v1/explain
解释Python代码的功能和逻辑

**请求体**:
```json
{
  "code": "def hello():\n    print('Hello, World!')",
  "language": "python",
  "analysis_type": "explain"
}
```

**响应体**:
```json
{
  "explanation": "这个函数定义了一个名为hello的函数...",
  "code_summary": "定义了一个打印问候语的函数",
  "key_concepts": ["函数定义", "print语句"],
  "execution_time": 1.23
}
```

**错误响应**:
```json
{
  "detail": "代码不能为空",
  "error_code": "INVALID_INPUT"
}
```

### 3. 代码审查

#### POST /api/v1/review
全面审查Python代码质量

**请求体**:
```json
{
  "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
  "language": "python",
  "analysis_type": "review"
}
```

**响应体**:
```json
{
  "overall_score": 75,
  "summary": "代码实现正确但存在性能问题",
  "bugs": [
    {
      "line_number": 4,
      "description": "递归实现效率低下",
      "severity": "medium",
      "suggestion": "考虑使用动态规划或迭代方法"
    }
  ],
  "style_issues": [],
  "optimizations": [
    {
      "category": "算法优化",
      "description": "使用记忆化递归提升性能",
      "performance_impact": "时间复杂度从O(2^n)降至O(n)",
      "before_code": "return fibonacci(n-1) + fibonacci(n-2)",
      "after_code": "@lru_cache(maxsize=None)\ndef fibonacci(n):\n    ..."
    }
  ],
  "execution_time": 2.45,
  "lines_analyzed": 4
}
```

### 4. 服务状态

#### GET /api/v1/status
检查AI服务和组件状态

**响应体**:
```json
{
  "ai_service": "available",
  "model_status": "ready",
  "vector_db": "connected",
  "timestamp": 1704067200.0
}
```

## 错误码说明

| 错误码 | HTTP状态码 | 说明 |
|--------|------------|------|
| INVALID_INPUT | 400 | 输入数据无效 |
| ANALYSIS_ERROR | 500 | 分析过程出错 |
| SERVICE_UNAVAILABLE | 503 | AI服务不可用 |
| TIMEOUT | 504 | 请求超时 |

## 使用示例

### Python客户端示例
```python
import requests

# 代码解释
response = requests.post('http://localhost:8000/api/v1/explain', json={
    'code': 'def hello():\n    print("Hello!")',
    'language': 'python',
    'analysis_type': 'explain'
})
result = response.json()
print(result['explanation'])

# 代码审查
response = requests.post('http://localhost:8000/api/v1/review', json={
    'code': 'def add(a,b):\nreturn a+b',
    'language': 'python', 
    'analysis_type': 'review'
})
result = response.json()
print(f"代码评分: {result['overall_score']}")
```

### JavaScript客户端示例
```javascript
// 使用fetch API
async function analyzeCode(code, type) {
  const response = await fetch(`http://localhost:8000/api/v1/${type}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      code: code,
      language: 'python',
      analysis_type: type
    })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return await response.json();
}

// 使用示例
analyzeCode('print("Hello")', 'explain')
  .then(result => console.log(result.explanation))
  .catch(error => console.error('Error:', error));
```

## 性能指标

- **平均响应时间**: 2-5秒
- **最大代码长度**: 10,000字符
- **并发支持**: 10个请求/秒
- **超时时间**: 60秒

## 限制说明

1. **代码长度限制**: 单次提交代码不超过10,000字符
2. **语言支持**: 当前仅支持Python代码分析
3. **频率限制**: 无硬性限制（开发版本）
4. **文件上传**: 暂不支持文件上传，仅支持文本提交