from utils import (
            Generator, Convertor, Validator, # Toolkits
            CountZeroError, CountFloatError, InputValueError, ValueRangeException, 
            HistoryManager, Timer, config
        )
from ui import MainWindow, EmptyWindow


import traceback
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from qfluentwidgets import setFontFamilies, qconfig
from pathlib import Path
import json


# main_icon_path = SRC_DIR / "icons" / "main_icon.png"
# result_icon_path = SRC_DIR / "icons" / "result.png"

def load_custom_fonts(SRC_DIR):
    """加载自定义字体并返回字体族名称列表"""
    fonts_dir = SRC_DIR / "fonts/"
    loaded_families = []

    for font_file in fonts_dir.glob("*.ttf"):
        font_id = QFontDatabase.addApplicationFont(str(font_file))
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                loaded_families.append(families[0])
        else:
            print(f"❌ 加载失败: {font_file.name}")
            
        return loaded_families


if __name__ == "__main__":
    try:
        app = QApplication()
        SRC_DIR = Path(__file__).parent
        # 1. 加载自定义字体
        custom_fonts = load_custom_fonts(SRC_DIR)

        # 2. 如果成功加载了字体，设置为 QFluentWidgets 的默认字体
        if custom_fonts:
            # 将自定义字体放在最前面，然后保留原有的后备字体[citation:1]
            default_fonts = custom_fonts + ["Microsoft YaHei", "Segoe UI", "PingFang SC"]
            setFontFamilies(default_fonts)

        pathfile = Path(SRC_DIR) / "config/path.json"
        if pathfile.exists():
            content = pathfile.read_text()
        else:
            raise Exception("启动文件损坏，请彻底删除软件的目录后重新安装。")
        path_dict = json.loads(content)

        qconfig.load('src/config/config.json', config)
        main_icon_path = SRC_DIR / path_dict.get("main_icon_path")
        avatar_icon_path = SRC_DIR / path_dict.get("avatar_icon_path")
        avatar_icon_path_2 = SRC_DIR / path_dict.get("avatar_icon_path_2")
        donate_window_icon_path = SRC_DIR / path_dict.get("donate_window_icon_path")
        wechat_icon_path = SRC_DIR / path_dict.get("wechat_icon")
        alipay_icon_path = SRC_DIR / path_dict.get("alipay_icon")
        wechat_qr_path = SRC_DIR / path_dict.get("wechat_qr_path")
        alipay_qr_path = SRC_DIR / path_dict.get("alipay_qr_path")
        yuanshen_icon_path = SRC_DIR / path_dict.get("yuanshen_icon_path")
        yuanshen_cloud_icon_path = SRC_DIR / path_dict.get("yuanshen_cloud_icon_path")

        history_mgr = HistoryManager(SRC_DIR / path_dict.get("history_path", "history/"), Timer)

        window = MainWindow(
            main_icon_path,
            avatar_icon_path,
            avatar_icon_path_2,
            donate_window_icon_path,
            wechat_icon_path,
            alipay_icon_path,
            yuanshen_icon_path,
            yuanshen_cloud_icon_path,
            wechat_qr_path,
            alipay_qr_path,
            [CountZeroError, CountFloatError, InputValueError, ValueRangeException],
            Validator,
            Convertor,
            Generator,
            Timer,
            history_mgr,
            config,
            "0.0.2")
        
        window.show()
        app.exec()
    except Exception as e:
        detail = traceback.format_exc()
        empty_window = EmptyWindow(f"{e}\n\n程序启动失败，请将此错误信息截图并发送给开发者，以便修复问题。")
        empty_window.show()
        app.exec()
        raise