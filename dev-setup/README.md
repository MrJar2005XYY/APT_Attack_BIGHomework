# 开发环境检测与配置工具

本文件夹包含 APT 威胁情报智能抽取系统的完整开发环境检测、配置和安装工具。

## 📁 文件夹结构

```
dev-setup/
├── scripts/              # 可执行脚本
│   └── check_env.py     # 环境检查与安装主脚本
├── config/              # 配置文件模板
│   ├── .env.example     # 环境变量配置示例
│   ├── requirements.txt # Python 依赖列表
│   └── package.json     # Node.js 依赖列表
└── docs/                # 文档
    ├── README.md                    # 使用指南
    ├── BUGFIX_ENV_SCRIPT.md         # 已知问题修复
    ├── CHANGELOG_ENV_SETUP.md       # 更新日志
    ├── QUICKFIX_LATEST.md           # 紧急修复说明
    └── 开发环境要求.md               # 详细环境配置指南
```

## 🚀 快速开始

### 方式一：交互式安装（推荐）

```bash
# 1. 进入项目根目录
cd APT_Attack_BIGHomework

# 2. 运行环境检查脚本
python dev-setup/scripts/check_env.py
```

脚本会：
1. 自动检查所有必需的环境
2. 显示详细的检查结果
3. 如果发现问题，会询问是否自动安装
4. 执行安装后再次检查

### 方式二：命令行参数

```bash
# 仅检查环境（不安装）
python dev-setup/scripts/check_env.py --check

# 直接安装缺失的环境
python dev-setup/scripts/check_env.py --install

# 查看帮助
python dev-setup/scripts/check_env.py --help
```

## 📋 检查项目

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

1. **创建 Python 虚拟环境**
   ```bash
   python -m venv venv
   ```

2. **安装后端依赖**（使用清华镜像源加速）
   ```bash
   pip install -r dev-setup/config/requirements.txt
   ```

3. **安装前端依赖**（使用淘宝镜像源加速）
   ```bash
   cd frontend
   npm install
   ```

4. **创建环境变量文件**
   ```bash
   cp dev-setup/config/.env.example .env
   ```

5. **Docker 服务安装**（可选）
   ```bash
   docker-compose up -d mysql neo4j
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

→ 检查 Docker...
✓ Docker 24.0.7 已安装
✓ Docker Compose 2.21.0 已安装

============================================================
检查结果汇总
============================================================

总计：8 项检查，通过 8 项

✓ 所有环境检查通过！
```

### 安装模式输出
```
============================================================
APT 威胁情报智能抽取系统 - 环境安装
============================================================

→ 创建 Python 虚拟环境...
✓ Python 虚拟环境创建成功

→ 安装后端依赖...
✓ 后端依赖安装成功

→ 安装前端依赖...
✓ 前端依赖安装成功

============================================================
安装结果汇总
============================================================
总计：5 项安装，成功 5 项

✓ 所有环境安装成功！
```

## 🛠️ 手动配置指南

### 1. 安装 Python
- Windows: https://www.python.org/downloads/
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
pip install -r dev-setup/config/requirements.txt

# 前端
cd frontend
npm install
```

## ⚠️ 常见问题

### Q1: pip 安装依赖失败
**解决方案**: 使用国内镜像源
```bash
pip install -r dev-setup/config/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
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
# Windows
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
1. 查看脚本输出的详细错误信息
2. 查阅 `docs/` 文件夹中的文档
3. 查看项目的 `开发文档.md`
4. 联系开发团队

## 📚 相关文档

- **docs/README.md** - 环境检查脚本详细使用指南
- **docs/开发环境要求.md** - 详细的本地开发环境配置指南
- **docs/BUGFIX_ENV_SCRIPT.md** - 已知问题修复记录
- **docs/QUICKFIX_LATEST.md** - 紧急修复说明
- **docs/CHANGELOG_ENV_SETUP.md** - 更新日志
- **开发文档.md** - 完整的系统开发文档

---

**版本**: v1.1.1  
**最后更新**: 2026-03-11  
**维护**: APT 威胁情报智能抽取系统开发团队
