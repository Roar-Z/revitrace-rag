"""随堂习题路由。"""

from fastapi import APIRouter

from ..core.response import success
from ..schemas.common import ApiResponse
from ..schemas.exercise import ExerciseRequest, ExerciseResponse
from ..services import study_service

router = APIRouter(prefix="/generate-exercise", tags=["学习辅助"])


@router.post(
    "",
    response_model=ApiResponse[ExerciseResponse],
    summary="生成随堂习题",
    description="生成选择题与简答题，包含答案和解析。",
)
def generate_exercise(req: ExerciseRequest):
    """随堂习题接口。"""
    data = study_service.generate_exercises(req)
    return success(data, msg="随堂习题生成完成")
