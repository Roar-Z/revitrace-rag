"""PDF 解析与文本分块。

这一步只做确定性的文本处理，不涉及大模型，方便单独测试与替换解析器。
分块时保留页码，是后续“溯源引用”的基础。
"""

import io
import re
from dataclasses import dataclass
from typing import List

from pypdf import PdfReader


@dataclass
class PageText:
    """一页 PDF 的文本。"""

    page: int
    text: str


def extract_pages(pdf_bytes: bytes) -> List[PageText]:
    """抽取 PDF 每页的文本，跳过扫描页（无文本）和空白页。"""
    reader = PdfReader(io.BytesIO(pdf_bytes))

    # 加密 PDF 无法直接读取，明确提示而不是抛出难以理解的底层错误
    if reader.is_encrypted:
        raise ValueError("PDF 已加密，暂不支持解析")

    pages: List[PageText] = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            pages.append(PageText(page=index, text=text))
    return pages


def split_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """按固定长度切分文本，相邻块保留重叠，减少语义被截断。

    中文场景下按字符切分即可满足需求，实现简单且稳定。
    """
    # 压缩多余的空白字符，避免分块里出现大量空行
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []

    step = max(chunk_size - chunk_overlap, 1)
    chunks: List[str] = []
    start = 0
    while start < len(normalized):
        end = min(start + chunk_size, len(normalized))
        chunks.append(normalized[start:end])
        if end >= len(normalized):
            break
        start += step
    return chunks
