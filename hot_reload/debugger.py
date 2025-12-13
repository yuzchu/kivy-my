"""
调试接口
提供代码调试和监控功能
"""
import json
import time
import traceback
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
import inspect
import threading
from datetime import datetime

class Debugger:
    """调试器"""
    
    def __init__(self, log_dir: str = "hot_reload/logs"):
        """
        初始化调试器
        
        Args:
            log_dir: 日志目录
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 调试会话
        self.sessions: Dict[str, Dict[str, Any]] = {}
        # 断点
        self.breakpoints: Dict[str, List[int]] = {}
        # 监视表达式
        self.watch_expressions: List[str] = []
        # 性能监控
        self.performance_data: Dict[str, List[Dict[str, Any]]] = {}
        
        # 创建日志文件
        self.log_file = self.log_dir / f"debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
    def start_session(self, session_id: str = None) -> str:
        """
        开始调试会话
        
        Args:
            session_id: 会话ID（可选）
            
        Returns:
            会话ID
        """
        if not session_id:
            session_id = f"session_{int(time.time())}"
        
        self.sessions[session_id] = {
            'start_time': time.time(),
            'status': 'running',
            'breakpoints_hit': [],
            'variables': {},
            'call_stack': []
        }
        
        self._log(f"Session started: {session_id}")
        return session_id
    
    def end_session(self, session_id: str):
        """
        结束调试会话
        
        Args:
            session_id: 会话ID
        """
        if session_id in self.sessions:
            session = self.sessions[session_id]
            session['end_time'] = time.time()
            session['status'] = 'ended'
            session['duration'] = session['end_time'] - session['start_time']
            
            self._log(f"Session ended: {session_id}, duration: {session['duration']:.2f}s")
    
    def add_breakpoint(self, file_path: str, line_number: int):
        """
        添加断点
        
        Args:
            file_path: 文件路径
            line_number: 行号
        """
        if file_path not in self.breakpoints:
            self.breakpoints[file_path] = []
        
        if line_number not in self.breakpoints[file_path]:
            self.breakpoints[file_path].append(line_number)
            self._log(f"Breakpoint added: {file_path}:{line_number}")
    
    def remove_breakpoint(self, file_path: str, line_number: int):
        """
        移除断点
        
        Args:
            file_path: 文件路径
            line_number: 行号
        """
        if file_path in self.breakpoints and line_number in self.breakpoints[file_path]:
            self.breakpoints[file_path].remove(line_number)
            self._log(f"Breakpoint removed: {file_path}:{line_number}")
    
    def add_watch_expression(self, expression: str):
        """
        添加监视表达式
        
        Args:
            expression: 表达式字符串
        """
        if expression not in self.watch_expressions:
            self.watch_expressions.append(expression)
            self._log(f"Watch expression added: {expression}")
    
    def evaluate_expression(self, expression: str, local_vars: Dict = None, global_vars: Dict = None) -> Any:
        """
        评估表达式
        
        Args:
            expression: 表达式字符串
            local_vars: 局部变量
            global_vars: 全局变量
            
        Returns:
            评估结果
        """
        try:
            # 安全评估
            if local_vars is None:
                local_vars = {}
            if global_vars is None:
                global_vars = {}
            
            # 限制可用的内置函数
            safe_builtins = {
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'min': min,
                'max': max,
                'sum': sum,
                'abs': abs,
                'round': round,
                'sorted': sorted,
                'reversed': reversed,
                'type': type,
                'isinstance': isinstance,
                'issubclass': issubclass,
                'hasattr': hasattr,
                'getattr': getattr,
                'setattr': setattr,
                'dir': dir,
                'id': id,
                'hex': hex,
                'oct': oct,
                'bin': bin,
                'chr': chr,
                'ord': ord,
                'repr': repr,
                'format': format,
                'divmod': divmod,
                'pow': pow,
                'all': all,
                'any': any,
                'callable': callable,
                'hash': hash,
                'iter': iter,
                'next': next,
                'slice': slice,
                'vars': vars,
                'locals': lambda: local_vars,
                'globals': lambda: global_vars
            }
            
            # 创建安全的全局命名空间
            safe_globals = {**global_vars, '__builtins__': safe_builtins}
            
            # 评估表达式
            result = eval(expression, safe_globals, local_vars)
            
            self._log(f"Expression evaluated: {expression} = {repr(result)}")
            return result
            
        except Exception as e:
            error_msg = f"Failed to evaluate expression '{expression}': {str(e)}"
            self._log(f"ERROR: {error_msg}")
            raise ValueError(error_msg)
    
    def trace_function_call(self, func, *args, **kwargs):
        """
        跟踪函数调用
        
        Args:
            func: 要跟踪的函数
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            函数调用结果
        """
        func_name = func.__name__
        start_time = time.time()
        
        try:
            # 记录调用信息
            call_info = {
                'function': func_name,
                'args': args,
                'kwargs': kwargs,
                'start_time': start_time,
                'thread': threading.current_thread().name
            }
            
            self._log(f"Function call: {func_name}({args}, {kwargs})")
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 记录结果
            end_time = time.time()
            duration = end_time - start_time
            
            call_info.update({
                'result': result,
                'end_time': end_time,
                'duration': duration,
                'success': True
            })
            
            # 保存性能数据
            if func_name not in self.performance_data:
                self.performance_data[func_name] = []
            self.performance_data[func_name].append(call_info)
            
            self._log(f"Function completed: {func_name}, duration: {duration:.4f}s")
            
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            
            error_info = {
                'function': func_name,
                'args': args,
                'kwargs': kwargs,
                'start_time': start_time,
                'end_time': end_time,
                'duration': duration,
                'error': str(e),
                'traceback': traceback.format_exc(),
                'success': False
            }
            
            # 保存错误数据
            if f"{func_name}_errors" not in self.performance_data:
                self.performance_data[f"{func_name}_errors"] = []
            self.performance_data[f"{func_name}_errors"].append(error_info)
            
            self._log(f"Function error: {func_name}, error: {str(e)}")
            raise
    
    def get_performance_report(self, func_name: str = None) -> Dict[str, Any]:
        """
        获取性能报告
        
        Args:
            func_name: 函数名称（可选）
            
        Returns:
            性能报告
        """
        if func_name:
            if func_name not in self.performance_data:
                return {'error': f'No data for function: {func_name}'}
            
            calls = self.performance_data[func_name]
            if not calls:
                return {'function': func_name, 'total_calls': 0}
            
            # 计算统计信息
            durations = [call['duration'] for call in calls if call.get('success', True)]
            error_calls = [call for call in calls if not call.get('success', True)]
            
            report = {
                'function': func_name,
                'total_calls': len(calls),
                'successful_calls': len(durations),
                'failed_calls': len(error_calls),
                'avg_duration': sum(durations) / len(durations) if durations else 0,
                'min_duration': min(durations) if durations else 0,
                'max_duration': max(durations) if durations else 0,
                'total_duration': sum(durations),
                'recent_calls': calls[-10:]  # 最近10次调用
            }
            
            return report
        else:
            # 所有函数的报告
            report = {
                'total_functions': len(self.performance_data),
                'functions': {}
            }
            
            for func_name, calls in self.performance_data.items():
                if calls:
                    durations = [call['duration'] for call in calls if call.get('success', True)]
                    if durations:
                        report['functions'][func_name] = {
                            'call_count': len(calls),
                            'avg_duration': sum(durations) / len(durations),
                            'total_duration': sum(durations)
                        }
            
            return report
    
    def inspect_object(self, obj: Any) -> Dict[str, Any]:
        """
        检查对象
        
        Args:
            obj: 要检查的对象
            
        Returns:
            对象信息
        """
        try:
            info = {
                'type': type(obj).__name__,
                'module': obj.__class__.__module__ if hasattr(obj, '__class__') else None,
                'repr': repr(obj),
                'str': str(obj),
                'id': id(obj)
            }
            
            # 获取属性
            if hasattr(obj, '__dict__'):
                info['attributes'] = {
                    key: type(value).__name__ 
                    for key, value in obj.__dict__.items() 
                    if not key.startswith('_')
                }
            
            # 获取方法
            methods = []
            for name in dir(obj):
                if not name.startswith('_'):
                    attr = getattr(obj, name)
                    if callable(attr):
                        methods.append(name)
            
            if methods:
                info['methods'] = methods
            
            # 如果是函数或方法
            if callable(obj):
                try:
                    sig = inspect.signature(obj)
                    info['signature'] = str(sig)
                    
                    # 获取参数信息
                    params = {}
                    for param_name, param in sig.parameters.items():
                        params[param_name] = {
                            'kind': str(param.kind),
                            'default': str(param.default) if param.default != inspect.Parameter.empty else None,
                            'annotation': str(param.annotation) if param.annotation != inspect.Parameter.empty else None
                        }
                    info['parameters'] = params
                except:
                    info['signature'] = 'Unable to get signature'
            
            return info
            
        except Exception as e:
            return {
                'error': f'Failed to inspect object: {str(e)}',
                'type': type(obj).__name__ if hasattr(obj, '__class__') else 'unknown'
            }
    
    def get_call_stack(self, depth: int = 10) -> List[Dict[str, Any]]:
        """
        获取调用栈
        
        Args:
            depth: 栈深度
            
        Returns:
            调用栈信息
        """
        stack = []
        
        try:
            frame = inspect.currentframe()
            # 跳过当前帧（get_call_stack自身）
            frame = frame.f_back if frame else None
            
            count = 0
            while frame and count < depth:
                frame_info = {
                    'filename': frame.f_code.co_filename,
                    'function': frame.f_code.co_name,
                    'line_number': frame.f_lineno,
                    'locals': {}
                }
                
                # 安全地获取局部变量（避免循环引用）
                for key, value in frame.f_locals.items():
                    try:
                        frame_info['locals'][key] = type(value).__name__
                    except:
                        frame_info['locals'][key] = 'unable_to_inspect'
                
                stack.append(frame_info)
                frame = frame.f_back
                count += 1
                
        except Exception as e:
            self._log(f"Error getting call stack: {e}")
        
        return stack
    
    def dump_session(self, session_id: str, file_path: str = None) -> str:
        """
        转储会话数据到文件
        
        Args:
            session_id: 会话ID
            file_path: 文件路径（可选）
            
        Returns:
            文件路径
        """
        if session_id not in self.sessions:
            raise KeyError(f"Session not found: {session_id}")
        
        if not file_path:
            file_path = self.log_dir / f"session_{session_id}_{int(time.time())}.json"
        
        session_data = self.sessions[session_id].copy()
        
        # 添加额外信息
        session_data['dump_time'] = time.time()
        session_data['breakpoints'] = self.breakpoints.copy()
        session_data['watch_expressions'] = self.watch_expressions.copy()
        
        # 保存到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, default=str)
        
        self._log(f"Session dumped: {session_id} -> {file_path}")
        return str(file_path)
    
    def _log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_message = f"[{timestamp}] {message}\n"
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message)
        except Exception as e:
            print(f"Failed to write log: {e}")
    
    def clear_logs(self, days_to_keep: int = 7):
        """
        清理旧日志
        
        Args:
            days_to_keep: 保留天数
        """
        cutoff_time = time.time() - (days_to_keep * 24 * 3600)
        
        for log_file in self.log_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_time:
                try:
                    log_file.unlink()
                    self._log(f"Old log file deleted: {log_file}")
                except Exception as e:
                    self._log(f"Failed to delete log file {log_file}: {e}")