# Baserowsdk


# Requirements

python3.8 +

# Installation

```shell
pip install --upgrade baserowsdk
```

# Getting started

### 初始化客户端
```python
from baserowsdk import Client

client = Client(
    api_key="your_api_key",
    base_url="http://your.baserow.domain"
)
```

### 获取字段信息
```python
# 获取表的所有字段定义
fields = client.fields(table_id=182)
print(fields)
```

### 查询数据
```python
# 单条查询
base = client.base(39)
row = base.table(182).row(row_id=1)
print(row)

# 批量查询
rows = base.table(182).select(page_size=100)
print(rows)

# 查询同时种缓存
# 注意: 缓存是基于 client 对象的, 不同 client 对象之间互不干扰
rows = base.table(182).select(page_size=100, cache_senconds=10)
print(rows)
```

### 创建数据
```python
# 创建新记录
row = client.base(39).table(182).create(
    fields={"黑话改写_输入": "1234567890","黑话改写_输出": "1234567890"}
)
print(row)
```

### 更新数据
```python
# 更新记录
updated_row = client.base(39).table(182).update(
    row_id=6,
    fields={
        "执行批次ID": "BATCH-001",
        "测试用例": [1, 2, 3]  # 关联字段支持多值
    },
    user_field_names=True  # 使用用户定义的字段名
)
print(updated_row)
```

### 删除数据
```python
# 删除记录
client.base(39).table(182).delete(row_id=7)
```