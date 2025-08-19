from fastapi import APIRouter, HTTPException
from db import DB

router = APIRouter(prefix="/nfc")

@router.post("/{chave}/cancel")
def cancelar_nfce(chave: str, justificativa: str):
    if chave not in DB:
        raise HTTPException(404, "Nota não encontrada")
    DB[chave]["status"] = "cancelada"
    DB[chave]["justificativa"] = justificativa
    return {"chave": chave, "status": "cancelada"}
