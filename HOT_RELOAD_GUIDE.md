# Python代码热更新系统使用指南

## 概述

这是一个专为Android应用设计的Python代码热更新系统，允许你在不重启应用的情况下动态更新和调试代码。系统提供了完整的模块管理、配置管理、调试工具和性能监控功能。

## 系统架构

### 核心组件

1. **HotReloadManager** - 热更新管理器
   - 动态加载/重载Python模块
   - 监控文件变化
   - 模块生命周期管理

2. **Debugger** - 调试器
   - 断点管理
   - 表达式求值
   - 性能监控
   - 对象检查

3. **ConfigManager** - 配置管理器
   - 配置加载/保存
   - 模块配置管理
   - 安全设置

4. **HotReloadSystem** - 主集成系统
   - 组件协调
   - 统一API接口
   - 状态管理

## 快速开始

### 1. 基本使用

```python
from hot_reload import HotReloadSystem

# 初始化系统
system = HotReloadSystem()

# 启动系统
system.start()

# 加载模块
module = system.load_new_module("path/to/module.py", "my_module")

# 使用模块功能
result = module.my_function()

# 修改代码后自动重载，或手动重载
system.reload_module("my_module")

# 停止系统
system.stop()
```

### 2. 在Kivy应用中使用

```python
class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hot_reload_system = HotReloadSystem()
    
    def build(self):
        # 构建UI
        # 添加热更新控制按钮
        pass
    
    def start_hot_reload(self):
        self.hot_reload_system.start()
    
    def stop_hot_reload(self):
        self.hot_reload_system.stop()
```

## 详细功能

### 模块管理

#### 加载模块
```python
# 自动生成模块名
module = system.load_new_module("path/to/module.py")

# 指定模块名
module = system.load_new_module("path/to/module.py", "custom_name")
```

#### 重载模块
```python
# 自动重载（监控文件变化）
# 或手动重载
system.reload_module("module_name")
```

#### 卸载模块
```python
system.manager.unload_module("module_name")
```

### 调试功能

#### 表达式求值
```python
result = system.evaluate_expression("2 + 3 * 4")
```

#### 对象检查
```python
info = system.inspect_object(some_object)
```

#### 性能监控
```python
report = system.get_performance_report()
# 或特定函数
report = system.get_performance_report("function_name")
```

#### 调用栈查看
```python
stack = system.debugger.get_call_stack()
```

### 配置管理

#### 查看配置
```python
config = system.config_manager.config
print(f"检查间隔: {config.check_interval}")
print(f"日志级别: {config.log_level.value}")
```

#### 更新配置
```python
system.update_config(
    check_interval=2.0,
    log_level="debug",
    show_notifications=False
)
```

#### 添加模块配置
```python
system.config_manager.add_module(
    name="my_module",
    path="path/to/module.py",
    enabled=True,
    auto_reload=True
)
```

## 安全特性

### 安全限制
- 默认禁用危险模块导入（subprocess、socket等）
- 表达式求值使用安全的内置函数
- 可配置允许/禁止的导入列表

### 配置安全设置
```python
system.update_config(
    allow_unsafe_code=False,
    allowed_imports=["os", "sys", "json", "math"],
    blocked_imports=["subprocess", "socket", "shutil"]
)
```

## 性能优化

### 监控设置
```python
system.update_config(
    profile_enabled=True,
    profile_sample_rate=0.1,  # 10%的调用会被分析
    max_profile_entries=1000
)
```

### 备份设置
```python
system.update_config(
    backup_enabled=True,
    backup_dir="hot_reload/backups",
    max_backups_per_module=10,
    backup_on_error=True
)
```

## 在Android环境中的注意事项

### 1. 文件权限
- Android应用通常有受限的文件系统访问权限
- 确保应用有读写存储的权限
- 使用应用私有目录或外部存储

### 2. 线程安全
- 热更新系统使用后台线程监控文件变化
- UI操作必须在主线程执行
- 使用Kivy的Clock.schedule_once进行线程间通信

