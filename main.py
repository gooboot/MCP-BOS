"""
MCP Server主入口文件

作者：kinbos 严富坤
邮箱：fookinbos@gmail.com
个人网站：htttps://www.yanfukun.com
"""

import os
import sys
import json
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# 重定向所有调试信息到标准错误输出，保持标准输出纯净
def debug_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

debug_print(f"Python路径: {sys.path}")
debug_print(f"当前目录: {current_dir}")
debug_print(f"查找模块: {os.listdir(current_dir)}")

# 导入核心服务器类
try:
    # 首先确保mcp已安装
    try:
        import mcp
        # 也可以尝试导入具体的模块，以确保它可用
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        debug_print("错误: 未找到mcp包，请安装: uv pip install mcp[cli]")
        sys.exit(1)

    from core.server import MCPServer
    debug_print("成功导入MCPServer")
except ImportError as e:
    debug_print(f"导入错误: {e}")
    debug_print(f"core目录内容: {os.listdir(current_dir / 'core')}")
    raise

def main():
    """
    主入口函数
    """
    # 默认配置文件路径
    config_path = current_dir / 'config.json'

    # 默认模块目录
    modules_dir = current_dir / 'modules'

    # 创建并初始化MCP服务器
    try:
        server = MCPServer(
            config_path=config_path,
            modules_dir=modules_dir
        ).initialize()

        # 运行服务器
        server.run()
    except Exception as e:
        debug_print(f"错误: 启动MCP服务器失败: {e}")
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()