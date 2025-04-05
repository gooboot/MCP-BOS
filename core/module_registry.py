class ModuleRegistry:
    """
    模块注册表，负责跟踪所有已加载的模块
    """
    
    def __init__(self):
        """
        初始化模块注册表
        """
        self.modules = {}
        
    def register(self, module_name, module_instance):
        """
        注册模块实例
        
        Args:
            module_name: 模块名称
            module_instance: 模块实例
        """
        self.modules[module_name] = module_instance
        debug_print(f"已注册模块: {module_name}")
        
    def get_module(self, module_name):
        """
        获取模块实例
        
        Args:
            module_name: 模块名称
            
        Returns:
            ModuleInterface: 模块实例
        """
        return self.modules.get(module_name)
        
    def get_all_modules(self):
        """
        获取所有已注册模块
        
        Returns:
            dict: 模块名称和实例的映射
        """
        return self.modules
        
    def list_modules(self):
        """
        列出所有已注册模块
        
        Returns:
            list: 模块信息列表
        """
        return [
            {
                "name": name,
                "info": module.get_info()
            }
            for name, module in self.modules.items()
        ]