"""考点总结接口的数据模型。"""

from typing import List, Optional

from pydantic import BaseModel, Field


class SummaryRequest(BaseModel):
    """入参：按文档（可选主题）生成考点总结。"""

    doc_id: str = Field(..., min_length=1, description="要总结的文档 id")
    topic: Optional[str] = Field(
        default=None, description="限定总结主题，为空表示总结整篇文档"
    )


class SummaryPoint(BaseModel):
    """单条考点。"""

    title: str = Field(..., description="考点标题")
    detail: str = Field(..., description="考点说明")


class SummaryResponse(BaseModel):
    """出参：总结正文 + 结构化考点列表。"""

    doc_id: str = Field(..., description="文档 id")
    topic: Optional[str] = Field(default=None, description="总结主题")
    summary: str = Field(..., description="考点总结正文（当前为占位实现）")
    points: List[SummaryPoint] = Field(
        default_factory=list, description="结构化考点列表"
    )
