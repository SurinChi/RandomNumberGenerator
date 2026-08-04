# ui.py

import traceback

from win11toast import notify

from PySide6.QtCore import Qt, QSize, QEventLoop, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import (
            MSFluentWindow, MessageBox, SplashScreen, InfoBar, InfoBarPosition, NavigationItemPosition
        )
from qfluentwidgets import FluentIcon as fi

from .qfw_component import HomePage, SettingsPage, InfoPage, HistoryPage
        
class ShowResult(MessageBox):
    def __init__(
            self,
            title,
            content,
            parent=None
        ):
        super().__init__(title, content, parent)
        self.hideCancelButton()

class EmptyWindow(MSFluentWindow):
    def __init__(self, e):
        super().__init__()
        desktop = QApplication.primaryScreen().availableSize()
        w, h = desktop.width(), desktop.height()
        self.resize(QSize(1000, 800))
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        i = MessageBox("Error", str(e), self)
        i.yesSignal.connect(self.close)
        i.hideCancelButton()
        i.show()

class MainWindowBase(MSFluentWindow):
    def __init__(
            self,
            icon,
            avatar_icon,
            avatar_icon_2,
            donate_window_icon,
            wechat_icon_path: str,
            alipay_icon_path: str,
            yuanshen_icon_path: str,
            yuanshen_cloud_icon_path: str,
            wechat_qr_path,
            alipay_qr_path,
            config,
            history_mgr,
            version="0.0.0",
    ):
        super().__init__()
        # data
        self.icon = QIcon(str(icon))
        self.sp = SplashScreen(self.icon, self)
        self.avatar_icon = QIcon(str(avatar_icon))
        self.avatar_icon_2 = QIcon(str(avatar_icon_2))
        self.donate_window_icon = QIcon(str(donate_window_icon))
        self.wechat_icon = QIcon(str(wechat_icon_path))
        self.alipay_icon = QIcon(str(alipay_icon_path))
        self.yuanshen_icon = QIcon(str(yuanshen_icon_path))
        self.yuanshen_cloud_icon = QIcon(str(yuanshen_cloud_icon_path))
        self.version = version

        # oprations
        self._init_args()
        

        self.homePage = HomePage(config, fi, self)
        self.historyPage = HistoryPage(config, history_mgr, self)
        self.settingsPage = SettingsPage(config, fi, self)
        self.infoPage = InfoPage(
                            config,
                            fi, 
                            self.donate_window_icon,
                            self.wechat_icon,
                            self.alipay_icon,
                            self.yuanshen_icon,
                            self.yuanshen_cloud_icon,
                            wechat_qr_path,
                            alipay_qr_path,
                            self.desktop,
                            self
                        )

        self._init_ui()


    def _init_args(self):
        self.setWindowIcon(self.icon)
        self.setWindowTitle(f'随机数生成器')
        self.resize(QSize(800, 600))
        self.desktop = QApplication.primaryScreen().availableSize()
        w, h = self.desktop.width(), self.desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def _init_ui(self):
        self.addSubInterface(self.homePage, fi.PLAY, "主页")
        self.addSubInterface(self.historyPage, fi.HISTORY, "历史")
        self.addSubInterface(self.settingsPage, fi.SETTING, "设置", position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.infoPage, fi.INFO, "关于", position=NavigationItemPosition.BOTTOM)

    def showError(self, content, window):
        InfoBar.warning(
            title='Error',
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=5000,    # 永不消失，值为-1
            parent=window
        )
    def showInfo(self, content, window):
        InfoBar.info(
            title='Info',
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=5000,    # 永不消失，值为-1
            parent=window
        )


class MainWindow(MainWindowBase):
    def __init__(
            self,
            icon,
            avatar_icon,
            avatar_icon_2,
            donate_window_icon,
            wechat_icon_path,
            alipay_icon_path,
            yuanshen_icon_path,
            yuanshen_cloud_icon,
            wechat_qr_path,
            alipay_qr_path,
            exceptions: list,
            validator,
            convertor,
            generator,
            timer,
            history_mgr,
            config,
            version="0.0.0"
        ):
        super().__init__(
            icon,
            avatar_icon,
            avatar_icon_2,
            donate_window_icon,
            wechat_icon_path,
            alipay_icon_path,
            yuanshen_icon_path,
            yuanshen_cloud_icon,
            wechat_qr_path,
            alipay_qr_path,
            config,
            history_mgr,
            version
        )

        self.exceptions = exceptions
        self.validator = validator
        
        self.convertor = convertor
        self.generator = generator
        self.timer = timer
        self.history_mgr = history_mgr
        self.config = config

        # 将配置对象传递给 Validator, Convertor, 和 Generator 类
        self.validator.globalCfg = self.config
        self.convertor.globalCfg = self.config
        self.generator.globalCfg = self.config
        
        self.homePage.generate_requested.connect(self.generate)
        self.homePage.generate_requested.connect(self.historyPage.refresh)
        self.sp.finish()

    def generate(self, request_dict: dict):
        timestamp = self.timer.get_timestamp(1)
        try:
            min = request_dict.get('min', '')
            max = request_dict.get('max', '')
            count = request_dict.get('count', '')
            self.validator.validate((min, max, count))
            min, max, count = self.convertor.convert(min, max, count)
            nums = self.generator.main_func(min, max, count)
            nums = sorted(nums)

            # 保存数据
            if self.config.enableHistory.value:
                self.history_mgr.add_record(min, max, count, str(self.config.current_mode()), nums)

            if len(nums) > 40:
                nums = nums[:40]
                nums = str(nums)[1:-1] + "......\n\n(完整结果请导出后查看)"
            else:
                nums = str(nums)[1:-1]

            loop = QEventLoop()                  # 创建循环
            self.homePage.setDisabled(True)  # 禁用主窗口
            QTimer.singleShot(600, loop.quit)    # 延迟 1 秒后退出事件循环
            loop.exec()                          # 进入事件循环，界面仍然可以响应
            self.homePage.setDisabled(False)  # 启用主窗口
            
            if self.config.current_notification() == self.config.NotificationMode.NOTI:
                notify(
                    title="随机数生成器",
                    body=f"范围：{min}~{max}，数量：{count}\n生成数：{nums}"
                )
            else:
                showResult = ShowResult("生成成功！", f"范围：{min} ~ {max}\n数量：{count}\n\n{nums}", self)
                showResult.show()
        
        except self.exceptions[0] as e:
            self.showError(f"{e}", self)
        except self.exceptions[1] as e:
            self.showError(f"{e}", self)
        except self.exceptions[2] as e:
            self.showInfo(f"{e}", self)
        except self.exceptions[3] as e:
            self.showError(f"{e}", self)
        except Exception as e:
            timestamp = self.timer.get_timestamp(1)
            msg = traceback.format_exc()
            self.showError(f"{timestamp}\n{msg}", self)
            raise
