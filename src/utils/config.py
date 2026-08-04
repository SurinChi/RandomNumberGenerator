# config.py
from enum import Enum
from qfluentwidgets import (
    QConfig, ConfigItem, OptionsConfigItem, RangeConfigItem, ConfigValidator,
    EnumSerializer, BoolValidator, OptionsValidator, RangeValidator
)


class AppConfig(QConfig):
    """应用的配置类"""

    VERSION = "0.0.2"  # 配置版本号，用于配置升级时的判断
    
    # 生成模式配置项
    class GenerateMode(Enum):
        UNIQUE = "整数 不重复"
        REPEAT = "整数 可重复"
        UNIQUE_FLOAT = "小数 不重复"
        REPEAT_FLOAT = "小数 可重复"

        @staticmethod
        def values():
            return [q.value for q in AppConfig.GenerateMode]
        
    
    class NotificationMode(Enum):
        POP  = "应用弹窗显示"
        NOTI = "Windows通知"

        @staticmethod
        def values():
            return [q.value for q in AppConfig.NotificationMode]

    enableHistory = ConfigItem(
        "History",          # 分组名称
        "EnableHistory",    # 键名
        True,               # 默认值：True 表示默认开启
        BoolValidator()     # 验证器：确保值为 True/False
    )

    # 使用 OptionsConfigItem 配合枚举序列化器处理下拉选项
    defaultMode = OptionsConfigItem(
        "Generate",
        "DefaultMode",
        GenerateMode.UNIQUE,
        OptionsValidator(GenerateMode),
        EnumSerializer(GenerateMode)
    )

    defaultNotification = OptionsConfigItem(
        "Generate",
        "DefaulNotificationt",
        NotificationMode.POP,
        OptionsValidator(NotificationMode),
        EnumSerializer(NotificationMode)
    )

        # ✅ 新增：小数精度（默认保留 2 位小数）
    decimalPrecision = RangeConfigItem(
        "Generate", "DecimalPrecision", 
        2,                              # 默认值
        RangeValidator(0, 10)           # 范围 0-10 位小数
    )
    
    classPopulation = RangeConfigItem(
            "Generate", "DecimalPrecision", 
            0,                              # 默认值
            RangeValidator(0, 2000)           # 范围 0-2000 人，应该没有班级人数能超过2000吧
    )

    historyDir = ConfigItem(
        "History", "HistoryDir",
        "history",
        ConfigValidator()
    )


    def current_mode(self):
        """获取当前的生成模式"""
        return self.defaultMode.value
    
    def current_notification(self):
        """获取当前的通知模式"""
        return self.defaultNotification.value
    def current_precision(self):
        """获取当前的小数精度"""
        return self.decimalPrecision.value

# 创建全局唯一的配置实例
config = AppConfig()
# 在程序启动时加载配置（例如在 main.py 中）
# qconfig.load('path/to/config.json', config)