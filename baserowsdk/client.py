import requests
from typing import List
from baserowsdk.models.field import Field
from baserowsdk.models.base import Base
from baserowsdk.models.row import RowList,Row

class Client:
    def __init__(self, api_key: str, base_url: str = "https://baserow.io"):
        """初始化客户端
        
        Args:
            api_key (str): API密钥
            base_url (str): 服务器地址
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json"
        }
    
    def base(self, base_id: int) -> Base:
        """获取指定 Base 的操作接口"""
        return Base(self, base_id)

    def _get_full_url(self, endpoint: str) -> str:
        """构建完整的API URL
        
        Args:
            endpoint (str): API端点路径
            
        Returns:
            str: 完整的API URL
        """
        return f"{self.base_url}/{endpoint.lstrip('/')}"


    def fields(self, table_id: int) -> List[Field]:
        """获取指定表的所有字段信息
        
        Args:
            table_id (int): 表的ID
            
        Returns:
            List[Field]: 表字段信息列表，每个元素都是Field对象，包含字段的完整信息
            
        Raises:
            requests.exceptions.RequestException: 当API请求失败时抛出异常
        """
        endpoint = f"api/database/fields/table/{table_id}/"
        url = self._get_full_url(endpoint)
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()        
        return [Field(**field) for field in response.json()]

if __name__ == "__main__":
    client = Client(api_key="...", base_url="http://192.168.40.220")
    # 获取字段
    # fields = client.fields(182)
    # print(fields)
    
    # 单条查询
    # row = client.row(table_id=182, row_id=1)
    # print(row)

    # 批量查询
    # base = client.base(39)
    # rows = base.table(182).select(page_size=100)
    # print(rows)

    # 创建
    # row = client.base(39).table(182).create(fields={"执行批次ID": "1234567890"})
    # print(row)

    # 删除
    # client.base(39).table(182).delete(row_id=7)

    # 更新
    # updated_row =  client.base(39).table(182).update(
    # row_id=6,
    # fields={
        # "执行批次ID": "BATCH-001",
    # },
    # user_field_names=True
    # )
    # print(updated_row)