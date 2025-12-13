"""
热更新系统UI界面
为Android应用提供图形化的热更新管理界面
"""

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import (
    StringProperty, BooleanProperty, NumericProperty,
    ListProperty, ObjectProperty, DictProperty
)

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.snackbar import Snackbar

import sys
from pathlib import Path

# 添加热更新系统路径
sys.path.insert(0, str(Path(__file__).parent))
from hot_reload import get_system, HotReloadSystem

# Kivy界面定义
KV = '''
<HotReloadUI>:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(10)
    
    MDBoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(50)
        spacing: dp(10)
        
        MDRaisedButton:
            id: btn_start
            text: '启动系统'
            on_press: root.start_system()
            disabled: root.system_running
        
        MDRaisedButton:
            id: btn_stop
            text: '停止系统'
            on_press: root.stop_system()
            disabled: not root.system_running
        
        MDRaisedButton:
            id: btn_refresh
            text: '刷新状态'
            on_press: root.refresh_status()
        
        MDLabel:
            text: '热更新系统'
            halign: 'center'
            font_style: 'H6'
            size_hint_x: 0.4
    
    MDBoxLayout:
        orientation: 'horizontal'
        spacing: dp(10)
        
        # 左侧：状态面板
        MDCard:
            orientation: 'vertical'
            size_hint_x: 0.4
            padding: dp(10)
            spacing: dp(10)
            
            MDLabel:
                text: '系统状态'
                font_style: 'H6'
                halign: 'center'
                size_hint_y: None
                height: dp(40)
            
            ScrollView:
                MDList:
                    id: status_list
            
            MDRaisedButton:
                text: '查看日志'
                on_press: root.show_logs()
                size_hint_y: None
                height: dp(40)
        
        # 右侧：模块管理
        MDCard:
            orientation: 'vertical'
            size_hint_x: 0.6
            padding: dp(10)
            spacing: dp(10)
            
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(50)
                spacing: dp(10)
                
                MDLabel:
                    text: '模块管理'
                    font_style: 'H6'
                    halign: 'left'
                    size_hint_x: 0.5
                
                MDRaisedButton:
                    text: '添加模块'
                    on_press: root.show_add_module_dialog()
                    size_hint_x: 0.5
            
            ScrollView:
                MDList:
                    id: module_list
    
    # 底部：控制面板
    MDCard:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(60)
        padding: dp(10)
        spacing: dp(10)
        
        MDRaisedButton:
            text: '配置管理'
            on_press: root.show_config_dialog()
        
        MDRaisedButton:
            text: '调试工具'
            on_press: root.show_debug_tools()
        
        MDRaisedButton:
            text: '性能监控'
            on_press: root.show_performance_monitor()
        
        MDRaisedButton:
            text: '运行演示'
            on_press: root.run_demo()

<ModuleItem>:
    orientation: 'horizontal'
    spacing: dp(10)
    padding: dp(5)
    size_hint_y: None
    height: dp(60)
    
    MDBoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.7
        
        MDLabel:
            text: root.module_name
            font_style: 'Subtitle1'
            halign: 'left'
        
        MDLabel:
            text: root.module_path
            font_style: 'Caption'
            halign: 'left'
            theme_text_color: 'Secondary'
    
    MDBoxLayout:
        orientation: 'horizontal'
        size_hint_x: 0.3
        spacing: dp(5)
        
        MDRaisedButton:
            text: '重载'
            size_hint_x: 0.5
            on_press: root.reload_module()
        
        MDRaisedButton:
            text: '删除'
            size_hint_x: 0.5
            on_press: root.delete_module()

<ConfigDialog>:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(20)
    size_hint_y: None
    height: dp(400)
    
    ScrollView:
        GridLayout:
            id: config_grid
            cols: 2
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height
            row_default_height: dp(40)
            
            # 配置项将动态添加

<DebugDialog>:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(20)
    size_hint_y: None
    height: dp(300)
    
    MDLabel:
        text: '调试工具'
        font_style: 'H6'
        halign: 'center'
        size_hint_y: None
        height: dp(40)
    
    TextInput:
        id: debug_input
        hint_text: '输入Python表达式进行求值'
        size_hint_y: None
        height: dp(100)
        multiline: True
    
    MDBoxLayout:
        orientation: 'horizontal'
        spacing: dp(10)
        
        MDRaisedButton:
            text: '求值'
            on_press: root.evaluate_expression()
        
        MDRaisedButton:
            text: '检查对象'
            on_press: root.inspect_object()
        
        MDRaisedButton:
            text: '调用栈'
            on_press: root.show_call_stack()
    
    ScrollView:
        MDLabel:
            id: debug_output
            text: ''
            size_hint_y: None
            height: self.texture_size[1]

<AddModuleDialog>:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(20)
    size_hint_y: None
    height: dp(200)
    
    MDLabel:
        text: '添加新模块'
        font_style: 'H6'
        halign: 'center'
    
    TextInput:
        id: module_name_input
        hint_text: '模块名称'
        size_hint_y: None
        height: dp(40)
    
    TextInput:
        id: module_path_input
        hint_text: '模块文件路径'
        size_hint_y: None
        height: dp(40)
    
    MDBoxLayout:
        orientation: 'horizontal'
        spacing: dp(10)
        
        MDRaisedButton:
            text: '浏览'
            on_press: root.browse_file()
        
        MDRaisedButton:
            text: '确定'
            on_press: root.add_module()
        
        MDFlatButton:
            text: '取消'
            on_press: root.dismiss()
'''

