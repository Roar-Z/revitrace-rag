"""通用响应体定义。

所有接口固定返回 {code, msg, data} 三层结构：
- code：业务状态码，0 表示成功，其余为错误码；
- msg：给人看的提示信息；
- data：真正的业务数据，失败时为 null。
"""

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

# 泛型参数，用于让 /docs 展示每个接口具体的 data 结构
T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一响应体。"""

    code: int = Field(default=0, description="业务状态码，0 表示成功")
    msg: str = Field(default="success", description="提示信息")
    data: Optional[T] = Field(default=None, description="业务数据")


class NothingData(BaseModel):
    """无业务数据时占位，保证文档中的 data 结构不为空。"""
