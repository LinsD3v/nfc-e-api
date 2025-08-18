from fastapi import APIRouter
from models.pedido import Pedido
from mock.key_mock import gerar_chave
from main import DB
import hashlib

router = APIRouter(prefix="/nfc/ ")

@router.post("/nfce")
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