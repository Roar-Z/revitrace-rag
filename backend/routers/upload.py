"""文档上传路由。"""

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..config import settings
from ..core.response import success
from ..schemas.common import ApiResponse
from ..schemas.upload import UploadResponse
from ..services import document_service

router = APIRouter(prefix="/upload", tags=["文档管理"])


@router.post(
    "",
    response_model=ApiResponse[UploadResponse],
    summary="上传 PDF 并完成文档入库",
    description="解析 PDF 文本、按页分块、向量化后写入 LanceDB，返回可用于溯源的文档 id。",
)
async def upload_pdf(
    file: UploadFile = File(..., description="待上传的 PDF 文件"),
):
    """接收 PDF 文件并完成入库。"""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="仅支持上传 PDF 文件")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="上传文件为空")
    if not content.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="文件内容不是有效的 PDF")

    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"文件超过大小限制（{settings.max_upload_mb} MB）",
        )

    try:
        data = document_service.ingest_pdf(file.filename, content)
    except ValueError as exc:
        # PDF 解析相关的业务异常统一按参数错误返回
        raise HTTPException(status_code=400, detail=str(exc))

    return success(data, msg="文档入库成功")
