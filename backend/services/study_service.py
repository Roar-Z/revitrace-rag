"""学习辅助服务：类比解读、考点总结、知识点对比、随堂习题。

服务层负责组装业务参数与返回模型，具体生成逻辑统一放在 llm_service，
后续接入大模型时职责边界不会变化。
"""

from ..schemas.assist import AnalogyRequest, AnalogyResponse
from ..schemas.compare import CompareRequest, CompareResponse
from ..schemas.exercise import ExerciseRequest, ExerciseResponse
from ..schemas.summary import SummaryRequest, SummaryResponse
from . import llm_service


def assist_analogy(req: AnalogyRequest) -> AnalogyResponse:
    """基于上一轮标准答案生成通俗解读（占位）。"""
    analogy = llm_service.generate_analogy(req.answer, req.style.value)
    return AnalogyResponse(style=req.style, analogy=analogy)


def summarize(req: SummaryRequest) -> SummaryResponse:
    """生成考点总结（占位）。"""
    summary, points = llm_service.generate_summary(req.doc_id, req.topic)
    return SummaryResponse(
        doc_id=req.doc_id,
        topic=req.topic,
        summary=summary,
        points=points,
    )


def compare(req: CompareRequest) -> CompareResponse:
    """生成 Markdown 对比表格（占位）。"""
    return llm_service.generate_compare_table(req.concept_a, req.concept_b)


def generate_exercises(req: ExerciseRequest) -> ExerciseResponse:
    """生成随堂习题（占位）。"""
    choice_questions = llm_service.generate_choice_questions(
        req.topic, req.choice_count
    )
    short_answer_questions = (
        llm_service.generate_short_answer_questions(req.topic)
        if req.include_short_answer
        else []
    )
    return ExerciseResponse(
        doc_id=req.doc_id,
        choice_questions=choice_questions,
        short_answer_questions=short_answer_questions,
    )
