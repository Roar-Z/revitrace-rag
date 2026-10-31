"""文档问答接口的数据模型。"""

from typing import List, Optional

from pydantic import BaseModel, Field

from ..config import settings


class Citation(BaseModel):
    """溯源片段：回答中引用的原文位置，前端据此高亮原文与页码。"""

    doc_id: str = Field(..., description="所属文档 id")
    chunk_id: int = Field(..., description="文档内的文本块序号")
    page: int = Field(..., description="原文页码，从 1 开始")
    text: str = Field(..., description="原文片段文本")
    score: float = Field(..., description="检索相关度，越大越相关")


class ChatRequest(BaseModel):
    """问答入参。"""

    question: str = Field(..., min_length=1, description="用户问题")
    doc_id: Optional[str] = Field(
        default=None, description="限定问答的文档 id，为空表示检索全部文档"
    )
    top_k: int = Field(
        default=settings.default_top_k,
        ge=1,
        le=settings.max_top_k,
        description="召回片段数量",
    )


class ChatResponse(BaseModel):
    """问答出参：标准答案 + 溯源原文片段。"""

    answer: str = Field(..., description="标准答案（当前为占位实现）")
    citations: List[Citation] = Field(
        default_factory=list, description="答案对应的原文片段列表"
    )
