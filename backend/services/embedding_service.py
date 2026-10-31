"""文本向量化服务。

当前阶段为占位实现：使用确定性的字符哈希向量，保证“上传—入库—检索”
整条链路可运行，且不引入 torch、模型权重等重量级依赖。

接入真实 BGE-M3 时，只需替换本文件的 embed 实现：
    from FlagEmbedding import BGEM3FlagModel
    model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=False)
    model.encode(texts)["dense_vecs"]
路由层、向量库结构都不需要改动。
"""

import hashlib
import math
from typing import List, Sequence

from ..config import settings


def _tokens(text: str) -> List[str]:
    """简易分词：去掉空白后取字符二元组，中英文都能覆盖。"""
    compact = "".join(text.lower().split())
    if not compact:
        return []
    if len(compact) == 1:
        return [compact]
    return [compact[i : i + 2] for i in range(len(compact) - 1)]


def _hash_embed(text: str) -> List[float]:
    """把字符二元组哈希到固定维度并归一化，作为 BGE-M3 的占位向量。"""
    dim = settings.embedding_dim
    vector = [0.0] * dim

    for token in _tokens(text):
        digest = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
        index = digest % dim
        # 用哈希的另一位决定正负号，降低不同词碰撞带来的偏差
        sign = 1.0 if (digest >> 1) % 2 == 0 else -1.0
        vector[index] += sign

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def embed_texts(texts: Sequence[str]) -> List[List[float]]:
    """批量向量化，供文档入库使用。"""
    return [_hash_embed(text) for text in texts]


def embed_query(text: str) -> List[float]:
    """单条向量化，供检索使用。"""
    return _hash_embed(text)
