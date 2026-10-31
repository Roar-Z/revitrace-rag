"""通俗解读（类比辅助）接口的数据模型。"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AnalogyStyle(str, Enum):
    """可切换的类比风格。"""

    life = "life"      # 生活化类比
    story = "story"    # 故事化类比
    game = "game"      # 游戏化类比


class AnalogyRequest(BaseModel):
    """入参：基于上一轮标准答案生成通俗解读。"""

    answer: str = Field(..., min_length=1, description="上一轮问答返回的标准答案")
    style: AnalogyStyle = Field(
        default=AnalogyStyle.life, description="类比风格，可切换"
    )
    doc_id: Optional[str] = Field(
        default=None, description="文档 id，用于补充原文背景（可选）"
    )


class AnalogyResponse(BaseModel):
    """出参：通俗解读文本。"""

    style: AnalogyStyle = Field(..., description="本次使用的类比风格")
    analogy: str = Field(..., description="通俗解读内容（当前为占位实现）")
