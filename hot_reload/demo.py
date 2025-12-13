"""
热更新系统演示
展示如何在Android应用中实现代码热更新
"""

import time
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from hot_reload import HotReloadSystem, get_system

def demo_basic_usage():
    """演示基本用法"""
    print("=== 热更新系统演示 - 基本用法 ===")
    
    # 获取系统实例
    system = get_system()
    
    # 启动系统
    print("1. 启动热更新系统...")
    system.start()
    
    # 显示状态
    status = system.get_status()
    print(f"2. 系统状态: {status}")
    
    # 加载示例模块
    print("3. 加载示例模块...")
    example_path = Path(__file__).parent / "example_module.py"
    module = system.load_new_module(
        str(example_path),
        "example_module"
    )
    
    # 使用模块
    print("4. 使用加载的模块...")
    if module:
        # 调用模块中的函数
        result = module.greet("开发者")
        print(f"  问候结果: {result}")
        
        # 使用计算器
        calc = module.Calculator("演示计算器")
        print(f"  计算器: {calc}")
        print(f"  加法: 10 + 5 = {calc.add(10, 5)}")
        print(f"  计算历史: {calc.get_history()}")
    
    # 手动重载模块
    print("5. 手动重载模块...")
    system.reload_module("example_module")
    
    # 检查性能
    print("6. 检查性能报告...")
    report = system.get_performance_report()
    print(f"  性能报告: {report}")
    
    # 停止系统
    print("7. 停止热更新系统...")
    system.stop()
    
    print("\n=== 演示完成 ===")

def demo_debug_features():
    """演示调试功能"""
    print("\n=== 热更新系统演示 - 调试功能 ===")
    
    system = get_system()
    system.start()
    
    # 加载模块
    example_path = Path(__file__).parent / "example_module.py"
    module = system.load_new_module(
        str(example_path),
        "debug_module"
    )
    
    # 演示调试功能
    print("1. 对象检查...")
    if module:
        # 检查对象
        calc = module.Calculator()
        calc_info = system.inspect_object(calc)
        print(f"  计算器对象信息: {calc_info}")
        
        # 检查函数
        func_info = system.inspect_object(module.greet)
        print(f"  函数信息: {func_info}")
    
    # 表达式求值
    print("\n2. 表达式求值...")
    try:
        result = system.evaluate_expression(
            "2 + 3 * 4",
            local_vars={'x': 10, 'y': 20}
        )
        print(f"  表达式结果: {result}")
    except Exception as e:
        print(f"  求值错误: {e}")
    
    # 跟踪函数调用
    print("\n3. 函数调用跟踪...")
    if module:
        debugger = system.debugger
        traced_result = debugger.trace_function_call(
            module.fibonacci,
            10
        )
        print(f"  跟踪结果: {traced_result}")
    
    system.stop()
    print("\n=== 调试演示完成 ===")

def demo_config_management():
    """演示配置管理"""
    print("\n=== 热更新系统演示 - 配置管理 ===")
    
    system = get_system()
    
    # 显示当前配置
    config = system.config_manager.config
    print("1. 当前配置:")
    print(f"  模式: {config.mode.value}")
    print(f"  检查间隔: {config.check_interval}秒")
    print(f"  监控目录: {config.watch_directories}")
    print(f"  日志级别: {config.log_level.value}")
    
    # 更新配置
    print("\n2. 更新配置...")
    system.update_config(
        check_interval=2.0,
        log_level="debug",
        show_notifications=False
    )
    
    # 验证配置
    print("\n3. 验证配置...")
    errors = system.config_manager.validate_config()
    if errors:
        print(f"  配置错误: {errors}")
    else:
        print("  配置验证通过")
    
    # 导出配置
    print("\n4. 导出配置...")
    try:
        export_path = system.config_manager.export_config('json')
        print(f"  配置已导出到: {export_path}")
    except Exception as e:
        print(f"  导出失败: {e}")
    
    print("\n=== 配置管理演示完成 ===")

def demo_hot_reload_scenario():
    """演示热更新场景"""
    print("\n=== 热更新系统演示 - 实时更新场景 ===")
    
    system = get_system()
    system.start()
    
    # 创建测试模块
    test_module_content = '''
"""
测试模块 - 版本1
"""

def get_message():
    """获取消息"""
    return "这是版本1的消息"

def calculate(x, y):
    """计算"""
    return x + y

print("模块版本1已加载")
'''
    
    test_module_path = Path(__file__).parent / "test_module_v1.py"
    with open(test_module_path, 'w', encoding='utf-8') as f:
        f.write(test_module_content)
    
    # 加载测试模块
    print("1. 加载测试模块（版本1）...")
    module = system.load_new_module(
        str(test_module_path),
        "test_module"
    )
    
    if module:
        print(f"  消息: {module.get_message()}")
        print(f"  计算: 5 + 3 = {module.calculate(5, 3)}")
    
    # 模拟代码更新
    print("\n2. 模拟代码更新...")
    time.sleep(2)  # 等待一下
    
    test_module_content_v2 = '''
"""
测试模块 - 版本2
"""

def get_message():
    """获取消息"""
    return "这是版本2的消息 - 已更新！"

def calculate(x, y):
    """计算"""
    return x * y  # 改为乘法

def new_function():
    """新增函数"""
    return "这是新增的功能"

print("模块版本2已加载")
'''
    
    # 写入新版本
    with open(test_module_path, 'w', encoding='utf-8') as f:
        f.write(test_module_content_v2)
    
    print("  代码已更新，等待热重载...")
    time.sleep(3)  # 等待热重载
    
    # 手动触发重载
    print("\n3. 手动触发重载...")
    system.reload_module("test_module")
    
    # 检查更新后的功能
    if module:
        print(f"  更新后消息: {module.get_message()}")
        print(f"  更新后计算: 5 * 3 = {module.calculate(5, 3)}")
        
        # 尝试调用新函数
        try:
            print(f"  新功能: {module.new_function()}")
        except AttributeError:
            print("  注意: 新函数需要重新导入模块引用")
    
    # 清理
    test_module_path.unlink()
    
    system.stop()
    print("\n=== 热更新场景演示完成 ===")

def main():
    """主演示函数"""
    print("Python代码热更新系统演示")
    print("=" * 50)
    
    try:
        # 运行各个演示
        demo_basic_usage()
        demo_debug_features()
        demo_config_management()
        demo_hot_reload_scenario()
        
        print("\n" + "=" * 50)
        print("所有演示完成！")
        print("\n使用说明:")
        print("1. 在应用启动时初始化: system = HotReloadSystem()")
        print("2. 启动系统: system.start()")
        print("3. 加载模块: module = system.load_new_module('path/to/module.py', 'module_name')")
        print("4. 修改代码后会自动重载，或手动调用: system.reload_module('module_name')")
        print("5. 停止系统: system.stop()")
        
    except Exception as e:
        print(f"\n演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()