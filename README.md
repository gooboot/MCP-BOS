# MCP-BOS: 可扩展的MCP服务器框架

一个基于Model Context Protocol (MCP)的模块化、可扩展服务器框架，专为与Claude Desktop集成设计。

## 架构思想

┌─────────────────────────────────────────────────────────────────┐
│                          MCP Server                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐            │
│  │   核心系统   │   │  模块注册表  │   │  配置管理器  │            │
│  └─────────────┘   └─────────────┘   └─────────────┘            │
│         │                 │                 │                    │
│         └────────────────┬─────────────────┘                    │
│                          │                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     模块加载器                            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                       模块池                             │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │    │
│  │  │ 模块 A   │  │ 模块 B   │  │ 模块 C   │  │ 模块 D   │...  │    │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
│                          ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    FastMCP适配器                         │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
└────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│                      Claude Desktop                            │
└────────────────────────────────────────────────────────────────┘

MCP-BOS框架采用了现代化的模块化架构设计，主要设计理念包括：

### 模块化设计
整个框架以模块为中心，每个功能都被封装在独立的模块中，使功能扩展变得简单直观。模块之间相互独立，但又通过标准接口相互协作，形成一个完整的服务生态。

### 自动发现机制
框架能够自动发现`modules`目录下的模块，无需手动注册每个模块。这种"约定优于配置"的方式大幅降低了扩展成本。

### 声明式配置
通过`config.json`文件进行全局和模块级别的配置，使框架具有很高的灵活性，可以根据不同需求启用或禁用特定模块。

### 分层架构
框架分为核心层和模块层，核心层负责框架基础功能，模块层负责具体业务功能，这种分层设计使框架更加健壮和可维护。


## 目录结构说明

```
mcp-bos/
├── config.json             # 全局配置文件
├── main.py                 # 主入口文件
├── core/                   # 核心系统
│   ├── __init__.py
│   ├── module_registry.py  # 模块注册表
│   ├── module_loader.py    # 模块加载器
│   ├── module_interface.py # 模块接口定义
│   ├── config_manager.py   # 配置管理器
│   └── server.py           # FastMCP服务器适配
├── modules/                # 功能模块目录
│   ├── __init__.py
│   ├── hello_world/        # Hello World示例模块
│   │   ├── __init__.py
│   │   └── hello.py
│   └── ...                 # 其他功能模块
├── utils/                  # 工具函数
│   ├── __init__.py
│   └── helpers.py
└── README.md               # 项目文档
```

### 核心组件说明

- **main.py**: 框架入口点，负责初始化和启动服务器
- **core/**: 核心组件目录
  - **module_interface.py**: 定义所有模块必须实现的接口
  - **module_registry.py**: 管理已注册的模块
  - **module_loader.py**: 自动发现和加载模块
  - **config_manager.py**: 加载和管理配置
  - **server.py**: 与FastMCP集成，提供服务器功能
- **modules/**: 功能模块目录，每个子目录是一个独立模块
- **utils/**: 通用工具函数

## 配置文件结构

`config.json`文件是框架的核心配置，分为全局配置和模块配置两部分：

```json
{
  "global": {
    "server_name": "MCP-BOS",
    "debug": true,
    "log_level": "INFO",
    "transport": "stdio",
    "dependencies": ["mcp[cli]"]
  },
  "modules": {
    "hello_world": {
      "enabled": true,
      "message": "Hello, {}!"
    },
    "module_name": {
      "enabled": false,
      "param1": "value1"
    }
  }
}
```

- **global**: 全局配置部分
  - **server_name**: 服务器名称
  - **debug**: 是否启用调试模式
  - **log_level**: 日志级别
  - **transport**: 传输协议，通常为"stdio"
  - **dependencies**: 依赖包列表

- **modules**: 模块配置部分，每个模块有自己的配置节
  - **enabled**: 是否启用该模块
  - 其他模块特定的配置参数

## 使用方法

### 安装

1. 克隆仓库:
```bash
git clone https://github.com/kinbos/mcp-bos.git
cd mcp-bos
```

2. 安装依赖:
```bash
uv pip install mcp[cli]
```

### 配置

编辑`config.json`文件来配置服务器和模块：

1. 设置服务器名称、日志级别等全局参数
2. 启用或禁用模块
3. 配置模块特定参数

### 运行

有以下几种方式运行服务器:

1. **直接运行**:
```bash
python main.py
```

2. **使用uv运行**:
```bash
uv run main.py
```

3. **与Claude Desktop集成**:
```bash
# 使用mcp CLI集成到Claude Desktop
mcp install main.py
```

4. **开发调试模式**:
```bash
# 使用mcp Inspector测试服务器
mcp inspect main.py
```

### 添加新模块

1. 在`modules`目录下创建一个新的模块目录:
```bash
mkdir modules/my_module
```

2. 创建必要的文件:
```bash
touch modules/my_module/__init__.py
touch modules/my_module/my_module.py
```

3. 实现模块接口:
```python
# modules/my_module/my_module.py
from core.module_interface import ModuleInterface

class MyModule(ModuleInterface):
    def get_info(self):
        return {
            "name": "my_module",
            "version": "1.0.0",
            "description": "我的自定义模块",
            "author": "kinbos 严富坤",
            "email": "fookinbos@gmail.com",
            "website": "htttps://www.yanfukun.com"
        }
        
    def register(self, server):
        @server.tool()
        def my_tool(param: str) -> str:
            """自定义工具"""
            return f"处理参数: {param}"
            
        @server.resource("my://resource")
        def my_resource() -> str:
            """自定义资源"""
            return "资源内容"
```

4. 导出模块类:
```python
# modules/my_module/__init__.py
from modules.my_module.my_module import MyModule

__all__ = ['MyModule']
```

5. 在配置文件中启用模块:
```json
{
  "modules": {
    "my_module": {
      "enabled": true,
      "custom_param": "value"
    }
  }
}
```

6. 重启服务器，新模块将被自动发现和加载

## 常见问题

### 模块未加载
- 检查模块目录结构是否正确
- 确认`__init__.py`文件是否导出了模块类
- 检查配置文件中模块是否启用
- 查看日志输出，了解详细错误信息

### 编码问题
如果在Windows环境下遇到中文编码问题，确保设置了正确的环境变量:
```json
"env": {
  "PYTHONIOENCODING": "utf-8"
}
```

### 服务器连接问题
- 确认Claude Desktop已正确配置
- 检查依赖是否正确安装
- 查看Claude Desktop日志文件

## 贡献指南

欢迎提交贡献，请遵循以下步骤:
1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 作者

- **kinbos 严富坤** - [个人网站](https://www.yanfukun.com)
- 邮箱: fookinbos@gmail.com

