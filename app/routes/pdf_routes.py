from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # TODO: call pdf_service to parse & store embeddings
    return {"filename": file.filename}
