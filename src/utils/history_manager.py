# src/utils/history_manager.py
import json
from pathlib import Path
from typing import List, Dict, Optional


class HistoryManager:
    """历史记录管理器，按日期切分文件"""
    
    def __init__(
            self,
            history_dir: Path,
            timer
        ):
        """
        初始化历史记录管理器
        
        Args:
            history_dir: 历史记录根目录
        """
        self.history_dir: Path = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)

        self.history_file: Path   = Path(self.history_dir / "history.json")
        content: str              = self.history_file.read_text(encoding='utf-8')
        self.data: dict           = json.loads(content)
        self.data_set: list       = self.data["records"]
        del content

        self.timer = timer
    
    def _get_date_file(self, date_str: str):
        """获取指定日期的记录文件路径"""
        pass
    
    def _save_file(self) -> None:
        """保存记录到 JSON 文件"""
        try:
            self.data["records"] = self.data_set
            content: str = json.dumps(self.data)
            self.history_file.write_text(content)
        except Exception as e:
            raise
    
    def add_record(
            self,
            min,
            max,
            count,
            mode,
            nums: list
        ) -> bool:
        """        
        Args:
            record: 记录字典
        
        Returns:
            bool: 是否成功
        """
        new_record: dict = {}

        try: # try者得天下
            new_record['id'] = self.timer.get_timestamp(2)
            new_record['min'] = min
            new_record['max'] = max
            new_record['count'] = count
            new_record['mode'] = mode
            new_record['nums'] = nums

            self.data_set.append(new_record)
            self._save_file()
        except:
            raise
        return True
    
    def get_records(self, days: Optional[int] = None) -> List[Dict]:
        """
        Args:
            days: 获取最近多少天的记录，None 表示全部
        
        Returns:
            List[Dict]: 所有记录（按时间倒序排列）
        """
        return self.data_set
        
    
    def get_records_by_date(self, date_str: str) -> List[Dict]:
        """获取指定日期的记录"""
        file_path = self._get_date_file(date_str)
        return self._load_file(file_path)
    
    def get_available_dates(self) -> List[str]:
        """获取所有有记录的日期列表"""
        dates = []
        for file_path in sorted(self.history_dir.glob('*.json')):
            dates.append(file_path.stem)
        return dates
    
    def delete_record(self, record_id: str) -> bool:
        """
        Args:
            record_id: 记录 ID
        
        Returns:
            bool: 是否删除成功
        """
        # 遍历所有文件查找并删除
        for d in self.data_set:
            if d['id'] == record_id:
                self.data_set.remove(d)
                self._save_file()
                return True
            else:
                return False

    
    def clear_all(self) -> bool:
        """清空所有历史记录"""
        try:
            self.data_set = []
            self._save_file()
            return True
        except:
            return False
    
    def get_total(self) -> int:
        """获取统计信息"""
        return len(self.data_set)

    def export(self) -> bool:
        """
        Save the history records as a .txt file.
        
        Returns:
            bool: 是否导出成功
        """

        import ctypes

        # 获取 Windows 系统的"桌面"绝对路径（无论是否被移动）
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, 0x0000, None, 0, buf)  # 0x0000 代表 CSIDL_DESKTOP

        desktop_path = Path(buf.value)
        exported_name = f"history_export_{self.timer.get_customised_time("%Y年%m月%d日%M时%H分%S秒")}.txt"
        export_path = desktop_path / exported_name
        final_text = ""
        mode_labels = {
                    'GenerateMode.UNIQUE' : '整数 不重复',
                    'GenerateMode.REPEAT' : '整数 可重复',
                    'GenerateMode.UNIQUE_FLOAT' : '浮点数 不重复',
                    'GenerateMode.REPEAT_FLOAT' : '浮点数 可重复'
                }


        try:
            records: list = self.data['records']
            for i in records:
                timestamp = i['id']
                min_val = i['min']
                max_val = i['max']
                count = i['count']
                mode = i['mode']
                text = mode_labels[mode]
                res = str(i['nums'])[1:-1]
                temp = f"时间: {timestamp}\n最小: {min_val}\n最大: {max_val}\n数量: {count}\n模式: {text}\n生成结果:\n{res}"
                final_text += temp
                final_text += "\n\n"

            # final_text = json.dumps(final_text)
            export_path.write_text(final_text)
            return True
        except Exception as e:
            raise