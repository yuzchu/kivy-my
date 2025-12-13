from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.utils.set_bars_colors import set_bars_colors

import sys
from pathlib import Path

# 添加热更新系统路径
sys.path.insert(0, str(Path(__file__).parent))
from hot_reload import HotReloadSystem, get_system


class SampleApp(MDApp):

    def __init__(self, **kwargs) -> None:
        super(SampleApp, self).__init__(**kwargs)
        self.theme_cls.primary_palette = "Darkblue"
        
        # 初始化热更新系统
        self.hot_reload_system = None
        self._init_hot_reload()

    def _init_hot_reload(self):
        """初始化热更新系统"""
        try:
            # 创建热更新系统实例
            self.hot_reload_system = HotReloadSystem()
            
            # 添加示例模块到配置
            example_path = Path(__file__).parent / "hot_reload" / "example_module.py"
            if example_path.exists():
                self.hot_reload_system.config_manager.add_module(
                    name="example_module",
                    path=str(example_path),
                    enabled=True
                )
            
            print("[App] 热更新系统初始化完成")
            
        except Exception as e:
            print(f"[App] 热更新系统初始化失败: {e}")

    def build(self) -> MDScreen:
        self.appKv="""
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)
        
        MDLabel:
            text: 'Python代码热更新演示'
            halign: 'center'
            font_style: 'H4'
            size_hint_y: None
            height: dp(60)
        
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            
            MDRaisedButton:
                id: btn_toggle_theme
                style: 'tonal'
                text: '切换主题'
                on_press:
                    app.apply_styles("Light") if (not app.theme_cls.theme_style == "Light") else app.apply_styles("Dark")
            
            MDRaisedButton:
                id: btn_start_hot_reload
                text: '启动热更新系统'
                on_press: app.start_hot_reload()
            
            MDRaisedButton:
                id: btn_stop_hot_reload
                text: '停止热更新系统'
                on_press: app.stop_hot_reload()
                disabled: True
            
            MDRaisedButton:
                id: btn_open_ui
                text: '打开热更新管理界面'
                on_press: app.open_hot_reload_ui()
            
            MDRaisedButton:
                id: btn_run_demo
                text: '运行热更新演示'
                on_press: app.run_hot_reload_demo()
        
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            
            MDLabel:
                text: '热更新系统状态'
                halign: 'center'
                font_style: 'H6'
                size_hint_y: None
                height: dp(40)
            
            MDLabel:
                id: lbl_status
                text: '未启动'
                halign: 'center'
                theme_text_color: 'Secondary'
        
        MDBoxLayout:
            orientation: 'horizontal'
            spacing: dp(10)
            size_hint_y: None
            height: dp(40)
            
            MDRaisedButton:
                text: '测试计算器'
                on_press: app.test_calculator()
            
            MDRaisedButton:
                text: '重载示例模块'
                on_press: app.reload_example_module()
"""
        AppScreen = Builder.load_string(self.appKv)
        self.apply_styles("Light")
        
        # 设置热更新系统状态标签
        self.status_label = AppScreen.ids.lbl_status
        
        return AppScreen

    def apply_styles(self, style: str = "Light") -> None:
        self.theme_cls.theme_style = style
        if style == "Light":
            Window.clearcolor = status_color = nav_color = self.theme_cls.surfaceColor
            style = "Dark"
        else:
            Window.clearcolor = status_color = nav_color = self.theme_cls.surfaceColor
            style = "Light"
        self.set_bars_colors(status_color, nav_color, style)

    def set_bars_colors(self, status_color: list[float] = [1.0, 1.0, 1.0, 1.0], nav_color: list[float] = [1.0, 1.0, 1.0, 1.0], style: str = "Dark") -> None:
        set_bars_colors(
            status_color,  # status bar color
            nav_color,  # navigation bar color
            style,  # icons style of status and navigation bar
        )

    def start_hot_reload(self):
        """启动热更新系统"""
        if self.hot_reload_system:
            try:
                self.hot_reload_system.start()
                self.status_label.text = "热更新系统运行中"
                self.root.ids.btn_start_hot_reload.disabled = True
                self.root.ids.btn_stop_hot_reload.disabled = False
                
                # 显示通知
                from kivymd.uix.snackbar import Snackbar
                Snackbar(text="热更新系统已启动", duration=2).open()
                
                print("[App] 热更新系统已启动")
                
            except Exception as e:
                self.status_label.text = f"启动失败: {str(e)}"
                print(f"[App] 热更新系统启动失败: {e}")

    def stop_hot_reload(self):
        """停止热更新系统"""
        if self.hot_reload_system:
            try:
                self.hot_reload_system.stop()
                self.status_label.text = "热更新系统已停止"
                self.root.ids.btn_start_hot_reload.disabled = False
                self.root.ids.btn_stop_hot_reload.disabled = True
                
                # 显示通知
                from kivymd.uix.snackbar import Snackbar
                Snackbar(text="热更新系统已停止", duration=2).open()
                
                print("[App] 热更新系统已停止")
                
            except Exception as e:
                self.status_label.text = f"停止失败: {str(e)}"
                print(f"[App] 热更新系统停止失败: {e}")

    def open_hot_reload_ui(self):
        """打开热更新管理界面"""
        try:
            from hot_reload_ui import HotReloadApp
            
            # 创建并运行热更新UI应用
            ui_app = HotReloadApp()
            
            # 注意：在Android应用中，可能需要使用不同的方式打开新窗口
            # 这里简化处理，直接运行演示
            print("[App] 打开热更新管理界面")
            
            # 显示提示
            from kivymd.uix.snackbar import Snackbar
            Snackbar(text="请查看控制台输出的热更新演示", duration=3).open()
            
            # 运行演示
            self.run_hot_reload_demo()
            
        except Exception as e:
            print(f"[App] 打开热更新UI失败: {e}")
            from kivymd.uix.snackbar import Snackbar
            Snackbar(text=f"打开界面失败: {str(e)}", duration=3).open()

    def run_hot_reload_demo(self):
        """运行热更新演示"""
        try:
            from hot_reload.demo import main
            
            # 运行演示
            print("[App] 开始运行热更新演示...")
            main()
            
            # 显示完成通知
            from kivymd.uix.snackbar import Snackbar
            Snackbar(text="热更新演示已完成，请查看控制台输出", duration=3).open()
            
        except Exception as e:
            print(f"[App] 运行热更新演示失败: {e}")
            from kivymd.uix.snackbar import Snackbar
            Snackbar(text=f"运行演示失败: {str(e)}", duration=3).open()

    def test_calculator(self):
        """测试计算器功能"""
        try:
            if self.hot_reload_system and self.hot_reload_system.is_running:
                # 获取示例模块
                module = self.hot_reload_system.manager.loaded_modules.get('example_module', {}).get('module')
                
                if module:
                    # 使用计算器
                    calc = module.Calculator("应用计算器")
                    result1 = calc.add(100, 50)
                    result2 = calc.multiply(10, 5)
                    
                    # 显示结果
                    from kivymd.uix.dialog import MDDialog
                    dialog = MDDialog(
                        title="计算器测试",
                        text=f"加法: 100 + 50 = {result1}\\n乘法: 10 × 5 = {result2}\\n历史记录: {calc.get_history()}",
                        buttons=[
                            MDFlatButton(text="确定", on_release=lambda x: dialog.dismiss())
                        ]
                    )
                    dialog.open()
                else:
                    from kivymd.uix.snackbar import Snackbar
                    Snackbar(text="请先启动热更新系统并加载示例模块", duration=3).open()
            else:
                from kivymd.uix.snackbar import Snackbar
                Snackbar(text="请先启动热更新系统", duration=3).open()
                
        except Exception as e:
            print(f"[App] 测试计算器失败: {e}")
            from kivymd.uix.snackbar import Snackbar
            Snackbar(text=f"测试失败: {str(e)}", duration=3).open()

    def reload_example_module(self):
        """重载示例模块"""
        try:
            if self.hot_reload_system and self.hot_reload_system.is_running:
                self.hot_reload_system.reload_module("example_module")
                
                from kivymd.uix.snackbar import Snackbar
                Snackbar(text="示例模块已重载", duration=2).open()
                
                print("[App] 示例模块已重载")
            else:
                from kivymd.uix.snackbar import Snackbar
                Snackbar(text="请先启动热更新系统", duration=3).open()
                
        except Exception as e:
            print(f"[App] 重载示例模块失败: {e}")
            from kivymd.uix.snackbar import Snackbar
            Snackbar(text=f"重载失败: {str(e)}", duration=3).open()

    def on_stop(self):
        """应用停止时清理"""
        if self.hot_reload_system and self.hot_reload_system.is_running:
            self.hot_reload_system.stop()
            print("[App] 应用停止，热更新系统已清理")


if __name__ == "__main__":
    app = SampleApp()
    app.run()