from fastapi import APIRouter
from models.pedido import Pedido
from mock.key_mock import gerar_chave
from db import salvar_nota
import hashlib

router = APIRouter(prefix="/nfc")

@router.post("/")
def criar_nfce(pedido: Pedido):
    chave = gerar_chave(pedido.numero, pedido.serie)
    protocolo = hashlib.sha1(chave.encode()).hexdigest()[:15]
    total = sum(i.quantidade * i.valor_unit for i in pedido.itens)
    qr_data = f"https://sefaz-fake.gov/nfce?q={chave}|{total:.2f}"
    
    pedido_dict = pedido.dict()
    # Serializa campos datetime para string ISO
    if isinstance(pedido_dict.get('dhEmi'), (str,)) is False and pedido_dict.get('dhEmi'):
        pedido_dict['dhEmi'] = pedido_dict['dhEmi'].isoformat()
    dados_nota = {
        "pedido": pedido_dict,
        "status": "autorizada",
        "protocolo": protocolo,
        "total": total,
        "qr": qr_data
    }
    salvar_nota(chave, dados_nota)
    return {
        "chave": chave,
        "protocolo": protocolo,
        "status": "autorizada",
        "total": round(total, 2),
        "qr_url": qr_data
    }