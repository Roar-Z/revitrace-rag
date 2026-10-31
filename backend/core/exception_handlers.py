"""全局异常处理。

把 FastAPI/Starlette 抛出的各类异常统一转换成 {code, msg, data} 结构，
前端只需要判断 code，不用再兼容默认的 JSON 错误格式。
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from .response import fail


def register_exception_handlers(app: FastAPI) -> None:
    """在应用初始化时注册所有异常处理器。"""

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(request: Request, exc: StarletteHTTPException):
        """业务主动抛出的 HTTPException（如 400、404）。"""
        return JSONResponse(
            status_code=exc.status_code,
            content=fail(exc.status_code, str(exc.detail)).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        """请求参数校验失败，提取首条错误方便前端定位。"""
        errors = exc.errors()
        msg = "参数校验失败"
        if errors:
            first = errors[0]
            location = ".".join(str(item) for item in first.get("loc", []))
            msg = f"参数校验失败：{location} {first.get('msg', '')}".strip()
        return JSONResponse(status_code=422, content=fail(422, msg).model_dump())

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception):
        """兜底异常：避免返回 HTML 报错页，同时保留原始错误信息便于排查。"""
        return JSONResponse(
            status_code=500,
            content=fail(500, f"服务器内部错误：{exc}").model_dump(),
        )
