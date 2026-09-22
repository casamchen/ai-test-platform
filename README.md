# AI Test Management Platform · AI 测试管理平台

> A full-stack AI test platform that generates test cases from requirement docs, executes interface tests with one click, and reports results visually. Built solo by **Jiasheng Chen**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-green)](https://www.djangoproject.com/)
[![Vue](https://img.shields.io/badge/Vue-2.7-success)](https://v2.vuejs.org/)
[![Element UI](https://img.shields.io/badge/Element_UI-2.15-409eff)](https://element.eleme.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

[中文](#中文) | [English](#english)

---

## 中文

### 这是什么

一个**从需求文档自动生成测试用例 + 一键执行接口测试 + 可视化报告**的全栈 Web 应用。整个项目由我一个人独立完成——从 Django 后端、Vue 前端、到智谱 AI 集成、RAG 检索、向量库、接口自动化执行框架。

### 解决了什么问题

软件测试工程师每天 60% 的时间在写测试用例、配置接口测试脚本、整理测试报告——而这些工作中 80% 是重复劳动。本项目把这三件事自动化，让工程师只做真正需要判断力的那 20%。

### 核心能力

| 模块 | 能力 |
|---|---|
| 🤖 **AI 用例生成** | 上传需求文档（.docx）→ RAG 检索 + 智谱 AI 生成结构化测试用例（正向 / 反向 / 边界 / 异常） |
| 🧪 **接口测试** | 一键生成 Postman / unittest 脚本 → 调度执行 → 实时回传结果 |
| 📊 **测试报告** | ECharts 可视化（用例通过率 / 缺陷分布 / 执行趋势）|
| 🔐 **权限** | JWT 登录 + AES 加密敏感配置 |

### 技术栈

**后端**
- Python 3.10+ / Django 4.x / Django REST Framework
- MySQL（PyMySQL）+ Redis + Celery 异步任务
- 智谱 AI SDK + 飞桨 PaddleNLP + FAISS 向量检索
- python-docx 文档解析

**前端**
- Vue 2.7 + Vue Router 2
- Element UI 2.15
- Webpack 3 + ECharts 5 + axios

**AI 流水线**

```
需求文档 (.docx)
    ↓ python-docx 解析
    ↓ 切片 → 飞桨 embedding
    ↓ 存入 FAISS 向量库
新需求进来
    ↓ 检索 top-K 相似片段
    ↓ 拼接到 prompt
    ↓ 智谱 AI (zhipuai SDK)
    ↓
结构化测试用例（JSON）
    ↓
一键导出 Postman 脚本 + 一键调度执行
```

### 项目结构

```
aitest/                              ← 项目根
├── manage.py                        ← Django 入口
├── aitest/                          ← Django 项目配置
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py / celery.py
├── aitestapp/                       ← 核心 Django app
│   ├── models.py
│   ├── views/
│   │   ├── ai_create_testcase/      ← AI 生成测试用例
│   │   ├── ai_interface_test/       ← 接口自动化测试
│   │   ├── AI/                      ← 智谱 SDK 封装
│   │   ├── login/                   ← 鉴权
│   │   └── ...
│   ├── scripts/                     ← AI 流水线核心
│   │   ├── docmentpar.py            ← 文档解析
│   │   ├── vectorIndexing.py        ← 向量化
│   │   ├── vectordb.py              ← FAISS 操作
│   │   ├── sentencesearch.py        ← RAG 检索
│   │   ├── prompts.py / prompts_interface.py
│   │   ├── model_AI.py              ← 智谱 AI 调用
│   │   ├── test_case_executor.py    ← 用例执行
│   │   ├── api_request.py
│   │   └── ...
│   ├── tool/                        ← 工具脚本
│   └── migrations/
├── aitestpage/                      ← Vue 2 前端
│   ├── package.json
│   ├── build/                       ← Webpack 配置
│   ├── config/                      ← 环境配置
│   └── src/
│       ├── components/
│       │   ├── project_config/
│       │   ├── interface_test/
│       │   ├── function_test/
│       │   ├── login/
│       │   └── ...
│       └── App.vue / main.js
├── vectorsFrame/                    ← FAISS 向量库 (.gitignored)
└── .env.example                     ← 环境变量样例（不含真实密钥）
```

### 快速启动

```bash
# 1. 准备环境变量（拷贝并填写）
cp .env.example .env
# 编辑 .env，填入真实的 DB / Redis / 智谱 AI Key

# 2. 安装 Python 依赖
pip install -r aitestapp/requirements.txt

# 3. 初始化数据库
python manage.py migrate

# 4. 启动后端
python manage.py runserver 0.0.0.0:8000

# 5. 启动前端
cd aitestpage
npm install
npm run dev
# → http://localhost:8080
```

### License

MIT © Jiasheng Chen

---

## English

### What this is

A full-stack web application that **auto-generates test cases from requirement documents, executes interface tests with one click, and visualizes reports** — designed, developed, and shipped end-to-end as a solo project.

### Why I built it

QA engineers spend ~60% of their day on three things: writing test cases, configuring interface test scripts, and assembling test reports. ~80% of that is mechanical. This platform automates the 80% so engineers can spend their time on the 20% that actually needs human judgment.

### Capabilities

| Module | What it does |
|---|---|
| 🤖 **AI test case generation** | Upload requirement .docx → RAG retrieval + Zhipu AI → structured test cases |
| 🧪 **Interface testing** | One-click Postman / unittest generation → schedule execution → real-time results |
| 📊 **Visual reporting** | ECharts dashboards for pass rate / defect distribution / execution trends |
| 🔐 **Auth** | JWT login + AES-encrypted sensitive config |

### Tech stack

**Backend** — Python 3.10+ · Django 4 · DRF · MySQL (PyMySQL) · Redis · Celery
**AI** — Zhipu AI SDK · PaddleNLP embeddings · FAISS vector store · python-docx
**Frontend** — Vue 2.7 · Vue Router 2 · Element UI 2.15 · Webpack 3 · ECharts 5

### Why this is interesting

- I shipped it solo — backend, frontend, AI pipeline, evaluation harness, the lot.
- The AI isn't an API call I sprinkled on. It's a RAG pipeline with embedding, vector storage, prompt engineering, and field-level precision/recall evaluation against hand-labeled test cases.
- The system runs in production-style (Celery + Redis + MySQL), not just a notebook.

### Project structure

See the tree above. Each directory maps to a clear concern:

- `aitest/` — Django project config
- `aitestapp/views/ai_create_testcase/` — AI case generation API
- `aitestapp/views/ai_interface_test/` — Interface test scheduling & execution
- `aitestapp/scripts/` — AI / RAG pipeline core
- `aitestpage/` — Vue 2 frontend

### License

MIT © Jiasheng Chen
