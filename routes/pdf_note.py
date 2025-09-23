from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pdf.generate_pdf import gerar_danfe
from db import buscar_nota

router = APIRouter(prefix="/nfc")

@router.get("/{chave}/danfe")
def baixar_danfe(chave: str):
    nota = buscar_nota(chave)
    if not nota:
        raise HTTPException(404, "Nota não encontrada")
    pdf = gerar_danfe(chave, nota)
    return FileResponse(pdf, media_type="application/pdf", filename=f"DANFE_{chave}.pdf")
