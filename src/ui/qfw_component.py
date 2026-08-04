# qfw_component.py
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QDesktopServices, QPixmap
from PySide6.QtWidgets import QSizePolicy, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QFileDialog
from qfluentwidgets import (
    MSFluentWindow, ImageLabel, PrimaryPushButton, PushButton, BodyLabel, SettingCardGroup, SubtitleLabel, LineEdit, FlowLayout,
    ComboBoxSettingCard, ScrollArea, RangeSettingCard, PrimaryPushSettingCard, HyperlinkCard, CardWidget, MessageBox, InfoBar,
    SwitchSettingCard, InfoBarPosition
)

import json
from pathlib import Path



class InputPage(QFrame):
    def __init__(self, icons, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("inputPage")
        self.icons = icons
        self.buttons = []
        self._init_ui()

    def _init_ui(self):
        self.layout = FlowLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setVerticalSpacing(20)
        self.layout.setHorizontalSpacing(10)

        self.clear_btn = PrimaryPushButton("清除", icon=self.icons.CLOSE)
        self.clear_btn.setFocusPolicy(Qt.NoFocus)
        self.clear_btn.setFixedWidth(125)  # 可适当加宽，便于识别
        self.buttons.append(self.clear_btn)
        self.layout.addWidget(self.clear_btn)

        self.backspace_btn = PushButton("⌫ 删除")
        self.backspace_btn.setFocusPolicy(Qt.NoFocus)
        self.backspace_btn.setFixedWidth(125)  # 可适当加宽，便于识别
        self.buttons.append(self.backspace_btn)
        self.layout.addWidget(self.backspace_btn)

        for i in range(0, 10):
            if i < 9:
                i += 1
            else:
                i = 0
            btn = PushButton(f"{i}")
            btn.setFocusPolicy(Qt.NoFocus)  # 关键：阻止按钮获得焦点
            self.buttons.append(btn)
            self.layout.addWidget(btn)
        
    def connect_all_buttons(self, slot):
        for btn in self.buttons:
            btn.clicked.connect(lambda checked, b=btn: slot(b.text()))


class HomePage(QFrame):

    generate_requested = Signal(dict)

    def __init__(self, cfg, icon, parent=None):
        super().__init__()
        self.setObjectName("homePage")
        self.icon = icon
        self.cfg = cfg
        self.parent = parent
        self._init_ui()

        # 默认焦点在最小值输入框
        self.current_lineEdit = self.min_lineEdit

        # 直接连接 InputPage 的按钮点击事件到本地的槽函数
        self.input_page.connect_all_buttons(self._on_num_clicked)

    def _init_ui(self):
        # 创建控件

        self.input_page = InputPage(self.icon, self)
        # Layouts
        self.hLayout = QHBoxLayout(self)
        self.vLayout = QVBoxLayout()
        
        # Labels
        self.suggest_mode_label = SubtitleLabel(text=f'当前模式：{self.cfg.current_mode()}')
        self.suggestion_label = SubtitleLabel(text='请按提示输入数据')
        self.min_label = BodyLabel('请输入最小值：')
        self.max_label = BodyLabel('请输入最大值：')
        self.count_label = BodyLabel('请输入生成随机数个数：')
        # lineEdits
        self.min_lineEdit = LineEdit()
        self.max_lineEdit = LineEdit()
        self.count_lineEdit = LineEdit()

        # btns
        self.btn = PrimaryPushButton(text="开始生成")

        # 定制
        self.suggestion_label.setFixedHeight(40)
        self.suggestion_label.setAlignment(Qt.AlignVCenter|Qt.AlignLeft)
        self.btn.setFixedHeight(32)
        self.btn.clicked.connect(self.generate_request)
        
        # 安装事件监听器
        self.min_lineEdit.installEventFilter(self)
        self.max_lineEdit.installEventFilter(self)
        self.count_lineEdit.installEventFilter(self)

        # 添加控件
        self.vLayout.addSpacing(10)
        self.vLayout.addWidget(self.suggestion_label)
        self.vLayout.addSpacing(20)

        self.vLayout.addWidget(self.min_label)
        self.vLayout.addSpacing(5)
        self.vLayout.addWidget(self.min_lineEdit)

        self.vLayout.addSpacing(10)
        
        self.vLayout.addWidget(self.max_label)
        self.vLayout.addSpacing(5)
        self.vLayout.addWidget(self.max_lineEdit)

        self.vLayout.addSpacing(10)
        
        self.vLayout.addWidget(self.count_label)
        self.vLayout.addSpacing(5)
        self.vLayout.addWidget(self.count_lineEdit)

        self.vLayout.addSpacing(20)
        self.vLayout.addWidget(self.btn)
        self.vLayout.addStretch(1)
        
        self.hLayout.addSpacing(10)
        self.hLayout.addLayout(self.vLayout)
        self.hLayout.addSpacing(10)
        line = QFrame()
        line.setFrameShape(QFrame.VLine)   # 水平线
        line.setFrameShadow(QFrame.Sunken) # 凹陷效果
        self.hLayout.addWidget(line)
        self.hLayout.addSpacing(10)
        self.hLayout.addWidget(self.input_page)
        self.hLayout.addSpacing(10)

    def eventFilter(self, obj, event):
        if event.type() == event.Type.FocusIn:
            if obj is self.min_lineEdit:
                self.current_lineEdit = self.min_lineEdit
            elif obj is self.max_lineEdit:
                self.current_lineEdit = self.max_lineEdit
            elif obj is self.count_lineEdit:
                self.current_lineEdit = self.count_lineEdit
        return super().eventFilter(obj, event)
    
    def _on_num_clicked(self, num_str: str):
        """直接处理数字按钮点击"""
        if self.current_lineEdit is None:
            self.current_lineEdit = self.min_lineEdit
            self.min_lineEdit.setFocus()

        if num_str == "⌫ 删除":                                              # 与按钮的文本保持一致
            current_text = self.current_lineEdit.text()                            # 删除输入框的最后一个字符
            if current_text:                                                       # 如果输入框不为空
                self.current_lineEdit.setText(current_text[:-1])                   # 去掉最后一个字符
        elif num_str == "清空":
            self.current_lineEdit.clear()                                          # 删除输入框的所有字符
        else:
            self.current_lineEdit.setText(self.current_lineEdit.text() + num_str)  # 插入数字

        # 确保光标在末尾，并保持焦点
        self.current_lineEdit.end(False)
        self.current_lineEdit.setFocus()

    def generate_request(self):
        request_dict = {}
        min_val = self.min_lineEdit.text()
        max_val = self.max_lineEdit.text()
        count_val = self.count_lineEdit.text()
        request_dict.update({'min':min_val, 'max':max_val, 'count':count_val})
        self.generate_requested.emit(request_dict)


class HistoryCard(CardWidget):
    """单条历史记录卡片"""
    card_clicked = Signal(dict)  # 点击时发射数据

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data
        self._init_ui()
        self.setCursor(Qt.PointingHandCursor)

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        # # ID/时间标签
        # id_label = BodyLabel(self.data.get('id', ''))
        # id_label.setFixedWidth(130)
        # layout.addWidget(id_label)

        # 参数信息
        params = f"最小值: {self.data['min']}  最大值: {self.data['max']}  个数: {self.data['count']}"
        param_label = BodyLabel(params)
        # param_label.setStyleSheet("color: #0066cc;")
        layout.addWidget(param_label) # , stretch=1

        # 模式标签
        mode_labels = {
                    'GenerateMode.UNIQUE' : '整数 不重复',
                    'GenerateMode.REPEAT' : '整数 可重复',
                    'GenerateMode.UNIQUE_FLOAT' : '浮点数 不重复',
                    'GenerateMode.REPEAT_FLOAT' : '浮点数 可重复'
                }
        text = mode_labels[self.data.get('mode_label', self.data.get('mode', ''))]
        mode_label = BodyLabel(text)
        mode_label.setFixedWidth(90)
        mode_label.setAlignment(Qt.AlignCenter)
        
        # # 为不同模式设置不同颜色（可选）
        # mode_colors = {
        #     '不重复整数': '#4CAF50',
        #     '可重复整数': '#FF9800',
        #     '不重复浮点数': '#2196F3',
        #     '可重复浮点数': '#9C27B0'
        # }
        # color = mode_colors.get(self.data.get('mode_label', ''), '#888')
        # mode_label.setStyleSheet(f"""
        #     background-color: {color};
        #     color: white;
        #     padding: 2px 8px;
        #     border-radius: 10px;
        # """)
    
        layout.addStretch(1)
        layout.addWidget(mode_label)
        layout.addStretch(1)

        # 结果预览
        nums = self.data.get('nums', [])
        preview = ', '.join(map(str, nums[:5]))
        if len(nums) > 5:
            preview += f"... ({len(nums)}个)"
        result_label = BodyLabel(preview)
        result_label.setFixedWidth(200)
        result_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        result_label.setStyleSheet("color: #666; font-family: monospace;")
        layout.addWidget(result_label)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.card_clicked.emit(self.data)


class HistoryPage(QFrame):  # ✅ 改为继承 QFrame，不再继承 ScrollArea
    """历史记录页面 - 控制栏固定，卡片区域平滑滚动"""
    
    history_item_clicked = Signal(dict)

    def __init__(
            self,
            cfg,
            mgr,
            parent=None
        ):
        super().__init__(parent)
        
        self.cfg = cfg
        self.mgr = mgr
        self.history_mgr = mgr
        
        self.setObjectName("historyPage")
        
        # ✅ 根布局：垂直布局
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(10, 10, 10, 10)
        self.root_layout.setSpacing(10)
        
        # ✅ 1. 控制栏（固定，不滚动）
        self._init_controls()
        
        # ✅ 2. 滚动区域（只包裹卡片容器）
        self.scroll_area = ScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # 卡片容器（放在滚动区域内）
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(8)
        self.cards_layout.addStretch(1)
        
        self.scroll_area.setWidget(self.cards_container)
        
        # ✅ 滚动区域添加到根布局，拉伸因子为 1 占满剩余空间
        self.root_layout.addWidget(self.scroll_area, 1)
        
        # 加载历史记录
        self._load_all_records()
    
    def _init_controls(self):
        """初始化顶部控制栏（固定高度）"""
        control_widget = QWidget()
        control_widget.setFixedHeight(50)
        control_layout = QHBoxLayout(control_widget)
        control_layout.setContentsMargins(0, 0, 0, 10)

        # 标题
        title_label = BodyLabel("历史记录")
        title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        control_layout.addWidget(title_label)

        # 统计信息
        self.stats_label = BodyLabel("")
        self.stats_label.setStyleSheet("color: #888;")
        control_layout.addWidget(self.stats_label)

        control_layout.addStretch(1)

        # 导出按钮
        self.export_btn = PushButton("导出")
        self.export_btn.clicked.connect(self._export_history)
        control_layout.addWidget(self.export_btn)

        # 清空按钮
        self.clear_btn = PushButton("清空全部")
        self.clear_btn.clicked.connect(self._clear_history)
        control_layout.addWidget(self.clear_btn)

        # ✅ 直接添加到根布局
        self.root_layout.addWidget(control_widget)
    
    def _load_all_records(self):
        """加载所有历史记录（不分页）"""
        # 清空现有卡片（保留底部弹簧）
        while self.cards_layout.count() > 1:
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        all_records = self.mgr.get_records()
        total = self.mgr.get_total()
        self.stats_label.setText(f"共 {total} 条记录")
        
        if len(all_records) == 0:
            empty_label = BodyLabel("暂无历史记录\n生成随机数后会自动记录")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #aaa; padding: 40px 0; font-size: 14px;")
            self.cards_layout.insertWidget(0, empty_label)
            return
        
        for record in all_records:
            card = HistoryCard(record, self)
            card.card_clicked.connect(self._on_card_clicked)
            self.cards_layout.insertWidget(0, card)
    
    def add_record(self, record: dict):
        """添加一条新记录并刷新显示"""
        if not self.cfg.enableHistory.value:
            return
        
        # ✅ 使用 mgr 添加记录
        success = self.mgr.add_record(
            min=record.get('min'),
            max=record.get('max'),
            count=record.get('count'),
            mode=record.get('mode'),
            nums=record.get('nums', [])
        )
        if success:
            self._load_all_records()
    
    def refresh(self):
        """手动刷新历史列表"""
        self._load_all_records()
    
    def _on_card_clicked(self, data: dict):
        """卡片点击事件"""
        self._show_detail_dialog(data)

    def _show_detail_dialog(self, data: dict):
        """显示历史记录详情"""
        raw_list = data.get('nums', [])
        length_too_long = False
        if len(raw_list) > 40:
            raw_list = raw_list[:40]
            length_too_long = True

        if len(raw_list) > 11:
            chunk_size = 11
            # 1. 排序：直接从大到小排好序
            sorted_list = sorted(raw_list, reverse=True)

            # 2. 分组：利用切片 [start:end] 将列表切成每份11个的小列表
            # range(0, len(sorted_data), chunk_size) 会生成 0, 11, 22... 这样的索引
            grouped_data = [ sorted_list[i : i + chunk_size] for i in range(0, len(sorted_list), chunk_size)]

            # 3. 格式化：将每个小列表转成字符串，并用换行符连接
            res = "<br>".join([", ".join(map(str, group)) for group in grouped_data])

            if length_too_long:
                res += "......<br><br>(生成数过多，仅展示前40个。完整结果请导出后查看。)"

            """ 
            temp_list = []
            total_line = ( len(l) // 11 ) + 1
            counts = 11
            while total_line != 0:
                while counts != 0 and len(l) != 0:
                    a = l.pop()
                    temp_list.append(a)
                    counts -= 1
                res += ', '.join(map(str, temp_list)) + "<br>" #\n"
                temp_list.clear()
                counts = 11
                total_line -= 1
            """

        else:
            res = ', '.join(map(str, raw_list))

        mode_labels = {
                    'GenerateMode.UNIQUE' : '整数 不重复',
                    'GenerateMode.REPEAT' : '整数 可重复',
                    'GenerateMode.UNIQUE_FLOAT' : '浮点数 不重复',
                    'GenerateMode.REPEAT_FLOAT' : '浮点数 可重复'
                }
        text = mode_labels[data.get('mode', '')] # self.data.get('mode_label', self.data.get('mode', ''))

        content = f"""
        数量过多可导出至桌面后查看<br><br>
        <b>生成时间:</b> {data['id']}<br>
        最小: {data['min']}<br>
        最大: {data['max']}<br>
        数量: {data['count']}<br>
        模式: {text}<br>
        生成结果:<br>
        <b>{res}</b>
        """
        msg = MessageBox("历史记录详情", content, self)
        msg.hideCancelButton()
        msg.yesButton.setText("关闭")
        msg.yesButton.clicked.connect(msg.close)
        msg.exec()

    def _export_history(self):
        """导出历史记录到 JSON 文件"""
        success = self.mgr.export()
        if success:
            InfoBar.success("导出成功", "历史记录已导出至桌面", duration=1500, parent=self, position=InfoBarPosition.BOTTOM_RIGHT)
        else:
            InfoBar.error("导出失败", "历史记录导出失败", duration=1500, parent=self, position=InfoBarPosition.BOTTOM_RIGHT)

    def _clear_history(self):
        """清空所有历史记录"""
        total = self.mgr.get_total()
        if total == 0:
            return
        msg = MessageBox("确认清空", "确定要删除所有历史记录吗？此操作不可恢复。", self)
        msg.yesButton.setText("确定")
        msg.cancelButton.setText("取消")
        if msg.exec():
            success = self.mgr.clear_all()
            if success:
                self._load_all_records()
                InfoBar.success("已清空", "所有历史记录已删除", duration=1500, parent=self, position=InfoBarPosition.BOTTOM_RIGHT)


class SettingsPage(ScrollArea):

    precisionChanged = Signal(int)

    def __init__(
            self,
            cfg,
            FluentIcon,
            parent=None
        ):
        super().__init__(parent)
        self.fi = FluentIcon
        self.cfg = cfg

        self.setWidgetResizable(True)
        self.setObjectName("settingPage")
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        # --------------------------------生成数设置--------------------------------------
        self.geneGroup = SettingCardGroup("生成数设置", self.view)
        
        self.modeCard = ComboBoxSettingCard(
            self.cfg.defaultMode,
            self.fi.EDIT,
            "生成模式",
            "生成整数或者小数，是否允许重复。",
            texts=self.cfg.GenerateMode.values()
        )
        self.precisionCard = RangeSettingCard(
            self.cfg.decimalPrecision,
            self.fi.PAGE_RIGHT,
            "小数精度",
            "生成小数的位数，小数模式下可编辑。",
        )
        if self.cfg.current_mode() in [self.cfg.GenerateMode.UNIQUE, self.cfg.GenerateMode.REPEAT]:
            self.precisionCard.setEnabled(False)
        self.cfg.defaultMode.valueChanged.connect(self._on_mode_changed)

        self.geneGroup.addSettingCard(self.modeCard)
        self.geneGroup.addSettingCard(self.precisionCard)


        # --------------------------------通知设置--------------------------------------
        self.notiGroup = SettingCardGroup("通知设置", self.view)

        self.notiCard = ComboBoxSettingCard(
            self.cfg.defaultNotification,
            self.fi.MESSAGE,
            "通知设置",
            "生成数将以何种方式通知",
            texts=self.cfg.NotificationMode.values()
        )

        self.notiGroup.addSettingCard(self.notiCard)

        # --------------------------------历史设置--------------------------------------
        self.histGroup = SettingCardGroup("历史记录", self.view)
        self.enableCard = SwitchSettingCard(
                icon=self.fi.HISTORY,
                title="启用历史记录",
                content="保存历史记录可能会占用部分电脑储存。",
                configItem=cfg.enableHistory
        )
        # self.enableCard.switchButton.setOnText("启用")
        # self.enableCard.switchButton.setOffText("未启用")
        self.histGroup.addSettingCard(self.enableCard)

        self.vBoxLayout.addWidget(self.geneGroup)
        self.vBoxLayout.addWidget(self.notiGroup)
        self.vBoxLayout.addWidget(self.histGroup)

        self.vBoxLayout.addStretch(1)
        self.setWidget(self.view)

    def _on_mode_changed(self):
        """模式变化时更新精度卡片的启用状态"""
        self._update_precision_card_state()

    def _update_precision_card_state(self):
        """根据模式更新精度卡片的启用状态"""
        if self.cfg.current_mode() in [self.cfg.GenerateMode.UNIQUE_FLOAT, self.cfg.GenerateMode.REPEAT_FLOAT]:
            self.precisionCard.setEnabled(True)
        else:
            self.precisionCard.setEnabled(False)
    
    def _on_precision_changed(self, value: int):
        """精度变化时的回调"""
        self.precisionChanged.emit(value)

class WeChatPay(QFrame):
    
    def __init__(self, qr_code_path, parent=None):
        super().__init__(parent)
        self.setObjectName("wechatPay")
        self.qr_code_path = qr_code_path
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加二维码图片
        qr_pixmap = QPixmap(self.qr_code_path)  # 替换为你的二维码图片路径
        qr_label = ImageLabel(self)
        qr_label.setPixmap(qr_pixmap)
        img_size = QSize(600, 600)
        qr_label.setPixmap(qr_pixmap.scaled(img_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # qr_label.setScaledContents(True)
        qr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(qr_label)

        # 添加提示文字
        tip_label = BodyLabel("请在您的个人能力范围内进行捐赠！")
        tip_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(tip_label)

class Alipay(QFrame):
    
    def __init__(self, qr_code_path, parent=None):
        super().__init__(parent)
        self.setObjectName("alipay")
        self.qr_code_path = qr_code_path
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # 添加二维码图片
        qr_pixmap = QPixmap(self.qr_code_path)  # 替换为你的二维码图片路径
        qr_label = ImageLabel(qr_pixmap)
        img_size = QSize(600, 600)
        qr_label.setPixmap(qr_pixmap.scaled(img_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        qr_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(qr_label)


        # 添加提示文字
        tip_label = BodyLabel("请在您的个人能力范围内进行捐赠！")
        tip_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(tip_label)

class InfoPage(ScrollArea):

    def __init__(
            self,
            cfg,
            FluentIcon,
            donate_window_icon,
            wechat_icon,
            alipay_icon,
            yuanshen_icon,
            yuanshen_cloud_icon,
            wechat_qr_path,
            alipay_qr_path,
            desktop,
            parent=None
        ):
        super().__init__(parent)
        self.fi = FluentIcon
        self.cfg = cfg
        self.donate_window_icon = donate_window_icon
        self.wechat_icon = wechat_icon
        self.alipay_icon = alipay_icon
        self.yuanshen_icon = yuanshen_icon
        self.yuanshen_cloud_icon = yuanshen_cloud_icon
        self.wechat_qr_path = wechat_qr_path
        self.alipay_qr_path = alipay_qr_path
        self.desktop = desktop
        
        self.setWidgetResizable(True)
        self.setObjectName("ifoPage")
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.infoGroup = SettingCardGroup("关于", self.view)

        self.githubCard = HyperlinkCard(
            "https://github.com/SurinChi/RandomNumberGenerator",
            "前往GitHub",
            self.fi.GITHUB,
            "项目GitHub",
            "程序使用过程中遇到错误？前往GitHub仓库提交issue，或者贡献你的代码。",
        )

        self.updateCard = PrimaryPushSettingCard(
            "检查更新",
            self.fi.UPDATE,
            "软件更新",
            f"当前版本: {self.cfg.VERSION}"
        )

        self.copyRightCard = PrimaryPushSettingCard(
            "查看简介",
            self.fi.INFO,
            "随机数生成器 Powered by Python 3.13",
            "© 2026 SurinChi. All rights reserved."
        )

        self.copyRightCard.button.hide()  # 隐藏按钮
        
        self.updateCard.clicked.connect(self._on_check_clicked)

        self.infoGroup.addSettingCard(self.githubCard)
        self.infoGroup.addSettingCard(self.updateCard)
        self.infoGroup.addSettingCard(self.copyRightCard)

        self.aurthorGroup = SettingCardGroup("开发者", self.view)

        self.aurthor_1_GithubCard = HyperlinkCard(
            "https://github.com/SurinChi",
            "前往ta的GitHub",
            self.parent().avatar_icon,
            "SurinChi",
            "人生天地间，忽如远行客。",
        )

        self.aurthor_2_GithubCard = HyperlinkCard(
            "https://github.com/YC-donot",
            "前往ta的GitHub",
            self.parent().avatar_icon_2,
            "YC-donot",
            "吹牛，我让你飞起来。",
        )

        self.aurthor_1_GithubCard.iconLabel.setFixedSize(46, 46)
        self.aurthor_2_GithubCard.iconLabel.setFixedSize(46, 46)
        self.aurthorGroup.addSettingCard(self.aurthor_1_GithubCard)
        self.aurthorGroup.addSettingCard(self.aurthor_2_GithubCard)

        self.lisenceGroup = SettingCardGroup("许可证", self.view)
        self.lisenceCard = HyperlinkCard(
            "https://github.com/SurinChi/RandomNumberGenerator?tab=GPL-3.0-1-ov-file",
            "查看",
            self.fi.VPN,
            "GPL-3.0",
            "软件按 GPL-3.0 协议分发，请在使用前确认合规性。"
        )
        self.lisenceCard.linkButton.hide()  # 隐藏按钮
        self.lisenceGroup.addSettingCard(self.lisenceCard)

        self.donateGroup = SettingCardGroup("捐赠", self.view)
        self.donateCard = PrimaryPushSettingCard(
            "立即捐赠",
            icon=self.fi.SEND,
            title="为该项目献出你的心意",
            content="如果你觉得这个软件对你有帮助，欢迎捐赠支持作者。",
        )
        self.donateCard.clicked.connect(self._on_donate_clicked)
        self.donateGroup.addSettingCard(self.donateCard)

        self.yuanshenGroup = SettingCardGroup("原神官网", self.view)
        self.yuanshenCard = HyperlinkCard(
            "https://ys.mihoyo.com/",
            "前往",
            self.yuanshen_icon,
            "原神",
            "https://ys.mihoyo.com/",
        )
        self.yuanshenCard.iconLabel.setFixedSize(46, 46)

        self.yuanshenCloudCard = HyperlinkCard(
                    "https://ys.mihoyo.com/cloud/",
                    "诶，云朵？",
                    self.yuanshen_cloud_icon,
                    "云·原神",
                    "https://ys.mihoyo.com/cloud/#/",
                )
        self.yuanshenCloudCard.iconLabel.setFixedSize(46, 46)

        self.yuanshenGroup.addSettingCard(self.yuanshenCard)
        self.yuanshenGroup.addSettingCard(self.yuanshenCloudCard)

        self.vBoxLayout.addWidget(self.infoGroup)
        self.vBoxLayout.addWidget(self.aurthorGroup)
        self.vBoxLayout.addWidget(self.lisenceGroup)
        self.vBoxLayout.addWidget(self.donateGroup)
        self.vBoxLayout.addWidget(self.yuanshenGroup)

        self.vBoxLayout.addStretch(1)
        self.setWidget(self.view)

    def _on_check_clicked(self):
        QDesktopServices.openUrl("https://github.com/SurinChi/RandomNumberGenerator/releases")

    def _on_donate_clicked(self):
        msg = MessageBox("捐赠提示", "请确认您已经年满18周岁，未满18周岁请勿捐赠。", self)
        # msg.hideCancelButton()
        msg.yesButton.setText("我未满18岁，取消捐赠")
        msg.cancelButton.setText("我已满18岁")
        msg.cancelButton.clicked.connect(self._on_is_aged)
        msg.exec()

    def _on_is_aged(self):
        window = MSFluentWindow()
        window.setWindowTitle("捐赠前请确保您已经年满18周岁")
        window.setWindowIcon(self.donate_window_icon)
        window.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        window.resize(700, 700)
        # window.setFixedSize(600, 480)
        w, h = self.desktop.width(), self.desktop.height()
        window.move(w//2 - window.width()//2, h//2 - window.height()//2)
        wechat = WeChatPay(self.wechat_qr_path, self)
        alipay = Alipay(self.alipay_qr_path, self)
        window.addSubInterface(wechat, self.wechat_icon, "微信")
        window.addSubInterface(alipay, self.alipay_icon, "支付宝")
        window.show()