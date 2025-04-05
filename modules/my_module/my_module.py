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

        # 一个简单的计算器
        @server.tool()
        def add(a: int, b: int) -> int:
            """两个整数的和相加"""
            return a + b

        @server.resource("my://resource")
        def my_resource() -> str:
            """自定义资源"""
            return "资源内容"