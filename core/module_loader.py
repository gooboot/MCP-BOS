"""
模块加载器，负责自动发现和加载模块

作者：kinbos 严富坤
邮箱：fookinbos@gmail.com
个人网站：htttps://www.yanfukun.com
"""

import importlib
import importlib.util
import inspect
import os
import sys
from pathlib import Path

from core.module_interface import ModuleInterface


class ModuleLoader:
    """
    模块加载器，负责自动发现和加载模块
    """

    def __init__(self, modules_dir, registry, config_manager):
        """
        初始化模块加载器

        Args:
            modules_dir: 模块目录
            registry: 模块注册表实例
            config_manager: 配置管理器实例
        """
        self.modules_dir = Path(modules_dir)
        self.registry = registry
        self.config_manager = config_manager

        # 确保模块目录存在
        if not self.modules_dir.exists():
            raise FileNotFoundError(f"模块目录不存在: {modules_dir}")

        # 添加模块目录到Python路径
        sys.path.append(str(self.modules_dir))

    def discover_modules(self):
        """
        发现可用模块

        Returns:
            list: 可用模块名称列表
        """
        modules = []

        # 遍历模块目录
        for item in self.modules_dir.iterdir():
            if not item.is_dir() or item.name.startswith('_') or item.name.startswith('.'):
                continue

            # 检查是否是有效的Python包
            init_file = item / "__init__.py"
            if not init_file.exists():
                continue

            modules.append(item.name)

        return modules

    def _find_module_class(self, module_name):
        """
        在模块中查找实现ModuleInterface的类

        Args:
            module_name: 模块名称

        Returns:
            type: 模块类
        """
        # 尝试导入模块
        try:
            # 先尝试直接导入主模块
            module = importlib.import_module(f"modules.{module_name}")
        except ImportError:
            try:
                # 尝试导入与模块同名的子模块
                module = importlib.import_module(f"modules.{module_name}.{module_name}")
            except ImportError:
                print(f"错误: 无法导入模块 {module_name}")
                return None

        # 查找实现ModuleInterface的类
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and
                    issubclass(obj, ModuleInterface) and
                    obj is not ModuleInterface):
                return obj

        # 查找所有子模块
        for item in (self.modules_dir / module_name).iterdir():
            if not item.is_file() or not item.name.endswith('.py') or item.name.startswith('_'):
                continue

            sub_module_name = item.stem
            try:
                sub_module = importlib.import_module(f"modules.{module_name}.{sub_module_name}")

                for name, obj in inspect.getmembers(sub_module):
                    if (inspect.isclass(obj) and
                            issubclass(obj, ModuleInterface) and
                            obj is not ModuleInterface):
                        return obj
            except ImportError:
                continue

        return None

    def load_module(self, module_name):
        """
        加载指定模块

        Args:
            module_name: 模块名称

        Returns:
            ModuleInterface: 加载的模块实例
        """
        # 获取模块配置
        module_config = self.config_manager.get_module_config(module_name)

        # 查找模块类
        module_class = self._find_module_class(module_name)
        if not module_class:
            print(f"错误: 模块 {module_name} 中未找到有效的模块类")
            return None

        # 实例化模块类
        try:
            module_instance = module_class(module_config)
            self.registry.register(module_name, module_instance)
            return module_instance
        except Exception as e:
            print(f"错误: 加载模块 {module_name} 失败: {e}")
            return None

    def load_enabled_modules(self):
        """
        加载配置中启用的所有模块

        Returns:
            list: 已加载模块列表
        """
        loaded_modules = []

        # 发现可用模块
        available_modules = self.discover_modules()

        # 加载启用的模块
        for module_name in available_modules:
            if self.config_manager.is_module_enabled(module_name):
                module = self.load_module(module_name)
                if module:
                    loaded_modules.append(module)

        return loaded_modules