Builder.load_string(KV)

class ModuleItem(MDBoxLayout):
    """模块列表项"""
    module_name = StringProperty()
    module_path = StringProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.system = get_system()
    
    def reload_module(self):
        """重载模块"""
        try:
            self.system.reload_module(self.module_name)
            Snackbar(
                text=f"模块 '{self.module_name}' 已重载",
                duration=2
            ).open()
        except Exception as e:
            Snackbar(
                text=f"重载失败: {str(e)}",
                duration=3
            ).open()
    
    def delete_module(self):
        """删除模块"""
        try:
            self.system.manager.unload_module(self.module_name)
            self.system.config_manager.remove_module(self.module_name)
            
            # 从父容器中移除
            if self.parent:
                self.parent.remove_widget(self)
            
            Snackbar(
                text=f"模块 '{self.module_name}' 已删除",
                duration=2
            ).open()
        except Exception as e:
            Snackbar(
                text=f"删除失败: {str(e)}",
                duration=3
            ).open()

class ConfigDialog(ModalView):
    """配置对话框"""
    def __init__(self, system, **kwargs):
        super().__init__(**kwargs)
        self.system = system
        self.config = system.config_manager.config
        self._build_ui()
    
    def _build_ui(self):
        """构建配置界面"""
        grid = self.ids.config_grid
        
        # 清空现有内容
        grid.clear_widgets()
        
        # 添加配置项
        config_items = [
            ('检查间隔(秒):', 'check_interval', 'float', 0.5, 10.0),
            ('自动重载:', 'auto_reload', 'bool'),
            ('显示通知:', 'show_notifications', 'bool'),
            ('日志级别:', 'log_level', 'choice', ['debug', 'info', 'warning', 'error']),
            ('备份启用:', 'backup_enabled', 'bool'),
        ]
        
        for label, key, type_, *args in config_items:
            # 标签
            grid.add_widget(Label(text=label, size_hint_x=0.5))
            
            # 输入控件
            if type_ == 'bool':
                switch = Switch(active=getattr(self.config, key, False))
                switch.bind(active=lambda s, v, k=key: self._update_config(k, v))
                grid.add_widget(switch)
            
            elif type_ == 'float':
                from kivy.uix.slider import Slider
                min_val, max_val = args
                current = getattr(self.config, key, 1.0)
                slider = Slider(min=min_val, max=max_val, value=current)
                slider.bind(value=lambda s, v, k=key: self._update_config(k, v))
                grid.add_widget(slider)
            
            elif type_ == 'choice':
                choices = args[0]
                current = getattr(self.config, key, 'info').value
                spinner = Spinner(text=current, values=choices)
                spinner.bind(text=lambda s, v, k=key: self._update_config(k, v))
                grid.add_widget(spinner)
    
    def _update_config(self, key, value):
        """更新配置"""
        try:
            self.system.update_config(**{key: value})
            Snackbar(text="配置已更新", duration=1).open()
        except Exception as e:
            Snackbar(text=f"更新失败: {str(e)}", duration=2).open()

class DebugDialog(ModalView):
    """调试对话框"""
    def __init__(self, system, **kwargs):
        super().__init__(**kwargs)
        self.system = system
    
    def evaluate_expression(self):
        """求值表达式"""
        expr = self.ids.debug_input.text.strip()
        if not expr:
            return
        
        try:
            result = self.system.evaluate_expression(expr)
            self.ids.debug_output.text = f"结果: {repr(result)}"
        except Exception as e:
            self.ids.debug_output.text = f"错误: {str(e)}"
    
    def inspect_object(self):
        """检查对象"""
        expr = self.ids.debug_input.text.strip()
        if not expr:
            return
        
        try:
            # 尝试求值表达式获取对象
            obj = self.system.evaluate_expression(expr)
            info = self.system.inspect_object(obj)
            
            # 格式化显示
            output = []
            for key, value in info.items():
                if isinstance(value, dict):
                    output.append(f"{key}:")
                    for k, v in value.items():
                        output.append(f"  {k}: {v}")
                else:
                    output.append(f"{key}: {value}")
            
            self.ids.debug_output.text = "\n".join(output)
        except Exception as e:
            self.ids.debug_output.text = f"错误: {str(e)}"
    
    def show_call_stack(self):
        """显示调用栈"""
        try:
            stack = self.system.debugger.get_call_stack()
            output = ["调用栈:"]
            for i, frame in enumerate(stack):
                output.append(f"{i+1}. {frame['function']} at {frame['filename']}:{frame['line_number']}")
            
            self.ids.debug_output.text = "\n".join(output)
        except Exception as e:
            self.ids.debug_output.text = f"错误: {str(e)}"

