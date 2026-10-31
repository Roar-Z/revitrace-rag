"""文档问答路由。"""

from fastapi import APIRouter

from ..core.response import success
from ..schemas.chat import ChatRequest, ChatResponse
from ..schemas.common import ApiResponse
from ..services import qa_service

router = APIRouter(prefix="/chat", tags=["文档问答"])


@router.post(
    "",
    response_model=ApiResponse[ChatResponse],
    summary="文档问答（返回标准答案与溯源片段）",
    description="根据问题在 LanceDB 中召回相关文本块，返回标准答案及对应原文页码与片段。",
)
def chat(req: ChatRequest):
    """问答接口。"""
    data = qa_service.answer_question(req)
    return success(data, msg="问答完成")
