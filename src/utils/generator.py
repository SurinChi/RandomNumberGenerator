# generater.py

from random import randint, uniform
from pathlib import Path

class Generator:

    globalCfg = None  # 用于存储配置对象的全局变量

    @classmethod
    def _get_float(cls, min, max, count) -> list:
        f_list = []                         # 定义一个容器，用来存放生成的数集
        if cls.globalCfg.current_mode() == cls.globalCfg.GenerateMode.REPEAT_FLOAT:
            length = 0                      # 初始数集长度为0
            while length < count:           # 当数集长度＜要求长度时继续生成
                float_num = uniform(min, max)
                float_num = round(float_num, cls.globalCfg.current_precision()) # 保留小数点后多少位
                if float_num in f_list:
                    continue
                else:
                    f_list.append(float_num)
                length = len(f_list)        # 重新计算长度
        else:
            for i in range(count):
                float_num = uniform(min, max)
                float_num = round(float_num, cls.globalCfg.current_precision()) # 保留小数点后多少位
                f_list.append(float_num)
        return f_list

    @classmethod
    def _get_random_integer(cls, min, max, count) -> list:
        num_list = []                       # 定义一个容器，用来存放生成的数集
        if cls.globalCfg.current_mode() == cls.globalCfg.GenerateMode.UNIQUE:
            length = 0                      # 初始数集长度为0
            while length < count:           # 当数集长度＜要求长度时继续生成
                integer = randint(min, max)
                if integer in num_list:
                    continue
                else:
                    num_list.append(integer)
                length = len(num_list)      # 重新计算长度
        else:
            for i in range(count):
                integer = randint(min, max)
                num_list.append(integer)
        return num_list

    # 主函数
    @classmethod
    def main_func(cls, min, max, count) -> list:
        # 获取随机数
        if cls.globalCfg.current_mode() in [cls.globalCfg.GenerateMode.UNIQUE, cls.globalCfg.GenerateMode.REPEAT]:
            num_list = cls._get_random_integer(min, max, count)
        elif cls.globalCfg.current_mode() in [cls.globalCfg.GenerateMode.UNIQUE_FLOAT, cls.globalCfg.GenerateMode.REPEAT_FLOAT]:
            num_list = cls._get_float(min, max, count)
        else:
            raise ValueError(
                "Invalid mode. You must choose from the given 4 modes: \"unique\", "
                + "\"repeat\", \"unique_float\", \"repeat_float\"."
            )
        parameters: tuple = (min, max, count)
        return num_list