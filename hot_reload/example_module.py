"""
示例模块
用于演示热更新功能
"""

class Calculator:
    """计算器类"""
    
    def __init__(self, name="Calculator"):
        self.name = name
        self.history = []
    
    def add(self, a, b):
        """加法"""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        """减法"""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a, b):
        """乘法"""
        result = a * b
        self.history.append(f"{a} × {b} = {result}")
        return result
    
    def divide(self, a, b):
        """除法"""
        if b == 0:
            raise ValueError("除数不能为零")
        result = a / b
        self.history.append(f"{a} ÷ {b} = {result}")
        return result
    
    def get_history(self):
        """获取计算历史"""
        return self.history.copy()
    
    def clear_history(self):
        """清空历史"""
        self.history.clear()
    
    def __str__(self):
        return f"{self.name} (历史记录: {len(self.history)} 条)"

def greet(name="World"):
    """问候函数"""
    return f"Hello, {name}!"

def fibonacci(n):
    """生成斐波那契数列"""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

def process_data(data):
    """处理数据"""
    if not data:
        return []
    
    # 计算统计信息
    stats = {
        'count': len(data),
        'sum': sum(data),
        'mean': sum(data) / len(data) if data else 0,
        'min': min(data) if data else 0,
        'max': max(data) if data else 0
    }
    
    return stats

# 全局实例
calculator = Calculator("示例计算器")

# 测试函数
def test_functions():
    """测试所有函数"""
    results = {}
    
    # 测试计算器
    calc = Calculator("测试计算器")
    results['add'] = calc.add(10, 5)
    results['subtract'] = calc.subtract(10, 5)
    results['multiply'] = calc.multiply(10, 5)
    results['divide'] = calc.divide(10, 5)
    results['history'] = calc.get_history()
    
    # 测试其他函数
    results['greet'] = greet("热更新")
    results['fibonacci'] = fibonacci(10)
    results['process_data'] = process_data([1, 2, 3, 4, 5])
    
    return results

if __name__ == "__main__":
    # 运行测试
    print("=== 示例模块测试 ===")
    results = test_functions()
    
    for key, value in results.items():
        print(f"{key}: {value}")
    
    print(f"\n全局计算器: {calculator}")
    print(f"计算历史: {calculator.get_history()}")
    
    print("\n=== 测试完成 ===")