# langgraph-playground
一个基于 FastAPI + Vue 3 + LangGraph 的智能助手系统，集成多种 AI 模型和智能搜索功能。

## ✨ 功能特性

### 🤖 AI 能力
- **多模型支持**: DeepSeek、Ollama 本地模型、OpenAI 兼容接口
- **智能对话**: 支持流式响应和上下文记忆
- **推理能力**: 集成 DeepSeek Reasoner 进行复杂推理
- **视觉理解**: 支持图片上传和分析

### 🔍 智能搜索
- **多搜索引擎**: 博查AI、百度AI搜索、SerpAPI

### 💬 对话系统
- **会话管理**: 多会话支持，历史记录保存
- **用户系统**: 注册、登录、个人设置
- **实时通信**: WebSocket 支持流式对话

## 🛠 技术栈

### 后端技术
- **框架**: FastAPI (高性能异步Web框架)
- **数据库**: MySQL + Redis + Neo4j
- **AI集成**: DeepSeek API, Ollama, OpenAI Compatible APIs
- **搜索服务**: 博查AI, 百度AI搜索, SerpAPI
- **缓存**: Redis 语义缓存
- **日志**: 结构化日志系统

### 前端技术
- **框架**: Vue 3
- **UI库**: Element Plus

### AI技术
- **AI框架**: LangGraph+GraphRag 

## 🚀 快速开始

### 📋 环境要求

- **Python**: 3.8 或更高版本
- **Node.js**: 16 或更高版本
- **数据库**: MySQL 8.0+, Redis 6.0+
- **可选**: Neo4j 4.0+ (用于知识图谱)

### 主要 API 端点

- `POST /api/chat` - 智能对话
- `POST /api/search` - 智能搜索
- `POST /api/token` - 用户认证
- `GET /api/conversations/user/{user_id}` - 获取用户会话
- `POST /api/upload/image` - 图片上传

## 🏗️ 项目结构

```
langgraph-playground/
├── llm_backend/                 # 后端代码
│   ├── app/                    # 应用核心
│   │   ├── api/               # API 路由
│   │   ├── core/              # 核心配置
│   │   ├── models/            # 数据模型
│   │   ├── services/          # 业务逻辑
│   │   ├── tools/             # 工具模块
│   │   └── utils/             # 工具函数
│   ├── static/                # 前端构建文件
│   ├── main.py                # FastAPI 应用入口
│   ├── run.py                 # 启动脚本
│   └── requirements.txt       # Python 依赖
└── README.md                  # 项目文档
```