"""ReviTrace 后端入口。

启动命令（在项目根目录执行）：
    uvicorn backend.main:app --reload
接口文档：
    http://127.0.0.1:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .core.exception_handlers import register_exception_handlers
from .routers import assist, chat, compare, exercise, summary, upload


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动时准备好本地存储目录。"""
    settings.ensure_dirs()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=(
        "ReviTrace：可溯源的 RAG 复习助手后端。\n\n"
        "提供文档入库、引用式问答、通俗解读、考点总结、知识点对比与随堂习题接口。"
    ),
    lifespan=lifespan,
)

# 允许前端 Vue3（Vite 默认 5173 端口）跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册全局异常处理，保证异常也返回 {code, msg, data} 结构
register_exception_handlers(app)

# 统一挂载到 /api 前缀下
for module in (upload, chat, assist, summary, compare, exercise):
    app.include_router(module.router, prefix=settings.api_prefix)
