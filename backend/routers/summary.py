"""考点总结路由。"""

from fastapi import APIRouter

from ..core.response import success
from ..schemas.common import ApiResponse
from ..schemas.summary import SummaryRequest, SummaryResponse
from ..services import study_service

router = APIRouter(prefix="/summary", tags=["学习辅助"])


@router.post(
    "",
    response_model=ApiResponse[SummaryResponse],
    summary="生成考点总结",
    description="按文档（可选主题）生成考点总结，并返回结构化考点列表。",
)
def summarize(req: SummaryRequest):
    """考点总结接口。"""
    data = study_service.summarize(req)
    return success(data, msg="考点总结生成完成")
