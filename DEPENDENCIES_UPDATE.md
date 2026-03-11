# 依赖配置统一说明

## 📅 更新日期
2026-03-11

## 🎯 更新目标

统一项目依赖配置，消除 `backend/requirements.txt` 和 `dev-setup/config/requirements.txt` 之间的不一致。

## ✅ 执行方案

采用 **方案一**：统一使用 `backend/requirements.txt` 作为标准依赖配置。

## 🔄 变更内容

### 1. 删除文件
- ❌ `dev-setup/config/requirements.txt` - 已删除

### 2. 更新文件
- ✅ `dev-setup/config/package.json` - 已更新为匹配 `frontend/package.json`

### 3. 标准依赖配置

#### 后端依赖 (`backend/requirements.txt`)

```txt
# APT 情报分析平台 - 后端依赖

# FastAPI 框架
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.6

# 数据库
sqlalchemy[asyncio]>=2.0.25
asyncpg>=0.29.0
alembic>=1.13.1
neo4j>=5.15.0

# 数据验证与序列化
pydantic>=2.5.3
pydantic-settings>=2.1.0

# 大模型 SDK
openai>=1.10.0

# HTTP 客户端
httpx>=0.26.0
aiohttp>=3.9.1

# 安全
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4

# 日志
loguru>=0.7.2

# 任务调度
apscheduler>=3.10.4

# 工具
python-dotenv>=1.0.0
tenacity>=8.2.3

# NLP 处理
jieba>=0.42.1

# 测试
pytest>=7.4.4
pytest-asyncio>=0.23.3
```

**关键变更**:
- ✅ 使用 `asyncpg` (PostgreSQL 驱动) 替代 `pymysql` (MySQL 驱动)
- ✅ 添加 `aiohttp` 用于异步 HTTP 请求
- ✅ 添加 `jieba` 用于中文分词
- ✅ 移除 `transformers` 和 `torch` (按需安装)
- ✅ 移除 `anthropic` (按需安装)
- ✅ 移除 `beautifulsoup4`, `lxml`, `selenium`, `playwright` (按需安装)
- ✅ 移除 `black`, `isort`, `flake8` (开发工具，不放入生产依赖)

#### 前端依赖 (`dev-setup/config/package.json`)

```json
{
  "name": "apt-intelligence-frontend",
  "version": "1.0.0",
  "description": "APT 情报分析平台前端",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix"
  },
  "dependencies": {
    "vue": "^3.4.15",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "element-plus": "^2.5.3",
    "@element-plus/icons-vue": "^2.3.1",
    "axios": "^1.6.5",
    "echarts": "^5.4.3",
    "vue-echarts": "^6.6.8",
    "dayjs": "^1.11.10",
    "@vueuse/core": "^10.7.2"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.3",
    "typescript": "^5.3.3",
    "vite": "^5.0.11",
    "vue-tsc": "^1.8.27",
    "@types/node": "^20.11.5",
    "sass": "^1.70.0",
    "unplugin-auto-import": "^0.17.3",
    "unplugin-vue-components": "^0.26.0"
  }
}
```

**关键变更**:
- ✅ 更新 `vue` 到 `^3.4.15`
- ✅ 更新 `element-plus` 到 `^2.5.3`
- ✅ 添加 `vue-echarts` 用于 ECharts 集成
- ✅ 添加 `dayjs` 用于日期处理
- ✅ 添加 `unplugin-auto-import` 用于自动导入
- ✅ 添加 `unplugin-vue-components` 用于组件自动导入
- ✅ 移除 `eslint`, `prettier` 相关配置（使用项目根目录配置）

## 📦 依赖对比

### 删除的依赖（从 dev-setup/config/requirements.txt）

| 包名 | 原因 |
|------|------|
| `transformers==4.45.2` | 按需安装，体积较大 |
| `torch==2.6.0` | 按需安装，体积较大 |
| `anthropic==0.39.0` | 按需安装，非必需 |
| `beautifulsoup4==4.12.2` | 已被其他解析器替代 |
| `lxml==4.9.3` | 按需安装 |
| `selenium==4.15.2` | 按需安装，体积较大 |
| `playwright==1.40.0` | 按需安装，体积较大 |
| `black==23.11.0` | 开发工具，不放入生产依赖 |
| `isort==5.12.0` | 开发工具，不放入生产依赖 |
| `flake8==6.1.0` | 开发工具，不放入生产依赖 |
| `pymysql==1.1.0` | 已更换为 asyncpg (PostgreSQL) |

