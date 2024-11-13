from requests.exceptions import HTTPError

class SdkException(HTTPError):
    """Baserow API 异常类"""
    def __init__(self, response):
        self.response = response
        self.status_code = response.status_code
        try:
            self.detail = response.json()
        except ValueError:
            self.detail = response.text
            
        message = f"""
状态码: {self.status_code}
URL: {response.url}
响应内容: {self.detail}
"""
        super().__init__(message, response=response) 