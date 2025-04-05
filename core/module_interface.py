"""
模块接口定义

作者：kinbos 严富坤
邮箱：fookinbos@gmail.com
个人网站：htttps://www.yanfukun.com
"""


class ModuleInterface:
    """
    模块接口定义，所有模块都需要实现这个接口
    """

    def __init__(self, config=None):
        """
        初始化模块

        Args:
            config: 模块配置参数
        """
        self.config = config or {}

    def get_info(self):
        """
        获取模块信息

        Returns:
            dict: 包含模块名称、版本、作者等信息的字典
        """
        raise NotImplementedError

    def register(self, server):
        """
        向MCP服务器注册功能

        Args:
            server: FastMCP服务器实例
        """
        raise NotImplementedError