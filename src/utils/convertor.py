""" 此工具不进行数据校验，使用前请确定类型再使用 """

class Convertor:

    globalCfg = None  # 用于存储配置对象的全局变量

    @classmethod
    def _str_to_int(cls, v: str) -> int:
        return int(v)
    
    @classmethod
    def _str_to_float(cls, v: str) -> float:
        return float(v)
    
    @classmethod
    def _strs_to_ints(cls, *v) -> list[int]:
        l = []
        for i in v:
            l.append(int(i))
        return l
    
    @classmethod
    def _strs_to_floats(cls, *v):
        l = []
        for i in v:
            float(i)
            l.append(i)
        return l
    
    @classmethod
    def convert(cls, min_val, max_val, count_val):
        if cls.globalCfg.current_mode() in [cls.globalCfg.GenerateMode.UNIQUE, cls.globalCfg.GenerateMode.REPEAT]:
            return (
                cls._str_to_int(min_val),
                cls._str_to_int(max_val),
                cls._str_to_int(count_val)
            )
        if cls.globalCfg.current_mode() in [cls.globalCfg.GenerateMode.UNIQUE_FLOAT, cls.globalCfg.GenerateMode.REPEAT_FLOAT]:
            return (
                cls._str_to_float(min_val),
                cls._str_to_float(max_val),
                cls._str_to_int(count_val)
            )