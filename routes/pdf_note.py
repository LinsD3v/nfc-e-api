from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pdf.generate_pdf import gerar_danfe
from db import DB

router = APIRouter(prefix="/nfc")

@router.get("/{chave}/danfe")
def baixar_danfe(chave: str):
    if chave not in DB:
        raise HTTPException(404, "Nota não encontrada")
    pdf = gerar_danfe(chave, DB[chave])
    return FileResponse(pdf, media_type="application/pdf", filename=f"DANFE_{chave}.pdf")