### 新增的依赖（在 backend/requirements.txt）

| 包名 | 用途 |
|------|------|
| `asyncpg>=0.29.0` | PostgreSQL 异步驱动 |
| `aiohttp>=3.9.1` | 异步 HTTP 客户端/服务器 |
| `jieba>=0.42.1` | 中文分词库 |

### 版本更新的依赖

| 包名 | 旧版本 | 新版本 | 原因 |
|------|--------|--------|------|
| `fastapi` | 0.104.1 | >=0.109.0 | 新功能和性能改进 |
| `uvicorn` | 0.24.0 | >=0.27.0 | 兼容性更新 |
| `sqlalchemy` | 2.0.23 | >=2.0.25 | Bug 修复 |
| `neo4j` | 5.14.1 | >=5.15.0 | 新特性 |
| `pydantic` | 2.5.2 | >=2.5.3 | Bug 修复 |
| `openai` | 1.52.1 | >=1.10.0 | 兼容性更好 |
| `httpx` | 0.25.2 | >=0.26.0 | 性能改进 |

## 🚀 安装指南

### 后端依赖安装

```bash
# 1. 进入后端目录
cd backend

# 2. 激活虚拟环境
# Windows PowerShell
..\venv\Scripts\Activate.ps1
# Linux/Mac
source ../venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt
```

### 前端依赖安装

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 或使用模板文件（如果需要重置）
cd frontend
cp ../dev-setup/config/package.json .
npm install
```

## 📊 优势

### 1. 配置统一
- ✅ 只有一个后端依赖配置文件
- ✅ 避免版本冲突和混淆
- ✅ 易于维护和更新

### 2. 按需安装
- ✅ 移除大型依赖（torch, transformers）
- ✅ 移除可选依赖（anthropic, selenium）
- ✅ 减小安装体积和时间

### 3. 技术栈清晰
- ✅ 使用 PostgreSQL (asyncpg) 替代 MySQL
- ✅ 使用异步 HTTP (aiohttp)
- ✅ 中文处理支持 (jieba)

## ⚠️ 注意事项

### 数据库驱动变更

**重要**: 项目现在使用 **PostgreSQL** 而不是 **MySQL**。

如果需要使用 MySQL，需要：
1. 修改 `backend/requirements.txt`:
   ```diff
   - asyncpg>=0.29.0
   + pymysql>=1.1.0
   ```

2. 修改数据库连接字符串:
   ```python
   # PostgreSQL
   DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/dbname"
   
   # MySQL
   DATABASE_URL = "mysql+pymysql://user:pass@localhost:3306/dbname"
   ```

### 按需安装的依赖

如果需要使用以下功能，请手动安装：

```bash
# OpenAI 兼容模型（如需要本地部署）
pip install transformers torch

# Anthropic Claude
pip install anthropic

# 浏览器自动化
pip install selenium playwright

# HTML/XML 解析
pip install beautifulsoup4 lxml

# 代码质量工具
pip install black isort flake8
```

## 📝 文件位置

### 标准依赖配置
- **后端**: [`backend/requirements.txt`](backend/requirements.txt)
- **前端**: [`frontend/package.json`](frontend/package.json)

### 模板文件（用于参考）
- ~~**后端**: `dev-setup/config/requirements.txt`~~ - ❌ 已删除
- **前端**: [`dev-setup/config/package.json`](dev-setup/config/package.json) - ✅ 已更新

## 🔗 相关文档

- [`backend/requirements.txt`](backend/requirements.txt) - 后端依赖清单
- [`frontend/package.json`](frontend/package.json) - 前端依赖清单
- [`dev-setup/config/package.json`](dev-setup/config/package.json) - 前端依赖模板
- [`dev-setup/README.md`](dev-setup/README.md) - 开发环境设置指南

## ✅ 验收清单

- [x] 删除 `dev-setup/config/requirements.txt`
- [x] 更新 `dev-setup/config/package.json`
- [x] 验证 `backend/requirements.txt` 完整性
- [x] 验证 `frontend/package.json` 完整性
- [x] 同步到 GitHub 仓库
- [ ] 测试依赖安装（由用户执行）

---

**更新版本**: v2.1.0  
**更新日期**: 2026-03-11  
**状态**: ✅ 已完成  
**下次检查**: 安装测试后确认所有功能正常
