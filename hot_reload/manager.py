"""
热更新管理器
负责模块的动态加载、重载和监控
"""
import importlib
import sys
import os
import time
import threading
from typing import Dict, Any, Optional, Callable, List
from pathlib import Path
import traceback
import hashlib

class HotReloadManager:
    """热更新管理器"""
    
    def __init__(self, watch_dirs: List[str] = None, 
                 watch_extensions: List[str] = None,
                 auto_reload: bool = True,
                 check_interval: float = 1.0):
        """
        初始化热更新管理器
        
        Args:
            watch_dirs: 监控的目录列表
            watch_extensions: 监控的文件扩展名列表
            auto_reload: 是否自动重载
            check_interval: 检查间隔（秒）
        """
        self.watch_dirs = watch_dirs or ['.']
        self.watch_extensions = watch_extensions or ['.py']
        self.auto_reload = auto_reload
        self.check_interval = check_interval
        
        # 已加载的模块
        self.loaded_modules: Dict[str, Dict[str, Any]] = {}
        # 文件哈希值（用于检测变化）
        self.file_hashes: Dict[str, str] = {}
        # 模块变更回调
        self.change_callbacks: List[Callable] = []
        # 错误回调
        self.error_callbacks: List[Callable] = []
        
        # 监控线程
        self.monitor_thread: Optional[threading.Thread] = None
        self.running = False
        
        # 创建必要的目录
        self._ensure_directories()
        
    def _ensure_directories(self):
        """确保必要的目录存在"""
        dirs = ['modules', 'logs', 'backups']
        for dir_name in dirs:
            dir_path = Path(f"hot_reload/{dir_name}")
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def load_module(self, module_path: str, module_name: str = None) -> Any:
        """
        动态加载模块
        
        Args:
            module_path: 模块文件路径
            module_name: 模块名称（可选）
            
        Returns:
            加载的模块对象
        """
        try:
            # 标准化路径
            module_path = Path(module_path).resolve()
            
            if not module_path.exists():
                raise FileNotFoundError(f"Module file not found: {module_path}")
            
            # 生成模块名称
            if not module_name:
                module_name = f"hot_module_{hashlib.md5(str(module_path).encode()).hexdigest()[:8]}"
            
            # 添加到Python路径
            sys.path.insert(0, str(module_path.parent))
            
            # 加载模块
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            # 记录模块信息
            self.loaded_modules[module_name] = {
                'module': module,
                'path': str(module_path),
                'name': module_name,
                'loaded_at': time.time(),
                'reload_count': 0
            }
            
            # 计算文件哈希
            self._update_file_hash(module_path)
            
            print(f"[HotReload] Module loaded: {module_name} from {module_path}")
            return module
            
        except Exception as e:
            error_msg = f"Failed to load module {module_path}: {str(e)}"
            print(f"[HotReload] ERROR: {error_msg}")
            self._notify_error(error_msg, traceback.format_exc())
            raise
    
    def reload_module(self, module_name: str) -> Any:
        """
        重新加载模块
        
        Args:
            module_name: 模块名称
            
        Returns:
            重新加载后的模块对象
        """
        if module_name not in self.loaded_modules:
            raise KeyError(f"Module not loaded: {module_name}")
        
        module_info = self.loaded_modules[module_name]
        module_path = Path(module_info['path'])
        
        try:
            # 备份旧模块
            old_module = module_info['module']
            
            # 重新加载
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            new_module = importlib.util.module_from_spec(spec)
            
            # 更新sys.modules
            sys.modules[module_name] = new_module
            
            # 执行模块
            spec.loader.exec_module(new_module)
            
            # 更新模块信息
            self.loaded_modules[module_name].update({
                'module': new_module,
                'reloaded_at': time.time(),
                'reload_count': module_info['reload_count'] + 1
            })
            
            # 更新文件哈希
            self._update_file_hash(module_path)
            
            print(f"[HotReload] Module reloaded: {module_name}")
            
            # 通知变更
            self._notify_change(module_name, old_module, new_module)
            
            return new_module
            
        except Exception as e:
            error_msg = f"Failed to reload module {module_name}: {str(e)}"
            print(f"[HotReload] ERROR: {error_msg}")
            self._notify_error(error_msg, traceback.format_exc())
            # 恢复旧模块
            sys.modules[module_name] = old_module
            raise
    
    def _update_file_hash(self, file_path: Path):
        """更新文件哈希值"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                file_hash = hashlib.md5(content).hexdigest()
                self.file_hashes[str(file_path)] = file_hash
        except Exception as e:
            print(f"[HotReload] Failed to calculate hash for {file_path}: {e}")
    
    def _check_for_changes(self):
        """检查文件变化"""
        changed_files = []
        
        for watch_dir in self.watch_dirs:
            watch_path = Path(watch_dir)
            if not watch_path.exists():
                continue
                
            for file_path in watch_path.rglob('*'):
                if file_path.suffix in self.watch_extensions:
                    try:
                        with open(file_path, 'rb') as f:
                            content = f.read()
                            current_hash = hashlib.md5(content).hexdigest()
                            
                            old_hash = self.file_hashes.get(str(file_path))
                            if old_hash and current_hash != old_hash:
                                changed_files.append(str(file_path))
                                self.file_hashes[str(file_path)] = current_hash
                    except Exception as e:
                        print(f"[HotReload] Error checking {file_path}: {e}")
        
        return changed_files
    
    def start_monitoring(self):
        """开始监控文件变化"""
        if self.monitor_thread and self.monitor_thread.is_alive():
            print("[HotReload] Monitoring already started")
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True
        )
        self.monitor_thread.start()
        print("[HotReload] File monitoring started")
    
    def stop_monitoring(self):
        """停止监控文件变化"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        print("[HotReload] File monitoring stopped")
    
    def _monitor_loop(self):
        """监控循环"""
        while self.running:
            try:
                changed_files = self._check_for_changes()
                
                if changed_files and self.auto_reload:
                    print(f"[HotReload] Files changed: {changed_files}")
                    
                    # 重新加载相关模块
                    for file_path in changed_files:
                        self._reload_modules_for_file(file_path)
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"[HotReload] Error in monitor loop: {e}")
                time.sleep(self.check_interval)
    
    def _reload_modules_for_file(self, file_path: str):
        """重新加载与文件相关的模块"""
        for module_name, module_info in self.loaded_modules.items():
            if module_info['path'] == file_path:
                try:
                    self.reload_module(module_name)
                except Exception as e:
                    print(f"[HotReload] Failed to reload {module_name}: {e}")
    
    def add_change_callback(self, callback: Callable):
        """添加模块变更回调"""
        self.change_callbacks.append(callback)
    
    def add_error_callback(self, callback: Callable):
        """添加错误回调"""
        self.error_callbacks.append(callback)
    
    def _notify_change(self, module_name: str, old_module: Any, new_module: Any):
        """通知模块变更"""
        for callback in self.change_callbacks:
            try:
                callback(module_name, old_module, new_module)
            except Exception as e:
                print(f"[HotReload] Error in change callback: {e}")
    
    def _notify_error(self, error_msg: str, traceback_str: str):
        """通知错误"""
        for callback in self.error_callbacks:
            try:
                callback(error_msg, traceback_str)
            except Exception as e:
                print(f"[HotReload] Error in error callback: {e}")
    
    def get_module_info(self, module_name: str) -> Dict[str, Any]:
        """获取模块信息"""
        if module_name not in self.loaded_modules:
            raise KeyError(f"Module not found: {module_name}")
        return self.loaded_modules[module_name].copy()
    
    def list_modules(self) -> List[str]:
        """列出所有已加载模块"""
        return list(self.loaded_modules.keys())
    
    def unload_module(self, module_name: str):
        """卸载模块"""
        if module_name in self.loaded_modules:
            # 从sys.modules中移除
            if module_name in sys.modules:
                del sys.modules[module_name]
            
            # 从加载模块中移除
            del self.loaded_modules[module_name]
            
            print(f"[HotReload] Module unloaded: {module_name}")
    
    def create_backup(self, module_name: str):
        """创建模块备份"""
        if module_name not in self.loaded_modules:
            raise KeyError(f"Module not found: {module_name}")
        
        module_info = self.loaded_modules[module_name]
        source_path = Path(module_info['path'])
        
        # 创建备份文件名
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_dir = Path("hot_reload/backups")
        backup_dir.mkdir(exist_ok=True)
        
        backup_name = f"{module_name}_{timestamp}.py"
        backup_path = backup_dir / backup_name
        
        # 复制文件
        import shutil
        shutil.copy2(source_path, backup_path)
        
        print(f"[HotReload] Backup created: {backup_path}")
        return str(backup_path)