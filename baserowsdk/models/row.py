from typing import List, Optional, Dict, Any

class Row:
    """表示单行数据的类,类似 Airtable Record"""
    def __init__(self, data: dict):
        self._data = data
        for key, value in data.items():
            setattr(self, key, value)
    
    @property
    def fields(self) -> dict:
        """返回行的所有字段数据"""
        return self._data
    
    def get(self, field: str, default=None):
        """获取指定字段的值"""
        return self._data.get(field, default)
        
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