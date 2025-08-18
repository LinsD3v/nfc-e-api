from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Literal, Optional
from datetime import datetime
import hashlib, qrcode, base64
from io import BytesIO

app = FastAPI(title="API Mock de NFC-e")


class Pedido(BaseModel):
    numero: int
    serie: int = 1
    modelo: Literal[65] = 65
    dhEmi: datetime = datetime.utcnow()
    itens: List[Item]
    pagamento: Literal["dinheiro","credito","debito","pix","outros"]

DB = {}

def gerar_chave(numero: int, serie: int) -> str:
    # Chave mock de 44 dígitos
    base = f"35{datetime.now().strftime('%y%m')}{numero:09d}{serie:03d}"
    return base.ljust(44, "0")

@app.post("/nfce")
def criar_nfce(pedido: Pedido):
    chave = gerar_chave(pedido.numero, pedido.serie)
    protocolo = hashlib.sha1(chave.encode()).hexdigest()[:15]
    total = sum(i.quantidade * i.valor_unit for i in pedido.itens)
    qr_data = f"https://sefaz-fake.gov/nfce?q={chave}|{total:.2f}"
    
    DB[chave] = {
        "pedido": pedido.dict(),
        "status": "autorizada",
        "protocolo": protocolo,
        "total": total,
        "qr": qr_data
    }
    return {
        "chave": chave,
        "protocolo": protocolo,
        "status": "autorizada",
        "total": total,
        "qr_url": qr_data
    }

@app.get("/nfce/{chave}")
def consultar_nfce(chave: str):
    if chave not in DB:
        raise HTTPException(404, "Nota não encontrada")
    return DB[chave]

@app.post("/nfce/{chave}/cancel")
def cancelar_nfce(chave: str, justificativa: str):
    if chave not in DB:
        raise HTTPException(404, "Nota não encontrada")
    DB[chave]["status"] = "cancelada"
    DB[chave]["justificativa"] = justificativa
    return {"chave": chave, "status": "cancelada"}
