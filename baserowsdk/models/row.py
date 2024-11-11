from typing import List, Optional, Dict, Any
from functools import lru_cache
import time

class Row:
    """表示单行数据的类,类似 Airtable Record"""
    def __init__(self, data: dict):
        self._data = data
        self._cache = {}
        self._cache_times = {}
        for key, value in data.items():
            setattr(self, key, value)
    
    @property
    def fields(self) -> dict:
        """返回行的所有字段数据"""
        return self._data
    
    def get(self, field: str, default=None, cache_minutes: int = 5):
        """
        获取指定字段的值，支持本地缓存
        
        Args:
            field: 字段名
            default: 默认值
            cache_minutes: 缓存时间(分钟)，默认5分钟
        """
        current_time = time.time()
        
        # 检查缓存是否存在且未过期
        if field in self._cache:
            cache_time = self._cache_times.get(field, 0)
            if current_time - cache_time < cache_minutes * 60:
                return self._cache[field]
        
        # 获取新值并更新缓存
        value = self._data.get(field, default)
        self._cache[field] = value
        self._cache_times[field] = current_time
        
        return value
        
    def __getattr__(self, name):
        """允许通过属性方式访问字段"""
        return self._data.get(name)
        
    def __repr__(self):
        return f"Row(fields={self._data})"

class RowList:
    """表示行数据列表的类,类似 Airtable Records"""
    def __init__(self, data: Dict[str, Any]):
        self.offset: Optional[str] = data.get('next')  # 改用 offset 分页
        self.records: List[Row] = [Row(row) for row in data.get('results', [])]
        
    @property
    def all(self) -> List[Row]:
        """返回所有记录"""
        return self.records
        
    def first(self) -> Optional[Row]:
        """返回第一条记录"""
        return self.records[0] if self.records else None
        
    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):
        return self.records[index]

    def __iter__(self):
        return iter(self.records)

    def __repr__(self):
        return f"RowList(records_count={len(self)}, records={self.records})" 