### 3. 资源管理
- 及时停止监控线程
- 清理不再使用的模块
- 定期清理日志和备份文件

### 4. 电池优化
- 调整检查间隔以减少电池消耗
- 在应用进入后台时暂停监控
- 使用适当的日志级别

## 最佳实践

### 1. 模块设计
```python
# 良好的热更新模块设计
class MyFeature:
    def __init__(self):
        self.state = {}
    
    def process(self, data):
        # 业务逻辑
        pass
    
    def cleanup(self):
        # 清理资源
        pass

# 避免全局状态
feature_instance = MyFeature()
```

### 2. 错误处理
```python
try:
    system.reload_module("important_module")
except Exception as e:
    # 记录错误
    logger.error(f"重载失败: {e}")
    # 恢复备份
    system.manager.create_backup("important_module")
```

### 3. 测试策略
```python
# 单元测试
def test_module_reload():
    system = HotReloadSystem()
    system.start()
    
    # 加载测试模块
    module = system.load_new_module("test.py", "test_module")
    
    # 修改代码
    with open("test.py", "w") as f:
        f.write(new_code)
    
    # 验证重载
    system.reload_module("test_module")
    assert module.new_function() == expected_result
    
    system.stop()
```

## 故障排除

### 常见问题

#### 1. 模块加载失败
- 检查文件路径是否正确
- 验证Python语法
- 检查导入依赖

#### 2. 重载后状态丢失
- 使用持久化存储保存重要状态
- 实现状态恢复机制
- 考虑使用数据库或文件存储

#### 3. 性能问题
- 减少监控目录范围
- 增加检查间隔
- 禁用不必要的调试功能

#### 4. 内存泄漏
- 定期卸载不再使用的模块
- 监控内存使用情况
- 实现资源清理回调

### 调试技巧

1. **启用详细日志**
```python
system.update_config(log_level="debug")
```

2. **检查系统状态**
```python
status = system.get_status()
print(f"运行状态: {status['running']}")
print(f"加载模块: {status['loaded_modules']}")
```

3. **查看性能报告**
```python
report = system.get_performance_report()
for func_name, data in report.get('functions', {}).items():
    print(f"{func_name}: {data['avg_duration']:.4f}s")
```

## 扩展开发

### 自定义模块加载器
```python
class CustomHotReloadManager(HotReloadManager):
    def load_module(self, module_path, module_name=None):
        # 自定义加载逻辑
        # 例如：从网络加载、加密模块等
        pass
```

### 集成其他框架
```python
# 集成到Flask应用
from flask import Flask
app = Flask(__name__)
hot_reload = HotReloadSystem()

@app.route('/reload/<module_name>')
def reload_module(module_name):
    hot_reload.reload_module(module_name)
    return f"Module {module_name} reloaded"
```

### 添加UI组件
```python
# 自定义热更新UI组件
class HotReloadWidget(MDBoxLayout):
    def __init__(self, system, **kwargs):
        super().__init__(**kwargs)
        self.system = system
        self.build_ui()
    
    def build_ui(self):
        # 构建UI
        pass
```

## 示例应用

系统包含完整的示例应用，演示了所有功能：

1. **基本演示** - 展示核心功能
2. **调试演示** - 展示调试工具
3. **配置演示** - 展示配置管理
4. **实时更新演示** - 展示代码热更新

运行演示：
```bash
# 在应用内运行
python hot_reload/demo.py

# 或通过UI运行
点击"运行演示"按钮
```

## 许可证

本项目使用MIT许可证。详见LICENSE文件。

## 支持与贡献

如有问题或建议，请：
1. 查看本文档
2. 检查示例代码
3. 提交Issue
4. 贡献代码

## 更新日志

### v1.0.0
- 初始版本发布
- 完整的模块热更新功能
- 集成调试工具
- 配置管理系统
- Android Kivy应用集成
- 示例应用和文档