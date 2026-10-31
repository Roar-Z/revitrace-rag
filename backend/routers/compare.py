"""知识点对比路由。"""

from fastapi import APIRouter

from ..core.response import success
from ..schemas.common import ApiResponse
from ..schemas.compare import CompareRequest, CompareResponse
from ..services import study_service

router = APIRouter(prefix="/compare", tags=["学习辅助"])


@router.post(
    "",
    response_model=ApiResponse[CompareResponse],
    summary="对比两个知识点",
    description="对比两个知识点，返回 Markdown 格式的对比表格，前端可直接渲染。",
)
def compare(req: CompareRequest):
    """知识点对比接口。"""
    data = study_service.compare(req)
    return success(data, msg="对比表格生成完成")
