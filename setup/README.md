# 环境检查与安装脚本使用指南

## 📋 脚本说明

本项目提供了一键式环境检查和安装脚本，自动检测开发环境并安装缺失的依赖。

## 🎯 脚本位置

```
APT_Attack_BIGHomework/
├── setup/
│   └── check_env.py          # 环境检查与安装脚本
├── .env.example              # 环境变量配置示例
├── backend/
│   └── requirements.txt      # Python 依赖列表
└── frontend/
    └── package.json          # Node.js 依赖列表
```

## 🚀 快速开始

### 方式一：交互式安装（推荐）

```bash
# 1. 进入项目目录
cd APT_Attack_BIGHomework

# 2. 运行脚本（自动检查并提示安装）
python setup/check_env.py
```

脚本会：
1. 自动检查所有必需的环境
2. 显示检查结果
3. 如果发现问题，会询问是否自动安装
4. 执行安装后再次检查

### 方式二：命令行参数

```bash
# 仅检查环境（不安装）
python setup/check_env.py --check

# 或直接运行（默认就是检查模式）
python setup/check_env.py

# 直接安装缺失的环境
python setup/check_env.py --install

# 查看帮助
python setup/check_env.py --help
```

## 📝 检查项目

脚本会检查以下内容：

### 基础环境
- ✅ Python 3.10+
- ✅ Node.js 18.x+
- ✅ Git
- ✅ pip 和 npm

### 数据库
- ✅ MySQL 8.0+
- ✅ Neo4j 5.x
- ✅ Docker（可选，用于容器化部署）

### 项目依赖
- ✅ Python 虚拟环境
- ✅ 后端依赖（requirements.txt）
- ✅ 前端依赖（package.json）
- ✅ 环境变量配置文件（.env）

## 🔧 自动安装功能

脚本可以自动安装以下内容：

### 1. 创建 Python 虚拟环境
```bash
# 在项目根目录创建 venv 文件夹
python -m venv venv
```

### 2. 安装后端依赖
```bash
# 使用清华镜像源加速安装
pip install -r backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 安装前端依赖
```bash
# 使用淘宝镜像源加速安装
cd frontend
npm config set registry https://registry.npmmirror.com
npm install
```

### 4. 创建环境变量文件
```bash
# 从 .env.example 复制创建 .env
cp .env.example .env
```

### 5. Docker 服务安装（可选）
```bash
# 使用 Docker Compose 启动数据库服务
docker-compose up -d mysql neo4j

# 或使用单个 Docker 命令
docker run --name mysql-apt -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:8.0
docker run --name neo4j-apt -e NEO4J_AUTH=neo4j/neo4j123 -p 7474:7474 -p 7687:7687 -d neo4j:5.14
```

## 📊 输出示例

### 检查模式输出
```
============================================================
APT 威胁情报智能抽取系统 - 环境检查
============================================================

→ 检查 Python 环境...
✓ Python 3.11.5 已安装
✓ pip 23.2.1 已安装

→ 检查 Node.js 环境...
✓ Node.js v18.18.2 已安装
✓ npm 10.2.0 已安装

→ 检查 Git...
✓ Git 2.42.0 已安装

→ 检查 MySQL...
✗ MySQL 未安装

→ 检查 Neo4j...
⚠ Neo4j 未安装（可使用 Docker 安装）

→ 检查 Docker...
✓ Docker 24.0.7 已安装
✓ Docker Compose 2.21.0 已安装

→ 检查后端依赖...
✓ Python 虚拟环境已创建
✓ 后端核心依赖已安装

→ 检查前端依赖...
⚠ 前端依赖未安装 (node_modules 不存在)

→ 检查环境变量配置...
⚠ .env 文件不存在，建议从 .env.example 复制

============================================================
检查结果汇总
============================================================

总计：8 项检查，通过 5 项

发现 3 个问题:
  - mysql
  - neo4j
  - frontend_deps
```

### 安装模式输出
```
============================================================
APT 威胁情报智能抽取系统 - 环境安装
============================================================

→ 创建 Python 虚拟环境...
✓ Python 虚拟环境创建成功

→ 创建环境变量文件...
✓ .env 文件创建成功（从 .env.example 复制）
⚠ 请编辑 .env 文件配置数据库密码和 API Key

→ 安装后端依赖...
✓ 后端依赖安装成功

→ 安装前端依赖...
✓ 前端依赖安装成功


是否使用 Docker 安装数据库服务？(y/n): y

→ 使用 Docker 安装数据库服务...
✓ 数据库服务启动成功

============================================================
安装结果汇总
============================================================
总计：5 项安装，成功 5 项

✓ 所有环境安装成功！
```

## 🛠️ 手动安装指南

如果自动安装失败，可以手动安装：

### 1. 安装 Python
- Windows: 从 https://www.python.org/downloads/ 下载
- macOS: `brew install python@3.10`
- Linux: `sudo apt install python3.10 python3-pip`

### 2. 安装 Node.js
- 从 https://nodejs.org/ 下载 LTS 版本
- macOS: `brew install node@18`
- Linux: 使用 NodeSource 仓库

### 3. 安装 MySQL
- Windows: 使用 MySQL Installer
- macOS: `brew install mysql@8.0`
- Docker: `docker run --name mysql -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:8.0`

### 4. 安装 Neo4j
- 从 https://neo4j.com/download/ 下载
- Docker: `docker run --name neo4j -e NEO4J_AUTH=neo4j/password -p 7474:7474 -p 7687:7687 -d neo4j:5.14`

### 5. 安装依赖
```bash
# 后端
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# 前端
cd frontend
npm install
```

## ⚠️ 常见问题

### Q1: pip 安装依赖失败
**解决方案**: 使用国内镜像源
```bash
pip install -r backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: npm install 太慢
**解决方案**: 使用淘宝镜像
```bash
npm config set registry https://registry.npmmirror.com
npm install
```

### Q3: Docker 容器启动失败
**解决方案**: 检查端口占用
```bash
# Windows/Mac
netstat -ano | findstr :3306
netstat -ano | findstr :7474

# Linux
sudo netstat -tulpn | grep :3306
sudo netstat -tulpn | grep :7474
```

### Q4: Python 版本过低
**解决方案**: 升级 Python 到 3.10+

### Q5: 权限错误（Linux/Mac）
**解决方案**: 使用 sudo 或修改目录权限
```bash
sudo chown -R $USER:$USER /path/to/project
```

## 📞 获取帮助

如果遇到问题：
1. 查看脚本输出的错误信息
2. 检查本文档的常见问题部分
3. 查看项目的开发文档.md
4. 联系开发团队

## 🔗 相关文档

- [开发文档.md](开发文档.md) - 完整的系统开发文档
- [开发环境要求.md](开发环境要求.md) - 详细的本地开发环境配置指南
- [开发文档_llm_update.md](开发文档_llm_update.md) - LLM API 增强模块补充文档

---

祝使用顺利！🚀
