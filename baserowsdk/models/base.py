from typing import List
from .table import Table

class Base:
    """表示一个 Base 的类"""
    def __init__(self, client, base_id: int):
        self.client = client
        self.base_id = base_id
        
    def table(self, table_id: str):
        """获取指定表的操作接口"""
        return Table(self.client, self.base_id, table_id) 