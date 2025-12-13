import os
import shutil
import logging
from kivy.config import Config
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.toast import toast
from android.permissions import request_permissions, Permission, check_permission

class DebugButton(BoxLayout):
    """调试工具按钮，整合调试功能"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 20
        
        # 创建标签
        self.label = MDLabel(
            text="调试工具第三.15版",
            halign="center",
            font_style="H6"
        )
        self.add_widget(self.label)
        
        # 创建按钮
        self.button = MDRaisedButton(
            text="执行调试操作",
            size_hint=(1, None),
            height=50,
            on_release=self.execute_debug
        )
        self.add_widget(self.button)
        
        # 状态标签
        self.status_label = MDLabel(
            text="就绪",
            halign="center",
            theme_text_color="Secondary"
        )
        self.add_widget(self.status_label)
        
        # 初始化变量
        self.DEBUG = '000debug2'
        self.SDMAIN = f'/sdcard/{self.DEBUG}/main.py'
        self.DEBGPATH = f'/sdcard/{self.DEBUG}'
        self.ROOT = os.getcwd()
        self.LOG_PATH = f'/sdcard/{self.DEBUG}/log'
    
    def execute_debug(self, *args):
        """执行调试操作"""
        try:
            self.status_label.text = "正在执行调试操作..."
            
            # 请求权限
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            
            # 检查调试目录是否存在
            if os.path.exists(self.DEBGPATH):
                # 清理日志目录
                self._del_files(self.LOG_PATH)
                
                # 设置Kivy日志配置
                Config.set('kivy', 'log_dir', f'/sdcard/{self.DEBUG}/log')
                
                # 确保main.py文件存在
                if not os.path.exists(self.SDMAIN):
                    with open(self.SDMAIN, 'w') as file:
                        file.close()
                    logging.info('文件不存在,新建空文件')
                
                # 复制调试文件到当前目录
                self._copyDir(self.DEBGPATH, self.ROOT)
                
                # 比较main.py文件内容
                if os.path.exists('main.py') and os.path.exists(self.SDMAIN):
                    with open('main.py', 'rb') as file:
                        lastfile = file.read().decode('utf8', errors='ignore')
                    with open(self.SDMAIN, 'rb') as file:
                        newfile = file.read().decode('utf8', errors='ignore')
                    
                    if lastfile != newfile:
                        # 删除main.pyc文件（如果存在）
                        pyc_file = 'main.pyc'
                        if os.path.exists(pyc_file):
                            os.remove(pyc_file)
                            self.status_label.text = "已删除main.pyc文件"
                
                toast('调试操作完成！')
                self.status_label.text = "调试操作完成"
                
            else:
                toast('调试目录不存在')
                self.status_label.text = "调试目录不存在"
                
        except Exception as e:
            self.status_label.text = f"错误: {str(e)}"
            toast(f'执行出错: {str(e)}')
    
    def _del_files(self, dir_path):
        """递归删除文件或目录"""
        if os.path.isfile(dir_path):
            try:
                os.remove(dir_path)
            except Exception as e:
                print(f"删除文件错误: {e}")
        elif os.path.isdir(dir_path):
            file_lis = os.listdir(dir_path)
            for file_name in file_lis:
                tf = os.path.join(dir_path, file_name)
                self._del_files(tf)
        print('清理完成')
    
    def _copyDir(self, srcDir, dstDir):
        """递归复制目录"""
        if not os.path.exists(srcDir):
            print(f"源目录不存在: {srcDir}")
            return
        
        if not os.path.exists(dstDir):
            shutil.copytree(srcDir, dstDir)
            return
        
        lists = os.listdir(srcDir)
        for lt in lists:
            srcPath = os.path.join(srcDir, lt)
            goalPath = os.path.join(dstDir, lt)
            
            if os.path.isfile(srcPath):
                try:
                    shutil.copyfile(srcPath, goalPath)
                except Exception as e:
                    print(f"复制文件错误 {srcPath} -> {goalPath}: {e}")
            else:
                self._copyDir(srcPath, goalPath)


# 使用示例
if __name__ == "__main__":
    from kivy.app import App
    
    class DebugApp(App):
        def build(self):
            return DebugButton()
    
    DebugApp().run()