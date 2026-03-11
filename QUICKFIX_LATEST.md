# 紧急修复说明 - PyTorch 版本和 npm 检测

## 📅 修复时间
2026-03-11

## 🐛 问题汇总

### 1. PyTorch 版本不存在 ❌

**错误信息**:
```
ERROR: Could not find a version that satisfies the requirement torch==2.4.1 
(from versions: 2.6.0, 2.7.0, 2.7.1, 2.8.0, 2.9.0, 2.9.1, 2.10.0)
```

**原因**:
- PyTorch 在您的 Python 环境中最低可用版本是 2.6.0
- 之前指定的 2.4.1 版本不存在

**✅ 已修复**:
- 更新 `torch` 版本为 **2.6.0**
- 文件：`backend/requirements.txt`

---

### 2. npm 检测失败 ❌

**错误信息**:
```
✗ npm 未安装，请先安装 Node.js
```

**原因**:
- Windows 下 npm 可能以 `.cmd` 或 `.ps1` 脚本形式存在
- 之前的检查逻辑没有正确处理这些脚本文件
- 没有通过 Node.js 安装路径推断 npm 位置

**✅ 已修复**:
- 添加 `npm.ps1` 路径检查
- 通过 `node` 路径自动推断 `npm` 位置
- 增强 `.cmd` 和 `.ps1` 文件的 shell 执行逻辑
- 支持从 stderr 读取版本信息
- 文件：`setup/check_env.py`

---

## 🔧 修复详情

### PyTorch 版本更新
```diff
# AI/ML
transformers==4.45.2
- torch==2.4.1
+ torch==2.6.0
openai==1.52.1
anthropic==0.39.0
```

### npm 检测增强

**新增逻辑**:
```python
# 检查 npm - 增强检查逻辑
installed, version = self.check_command('npm')
if not installed:
    # 尝试通过 node 路径推断 npm 路径
    node_path = shutil.which('node')
    if node_path:
        node_dir = Path(node_path).parent
        npm_paths = [
            node_dir / 'npm.cmd',
            node_dir / 'npm.ps1',
            node_dir / 'npm',
        ]
        for npm_path in npm_paths:
            if npm_path.exists():
                try:
                    result = subprocess.run(
                        [str(npm_path), '--version'],
                        capture_output=True,
                        text=True,
                        timeout=10,
                        shell=True
                    )
                    if result.returncode == 0:
                        installed = True
                        version = result.stdout.strip() or result.stderr.strip()
                        break
                except:
                    continue
```

---

## ✅ 测试步骤

### 1. 测试环境检查
```bash
python setup/check_env.py --check
```

**预期输出**:
```
→ 检查 Node.js 环境...
✓ Node.js v20.x.x 已安装
✓ npm 10.x.x 已安装
```

### 2. 测试依赖安装
```bash
python setup/check_env.py --install
```

**预期输出**:
```
→ 安装后端依赖...
✓ 后端依赖安装成功
```

---

## 🎯 改进内容

### 代码改进
- ✅ 更新 PyTorch 到可用版本 2.6.0
- ✅ 增强 npm 检测逻辑
- ✅ 支持多种 npm 安装位置
- ✅ 改进脚本文件执行方式

### 功能增强
- ✅ 自动通过 node 路径查找 npm
- ✅ 支持 .cmd 和 .ps1 脚本
- ✅ 更可靠的版本检测

---

## 📊 修改文件

| 文件 | 修改内容 | 状态 |
|------|---------|------|
| `backend/requirements.txt` | PyTorch 2.4.1 → 2.6.0 | ✅ 已修复 |
| `setup/check_env.py` | 增强 npm 检测 | ✅ 已修复 |

---

## 🔗 相关提交

- Commit: `f33fcf3c87e9e4f3c36286cddfa56f72969506fc`
- 仓库：https://github.com/MrJar2005XYY/APT_Attack_BIGHomework

---

## ⚠️ 如果仍有问题

### PyTorch 安装失败
```bash
# 手动安装 PyTorch
pip install torch==2.6.0 -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用官方源
pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu118
```

### npm 仍然检测不到
```bash
# 检查 Node.js 安装
node --version
npm --version

# 如果 npm 未安装，重新安装 Node.js
# 从 https://nodejs.org/ 下载并安装

# 检查 PATH 环境变量
echo %PATH%

# 确认 npm.cmd 存在位置
where npm
```

---

**修复版本**: v1.1.1  
**状态**: ✅ 已修复并上传到 GitHub  
**更新时间**: 2026-03-11
