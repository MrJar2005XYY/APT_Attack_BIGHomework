# 环境检查脚本修复说明

## 📅 修复日期
2026-03-11

## 🐛 修复的问题

### 1. PyTorch 版本不存在问题 ✅

**问题描述**:
```
ERROR: Could not find a version that satisfies the requirement torch==2.1.1 
(from versions: 2.6.0, 2.7.0, 2.7.1, 2.8.0, 2.9.0, 2.9.1, 2.10.0)
```

**原因**:
- `requirements.txt` 中指定的 `torch==2.1.1` 版本在 PyPI 上不存在

**解决方案**:
- 更新 `backend/requirements.txt` 中的依赖版本为最新可用版本：
  - `torch`: 2.1.1 → **2.4.1**
  - `transformers`: 4.35.2 → **4.45.2**
  - `openai`: 1.3.5 → **1.52.1**
  - `anthropic`: 0.7.0 → **0.39.0**

**修改文件**:
- [`backend/requirements.txt`](backend/requirements.txt)

---

### 2. Node.js 检测失败问题 ✅

**问题描述**:
- 脚本无法检测到本地安装的 Node.js
- 即使 Node.js 已安装，脚本也显示"Node.js 未安装"

**原因**:
- Windows 系统下，某些命令需要通过 shell 执行
- Node.js 可能安装在非标准路径
- 某些程序的版本信息输出到 stderr 而非 stdout

**解决方案**:

#### 增强 `check_command()` 方法
```python
def check_command(self, cmd: str) -> Tuple[bool, Optional[str]]:
    """检查命令是否可用"""
    try:
        # Windows 下使用 shell
        result = subprocess.run(
            [cmd, '--version'],
            capture_output=True,
            text=True,
            timeout=10,
            shell=(platform.system() == 'Windows')
        )
        # 检查 stdout 和 stderr
        if result.returncode == 0 and result.stdout:
            return True, result.stdout.strip().split('\n')[0]
        if result.stderr.strip():
            return True, result.stderr.strip().split('\n')[0]
        return False, None
    except (subprocess.SubprocessError, FileNotFoundError):
        # Windows 特殊处理：尝试常见安装路径
        if platform.system() == 'Windows':
            return self._check_windows_command(cmd)
        return False, None
```

#### 新增 `_check_windows_command()` 方法
检查 Windows 常见安装路径：
- `C:\Program Files\nodejs\node.exe`
- `C:\Program Files (x86)\nodejs\node.exe`
- `~\AppData\Roaming\npm\node.exe`
- Python 的多个版本路径

**修改文件**:
- [`setup/check_env.py`](setup/check_env.py)

---

### 3. Docker 启动失败但无详细错误信息 ✅

**问题描述**:
- 脚本能检测到 Docker 环境
- Docker 容器启动失败
- 没有详细的错误诊断信息

**原因**:
- 缺少 Docker 服务状态检查
- 错误处理过于简单
- 没有端口冲突、权限问题等常见问题的诊断

**解决方案**:

#### 增强 Docker 检查
```python
# 检查 Docker 是否正在运行
result = subprocess.run(['docker', 'info'], capture_output=True, text=True, timeout=5)
if result.returncode != 0:
    print_error("Docker 服务未运行")
    if 'permission denied' in result.stderr.lower():
        print_warning("权限问题：尝试以管理员身份运行此脚本")
    return False
```

#### 改进 Docker Compose 支持
- 支持 Docker Compose V1 (`docker-compose`) 和 V2 (`docker compose`)
- 先停止旧容器再启动新容器
- 增加超时设置和详细错误输出

#### 新增 `_diagnose_docker_issue()` 方法
自动诊断常见 Docker 问题：
- **端口冲突**: `port is already allocated`
- **权限问题**: `permission denied` / `access is denied`
- **Docker 守护进程**: `cannot connect to the docker daemon`
- **镜像拉取失败**: `image not found` / `pull access denied`

#### 新增 `_verify_docker_containers()` 方法
启动后验证容器状态：
- 显示运行中的容器列表
- 检查 MySQL 和 Neo4j 容器是否正常运行
- 显示容器状态和端口信息

#### 改进错误输出
提供具体的解决方案：
```
✗ MySQL 启动失败：端口 3306 被占用
ℹ 请停止占用 3306 端口的程序或使用其他端口

✗ Neo4j 启动失败：权限不足
ℹ 请以管理员身份运行此脚本
```

