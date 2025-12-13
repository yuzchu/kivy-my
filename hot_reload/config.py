"""
配置管理器
管理热更新系统的配置
"""
import json
import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field
from enum import Enum

class ReloadMode(Enum):
    """重载模式"""
    AUTO = "auto"          # 自动重载
    MANUAL = "manual"      # 手动重载
    SCHEDULED = "scheduled" # 定时重载

class LogLevel(Enum):
    """日志级别"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ModuleConfig:
    """模块配置"""
    name: str
    path: str
    enabled: bool = True
    auto_reload: bool = True
    watch_changes: bool = True
    backup_before_reload: bool = True
    max_reloads_per_minute: int = 10

@dataclass
class HotReloadConfig:
    """热更新配置"""
    # 基本设置
    enabled: bool = True
    mode: ReloadMode = ReloadMode.AUTO
    check_interval: float = 1.0  # 秒
    
    # 监控设置
    watch_directories: List[str] = field(default_factory=lambda: ['.'])
    watch_extensions: List[str] = field(default_factory=lambda: ['.py'])
    recursive_watch: bool = True
    ignore_patterns: List[str] = field(default_factory=lambda: [
        '__pycache__', '*.pyc', '*.pyo', '*.pyd',
        '.git', '.svn', '.hg', '.idea', '.vscode'
    ])
    
    # 模块设置
    modules: List[ModuleConfig] = field(default_factory=list)
    default_module_settings: Dict[str, Any] = field(default_factory=lambda: {
        'auto_reload': True,
        'backup_before_reload': True,
        'max_reloads_per_minute': 10
    })
    
    # 调试设置
    debug_enabled: bool = True
    log_level: LogLevel = LogLevel.INFO
    log_to_file: bool = True
    log_file: str = "hot_reload/logs/hot_reload.log"
    max_log_size_mb: int = 10
    keep_logs_days: int = 7
    
    # 性能设置
    profile_enabled: bool = False
    profile_sample_rate: float = 0.1  # 10%的调用会被分析
    max_profile_entries: int = 1000
    
    # 安全设置
    allow_unsafe_code: bool = False
    allowed_imports: List[str] = field(default_factory=lambda: [
        'os', 'sys', 'time', 'datetime', 'json', 'math',
        'random', 're', 'collections', 'itertools', 'functools',
        'typing', 'pathlib', 'hashlib', 'base64', 'uuid'
    ])
    blocked_imports: List[str] = field(default_factory=lambda: [
        'subprocess', 'shutil', 'socket', 'multiprocessing',
        'threading', 'ctypes', 'pickle', 'marshal'
    ])
    
    # 备份设置
    backup_enabled: bool = True
    backup_dir: str = "hot_reload/backups"
    max_backups_per_module: int = 10
    backup_on_error: bool = True
    
    # UI设置
    show_notifications: bool = True
    notification_duration: float = 3.0  # 秒
    show_reload_progress: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['mode'] = self.mode.value
        data['log_level'] = self.log_level.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HotReloadConfig':
        """从字典创建"""
        # 转换枚举值
        if 'mode' in data and isinstance(data['mode'], str):
            data['mode'] = ReloadMode(data['mode'])
        if 'log_level' in data and isinstance(data['log_level'], str):
            data['log_level'] = LogLevel(data['log_level'])
        
        # 转换模块配置
        if 'modules' in data and isinstance(data['modules'], list):
            modules = []
            for module_data in data['modules']:
                if isinstance(module_data, dict):
                    modules.append(ModuleConfig(**module_data))
                elif isinstance(module_data, ModuleConfig):
                    modules.append(module_data)
            data['modules'] = modules
        
        return cls(**data)

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_dir: str = "hot_reload/config"):
        """
        初始化配置管理器
        
        Args:
            config_dir: 配置目录
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / "config.json"
        self.default_config = HotReloadConfig()
        
        # 加载或创建配置
        self.config = self.load_config()
    
    def load_config(self) -> HotReloadConfig:
        """
        加载配置
        
        Returns:
            配置对象
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return HotReloadConfig.from_dict(data)
            except Exception as e:
                print(f"[Config] Failed to load config: {e}")
                return self.default_config
        else:
            # 创建默认配置
            self.save_config(self.default_config)
            return self.default_config
    
    def save_config(self, config: Optional[HotReloadConfig] = None):
        """
        保存配置
        
        Args:
            config: 配置对象（如果为None，保存当前配置）
        """
        if config is None:
            config = self.config
        
        try:
            # 确保目录存在
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            # 转换为字典并保存
            data = config.to_dict()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"[Config] Configuration saved to {self.config_file}")
            
        except Exception as e:
            print(f"[Config] Failed to save config: {e}")
    
    def update_config(self, **kwargs):
        """
        更新配置
        
        Args:
            **kwargs: 配置参数
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                # 特殊处理枚举值
                if key == 'mode' and isinstance(value, str):
                    value = ReloadMode(value)
                elif key == 'log_level' and isinstance(value, str):
                    value = LogLevel(value)
                
                setattr(self.config, key, value)
            else:
                print(f"[Config] Warning: Unknown config key: {key}")
        
        self.save_config()
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        return getattr(self.config, key, default)
    
    def add_module(self, name: str, path: str, **kwargs):
        """
        添加模块配置
        
        Args:
            name: 模块名称
            path: 模块路径
            **kwargs: 额外配置
        """
        # 检查是否已存在
        for module in self.config.modules:
            if module.name == name:
                print(f"[Config] Module '{name}' already exists")
                return
        
        # 创建新模块配置
        module_config = ModuleConfig(name=name, path=path, **kwargs)
        self.config.modules.append(module_config)
        self.save_config()
        
        print(f"[Config] Module '{name}' added")
    
    def remove_module(self, name: str):
        """
        移除模块配置
        
        Args:
            name: 模块名称
        """
        for i, module in enumerate(self.config.modules):
            if module.name == name:
                self.config.modules.pop(i)
                self.save_config()
                print(f"[Config] Module '{name}' removed")
                return
        
        print(f"[Config] Module '{name}' not found")
    
    def update_module(self, name: str, **kwargs):
        """
        更新模块配置
        
        Args:
            name: 模块名称
            **kwargs: 要更新的配置
        """
        for module in self.config.modules:
            if module.name == name:
                for key, value in kwargs.items():
                    if hasattr(module, key):
                        setattr(module, key, value)
                    else:
                        print(f"[Config] Warning: Unknown module key: {key}")
                
                self.save_config()
                print(f"[Config] Module '{name}' updated")
                return
        
        print(f"[Config] Module '{name}' not found")
    
    def get_module(self, name: str) -> Optional[ModuleConfig]:
        """
        获取模块配置
        
        Args:
            name: 模块名称
            
        Returns:
            模块配置或None
        """
        for module in self.config.modules:
            if module.name == name:
                return module
        return None
    
    def list_modules(self) -> List[ModuleConfig]:
        """
        列出所有模块配置
        
        Returns:
            模块配置列表
        """
        return self.config.modules.copy()
    
    def export_config(self, format: str = 'json', file_path: str = None) -> str:
        """
        导出配置
        
        Args:
            format: 导出格式（json/yaml）
            file_path: 文件路径（可选）
            
        Returns:
            文件路径
        """
        if not file_path:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            file_path = self.config_dir / f"config_export_{timestamp}.{format}"
        
        data = self.config.to_dict()
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if format.lower() == 'json':
                    json.dump(data, f, indent=2, ensure_ascii=False)
                elif format.lower() == 'yaml':
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
                else:
                    raise ValueError(f"Unsupported format: {format}")
            
            print(f"[Config] Configuration exported to {file_path}")
            return str(file_path)
            
        except Exception as e:
            print(f"[Config] Failed to export config: {e}")
            raise
    
    def import_config(self, file_path: str):
        """
        导入配置
        
        Args:
            file_path: 配置文件路径
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.suffix.lower() == '.json':
                    data = json.load(f)
                elif file_path.suffix.lower() in ['.yaml', '.yml']:
                    data = yaml.safe_load(f)
                else:
                    raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
            # 导入配置
            self.config = HotReloadConfig.from_dict(data)
            self.save_config()
            
            print(f"[Config] Configuration imported from {file_path}")
            
        except Exception as e:
            print(f"[Config] Failed to import config: {e}")
            raise
    
    def reset_to_defaults(self):
        """重置为默认配置"""
        self.config = self.default_config
        self.save_config()
        print("[Config] Configuration reset to defaults")
    
    def validate_config(self) -> List[str]:
        """
        验证配置
        
        Returns:
            错误消息列表
        """
        errors = []
        
        # 检查监控目录
        for dir_path in self.config.watch_directories:
            if not Path(dir_path).exists():
                errors.append(f"Watch directory does not exist: {dir_path}")
        
        # 检查模块路径
        for module in self.config.modules:
            if not Path(module.path).exists():
                errors.append(f"Module path does not exist: {module.path} (module: {module.name})")
        
        # 检查备份目录
        if self.config.backup_enabled:
            backup_dir = Path(self.config.backup_dir)
            if not backup_dir.exists():
                try:
                    backup_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    errors.append(f"Failed to create backup directory: {e}")
        
        # 检查日志目录
        if self.config.log_to_file:
            log_dir = Path(self.config.log_file).parent
            if not log_dir.exists():
                try:
                    log_dir.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    errors.append(f"Failed to create log directory: {e}")
        
        return errors

# 导入time模块用于时间戳
import time