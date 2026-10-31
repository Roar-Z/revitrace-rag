"""问答服务：检索原文片段 + 生成标准答案。

检索是真实执行的（LanceDB 向量召回），生成部分是占位实现，
这样既能演示溯源链路，又暂时不依赖大模型。
"""

from ..schemas.chat import ChatRequest, ChatResponse, Citation
from . import embedding_service, llm_service, vector_store


def answer_question(req: ChatRequest) -> ChatResponse:
    """完成一次问答：先召回相关文本块，再组装答案与引用。"""
    query_vector = embedding_service.embed_query(req.question)
    rows = vector_store.search(query_vector, req.top_k, req.doc_id)

    citations = [
        Citation(
            doc_id=row["doc_id"],
            chunk_id=row["chunk_id"],
            page=row["page"],
            text=row["text"],
            score=row["score"],
        )
        for row in rows
    ]

    answer = llm_service.generate_answer(req.question, citations)
    return ChatResponse(answer=answer, citations=citations)