class AddModuleDialog(ModalView):
    """添加模块对话框"""
    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
    
    def browse_file(self):
        """浏览文件"""
        # 这里可以集成文件浏览器
        # 暂时使用示例路径
        self.ids.module_path_input.text = "./hot_reload/example_module.py"
    
    def add_module(self):
        """添加模块"""
        name = self.ids.module_name_input.text.strip()
        path = self.ids.module_path_input.text.strip()
        
        if not name or not path:
            Snackbar(text="请填写模块名称和路径", duration=2).open()
            return
        
        if self.callback:
            self.callback(name, path)
        
        self.dismiss()

class HotReloadUI(MDBoxLayout):
    """热更新系统主界面"""
    system_running = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.system = get_system()
        self._update_status()
        
        # 定时刷新状态
        Clock.schedule_interval(self._update_status, 1.0)
    
    def _update_status(self, *args):
        """更新状态显示"""
        status = self.system.get_status()
        self.system_running = status['running']
        
        # 更新状态列表
        status_list = self.ids.status_list
        status_list.clear_widgets()
        
        status_items = [
            ("运行状态", "运行中" if status['running'] else "已停止"),
            ("会话ID", status['session_id'] or "无"),
            ("加载模块数", str(len(status['loaded_modules']))),
            ("调试会话", "启用" if status['debug_session'] else "禁用"),
        ]
        
        for title, value in status_items:
            item = TwoLineListItem(
                text=title,
                secondary_text=value
            )
            status_list.add_widget(item)
        
        # 更新模块列表
        module_list = self.ids.module_list
        module_list.clear_widgets()
        
        for module_name in status['loaded_modules']:
            module_info = self.system.manager.get_module_info(module_name)
            item = ModuleItem(
                module_name=module_name,
                module_path=module_info.get('path', '未知')
            )
            module_list.add_widget(item)
    
    def start_system(self):
        """启动系统"""
        try:
            self.system.start()
            self.system_running = True
            Snackbar(text="热更新系统已启动", duration=2).open()
        except Exception as e:
            Snackbar(text=f"启动失败: {str(e)}", duration=3).open()
    
    def stop_system(self):
        """停止系统"""
        try:
            self.system.stop()
            self.system_running = False
            Snackbar(text="热更新系统已停止", duration=2).open()
        except Exception as e:
            Snackbar(text=f"停止失败: {str(e)}", duration=3).open()
    
    def refresh_status(self):
        """刷新状态"""
        self._update_status()
        Snackbar(text="状态已刷新", duration=1).open()
    
    def show_logs(self):
        """显示日志"""
        # 这里可以集成日志查看器
        Snackbar(text="日志功能开发中", duration=2).open()
    
    def show_add_module_dialog(self):
        """显示添加模块对话框"""
        dialog = AddModuleDialog(callback=self._add_module_callback)
        dialog.open()
    
    def _add_module_callback(self, name, path):
        """添加模块回调"""
        try:
            self.system.load_new_module(path, name)
            Snackbar(text=f"模块 '{name}' 已添加", duration=2).open()
            self._update_status()
        except Exception as e:
            Snackbar(text=f"添加失败: {str(e)}", duration=3).open()
    
    def show_config_dialog(self):
        """显示配置对话框"""
        dialog = ConfigDialog(self.system)
        dialog.open()
    
    def show_debug_tools(self):
        """显示调试工具"""
        dialog = DebugDialog(self.system)
        dialog.open()
    
    def show_performance_monitor(self):
        """显示性能监控"""
        try:
            report = self.system.get_performance_report()
            
            # 创建性能报告对话框
            content = BoxLayout(orientation='vertical', spacing=dp(10))
            scroll = ScrollView()
            
            text = "性能报告:\n"
            for func_name, data in report.get('functions', {}).items():
                text += f"\n{func_name}:\n"
                text += f"  调用次数: {data['call_count']}\n"
                text += f"  平均耗时: {data['avg_duration']:.4f}s\n"
                text += f"  总耗时: {data['total_duration']:.4f}s\n"
            
            label = Label(text=text, size_hint_y=None, halign='left', valign='top')
            label.bind(texture_size=lambda lbl, size: setattr(lbl, 'height', size[1]))
            scroll.add_widget(label)
            content.add_widget(scroll)
            
            dialog = MDDialog(
                title="性能监控",
                type="custom",
                content_cls=content,
                buttons=[
                    MDFlatButton(text="关闭", on_release=lambda x: dialog.dismiss())
                ]
            )
            dialog.open()
            
        except Exception as e:
            Snackbar(text=f"获取性能数据失败: {str(e)}", duration=3).open()
    
    def run_demo(self):
        """运行演示"""
        try:
            # 导入并运行演示
            from hot_reload.demo import main
            main()
            Snackbar(text="演示已运行，请查看控制台输出", duration=3).open()
        except Exception as e:
            Snackbar(text=f"运行演示失败: {str(e)}", duration=3).open()

class HotReloadApp(MDApp):
    """热更新系统应用"""
    def build(self):
        self.title = "Python代码热更新系统"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        return HotReloadUI()

def main():
    """主函数"""
    app = HotReloadApp()
    app.run()

if __name__ == "__main__":
    main()