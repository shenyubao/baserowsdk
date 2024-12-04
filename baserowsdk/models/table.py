from typing import List
from baserowsdk.models.row import Row, RowList
from baserowsdk.sdk_exception import SdkException
import requests
import json
import urllib.parse
import time

class Table:
    """表示一个 Table 的类"""
    def __init__(self, client, base_id: int, table_id: str):
        self.client = client
        self.base_id = base_id
        self.table_id = table_id
        
    def select(
        self,
        page_size: int = 100,
        offset: int = None,
        fields: List[str] = None,
        sort: List[dict] = None,
        formula: str = None,
        view: str = None,
        max_records: int = None,
        cache_senconds: int = None,
        **kwargs
    ) -> RowList:
        """查询表中的记录"""
        # 清理过期的缓存
        if cache_senconds:
            current_time = time.time()
            expired_keys = [key for key, value in self.client.cache.items() 
                            if current_time - value['timestamp'] >= cache_senconds]
            for key in expired_keys:
                print(f"cache expired: {key}")
                del self.client.cache[key]
        
        params = {
            'size': page_size
        }
        
        if offset:
            params['page'] = offset
        if fields:
            params['include'] = ','.join(fields)
        if sort:
            params['order_by'] = ','.join([f"{'-' if s['direction']=='desc' else ''}{s['field']}" for s in sort])
        if formula:
            params['filters'] = formula
        if view:
            params['view_id'] = view
            
        # 添加缓存逻辑
        cache_key = f"select_cache_{self.base_id}_{self.table_id}_{hash(str(sorted(params.items())))}"

        if cache_key in self.client.cache:
            # print(f"cache hit: {cache_key}")
            return self.client.cache[cache_key]['data']
        
        # 进行 API 请求
        response = self.rows(**params)
        
        # 更新缓存
        if cache_senconds:
            self.client.cache[cache_key] = {
                'data': response,
                'timestamp': time.time()
            }
        
        return response
        
    def get(self, record_id: str, user_field_names: bool = True) -> Row:
        """获取单条记录"""
        return self.row(record_id, user_field_names)
        
    def create(
        self, 
        fields: dict, 
        user_field_names: bool = True,
        before: int = None
    ) -> Row:
        """创建记录
        
        Args:
            fields: 要创建的字段值字典
            user_field_names: 是否使用用户定义的字段名称
            before: 可选的行ID,新创建的行将被放置在该行之前
            
        Returns:
            Row: 创建的行记录
        """
        endpoint = f"api/database/rows/table/{self.table_id}/"
        url = self.client._get_full_url(endpoint)
        
        params = {}
        if user_field_names:
            params['user_field_names'] = 'true'
        if before:
            params['before'] = before
            
        response = requests.post(
            url,
            headers=self.client.headers,
            params=params,
            json=fields
        )
        if response.status_code >=400:
            raise SdkException(response)
        return Row(response.json())
        
    def update(
        self, 
        row_id: int, 
        fields: dict,
        user_field_names: bool = True
    ) -> Row:
        """更新表中的指定行记录
        
        Args:
            row_id: 要更新的行ID
            fields: 要更新的字段值字典
            user_field_names: 是否使用用户定义的字段名称，默认为True
            
        Returns:
            Row: 更新后的行记录
            
        Raises:
            requests.exceptions.HTTPError: 当API请求失败时抛出
        """
        endpoint = f"api/database/rows/table/{self.table_id}/{row_id}/"
        url = self.client._get_full_url(endpoint)
        
        params = {}
        if user_field_names:
            params['user_field_names'] = 'true'
            
        response = requests.patch(
            url,
            headers=self.client.headers,
            params=params,
            json=fields
        )
        if response.status_code >=400:
            raise SdkException(response)
        return Row(response.json())
        
    def delete(self, row_id: int) -> None:
        """删除指定行记录
        
        Args:
            row_id: 要删除的行ID
            
        Raises:
            requests.exceptions.HTTPError: 当API请求失败时抛出
        """
        endpoint = f"api/database/rows/table/{self.table_id}/{row_id}/"
        url = self.client._get_full_url(endpoint)
        
        response = requests.delete(
            url,
            headers=self.client.headers
        )
        response.raise_for_status()
        
    def row(self, row_id: int, user_field_names: bool = True) -> dict:
        """获取指定表中的单行数据"""
        endpoint = f"api/database/rows/table/{self.table_id}/{row_id}/"
        url = self.client._get_full_url(endpoint)
        
        params = {}
        if user_field_names:
            params['user_field_names'] = 'true'
            
        response = requests.get(url, headers=self.client.headers, params=params)
        if response.status_code >=400:
            raise SdkException(response)
        return response.json()

    def rows(
        self, 
        page: int = 1,
        size: int = 100,
        user_field_names: bool = True,
        search: str = None,
        order_by: str = None,
        filters: dict = None,
        filter_type: str = 'AND',
        include: str = None,
        exclude: str = None,
        view_id: int = None,
        **kwargs
    ) -> dict:
        """获取表格中的多行数据"""
        endpoint = f"api/database/rows/table/{self.table_id}/"
        url = self.client._get_full_url(endpoint)
        
        params = {
            'page': page,
            'size': size
        }
        
        if user_field_names:
            params['user_field_names'] = 'true'
        
        if search:
            params['search'] = search
            
        if order_by:
            params['order_by'] = order_by
            
        if filters:
            filters_json = json.dumps(filters)
            params['filters'] = filters_json
            
        if filter_type and filter_type.upper() in ['AND', 'OR']:
            params['filter_type'] = filter_type.upper()
            
        if include:
            params['include'] = include
            
        if exclude:
            params['exclude'] = exclude
            
        if view_id:
            params['view_id'] = view_id
            
        params.update({
            k: v for k, v in kwargs.items() 
            if k.startswith('filter__')
        })
        
        response = requests.get(url, headers=self.client.headers, params=params)
        if response.status_code >=400:
            raise SdkException(response)
        return RowList(response.json()) 