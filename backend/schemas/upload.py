"""文档上传接口的数据模型。"""

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """上传入库结果：文档 id 用于后续问答、总结等接口的溯源定位。"""

    doc_id: str = Field(..., description="文档唯一 id")
    filename: str = Field(..., description="原始文件名")
    pages: int = Field(..., description="成功提取到文本的页数")
    chunk_count: int = Field(..., description="写入向量库的文本块数量")
