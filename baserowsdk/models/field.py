from typing import Optional
from dataclasses import dataclass

@dataclass
class Field:
    """BaseRow表字段信息类
    
    Attributes:
        id (int): 字段主键，可通过添加field_前缀生成数据库列名
        name (str): 字段名称
        table_id (int): 关联的表ID
        order (int): 字段在表中的顺序，0表示第一个字段
        primary (bool): 是否为主键字段，如果为True则该字段不能被删除，且其值应该代表整行数据
        type (str): 字段类型
        read_only (bool): 是否为只读字段，如果为True则无法更新单元格值
        description (Optional[str]): 字段描述，可选
    """
    id: int
    name: str
    table_id: int
    order: int
    primary: bool
    type: str
    read_only: bool
    link_row_table:Optional[int] = None
    link_row_table_id: Optional[int] = None
    link_row_related_field: Optional[int] = None
    link_row_related_field_id: Optional[int] = None
    description: Optional[str] = None 
    immutable_type: bool = False
    immutable_properties: bool = False
    description: Optional[str] = None 
    link_row_limit_selection_view_id: Optional[int] = None
    text_default: str = ""
