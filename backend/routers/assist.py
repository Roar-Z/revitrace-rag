"""通俗解读（类比辅助）路由。"""

from fastapi import APIRouter

from ..core.response import success
from ..schemas.assist import AnalogyRequest, AnalogyResponse
from ..schemas.common import ApiResponse
from ..services import study_service

router = APIRouter(prefix="/assist-analogy", tags=["学习辅助"])


@router.post(
    "",
    response_model=ApiResponse[AnalogyResponse],
    summary="生成通俗解读（支持切换类比风格）",
    description="基于上一轮标准答案生成通俗解读，style 可选 life / story / game。",
)
def assist_analogy(req: AnalogyRequest):
    """类比解读接口。"""
    data = study_service.assist_analogy(req)
    return success(data, msg="通俗解读生成完成")
