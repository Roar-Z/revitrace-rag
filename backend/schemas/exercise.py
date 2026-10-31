"""随堂习题接口的数据模型。"""

from typing import List, Optional

from pydantic import BaseModel, Field


class ChoiceQuestion(BaseModel):
    """选择题：题干、选项、答案与解析。"""

    question: str = Field(..., description="题干")
    options: List[str] = Field(..., description="选项列表，如 A/B/C/D")
    answer: str = Field(..., description="正确答案")
    explanation: str = Field(..., description="答案解析")


class ShortAnswerQuestion(BaseModel):
    """简答题：题干与参考答案。"""

    question: str = Field(..., description="题干")
    reference_answer: str = Field(..., description="参考答案")


class ExerciseRequest(BaseModel):
    """入参：按文档（可选主题）生成随堂习题。"""

    doc_id: str = Field(..., min_length=1, description="出题依据的文档 id")
    topic: Optional[str] = Field(default=None, description="限定出题主题")
    choice_count: int = Field(
        default=3, ge=1, le=10, description="选择题数量"
    )
    include_short_answer: bool = Field(
        default=True, description="是否生成简答题"
    )


class ExerciseResponse(BaseModel):
    """出参：选择题 + 简答题。"""

    doc_id: str = Field(..., description="文档 id")
    choice_questions: List[ChoiceQuestion] = Field(
        default_factory=list, description="选择题列表"
    )
    short_answer_questions: List[ShortAnswerQuestion] = Field(
        default_factory=list, description="简答题列表"
    )
