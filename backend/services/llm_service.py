"""大模型能力占位层。

现阶段只返回结构完整的模拟内容，保证接口联调不被模型阻塞；
接入真实大模型时，仅替换本文件各函数的实现，路由与 Schema 无需改动。
"""

from typing import List, Tuple

from ..schemas.chat import Citation
from ..schemas.compare import CompareResponse
from ..schemas.exercise import ChoiceQuestion, ShortAnswerQuestion
from ..schemas.summary import SummaryPoint

# 类比风格的中文名称，用于占位文案展示
_STYLE_LABELS = {
    "life": "生活化类比",
    "story": "故事化类比",
    "game": "游戏化类比",
}


def generate_answer(question: str, citations: List[Citation]) -> str:
    """生成标准答案（占位）。真实实现应把 citations 作为上下文交给大模型。"""
    if citations:
        pages = "、".join(str(item.page) for item in citations)
        return (
            f"【占位回答】已从文档检索到 {len(citations)} 个相关片段"
            f"（页码：{pages}）。接入大模型后，将基于这些原文片段回答：{question}"
        )
    return "【占位回答】暂未检索到相关原文。接入大模型后会结合文档内容作答。"


def generate_analogy(answer: str, style: str) -> str:
    """基于上一轮标准答案生成通俗解读（占位）。"""
    label = _STYLE_LABELS.get(style, "生活化类比")
    return (
        f"【占位解读·{label}】接入大模型后，将把上一轮答案转换成通俗表达。\n"
        f"上一轮答案：{answer}"
    )


def generate_summary(
    doc_id: str, topic: str | None
) -> Tuple[str, List[SummaryPoint]]:
    """生成考点总结（占位）。"""
    scope = f"主题「{topic}」" if topic else "整篇文档"
    summary = f"【占位总结】将基于文档 {doc_id} 的{scope}生成考点总结。"
    points = [
        SummaryPoint(
            title="考点一（占位）",
            detail="接入大模型后，这里会给出该考点的核心结论与原文依据。",
        ),
        SummaryPoint(
            title="考点二（占位）",
            detail="接入大模型后，这里会给出该考点的常见考法与易错点。",
        ),
    ]
    return summary, points


def generate_compare_table(concept_a: str, concept_b: str) -> CompareResponse:
    """生成 Markdown 对比表格（占位）。"""
    table = (
        f"| 对比维度 | {concept_a} | {concept_b} |\n"
        "| --- | --- | --- |\n"
        "| 定义 | 待接入大模型后填充 | 待接入大模型后填充 |\n"
        "| 核心特点 | 待接入大模型后填充 | 待接入大模型后填充 |\n"
        "| 适用场景 | 待接入大模型后填充 | 待接入大模型后填充 |\n"
        "| 常见误区 | 待接入大模型后填充 | 待接入大模型后填充 |"
    )
    return CompareResponse(
        concept_a=concept_a, concept_b=concept_b, table_markdown=table
    )


def generate_choice_questions(topic: str | None, count: int) -> List[ChoiceQuestion]:
    """生成选择题（占位）。"""
    stem_topic = topic or "文档核心内容"
    questions: List[ChoiceQuestion] = []
    for index in range(count):
        questions.append(
            ChoiceQuestion(
                question=f"【占位题 {index + 1}】关于「{stem_topic}」，下列说法正确的是？",
                options=[
                    "A. 选项 A（待接入大模型后生成）",
                    "B. 选项 B（待接入大模型后生成）",
                    "C. 选项 C（待接入大模型后生成）",
                    "D. 选项 D（待接入大模型后生成）",
                ],
                answer="A",
                explanation="【占位解析】接入大模型后将结合原文给出解析。",
            )
        )
    return questions


def generate_short_answer_questions(topic: str | None) -> List[ShortAnswerQuestion]:
    """生成简答题（占位）。"""
    stem_topic = topic or "文档核心内容"
    return [
        ShortAnswerQuestion(
            question=f"【占位简答题】请简述「{stem_topic}」的核心要点。",
            reference_answer="接入大模型后，这里会给出分点作答的参考答案。",
        )
    ]
