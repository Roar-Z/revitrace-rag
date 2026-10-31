"""文档入库服务。

流程：PDF 解析 -> 文本分块 -> 向量化 -> 写入 LanceDB。
这一步不含大模型逻辑，入参出参都已稳定，方便后续替换真实向量模型。
"""

import uuid
from typing import Any, Dict, List

from ..config import settings
from ..schemas.upload import UploadResponse
from . import embedding_service, pdf_service, vector_store


def ingest_pdf(filename: str, content: bytes) -> UploadResponse:
    """解析 PDF 并完成向量入库，返回文档 id 供后续接口使用。"""
    pages = pdf_service.extract_pages(content)
    if not pages:
        raise ValueError("未能从 PDF 中提取到文本，可能是扫描件或空文档")

    doc_id = uuid.uuid4().hex
    records: List[Dict[str, Any]] = []

    # 逐页分块，保证每个块都能记住自己的页码
    chunk_id = 0
    for page in pages:
        pieces = pdf_service.split_text(
            page.text, settings.chunk_size, settings.chunk_overlap
        )
        for piece in pieces:
            records.append(
                {
                    "id": f"{doc_id}-{chunk_id}",
                    "doc_id": doc_id,
                    "chunk_id": chunk_id,
                    "text": piece,
                    "page": page.page,
                }
            )
            chunk_id += 1

    if not records:
        raise ValueError("PDF 文本为空，未生成任何文本块")

    # 批量向量化后与元数据合并，一次性写入向量库
    vectors = embedding_service.embed_texts([item["text"] for item in records])
    for record, vector in zip(records, vectors):
        record["vector"] = vector

    vector_store.add_records(records)

    return UploadResponse(
        doc_id=doc_id,
        filename=filename,
        pages=len(pages),
        chunk_count=len(records),
    )
