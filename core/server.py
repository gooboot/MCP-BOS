"""
MCP Server适配器，整合核心系统和FastMCP

作者：kinbos 严富坤
邮箱：fookinbos@gmail.com
个人网站：htttps://www.yanfukun.com
"""

import os
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP, Context

# 重定向所有调试信息到标准错误输出
def debug_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# 确保mcp依赖已安装
try:
    from mcp.server.fastmcp import FastMCP, Context
except ImportError:
    debug_print("错误: 未找到mcp包，请执行以下命令安装:")
    debug_print("uv pip install mcp[cli]")
    sys.exit(1)

from core.config_manager import ConfigManager
from core.module_loader import ModuleLoader
from core.module_registry import ModuleRegistry

class MCPServer:
    """
    MCP Server适配器，整合核心系统和FastMCP
    """

    def __init__(self, config_path='config.json', modules_dir='modules'):
        """
        初始化MCP服务器

        Args:
            config_path: 配置文件路径
            modules_dir: 模块目录
        """
        # 初始化核心组件
        self.config_manager = ConfigManager(config_path)
        self.registry = ModuleRegistry()
        self.module_loader = ModuleLoader(modules_dir, self.registry, self.config_manager)

        # 创建FastMCP服务器实例
        global_config = self.config_manager.get_global_config()
        server_name = global_config.get('server_name', 'MCP Server')

        # 获取配置的依赖
        dependencies = global_config.get('dependencies', [])

        # 创建FastMCP实例
        self.server = FastMCP(
            server_name,
            dependencies=dependencies,
            log_level=global_config.get('log_level', 'INFO'),
            debug=global_config.get('debug', False)
        )

        # 注册核心工具
        self._register_core_tools()

    def _register_core_tools(self):
        """
        注册核心工具
        """
        # 注册服务器信息工具
        @self.server.tool()
        def server_info(ctx: Context) -> dict:
            """
            获取服务器信息

            Args:
                ctx: MCP上下文

            Returns:
                dict: 服务器信息
            """
            global_config = self.config_manager.get_global_config()

            return {
                "name": global_config.get('server_name', 'MCP Server'),
                "version": "1.0.0",
                "modules": self.registry.list_modules()
            }

    def initialize(self):
        """
        初始化服务器，加载模块

        Returns:
            self: 服务器实例，用于链式调用
        """
        # 加载启用的模块
        debug_print("开始加载模块...")
        modules = self.module_loader.load_enabled_modules()

        # 注册模块功能
        for module_name, module in self.registry.get_all_modules().items():
            try:
                module.register(self.server)
                debug_print(f"已注册模块功能: {module_name}")
            except Exception as e:
                debug_print(f"错误: 注册模块 {module_name} 功能失败: {e}")

        return self

    def run(self, transport='stdio'):
        """
        运行MCP服务器

        Args:
            transport: 传输协议，默认为stdio
        """
        global_config = self.config_manager.get_global_config()
        transport = global_config.get('transport', transport)

        # 运行服务器
        debug_print(f"启动MCP服务器，传输协议: {transport}")
        self.server.run(transport=transport)