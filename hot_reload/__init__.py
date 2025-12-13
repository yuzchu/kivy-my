"""
Python代码热更新系统
适用于Android应用的动态代码更新和调试
"""

from .manager import HotReloadManager
from .debugger import Debugger
from .config import ConfigManager, HotReloadConfig, ModuleConfig, ReloadMode, LogLevel

__version__ = "1.0.0"
__all__ = [
    'HotReloadManager',
    'Debugger', 
    'ConfigManager',
    'HotReloadConfig',
    'ModuleConfig',
    'ReloadMode',
    'LogLevel',
    'HotReloadSystem'
]

class HotReloadSystem:
    """热更新系统（主集成类）"""
    
    def __init__(self, config_dir: str = "hot_reload/config"):
        """
        初始化热更新系统
        
        Args:
            config_dir: 配置目录
        """
        # 初始化组件
        self.config_manager = ConfigManager(config_dir)
        self.debugger = Debugger()
        self.manager = None
        
        # 应用配置
        self._apply_config()
        
        # 会话状态
        self.session_id = None
        self.is_running = False
        
    def _apply_config(self):
        """应用配置到管理器"""
        config = self.config_manager.config
        
        # 创建管理器
        self.manager = HotReloadManager(
            watch_dirs=config.watch_directories,
            watch_extensions=config.watch_extensions,
            auto_reload=(config.mode == ReloadMode.AUTO),
            check_interval=config.check_interval
        )
        
        # 设置回调
        if config.debug_enabled:
            self.manager.add_change_callback(self._on_module_change)
            self.manager.add_error_callback(self._on_error)
    
    def start(self):
        """启动热更新系统"""
        if self.is_running:
            print("[HotReload] System already running")
            return
        
        # 启动调试会话
        self.session_id = self.debugger.start_session()
        
        # 启动监控
        self.manager.start_monitoring()
        
        # 加载配置的模块
        for module_config in self.config_manager.list_modules():
            if module_config.enabled:
                try:
                    self.manager.load_module(
                        module_config.path,
                        module_config.name
                    )
                except Exception as e:
                    print(f"[HotReload] Failed to load module {module_config.name}: {e}")
        
        self.is_running = True
        print("[HotReload] System started")
    
    def stop(self):
        """停止热更新系统"""
        if not self.is_running:
            print("[HotReload] System not running")
            return
        
        # 停止监控
        self.manager.stop_monitoring()
        
        # 结束调试会话
        if self.session_id:
            self.debugger.end_session(self.session_id)
        
        self.is_running = False
        print("[HotReload] System stopped")
    
    def reload_module(self, module_name: str):
        """
        手动重载模块
        
        Args:
            module_name: 模块名称
        """
        if not self.is_running:
            print("[HotReload] System not running")
            return
        
        try:
            self.manager.reload_module(module_name)
            print(f"[HotReload] Module '{module_name}' reloaded manually")
        except Exception as e:
            print(f"[HotReload] Failed to reload module '{module_name}': {e}")
    
    def load_new_module(self, module_path: str, module_name: str = None):
        """
        加载新模块
        
        Args:
            module_path: 模块路径
            module_name: 模块名称（可选）
        """
        try:
            module = self.manager.load_module(module_path, module_name)
            
            # 添加到配置
            if module_name:
                self.config_manager.add_module(
                    name=module_name,
                    path=module_path,
                    enabled=True
                )
            
            return module
        except Exception as e:
            print(f"[HotReload] Failed to load new module: {e}")
            raise
    
    def _on_module_change(self, module_name: str, old_module, new_module):
        """模块变更回调"""
        print(f"[HotReload] Module changed: {module_name}")
        
        # 记录调试信息
        self.debugger._log(f"Module reloaded: {module_name}")
        
        # 发送通知（如果启用）
        if self.config_manager.config.show_notifications:
            self._show_notification(f"模块已更新: {module_name}")
    
    def _on_error(self, error_msg: str, traceback_str: str):
        """错误回调"""
        print(f"[HotReload] Error: {error_msg}")
        
        # 记录错误
        self.debugger._log(f"ERROR: {error_msg}\n{traceback_str}")
        
        # 发送错误通知（如果启用）
        if self.config_manager.config.show_notifications:
            self._show_notification(f"热更新错误: {error_msg[:50]}...")
    
    def _show_notification(self, message: str):
        """显示通知（需要根据具体UI框架实现）"""
        # 这里可以集成到具体的UI框架中
        # 例如：使用Kivy的Toast或MDDialog
        print(f"[Notification] {message}")
    
    def get_status(self) -> dict:
        """
        获取系统状态
        
        Returns:
            状态字典
        """
        return {
            'running': self.is_running,
            'session_id': self.session_id,
            'loaded_modules': self.manager.list_modules() if self.manager else [],
            'config': self.config_manager.config.to_dict() if self.config_manager.config else None,
            'debug_session': self.session_id is not None
        }
    
    def get_performance_report(self, func_name: str = None):
        """
        获取性能报告
        
        Args:
            func_name: 函数名称（可选）
            
        Returns:
            性能报告
        """
        return self.debugger.get_performance_report(func_name)
    
    def inspect_object(self, obj):
        """
        检查对象
        
        Args:
            obj: 要检查的对象
            
        Returns:
            对象信息
        """
        return self.debugger.inspect_object(obj)
    
    def evaluate_expression(self, expression: str, local_vars: dict = None, global_vars: dict = None):
        """
        评估表达式
        
        Args:
            expression: 表达式
            local_vars: 局部变量
            global_vars: 全局变量
            
        Returns:
            评估结果
        """
        return self.debugger.evaluate_expression(expression, local_vars, global_vars)
    
    def update_config(self, **kwargs):
        """
        更新配置
        
        Args:
            **kwargs: 配置参数
        """
        self.config_manager.update_config(**kwargs)
        self._apply_config()
    
    def reload_config(self):
        """重新加载配置"""
        self.config_manager.load_config()
        self._apply_config()
        print("[HotReload] Configuration reloaded")

# 创建全局实例
_system_instance = None

def get_system() -> HotReloadSystem:
    """
    获取热更新系统实例（单例模式）
    
    Returns:
        热更新系统实例
    """
    global _system_instance
    if _system_instance is None:
        _system_instance = HotReloadSystem()
    return _system_instance

def init_system(config_dir: str = "hot_reload/config") -> HotReloadSystem:
    """
    初始化热更新系统
    
    Args:
        config_dir: 配置目录
        
    Returns:
        热更新系统实例
    """
    global _system_instance
    _system_instance = HotReloadSystem(config_dir)
    return _system_instance