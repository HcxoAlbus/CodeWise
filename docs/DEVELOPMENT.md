# CodeWise AI 开发指南

## 项目简介
CodeWise AI是一个基于大型语言模型的智能编程学习伙伴与代码审查员，旨在帮助编程初学者和中级开发者提升代码质量和编程技能。

## 重新规划的团队分工

### 组长职责（任务量减少）
- **主要负责**：项目架构设计、AI核心服务、团队协调
- **具体任务**：
  - 系统整体架构设计和技术方案制定
  - LangChain Agent和LLM集成（code_explainer.py, code_reviewer.py）
  - 核心AI服务的Prompt设计和优化
  - 团队进度管理和代码审查
  - 技术难点攻关和问题解决

### 组员A职责（前端 + API层）
- **主要负责**：前端开发、API接口设计
- **具体任务**：
  - React前端应用开发（已完成）
  - Monaco Editor代码编辑器集成
  - 用户界面和交互设计
  - **新增**：后端API路由实现（routes.py）
  - **新增**：请求/响应数据模型设计（schemas.py）
  - 前后端接口联调和测试

### 组员B职责（数据层 + 业务逻辑）
- **主要负责**：数据处理、业务逻辑、应用层
- **具体任务**：
  - RAG知识库构建和维护（rag_tool.py）
  - 向量数据库集成和优化
  - **新增**：应用主类开发（application.py）
  - **新增**：业务逻辑协调和服务管理
  - **新增**：数据处理和存储优化
  - 知识库内容扩展和质量提升

### 组员C职责（工具链 + 运维配置）
- **主要负责**：工具开发、测试、部署配置
- **具体任务**：
  - 静态分析工具集成（flake8_tool.py）
  - **新增**：应用中间件开发（middleware.py）
  - **新增**：事件处理器配置（events.py）
  - **新增**：工具类库开发（utils/文件夹）
  - 测试框架搭建和用例编写
  - CI/CD和Docker部署配置
  - 性能监控和错误处理

## 新增文件说明

### backend/app/ 目录（组员B负责）
- `__init__.py` - 应用模块初始化
- `application.py` - 应用主类，管理所有服务组件
- `middleware.py` - 请求中间件配置（组员C负责）
- `events.py` - 应用生命周期事件处理（组员C负责）

### backend/utils/ 目录（组员C负责）
- `__init__.py` - 工具模块初始化
- `text_processor.py` - 文本处理工具
- `code_analyzer.py` - 代码结构分析工具
- `validation.py` - 输入验证和安全检查
- `formatters.py` - 响应格式化工具

## 开发流程优化

### 第一周任务分配
**周一-周二：基础设施完善**
- 组长：完善AI服务核心逻辑
- 组员A：API接口开发和前端优化
- 组员B：应用层架构实现
- 组员C：中间件和工具类开发

**周三-周四：功能集成测试**
- 组长：AI模型调优和Prompt优化
- 组员A：前后端联调测试
- 组员B：数据层和业务逻辑测试
- 组员C：工具链集成和单元测试

**周五-周日：系统集成和调试**
- 全员：系统集成测试、性能优化、bug修复

### 第二周任务分配
**周一-周三：功能完善和优化**
- 组长：AI服务性能优化和错误处理
- 组员A：用户体验优化和界面完善
- 组员B：知识库扩展和检索优化
- 组员C：测试覆盖率提升和部署准备

**周四-周五：文档和部署**
- 组员A：用户手册和API文档
- 组员B：技术文档和维护指南
- 组员C：部署文档和运维配置

## 技术要点

### 新增技术组件
- **应用层管理**：统一的服务组件管理
- **中间件系统**：请求日志、性能监控、安全防护
- **工具链扩展**：代码分析、文本处理、数据验证
- **事件驱动**：应用生命周期管理

### 代码质量保证
- 每个文件明确负责人和功能说明
- 统一的错误处理和日志记录
- 完善的输入验证和安全检查
- 模块化设计，低耦合高内聚

## 协作规范

### 代码提交规范
- 提交信息格式：`[负责人] 功能模块: 具体修改内容`
- 例如：`[组员A] API路由: 添加代码解释接口`

### 代码审查流程
1. 开发完成后提交PR
2. 组长进行代码审查
3. 至少一名其他组员进行交叉review
4. 通过审查后合并到主分支

### 测试要求
- 每个功能模块需要对应的单元测试
- API接口需要集成测试
- 关键功能需要端到端测试
- 测试覆盖率目标：80%以上

## 注意事项
1. **任务分配更均匀**：组长专注核心AI功能，其他成员承担更多责任
2. **模块化开发**：每个人负责的模块相对独立，便于并行开发
3. **定期沟通**：每日站会同步进度，及时解决依赖问题
4. **文档优先**：重要功能先写文档再开发，确保需求明确