"""Pydantic 数据模型统一出口。

schemas 层只描述接口的入参与出参，不包含任何业务逻辑，
便于前后端联调和答辩时展示接口契约。
"""

from .assist import AnalogyRequest, AnalogyResponse, AnalogyStyle
from .chat import ChatRequest, ChatResponse, Citation
from .common import ApiResponse
from .compare import CompareRequest, CompareResponse
from .exercise import ChoiceQuestion, ExerciseRequest, ExerciseResponse, ShortAnswerQuestion
from .summary import SummaryPoint, SummaryRequest, SummaryResponse
from .upload import UploadResponse

__all__ = [
    "ApiResponse",
    "UploadResponse",
    "ChatRequest",
    "ChatResponse",
    "Citation",
    "AnalogyRequest",
    "AnalogyResponse",
    "AnalogyStyle",
    "SummaryRequest",
    "SummaryResponse",
    "SummaryPoint",
    "CompareRequest",
    "CompareResponse",
    "ExerciseRequest",
    "ExerciseResponse",
    "ChoiceQuestion",
    "ShortAnswerQuestion",
]
