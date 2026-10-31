"""知识点对比接口的数据模型。"""

from typing import Optional

from pydantic import BaseModel, Field


class CompareRequest(BaseModel):
    """入参：对比两个知识点。"""

    concept_a: str = Field(..., min_length=1, description="知识点 A")
    concept_b: str = Field(..., min_length=1, description="知识点 B")
    doc_id: Optional[str] = Field(
        default=None, description="限定对比所依据的文档 id（可选）"
    )


class CompareResponse(BaseModel):
    """出参：Markdown 对比表格，前端可直接渲染。"""

    concept_a: str = Field(..., description="知识点 A")
    concept_b: str = Field(..., description="知识点 B")
    table_markdown: str = Field(..., description="Markdown 格式的对比表格")
