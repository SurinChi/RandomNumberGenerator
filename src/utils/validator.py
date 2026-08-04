# validator.py
class CountZeroError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class CountFloatError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class InputValueError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class ValueRangeException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class Validator:

    globalCfg = None  # 用于存储配置对象的全局变量

    min = None
    max = None
    count = None
    mode = None

    @classmethod
    def _is_count_zero(cls, count_val):
        if int(count_val) == 0:
            raise CountZeroError("生成次数不能为0！")

    @classmethod
    def _is_count_float(cls, count_val):
        count_val = float(count_val)
        if count_val.is_integer():
            pass
        else:
            raise CountFloatError("生成次数不能为小数！")

    @classmethod
    def _max_less_min(cls, min_val, max_val):
        min_val = float(min_val)
        max_val = float(max_val)
        if min_val >= max_val:
            raise InputValueError("最小值必须小于最大值！")

    @classmethod
    def _is_input_str(cls, min_val, max_val, count_val):
        if cls.globalCfg.current_mode():
            if cls.globalCfg.current_mode() in [cls.globalCfg.GenerateMode.UNIQUE, cls.globalCfg.GenerateMode.REPEAT]:
                try:
                    min_val = int(min_val)
                    max_val = int(max_val)
                    count_val = int(count_val)
                except ValueError:
                    raise InputValueError("请在输入框中填写正确的实数")
            elif cls.globalCfg.current_mode() in [cls.globalCfg.GenerateMode.UNIQUE_FLOAT, cls.globalCfg.GenerateMode.REPEAT_FLOAT]:
                try:
                    min_val = float(min_val)
                    max_val = float(max_val)
                    count_val = int(count_val)
                except ValueError:
                    raise InputValueError("请在输入框中填写正确的实数")
            else:
                raise Exception("模式错误，请重置应用设置后重新生成！")

        else:
            raise Exception("配置文件损坏，请重置应用设置后重新生成！")
    
    @classmethod
    def _is_range_less_count(cls, min_val, max_val, count_val):
        if cls.globalCfg.current_mode() == cls.globalCfg.GenerateMode.UNIQUE:
            min_val = int(min_val)
            max_val = int(max_val)
            count_val = int(count_val)
            if count_val > (max_val - min_val + 1):
                raise ValueRangeException(f"当生成模式为\"{cls.globalCfg.GenerateMode.UNIQUE.value}\"时，生成次数不能大于范围！")
    
    @classmethod
    def validate(cls, inputs: tuple[str, str, str]):
        cls.min, cls.max, cls.count = inputs
        if cls.min and cls.max and cls.count:
            cls._is_input_str(cls.min, cls.max, cls.count)
            cls._is_count_float(cls.count)
            cls._is_count_zero(cls.count)
            cls._max_less_min(cls.min, cls.max)
            cls._is_range_less_count(cls.min, cls.max, cls.count)
        else:
            raise InputValueError("发现未填写的数据，请填写后重新生成！")
        
if __name__ == "__main__":
    Validator.validate(("0.1"))