"""LanceDB 向量库封装。

LanceDB 是嵌入式向量库，数据以 Lance 列式文件落盘，查询时通过 mmap
按需读取，不需要独立数据库进程，内存占用低、部署简单。

表结构（每条记录对应一个文本块）：
    id       唯一主键（doc_id + chunk_id）
    doc_id   文档 id
    chunk_id 文档内块序号
    text     文本块原文
    page     原文页码
    vector   文本向量

其中 doc_id / chunk_id / page / text 就是溯源引用所需的元数据。
"""

from typing import Any, Dict, List, Optional

from ..config import settings


def _connect():
    """延迟导入并连接 LanceDB。

    延迟导入的好处是：未安装向量库依赖时，应用仍能启动并展示 /docs，
    只有真正调用上传/问答接口时才给出明确的依赖提示。
    """
    try:
        import lancedb
    except ImportError as exc:  # pragma: no cover - 依赖缺失时的兜底提示
        raise RuntimeError(
            "LanceDB 未安装，请先执行：pip install -r requirements.txt"
        ) from exc
    return lancedb.connect(str(settings.lancedb_dir))


def _table_names(db) -> List[str]:
    """兼容不同 LanceDB 版本的表名查询接口。"""
    try:
        return list(db.table_names())
    except AttributeError:
        tables = db.list_tables()
        return list(getattr(tables, "tables", tables))


def _open_table(db):
    """表不存在时返回 None，避免调用方重复判断。"""
    if settings.table_name not in _table_names(db):
        return None
    return db.open_table(settings.table_name)


def add_records(records: List[Dict[str, Any]]) -> None:
    """批量写入文本块；首次写入时自动建表。"""
    if not records:
        return

    db = _connect()
    table = _open_table(db)
    if table is None:
        db.create_table(settings.table_name, data=records)
    else:
        table.add(records)


def search(
    vector: List[float],
    top_k: int,
    doc_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """向量相似度检索，返回带元数据的文本块列表。"""
    db = _connect()
    table = _open_table(db)
    if table is None:
        # 还没有任何文档入库，直接返回空结果
        return []

    query = table.search(vector)
    if doc_id:
        # doc_id 由后端生成的十六进制字符串，这里仍做一次引号转义，防止过滤语法被破坏
        safe_doc_id = doc_id.replace("'", "''")
        query = query.where(f"doc_id = '{safe_doc_id}'")

    rows = query.limit(top_k).to_list()

    results: List[Dict[str, Any]] = []
    for row in rows:
        distance = float(row.get("_distance", 0.0))
        results.append(
            {
                "doc_id": row.get("doc_id", ""),
                "chunk_id": int(row.get("chunk_id", 0)),
                "page": int(row.get("page", 0)),
                "text": row.get("text", ""),
                # 距离越小越相关，转换成 0~1 的相关度分数方便前端展示
                "score": round(1.0 / (1.0 + distance), 4),
            }
        )
    return results
