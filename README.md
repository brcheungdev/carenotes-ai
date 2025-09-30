CareNotes AI — AI-powered nursing assistant that transforms voice and text notes into structured, auditable care records with timeline and PDF export. CareNotes AI —— 一款面向护理场景的 AI 助手，能将口述/手写笔记快速转化为结构化护理记录，支持时间线视图与 PDF 导出。

# CareNotes AI

版本：v0.1.0（MVP）
[English](READMEen.md)

## 项目背景与愿景

CareNotes AI 源于我对护理工作的看法，护理人员的减负是必要的也是极其重要的。我做这项工作的初始目的是帮助临床护士将零散的口述、手写笔记快速转化为结构化的护理记录。

该项目坚持以下理念：
- **临床优先**：用数字化工具解放护理工作量，把时间还给护理工作者。
- **数据可追溯**：服务全过程都保留原始记录，便于质量审核和交接班。
- **结构化 + 叙事**：既支持标准化字段，也保留必要的情境描述。
- **模块化演进**：核心功能解耦，便于后续叠加更多 AI 能力（实时预警、多语言、移动端等）。

## 功能概览

- 🔐 **登录与权限**：示例账号登录，基于 JWT 区分 nurse/admin 角色。
- 👥 **患者管理**：创建与查询患者信息，作为护理记录归属入口。
- 📝 **护理记录**：支持文本录入、语音转写（Whisper）、结构化解析（LLM），形成 SOAP、生命体征、I/O 等字段。
- 📄 **PDF 导出**：按模板生成可打印、可归档的护理记录 PDF。
- 🕒 **时间线视图**：重建护理事件时间轴，支持过滤与预警提示。
- 🔌 **开放 API**：RESTful 接口输出统一 JSON，方便院内系统集成。

## 技术栈

| 层次 | 主要技术 |
| --- | --- |
| 后端 | Python 3.10、Flask、Flask-CORS、SQLAlchemy、PyJWT、WeasyPrint、OpenAI API（Whisper + Responses） |
| 数据库 | MySQL 8.0 |
| 前端 | 原生 HTML/CSS/JavaScript（模块化脚本：api/auth/recorder/ui） |
| 工具 | PowerShell 启动脚本、Python 自定义静态服务器、虚拟环境 `.venv` |

## 目录结构

```
backend/
  app.py              # Flask 应用入口
  config.py           # 环境变量加载与配置
  db.py               # SQLAlchemy 初始化
  models/             # ORM 模型
  routes/             # 认证/患者/护理记录/导出接口
  services/           # STT、LLM、PDF 等服务封装
  templates/pdf/      # PDF 模板
  migrations/schema.sql
frontend/
  index.html          # 登录页面
  patient.html        # 患者管理
  record.html         # 护理记录编辑
  timeline.html       # 时间线视图
  assets/css/style.css
  assets/js/
README.md
StartCareNotes.bat    # 一键启动脚本（暂未实装）
```

## 环境与前置条件

- Windows 10/11 + PowerShell（或兼容终端）
- Python 3.10 及以上
- pip / venv（Python 内置）
- MySQL 8.0
- 现代浏览器（Edge / Chrome）
- 可选：OpenAI API Key（启用语音转写与结构化解析）

> 若需编译 WeasyPrint 依赖，请确保安装 Microsoft Visual C++ Build Tools。

## 安装与配置步骤

1. **克隆代码并进入目录**
   ```powershell
   git clone <your-repo>
   cd carenotes-ai
   ```
2. **创建虚拟环境并安装依赖**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r backend\requirements.txt
   ```
3. **初始化数据库**
   ```powershell
   mysql -u <user> -p -e "CREATE DATABASE IF NOT EXISTS carenotes CHARACTER SET utf8mb4;"
   mysql -u <user> -p carenotes < backend\migrations\schema.sql
   ```
4. **配置环境变量**
   ```powershell
   copy backend\.env.example backend\.env
   notepad backend\.env
   ```
   需要填写的关键项：
   - `OPENAI_API_KEY`
   - `OPENAI_TRANSCRIBE_MODEL`（示例：whisper-1）
   - `OPENAI_PARSE_MODEL`（示例：gpt-4o-mini）
   - `MYSQL_URL`（示例：mysql+pymysql://user:pass@127.0.0.1:3306/carenotes）
   - `JWT_SECRET`

> 仓库中的 `.env` 默认使用占位符（如 `你的apikey`、`mysql用户名`、`mysql密码`），请在本地替换为真实数据，否则无法连接 OpenAI 服务与数据库。

> 如果在处理配置文件时遇到 `'latin-1' codec can't encode characters` 报错，说明内容含有中文占位符或其他 Unicode 字符；请使用 UTF-8 编码读取/写入文件，即可避免错误。

## 启动项目

### 方式一：手动启动

1. **启动后端服务**
   ```powershell
   cd backend
   ..\.venv\Scripts\activate
   flask --app app run --debug
   ```
   默认地址：`http://127.0.0.1:5000`（API 前缀 `/api`）。

2. **启动前端静态服务**
   ```powershell
   cd ..\frontend
   ..\.venv\Scripts\python serve.py
   ```
   默认地址：`http://127.0.0.1:8001/index.html`。

### 方式二：一键启动脚本（暂未实装）

在项目根目录运行：
```powershell
StartCareNotes.bat
```
脚本会依次启动后端、前端，并自动打开浏览器。

## 演示账号

测试开源版本默认提供以下示例账号，仅供体验与调试：

- `admin / Passw0rd!`
- `nurse / Passw0rd!`

登入后可体验患者管理、护理记录编写、PDF 导出与时间线功能。

## 版本规划

- 当前版本：v0.1.0（MVP）。
- 未来优化方向：
  - 更细粒度的角色权限与审计日志；
  - 改进的语音处理（实时降噪、说话人分离）；
  - 与 HIS/EMR 等院内系统的集成接口；
  - 更丰富的可视化与移动端适配；
  - 自动化测试与 CI/CD 流程。

## 免责声明

本项目仅供学习、研究与原型验证使用，不适用于生产环境或真实医疗场景。所有示例数据、账号与配置仅为演示。我们将持续根据反馈对功能与安全性进行迭代优化。
合作意图请通过主页联系方式联系
