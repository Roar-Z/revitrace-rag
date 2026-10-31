"""HTTP 响应工具。

路由层只调用 `success()` / `fail()` 构造统一响应，
避免每个接口各写一套返回格式。
"""

from typing import Any

from ..schemas.common import ApiResponse


def success(data: Any = None, msg: str = "success") -> ApiResponse[Any]:
    """成功响应：code 固定为 0。"""
    return ApiResponse(code=0, msg=msg, data=data)


def fail(code: int, msg: str) -> ApiResponse[None]:
    """失败响应：data 固定为 None，错误码与提示由调用方决定。"""
    return ApiResponse(code=code, msg=msg, data=None)
