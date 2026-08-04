# time.py

from datetime import datetime


class Timer:
    @classmethod
    def today(cls):
        return datetime.today().strftime("%Y%m%d")

    @classmethod
    def get_timestamp(cls, index: int):
        """ 
        `standard_format` is a standard format of time.
        For example: "2026-06-19 12:25:09".

        `fileName_format` is a file name customised format of time.
        For example: "20260619_122509".
        """
        current_time = datetime.today()
        standard_format = cls._getStandardTime(current_time)
        fileName_format = cls._getTime(current_time)
        if index == 1:
            return standard_format
        if index == 2:
            return fileName_format
    
    @classmethod
    def get_customised_time(cls, strformat:str):
        """
        The arguments of `strformat`:\n
        `%Y`: Year.
        `%m`: Month.
        `%d`: Day.\n
        `%H`: Hour.
        `%M`: Minute.
        `%S`: Second.

        Please pay attention to the Upper or Lower cases, incorrect spelling may lead to unexpected results.
        """
        return datetime.now().strftime(strformat)

    @classmethod
    def _getStandardTime(cls, inputTime=None) -> str:
        # 获取当前时间
        if inputTime:
            return inputTime.strftime("%Y-%m-%d %H:%M:%S")
        else:
            current_time = datetime.now()
            # 格式化为 YYYYmmddhhmmss
            current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            return current_time
    
    @classmethod
    def _getTime(cls, inputTime) -> str:
        if inputTime:
            return inputTime.strftime("%Y%m%d_%H%M%S")
        else:
            # 获取当前时间
            current_time = datetime.now()
            current_time = current_time.strftime("%Y%m%d_%H%M%S")
            return current_time
