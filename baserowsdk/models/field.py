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
    read_only: bool = False
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

    def __init__(self, id: int, table_id: int, name: str, order: int, type: str, primary: bool, **kwargs):
        """初始化字段对象
        
        Args:
            id (int): 字段ID
            table_id (int): 表ID
            name (str): 字段名称
            order (int): 字段顺序
            type (str): 字段类型
            primary (bool): 是否为主键
            **kwargs: 其他额外的字段参数
        """
        self.id = id
        self.table_id = table_id
        self.name = name
        self.order = order
        self.type = type
        self.primary = primary

        self.read_only = kwargs.get('read_only')
        
        # 设置链接行相关字段
        self.link_row_table = kwargs.get('link_row_table')
        self.link_row_table_id = kwargs.get('link_row_table_id')
        self.link_row_related_field = kwargs.get('link_row_related_field')
        self.link_row_related_field_id = kwargs.get('link_row_related_field_id')
        
        # 设置其他属性
        self.description = kwargs.get('description')
        self.immutable_type = kwargs.get('immutable_type', False)
        self.immutable_properties = kwargs.get('immutable_properties', False)
        self.link_row_limit_selection_view_id = kwargs.get('link_row_limit_selection_view_id')
        self.text_default = kwargs.get('text_default', '')
        
        # 保存额外的字段信息
        self.extra_fields = kwargs
