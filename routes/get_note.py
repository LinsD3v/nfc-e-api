from fastapi import APIRouter, HTTPException
from db import DB

router = APIRouter(prefix="/nfc")

@router.get("/{chave}")
def consultar_nfce(chave: str):
    if chave not in DB:
        raise HTTPException(404, "Nota não encontrada")
    return DB[chave]