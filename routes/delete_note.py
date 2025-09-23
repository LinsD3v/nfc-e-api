from fastapi import APIRouter, HTTPException
from db import buscar_nota, salvar_nota

router = APIRouter(prefix="/nfc")

@router.post("/{chave}/cancel")
def cancelar_nfce(chave: str, justificativa: str):
    nota = buscar_nota(chave)
    if not nota:
        raise HTTPException(404, "Nota não encontrada")
    nota["status"] = "cancelada"
    nota["justificativa"] = justificativa
    salvar_nota(chave, nota)
    return {"chave": chave, "status": "cancelada"}