**修改文件**:
- [`setup/check_env.py`](setup/check_env.py)

---

## 📝 测试建议

### 测试步骤

1. **测试 Node.js 检测**
   ```bash
   python setup/check_env.py --check
   ```
   应该能正确显示 Node.js 版本

2. **测试依赖安装**
   ```bash
   python setup/check_env.py --install
   ```
   PyTorch 应该能正常安装

3. **测试 Docker 启动**（以管理员身份运行）
   ```bash
   # Windows: 右键 → 以管理员身份运行
   python setup/check_env.py --install
   # 选择 'y' 安装 Docker 服务
   ```

### 预期输出

#### Node.js 检测成功
```
→ 检查 Node.js 环境...
✓ Node.js v20.10.0 已安装
✓ npm 10.2.3 已安装
```

#### PyTorch 安装成功
```
→ 安装后端依赖...
✓ 后端依赖安装成功
```

#### Docker 启动成功
```
→ 使用 Docker 安装数据库服务...
ℹ Docker 版本：Docker version 24.0.7, build afdd53b
ℹ 使用 docker-compose 启动服务...
✓ 数据库服务启动成功

验证容器状态...

运行中的容器:
NAMES         STATUS         PORTS
mysql-apt     Up 2 seconds   0.0.0.0:3306->3306/tcp
neo4j-apt     Up 2 seconds   0.0.0.0:7474->7474/tcp, 0.0.0.0:7687->7687/tcp

✓ MySQL 容器运行正常
✓ Neo4j 容器运行正常
```

---

## 🔧 手动修复指南

### 如果仍然遇到问题

#### 1. PyTorch 安装失败
```bash
# 手动安装最新 PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 或使用国内镜像
pip install torch -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 2. Node.js 检测失败
```bash
# 检查 Node.js 是否安装
node --version

# 如果未找到，检查 PATH
echo $PATH  # macOS/Linux
echo %PATH%  # Windows

# 重新安装 Node.js
# 从 https://nodejs.org/ 下载并安装
```

#### 3. Docker 启动失败
```bash
# 检查 Docker 状态
docker info

# 检查端口占用
netstat -ano | findstr :3306  # Windows
sudo lsof -i :3306  # macOS/Linux

# 停止占用端口的进程
# Windows: taskkill /PID <PID> /F
# macOS/Linux: kill -9 <PID>

# 手动启动 Docker 容器
docker run --name mysql-apt -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:8.0
docker run --name neo4j-apt -e NEO4J_AUTH=neo4j/neo4j123 -p 7474:7474 -p 7687:7687 -d neo4j:5.14
```

---

## 📊 修改文件清单

| 文件 | 修改内容 | 影响范围 |
|------|---------|---------|
| `backend/requirements.txt` | 更新 PyTorch 等依赖版本 | 后端依赖安装 |
| `setup/check_env.py` | 增强 Node.js 检测 | 环境检查 |
| `setup/check_env.py` | 改进 Docker 启动和诊断 | Docker 部署 |
| `setup/check_env.py` | 新增错误诊断功能 | 故障排查 |

---

## 🎯 改进总结

### 代码改进
- ✅ 增强 Windows 兼容性（shell 参数、路径检查）
- ✅ 改进错误处理（详细错误信息、诊断建议）
- ✅ 新增诊断功能（自动识别常见问题）
- ✅ 改进用户体验（彩色输出、清晰的解决方案）

### 功能增强
- ✅ 支持 Docker Compose V1 和 V2
- ✅ 容器状态验证
- ✅ 端口冲突检测
- ✅ 权限问题识别
- ✅ 镜像拉取失败处理

### 文档完善
- ✅ 详细的修复说明
- ✅ 测试步骤指南
- ✅ 故障排查手册
- ✅ 常见问题解答

---

## 🔗 相关资源

- [环境检查脚本使用指南](setup/README.md)
- [开发环境要求.md](开发环境要求.md)
- [开发文档.md](开发文档.md)
- [Docker 官方文档](https://docs.docker.com/)
- [PyTorch 安装指南](https://pytorch.org/get-started/locally/)

---

**修复版本**: v1.1.0  
**更新日期**: 2026-03-11  
**状态**: ✅ 已修复并上传到 GitHub
