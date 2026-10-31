"""全局配置。

所有可调参数都支持通过环境变量覆盖，默认值面向本地开发，
既方便调试，也方便答辩时说明配置项来源。
"""

import os
from pathlib import Path


def _env_int(name: str, default: int) -> int:
    """读取整数型环境变量，格式非法时回退到默认值。"""
    raw = os.getenv(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_list(name: str, default: list[str]) -> list[str]:
    """读取逗号分隔的环境变量，用于 CORS 白名单等场景。"""
    raw = os.getenv(name)
    if not raw:
        return default
    return [item.strip() for item in raw.split(",") if item.strip()]


class Settings:
    """项目配置集合，一次初始化后在全局复用。"""

    def __init__(self) -> None:
        base_dir = Path(__file__).resolve().parent

        # 应用基础信息（会展示在 /docs 页面上）
        self.app_name = os.getenv("REVITRACE_APP_NAME", "ReviTrace API")
        self.version = os.getenv("REVITRACE_VERSION", "0.1.0")
        self.api_prefix = "/api"

        # 前端跨域白名单，默认允许 Vue3 + Vite 的本地开发端口
        self.cors_origins = _env_list(
            "REVITRACE_CORS_ORIGINS",
            ["http://localhost:5173", "http://127.0.0.1:5173"],
        )

        # 本地存储目录（LanceDB 数据目录放在 storage 下，已在 .gitignore 中忽略）
        self.storage_dir = Path(
            os.getenv("REVITRACE_STORAGE_DIR", str(base_dir / "storage"))
        ).expanduser()
        self.lancedb_dir = Path(
            os.getenv("REVITRACE_LANCE_DIR", str(self.storage_dir / "lancedb"))
        ).expanduser()
        self.table_name = os.getenv("REVITRACE_LANCE_TABLE", "chunks")

        # 向量与文本分块参数。BGE-M3 的默认向量维度为 1024
        self.embedding_dim = _env_int("REVITRACE_EMBEDDING_DIM", 1024)
        self.chunk_size = _env_int("REVITRACE_CHUNK_SIZE", 800)
        self.chunk_overlap = _env_int("REVITRACE_CHUNK_OVERLAP", 150)

        # 上传与检索限制
        self.max_upload_mb = _env_int("REVITRACE_MAX_UPLOAD_MB", 50)
        self.default_top_k = _env_int("REVITRACE_DEFAULT_TOP_K", 4)
        self.max_top_k = _env_int("REVITRACE_MAX_TOP_K", 10)

        # 防御性处理：重叠长度不能超过分块长度的一半，否则分块会死循环
        self.chunk_overlap = min(self.chunk_overlap, self.chunk_size // 2)
        # 默认召回数量不能超过上限，避免 Schema 默认值越界
        self.default_top_k = min(self.default_top_k, self.max_top_k)

    def ensure_dirs(self) -> None:
        """确保本地存储目录存在，服务启动时调用一次即可。"""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.lancedb_dir.mkdir(parents=True, exist_ok=True)


# 全局配置单例，其他模块通过 `from ..config import settings` 使用
settings = Settings()
