from fastapi import APIRouter, HTTPException
from db import buscar_nota

router = APIRouter(prefix="/nfc")

@router.get("/{chave}")
def consultar_nfce(chave: str):
    nota = buscar_nota(chave)
    if not nota:
        raise HTTPException(404, "Nota não encontrada")
    return nota