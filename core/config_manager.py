"""
配置管理器，负责加载和管理全局配置

作者：kinbos 严富坤
邮箱：fookinbos@gmail.com
个人网站：htttps://www.yanfukun.com
"""

import json
import os
from pathlib import Path


class ConfigManager:
    """
    配置管理器，负责加载和管理全局配置
    """

    def __init__(self, config_path):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self):
        """
        加载配置文件

        Returns:
            dict: 配置字典
        """
        if not self.config_path.exists():
            print(f"警告: 配置文件 {self.config_path} 不存在，使用默认配置")
            return self._default_config()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"错误: 加载配置文件失败: {e}")
            return self._default_config()

    def _default_config(self):
        """
        返回默认配置

        Returns:
            dict: 默认配置字典
        """
        return {
            "global": {
                "server_name": "MCP Server",
                "debug": False,
                "log_level": "INFO"
            },
            "modules": {
                "hello_world": {
                    "enabled": True,
                    "message": "Hello, {}!"
                }
            }
        }

    def get_global_config(self):
        """
        获取全局配置

        Returns:
            dict: 全局配置字典
        """
        return self.config.get('global', {})

    def get_modules_config(self):
        """
        获取模块配置

        Returns:
            dict: 模块配置字典
        """
        return self.config.get('modules', {})

    def get_module_config(self, module_name):
        """
        获取指定模块的配置

        Args:
            module_name: 模块名称

        Returns:
            dict: 模块配置
        """
        modules_config = self.get_modules_config()
        return modules_config.get(module_name, {})

    def is_module_enabled(self, module_name):
        """
        检查模块是否启用

        Args:
            module_name: 模块名称

        Returns:
            bool: 模块是否启用
        """
        module_config = self.get_module_config(module_name)
        return module_config.get('enabled', False)

    def save_config(self):
        """
        保存配置到文件

        Returns:
            bool: 是否保存成功
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"错误: 保存配置文件失败: {e}")
            return False