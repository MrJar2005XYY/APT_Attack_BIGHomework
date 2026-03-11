# 环境检查脚本更新日志

## 📅 更新日期
2026-03-11

## 🎯 更新内容

### 新增文件

1. **setup/check_env.py** - 环境检查与安装脚本
   - 自动检查 Python、Node.js、Git、MySQL、Neo4j、Docker 等环境
   - 支持交互式安装缺失的依赖
   - 使用国内镜像源加速安装（清华 PyPI、淘宝 npm）
   - 支持 Docker 一键部署数据库服务
   - 详细的检查结果和错误提示
   - 支持命令行参数：--check, --install, --help

2. **.env.example** - 环境变量配置示例
   - 完整的数据库配置示例
   - 多 LLM 提供商配置（OpenAI、Azure、Anthropic、Custom）
   - 应用配置、API 配置、采集器配置
   - 文件存储、日志等配置项

3. **backend/requirements.txt** - Python 依赖列表
   - FastAPI 及 Web 框架依赖
   - 数据库驱动（MySQL、Neo4j）
   - AI/ML 库（transformers、torch、openai、anthropic）
   - 网络请求、任务调度、数据验证等库
   - 测试和代码质量工具

4. **frontend/package.json** - Node.js 依赖列表
   - Vue 3 及相关生态（vue-router、pinia）
   - Element Plus UI 组件库
   - ECharts 图表库
   - 开发工具（Vite、TypeScript、ESLint、Prettier）

5. **setup/README.md** - 环境检查脚本使用指南
   - 快速开始指南
   - 检查项目说明
   - 自动安装功能详解
   - 输出示例
   - 手动安装指南
   - 常见问题解答

6. **开发环境要求.md** - 详细的本地开发环境配置指南
   - 软件要求清单
   - 开发环境配置
   - 数据库要求
   - 后端和前端开发环境
   - 可选工具
   - 快速启动指南

## 🚀 使用方法

### 快速检查环境
```bash
cd APT_Attack_BIGHomework
python setup/check_env.py
```

### 自动安装缺失环境
```bash
python setup/check_env.py --install
```

### 查看帮助
```bash
python setup/check_env.py --help
```

## ✨ 主要特性

1. **智能检测** - 自动检测所有必需的开发环境
2. **交互式安装** - 发现问题后询问是否自动安装
3. **镜像加速** - 使用国内镜像源加速依赖安装
4. **Docker 支持** - 可选的 Docker 容器化部署
5. **详细报告** - 提供清晰的检查结果和错误提示
6. **跨平台** - 支持 Windows、macOS、Linux

## 📊 检查项目

- ✅ Python 3.10+
- ✅ Node.js 18.x+
- ✅ Git
- ✅ MySQL 8.0+
- ✅ Neo4j 5.x
- ✅ Docker（可选）
- ✅ Python 虚拟环境
- ✅ 后端依赖
- ✅ 前端依赖
- ✅ 环境变量配置

## 🔧 技术实现

### EnvironmentChecker 类
- 检查命令可用性
- 检查各软件版本
- 检查 Docker 容器状态
- 检查项目依赖
- 生成检查报告

### EnvironmentInstaller 类
- 创建 Python 虚拟环境
- 安装后端依赖（使用镜像源）
- 安装前端依赖（使用镜像源）
- 创建环境变量文件
- 启动 Docker 服务

### 颜色输出
- 绿色 ✓ - 成功
- 红色 ✗ - 错误
- 黄色 ⚠ - 警告
- 蓝色 ℹ - 信息
- 青色 → - 步骤

## 📝 输出示例

脚本提供美观的彩色输出，包括：
- 进度指示
- 检查结果
- 问题汇总
- 安装统计

## 🛠️ 故障排除

详见 [setup/README.md](setup/README.md) 中的常见问题部分。

## 📞 相关文档

- [开发文档.md](开发文档.md) - 完整的系统开发文档
- [开发环境要求.md](开发环境要求.md) - 详细的本地开发环境配置指南
- [开发文档_llm_update.md](开发文档_llm_update.md) - LLM API 增强模块补充文档
- [setup/README.md](setup/README.md) - 环境检查脚本使用指南

## 🎉 贡献

此脚本旨在简化开发环境配置流程，提高开发效率。如有问题或建议，欢迎提交 Issue 或 Pull Request。

---

**更新时间**: 2026-03-11  
**版本**: v1.0.0  
**作者**: APT 威胁情报智能抽取系统开发团队
