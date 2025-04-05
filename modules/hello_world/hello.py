"""
Hello World示例模块

作者：kinbos 严富坤
邮箱：fookinbos@gmail.com
个人网站：htttps://www.yanfukun.com
"""

from core.module_interface import ModuleInterface


class HelloWorldModule(ModuleInterface):
    """
    Hello World示例模块，展示了一个简单的MCP模块实现
    """

    def get_info(self):
        """
        获取模块信息

        Returns:
            dict: 模块信息
        """
        return {
            "name": "hello_world",
            "version": "1.0.0",
            "description": "Hello World示例模块",
            "author": "kinbos 严富坤",
            "email": "fookinbos@gmail.com",
            "website": "htttps://www.yanfukun.com"
        }

    def register(self, server):
        """
        向MCP服务器注册功能

        Args:
            server: FastMCP服务器实例
        """

        # 注册一个简单的工具
        @server.tool()
        def hello(name: str = "World") -> str:
            """
            返回问候消息

            Args:
                name: 要问候的名称

            Returns:
                str: 问候消息
            """
            message = self.config.get('message', 'Hello, {}!')
            return message.format(name)



        # 注册一个资源
        @server.resource("hello://greeting")
        def get_greeting() -> str:
            """
            获取问候消息

            Returns:
                str: 问候消息
            """
            return "Welcome to MCP Server!"

        # 注册一个提示模板
        @server.prompt()
        def hello_prompt(name: str = "User") -> str:
            """
            创建一个问候提示

            Args:
                name: 要问候的名称

            Returns:
                str: 问候提示
            """
            return f"Welcome, {name}! How can I assist you today?"