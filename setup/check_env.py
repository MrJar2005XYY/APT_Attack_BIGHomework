#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APT 威胁情报智能抽取系统 - 环境检查与安装脚本
自动检查开发环境并安装缺失的依赖
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from typing import Tuple, List, Optional
import json

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg: str):
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")

def print_error(msg: str):
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}")

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.RESET}")

def print_step(msg: str):
    print(f"{Colors.CYAN}{Colors.BOLD}→ {msg}{Colors.RESET}")

class EnvironmentChecker:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.results = {
            'python': {'installed': False, 'version': None, 'required': '3.10'},
            'node': {'installed': False, 'version': None, 'required': '18'},
            'git': {'installed': False, 'version': None},
            'mysql': {'installed': False, 'version': None, 'required': '8.0'},
            'neo4j': {'installed': False, 'version': None, 'required': '5.x'},
            'docker': {'installed': False, 'version': None},
            'backend_deps': {'installed': False},
            'frontend_deps': {'installed': False},
        }
        self.missing = []
        
    def check_command(self, cmd: str) -> Tuple[bool, Optional[str]]:
        """检查命令是否可用"""
        try:
            # 尝试直接运行命令
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                text=True,
                timeout=10,
                shell=(platform.system() == 'Windows')  # Windows 下使用 shell
            )
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0] if result.stdout else 'Unknown'
                return True, version
            # 如果失败，尝试 stderr（某些程序输出版本信息到 stderr）
            if result.stderr.strip():
                version = result.stderr.strip().split('\n')[0]
                return True, version
            return False, None
        except (subprocess.SubprocessError, FileNotFoundError):
            # Windows 特殊处理：尝试常见安装路径
            if platform.system() == 'Windows':
                return self._check_windows_command(cmd)
            return False, None
    
    def _check_windows_command(self, cmd: str) -> Tuple[bool, Optional[str]]:
        """Windows 下检查命令的增强方法"""
        # 常见安装路径
        common_paths = []
        
        if cmd == 'node':
            common_paths = [
                r"C:\Program Files\nodejs\node.exe",
                r"C:\Program Files (x86)\nodejs\node.exe",
                os.path.expanduser(r"~\AppData\Roaming\npm\node.exe"),
            ]
        elif cmd == 'npm':
            common_paths = [
                r"C:\Program Files\nodejs\npm.cmd",
                r"C:\Program Files (x86)\nodejs\npm.cmd",
                r"C:\Program Files\nodejs\npm.ps1",
            ]
        elif cmd == 'python':
            common_paths = [
                os.path.expanduser(r"~\AppData\Local\Programs\Python\Python310\python.exe"),
                os.path.expanduser(r"~\AppData\Local\Programs\Python\Python311\python.exe"),
                os.path.expanduser(r"~\AppData\Local\Programs\Python\Python312\python.exe"),
            ]
        
        for path in common_paths:
            if os.path.exists(path):
                try:
                    # 对于 .cmd 文件，需要使用 shell 执行
                    if path.endswith('.cmd') or path.endswith('.ps1'):
                        result = subprocess.run(
                            [path, '--version'],
                            capture_output=True,
                            text=True,
                            timeout=10,
                            shell=True
                        )
                    else:
                        result = subprocess.run(
                            [path, '--version'],
                            capture_output=True,
                            text=True,
                            timeout=10
                        )
                    
                    if result.returncode == 0 and result.stdout:
                        version = result.stdout.strip().split('\n')[0]
                        return True, version
                    # 某些情况下版本信息在 stderr
                    if result.stderr and result.stderr.strip():
                        version = result.stderr.strip().split('\n')[0]
                        return True, version
                except Exception as e:
                    continue
        
        return False, None
    
    def check_python(self):
        """检查 Python 环境"""
        print_step("检查 Python 环境...")
        
        # 检查 Python
        installed, version = self.check_command('python')
        if not installed:
            installed, version = self.check_command('python3')
        
        if installed:
            self.results['python']['installed'] = True
            self.results['python']['version'] = version
            
            # 提取版本号
            import re
            match = re.search(r'(\d+)\.(\d+)', version)
            if match:
                major, minor = int(match.group(1)), int(match.group(2))
                if major < 3 or (major == 3 and minor < 10):
                    print_error(f"Python 版本过低：{version} (需要 3.10+)")
                    self.missing.append('python_version')
                else:
                    print_success(f"Python {version} 已安装")
        else:
            print_error("Python 未安装")
            self.missing.append('python')
        
        # 检查 pip
        installed, version = self.check_command('pip')
        if not installed:
            installed, version = self.check_command('pip3')
        
        if installed:
            print_success(f"pip {version} 已安装")
        else:
            print_warning("pip 未安装")
    
    def check_node(self):
        """检查 Node.js 环境"""
        print_step("检查 Node.js 环境...")
        
        installed, version = self.check_command('node')
        if installed:
            self.results['node']['installed'] = True
            self.results['node']['version'] = version
            
            # 提取版本号
            import re
            match = re.search(r'v(\d+)\.', version)
            if match:
                major = int(match.group(1))
                if major < 18:
                    print_error(f"Node.js 版本过低：{version} (需要 18+)")
                    self.missing.append('node_version')
                else:
                    print_success(f"Node.js {version} 已安装")
        else:
            print_error("Node.js 未安装")
            self.missing.append('node')
        
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
        
        if installed:
            print_success(f"npm {version} 已安装")
        else:
            print_warning("npm 未安装")
    
    def check_git(self):
        """检查 Git"""
        print_step("检查 Git...")
        
        installed, version = self.check_command('git')
        if installed:
            self.results['git']['installed'] = True
            self.results['git']['version'] = version
            print_success(f"Git {version} 已安装")
        else:
            print_error("Git 未安装")
            self.missing.append('git')
    
    def check_mysql(self):
        """检查 MySQL"""
        print_step("检查 MySQL...")
        
        # 尝试 mysql 命令
        installed, version = self.check_command('mysql')
        if installed:
            self.results['mysql']['installed'] = True
            self.results['mysql']['version'] = version
            print_success(f"MySQL {version} 已安装")
            return
        
        # 检查 Docker 中的 MySQL
        try:
            result = subprocess.run(
                ['docker', 'ps', '--format', '{{.Names}}'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if 'mysql' in result.stdout.lower():
                print_success("MySQL (Docker) 已安装并运行")
                self.results['mysql']['installed'] = True
                return
        except:
            pass
        
        print_error("MySQL 未安装")
        self.missing.append('mysql')
    
    def check_neo4j(self):
        """检查 Neo4j"""
        print_step("检查 Neo4j...")
        
        # 检查 Docker 中的 Neo4j
        try:
            result = subprocess.run(
                ['docker', 'ps', '--format', '{{.Names}}'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if 'neo4j' in result.stdout.lower():
                print_success("Neo4j (Docker) 已安装并运行")
                self.results['neo4j']['installed'] = True
                return
        except:
            pass
        
        # 检查 neo4j 命令
        installed, version = self.check_command('neo4j')
        if installed:
            self.results['neo4j']['installed'] = True
            self.results['neo4j']['version'] = version
            print_success(f"Neo4j {version} 已安装")
        else:
            print_warning("Neo4j 未安装（可使用 Docker 安装）")
            self.missing.append('neo4j')
    
    def check_docker(self):
        """检查 Docker"""
        print_step("检查 Docker...")
        
        installed, version = self.check_command('docker')
        if installed:
            self.results['docker']['installed'] = True
            self.results['docker']['version'] = version
            print_success(f"Docker {version} 已安装")
            
            # 检查 docker-compose
            installed, version = self.check_command('docker-compose')
            if not installed:
                installed, version = self.check_command('docker compose')
            
            if installed:
                print_success(f"Docker Compose {version} 已安装")
            else:
                print_warning("Docker Compose 未安装")
        else:
            print_warning("Docker 未安装（可选，用于容器化部署）")
    
    def check_backend_deps(self):
        """检查后端依赖"""
        print_step("检查后端依赖...")
        
        backend_dir = self.project_root / 'backend'
        requirements_file = backend_dir / 'requirements.txt'
        
        if not requirements_file.exists():
            print_warning("未找到 requirements.txt")
            return
        
        # 检查虚拟环境
        venv_dir = self.project_root / 'venv'
        if not venv_dir.exists():
            venv_dir = backend_dir / 'venv'
        
        if venv_dir.exists():
            print_success("Python 虚拟环境已创建")
        else:
            print_warning("Python 虚拟环境未创建")
            self.missing.append('venv')
        
        # 检查关键包
        try:
            import fastapi
            import sqlalchemy
            import neo4j
            print_success("后端核心依赖已安装")
            self.results['backend_deps']['installed'] = True
        except ImportError as e:
            print_error(f"缺少后端依赖：{e.name}")
            self.missing.append('backend_deps')
    
    def check_frontend_deps(self):
        """检查前端依赖"""
        print_step("检查前端依赖...")
        
        frontend_dir = self.project_root / 'frontend'
        package_file = frontend_dir / 'package.json'
        
        if not package_file.exists():
            print_warning("未找到 package.json")
            return
        
        # 检查 node_modules
        node_modules = frontend_dir / 'node_modules'
        if node_modules.exists():
            print_success("前端依赖已安装 (node_modules 存在)")
            self.results['frontend_deps']['installed'] = True
        else:
            print_warning("前端依赖未安装 (node_modules 不存在)")
            self.missing.append('frontend_deps')
    
    def check_env_file(self):
        """检查环境变量文件"""
        print_step("检查环境变量配置...")
        
        env_example = self.project_root / '.env.example'
        env_file = self.project_root / '.env'
        
        if env_file.exists():
            print_success(".env 文件已存在")
        else:
            if env_example.exists():
                print_warning(".env 文件不存在，建议从 .env.example 复制")
                self.missing.append('env_file')
            else:
                print_warning("未找到 .env.example 文件")
    
    def run_all_checks(self):
        """运行所有检查"""
        print("\n" + "="*60)
        print(f"{Colors.BOLD}APT 威胁情报智能抽取系统 - 环境检查{Colors.RESET}")
        print("="*60 + "\n")
        
        self.check_python()
        self.check_node()
        self.check_git()
        self.check_mysql()
        self.check_neo4j()
        self.check_docker()
        self.check_backend_deps()
        self.check_frontend_deps()
        self.check_env_file()
        
        print("\n" + "="*60)
        print(f"{Colors.BOLD}检查结果汇总{Colors.RESET}")
        print("="*60)
        
        # 统计
        total = len([v for v in self.results.values() if isinstance(v, dict) and 'installed' in v])
        passed = len([v for v in self.results.values() if isinstance(v, dict) and 'installed' in v and v['installed']])
        
        print(f"\n总计：{total} 项检查，通过 {passed} 项")
        
        if self.missing:
            print(f"\n{Colors.RED}发现 {len(self.missing)} 个问题:{Colors.RESET}")
            for item in self.missing:
                print(f"  - {item}")
        else:
            print(f"\n{Colors.GREEN}✓ 所有环境检查通过！{Colors.RESET}")
        
        print()
        return len(self.missing) == 0

class EnvironmentInstaller:
    def __init__(self, project_root: Path):
        self.project_root = project_root
    
    def install_python_venv(self):
        """创建 Python 虚拟环境"""
        print_step("创建 Python 虚拟环境...")
        
        venv_dir = self.project_root / 'venv'
        
        try:
            subprocess.run(
                [sys.executable, '-m', 'venv', str(venv_dir)],
                check=True
            )
            print_success("Python 虚拟环境创建成功")
            return True
        except subprocess.SubprocessError as e:
            print_error(f"创建虚拟环境失败：{e}")
            return False
    
    def install_backend_deps(self):
        """安装后端依赖"""
        print_step("安装后端依赖...")
        
        requirements_file = self.project_root / 'backend' / 'requirements.txt'
        
        if not requirements_file.exists():
            print_error("未找到 requirements.txt")
            return False
        
        # 确定 pip 命令
        pip_cmd = 'pip'
        venv_dir = self.project_root / 'venv'
        
        if venv_dir.exists():
            if platform.system() == 'Windows':
                pip_cmd = str(venv_dir / 'Scripts' / 'pip.exe')
            else:
                pip_cmd = str(venv_dir / 'bin' / 'pip')
        
        try:
            # 使用国内镜像加速
            subprocess.run(
                [pip_cmd, 'install', '-r', str(requirements_file), 
                 '-i', 'https://pypi.tuna.tsinghua.edu.cn/simple'],
                check=True
            )
            print_success("后端依赖安装成功")
            return True
        except subprocess.SubprocessError as e:
            print_error(f"安装后端依赖失败：{e}")
            print_info("尝试不使用镜像源重新安装...")
            
            try:
                subprocess.run(
                    [pip_cmd, 'install', '-r', str(requirements_file)],
                    check=True
                )
                print_success("后端依赖安装成功")
                return True
            except:
                print_error("安装失败，请检查网络连接或手动安装")
                return False
    
    def install_frontend_deps(self):
        """安装前端依赖"""
        print_step("安装前端依赖...")
        
        frontend_dir = self.project_root / 'frontend'
        package_file = frontend_dir / 'package.json'
        
        if not package_file.exists():
            print_error("未找到 package.json")
            return False
        
        # 检查 npm
        npm_cmd = 'npm'
        try:
            subprocess.run([npm_cmd, '--version'], check=True, capture_output=True)
        except:
            print_error("npm 未安装，请先安装 Node.js")
            return False
        
        # 使用淘宝镜像
        try:
            subprocess.run(
                [npm_cmd, 'config', 'set', 'registry', 'https://registry.npmmirror.com'],
                cwd=str(frontend_dir),
                check=True
            )
            
            subprocess.run(
                [npm_cmd, 'install'],
                cwd=str(frontend_dir),
                check=True
            )
            print_success("前端依赖安装成功")
            return True
        except subprocess.SubprocessError as e:
            print_error(f"安装前端依赖失败：{e}")
            return False
    
    def create_env_file(self):
        """创建环境变量文件"""
        print_step("创建环境变量文件...")
        
        env_example = self.project_root / '.env.example'
        env_file = self.project_root / '.env'
        
        if env_file.exists():
            print_warning(".env 文件已存在，跳过")
            return True
        
        if env_example.exists():
            try:
                shutil.copy(env_example, env_file)
                print_success(".env 文件创建成功（从 .env.example 复制）")
                print_warning("请编辑 .env 文件配置数据库密码和 API Key")
                return True
            except Exception as e:
                print_error(f"复制文件失败：{e}")
                return False
        else:
            # 创建默认的 .env 文件
            default_env = """# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=apt_intelligence

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password

# 大模型配置
DEFAULT_LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
DEFAULT_LLM_MODEL=gpt-4-turbo-preview

# 应用配置
APP_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key-here
"""
            try:
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write(default_env)
                print_success(".env 文件创建成功")
                print_warning("请编辑 .env 文件配置数据库密码和 API Key")
                return True
            except Exception as e:
                print_error(f"创建文件失败：{e}")
                return False
    
    def install_docker_services(self):
        """使用 Docker 安装数据库服务"""
        print_step("使用 Docker 安装数据库服务...")
        
        # 检查 Docker
        try:
            result = subprocess.run(['docker', '--version'], check=True, capture_output=True, text=True)
            print_info(f"Docker 版本：{result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print_error(f"Docker 未安装或无法访问：{e}")
            print_info("请先安装 Docker Desktop: https://www.docker.com/products/docker-desktop")
            return False
        except FileNotFoundError:
            print_error("Docker 命令未找到")
            print_info("请确保 Docker 已安装并添加到系统 PATH")
            return False
        
        # 检查 Docker 是否正在运行
        try:
            result = subprocess.run(['docker', 'info'], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                print_error("Docker 服务未运行")
                print_info("请启动 Docker Desktop 或 Docker 服务")
                if 'permission denied' in result.stderr.lower() or 'access is denied' in result.stderr.lower():
                    print_warning("权限问题：尝试以管理员身份运行此脚本")
                return False
        except subprocess.TimeoutExpired:
            print_warning("Docker 响应超时，可能未正常运行")
            return False
        
        docker_compose_file = self.project_root / 'docker-compose.yml'
        
        if docker_compose_file.exists():
            print_info("使用 docker-compose 启动服务...")
            
            # 先尝试停止旧容器
            try:
                subprocess.run(
                    ['docker-compose', 'down'],
                    cwd=str(self.project_root),
                    capture_output=True,
                    timeout=30
                )
            except:
                pass
            
            try:
                # 尝试 docker-compose
                result = subprocess.run(
                    ['docker-compose', 'up', '-d', 'mysql', 'neo4j'],
                    cwd=str(self.project_root),
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode == 0:
                    print_success("数据库服务启动成功")
                    self._verify_docker_containers()
                    return True
                else:
                    print_error(f"docker-compose 启动失败：{result.stderr}")
                    raise Exception(result.stderr)
            except Exception as e:
                # 尝试 docker compose (新版本)
                print_info("尝试使用 'docker compose' (Docker Compose V2)...")
                try:
                    result = subprocess.run(
                        ['docker', 'compose', 'up', '-d', 'mysql', 'neo4j'],
                        cwd=str(self.project_root),
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                    if result.returncode == 0:
                        print_success("数据库服务启动成功")
                        self._verify_docker_containers()
                        return True
                    else:
                        print_error(f"docker compose 启动失败：{result.stderr}")
                        self._diagnose_docker_issue(result.stderr)
                        return False
                except Exception as e:
                    print_error(f"启动服务失败：{e}")
                    self._diagnose_docker_issue(str(e))
                    return False
        else:
            print_warning("未找到 docker-compose.yml，手动启动 Docker 服务...")
            
            # 先停止可能存在的旧容器
            try:
                subprocess.run(['docker', 'stop', 'mysql-apt'], capture_output=True, timeout=10)
                subprocess.run(['docker', 'rm', 'mysql-apt'], capture_output=True, timeout=10)
            except:
                pass
            
            try:
                subprocess.run(['docker', 'stop', 'neo4j-apt'], capture_output=True, timeout=10)
                subprocess.run(['docker', 'rm', 'neo4j-apt'], capture_output=True, timeout=10)
            except:
                pass
            
            # 启动 MySQL
            print_info("启动 MySQL 容器...")
            try:
                result = subprocess.run([
                    'docker', 'run', '-d',
                    '--name', 'mysql-apt',
                    '-e', 'MYSQL_ROOT_PASSWORD=root',
                    '-e', 'MYSQL_DATABASE=apt_intelligence',
                    '-p', '3306:3306',
                    'mysql:8.0'
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print_success("MySQL Docker 容器启动成功")
                else:
                    error_msg = result.stderr
                    if 'port is already allocated' in error_msg.lower() or '3306' in error_msg:
                        print_error(f"MySQL 启动失败：端口 3306 被占用")
                        print_info("请停止占用 3306 端口的程序或使用其他端口")
                    elif 'permission denied' in error_msg.lower():
                        print_error(f"MySQL 启动失败：权限不足")
                        print_info("请以管理员身份运行此脚本")
                    else:
                        print_error(f"MySQL 启动失败：{error_msg}")
            except Exception as e:
                print_error(f"MySQL 启动异常：{e}")
            
            # 启动 Neo4j
            print_info("启动 Neo4j 容器...")
            try:
                result = subprocess.run([
                    'docker', 'run', '-d',
                    '--name', 'neo4j-apt',
                    '-e', 'NEO4J_AUTH=neo4j/neo4j123',
                    '-p', '7474:7474', '-p', '7687:7687',
                    'neo4j:5.14'
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print_success("Neo4j Docker 容器启动成功")
                    self._verify_docker_containers()
                    return True
                else:
                    error_msg = result.stderr
                    if 'port is already allocated' in error_msg.lower():
                        print_error(f"Neo4j 启动失败：端口 7474 或 7687 被占用")
                        print_info("请停止占用端口的程序或使用其他端口")
                    elif 'permission denied' in error_msg.lower():
                        print_error(f"Neo4j 启动失败：权限不足")
                        print_info("请以管理员身份运行此脚本")
                    else:
                        print_error(f"Neo4j 启动失败：{error_msg}")
                    return False
            except Exception as e:
                print_error(f"Neo4j 启动异常：{e}")
                return False
    
    def _diagnose_docker_issue(self, error_msg: str):
        """诊断 Docker 启动问题"""
        print_info("\n诊断信息:")
        
        if 'port is already allocated' in error_msg.lower():
            print_warning("检测到端口冲突")
            print_info("检查端口占用情况:")
            print_info("  Windows: netstat -ano | findstr :3306")
            print_info("  macOS/Linux: sudo lsof -i :3306")
        elif 'permission denied' in error_msg.lower() or 'access is denied' in error_msg.lower():
            print_warning("检测到权限问题")
            print_info("解决方案:")
            print_info("  1. 以管理员身份运行此脚本")
            print_info("  2. 或将当前用户添加到 docker 用户组")
        elif 'cannot connect to the docker daemon' in error_msg.lower():
            print_warning("无法连接到 Docker 守护进程")
            print_info("解决方案:")
            print_info("  1. 确保 Docker Desktop 已启动")
            print_info("  2. 检查 Docker 服务状态")
        elif 'image not found' in error_msg.lower() or 'pull access denied' in error_msg.lower():
            print_warning("Docker 镜像拉取失败")
            print_info("解决方案:")
            print_info("  1. 检查网络连接")
            print_info("  2. 配置 Docker 镜像加速器")
        else:
            print_info(f"错误详情：{error_msg}")
    
    def _verify_docker_containers(self):
        """验证 Docker 容器是否正常运行"""
        print_info("\n验证容器状态...")
        try:
            result = subprocess.run(
                ['docker', 'ps', '--format', 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print_info("\n运行中的容器:")
                print(result.stdout)
                
                # 检查关键容器
                if 'mysql-apt' in result.stdout or 'mysql' in result.stdout.lower():
                    print_success("MySQL 容器运行正常")
                else:
                    print_warning("MySQL 容器可能未运行")
                
                if 'neo4j-apt' in result.stdout or 'neo4j' in result.stdout.lower():
                    print_success("Neo4j 容器运行正常")
                else:
                    print_warning("Neo4j 容器可能未运行")
        except Exception as e:
            print_warning(f"无法验证容器状态：{e}")
    
    def run_all_installs(self):
        """运行所有安装步骤"""
        print("\n" + "="*60)
        print(f"{Colors.BOLD}APT 威胁情报智能抽取系统 - 环境安装{Colors.RESET}")
        print("="*60 + "\n")
        
        success_count = 0
        total = 0
        
        # 1. 创建虚拟环境
        if not (self.project_root / 'venv').exists():
            total += 1
            if self.install_python_venv():
                success_count += 1
        else:
            print_success("Python 虚拟环境已存在")
        
        # 2. 创建 .env 文件
        if not (self.project_root / '.env').exists():
            total += 1
            if self.create_env_file():
                success_count += 1
        else:
            print_success(".env 文件已存在")
        
        # 3. 安装后端依赖
        total += 1
        if self.install_backend_deps():
            success_count += 1
        
        # 4. 安装前端依赖
        total += 1
        if self.install_frontend_deps():
            success_count += 1
        
        # 5. Docker 服务（可选）
        print("\n")
        choice = input("是否使用 Docker 安装数据库服务？(y/n): ")
        if choice.lower() == 'y':
            total += 1
            if self.install_docker_services():
                success_count += 1
        
        print("\n" + "="*60)
        print(f"{Colors.BOLD}安装结果汇总{Colors.RESET}")
        print("="*60)
        print(f"总计：{total} 项安装，成功 {success_count} 项")
        
        if success_count == total:
            print(f"\n{Colors.GREEN}✓ 所有环境安装成功！{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}⚠ 部分安装失败，请检查错误信息{Colors.RESET}")
        
        print()

def main():
    """主函数"""
    project_root = Path(__file__).parent.parent
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--install' or sys.argv[1] == '-i':
            # 安装模式
            installer = EnvironmentInstaller(project_root)
            installer.run_all_installs()
        elif sys.argv[1] == '--check' or sys.argv[1] == '-c':
            # 检查模式
            checker = EnvironmentChecker()
            checker.run_all_checks()
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("用法：python check_env.py [选项]")
            print("\n选项:")
            print("  -c, --check    仅检查环境（默认）")
            print("  -i, --install  安装缺失的环境")
            print("  -h, --help     显示帮助信息")
        else:
            print_error(f"未知选项：{sys.argv[1]}")
            print("使用 --help 查看帮助")
    else:
        # 默认：先检查，如果发现问题则询问是否安装
        checker = EnvironmentChecker()
        all_ok = checker.run_all_checks()
        
        if not all_ok:
            print("\n" + "="*60)
            choice = input("是否自动安装缺失的环境？(y/n): ")
            print("="*60 + "\n")
            
            if choice.lower() == 'y':
                installer = EnvironmentInstaller(project_root)
                installer.run_all_installs()
                
                # 再次检查
                print("\n重新检查环境...\n")
                checker2 = EnvironmentChecker()
                checker2.run_all_checks()
            else:
                print_info("已跳过安装，请手动安装缺失的环境")

if __name__ == '__main__':
    main()
