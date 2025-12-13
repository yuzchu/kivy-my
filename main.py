
DEBUG='000debug2'
SDMAIN=f'/sdcard/{DEBUG}/main.py'
DEBUGPATH=f'/sdcard/{DEBUG}'

ROOT=os.getcwd()
if  os.path.exists(DEBUGPATH):
    def del_files(dir_path):
        if os.path.isfile(dir_path):
            try:
                os.remove(dir_path) # 这个可以删除单个文件，不能删除文件夹
            except BaseException as e:
                print(e)
        elif os.path.isdir(dir_path):
            file_lis = os.listdir(dir_path)
            for file_name in file_lis:
                # if file_name != 'wibot.log':
                tf = os.path.join(dir_path, file_name)
                del_files(tf)
        print('ok')
    from android.permissions import request_permissions, Permission, check_permission
    
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
    # permissions()
    # vthread.pool.waitall() 
    LOG_PATH=f'/sdcard/{DEBUG}/log'
    del_files(LOG_PATH)
    Config.set('kivy', 'log_dir', f'/sdcard/{DEBUG}/log')
    import logging
    from kivymd.toast import toast
    import android
    import shutil
    import py_compile
    # toast('调试工具第三.15版')
    #拷贝目录【类似unix下的cp -r aa bb】
    def copyDir(srcDir,dstDir):
        if os.path.exists(srcDir):
            __copyDir(srcDir,dstDir)
        else:
            print(srcDir+' not exist')
    def __copyDir(srcDir,dstDir):
        if not os.path.exists(dstDir):
            shutil.copytree(srcDir,dstDir)
            return
        lists=os.listdir(srcDir)
        for lt in lists:
            srcPath=os.path.join(srcDir,lt)
            goalPath=os.path.join(dstDir,lt)
            if os.path.isfile(srcPath):
                shutil.copyfile(srcPath,goalPath)
            else:
                __copyDir(srcPath,goalPath)
    
    if not os.path.exists(SDMAIN):
        file=open(SDMAIN, 'w')
        file.close()
        # if not os.path.exists('/sdcard/00spy/log'):
            # os.makedirs('/sdcard/00spy/log')
            
        # Config.set('kivy', 'log_dir', '/sdcard/00spy')
        # Config.set('kivy', 'log_level', 'error')
        logging.info('文件不存在,新建空文件')
    
        
       
    else:
        if not os.path.exists('main.py'):
            file=open('main.py', 'w')
            file.close()
        # Config.set('kivy', 'log_dir', '/sdcard/00spy')??%
        # Config.set('kivy', 'log_level', 'error')
        with open('main.py', 'rb') as file:
            lastfile = file.read().decode('utf8')
        with open(SDMAIN, 'rb') as file:
            newfile = file.read().decode('utf8')
        
                
    
        copyDir(f'/sdcard/{DEBUG}',ROOT)
        if lastfile!=newfile:
            os.remove('main.pyc')
from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.utils.set_bars_colors import set_bars_colors


class SampleApp(MDApp):

    def __init__(self, **kwargs) -> None:
        super(SampleApp, self).__init__(**kwargs)
        self.theme_cls.primary_palette = "Darkblue"

    def build(self) -> MDScreen:
        self.appKv="""
MDScreen:
    MDButton:
        style: 'tonal'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_press:
            app.apply_styles("Light") if (not app.theme_cls.theme_style == "Light") else app.apply_styles("Dark")

        MDButtonText:
            text: '我的!'
"""
        AppScreen = Builder.load_string(self.appKv)
        self.apply_styles("Light")
        return AppScreen

    def apply_styles(self, style: str = "Light") -> None:
        self.theme_cls.theme_style = style
        if style == "Light":
            Window.clearcolor = status_color = nav_color = app.theme_cls.surfaceColor
            style = "Dark"
        else:
            Window.clearcolor = status_color = nav_color = app.theme_cls.surfaceColor
            style = "Light"
        self.set_bars_colors(status_color, nav_color, style)

    def set_bars_colors(self, status_color: list[float] = [1.0, 1.0, 1.0, 1.0], nav_color: list[float] = [1.0, 1.0, 1.0, 1.0], style: str = "Dark") -> None:
        set_bars_colors(
            status_color,  # status bar color
            nav_color,  # navigation bar color
            style,  # icons style of status and navigation bar
        )

if __name__ == "__main__":
    app = SampleApp()
    app.run()
    
