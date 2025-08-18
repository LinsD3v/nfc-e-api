from pydantic import BaseModel
from typing import List, Literal, Optional
from models.item import Item
from datetime import datetime

class Pedido(BaseModel):
    numero: int
    serie: int = 1
    modelo: Literal[65] = 65
    dhEmi: datetime = datetime.utcnow()
    itens: List[Item]
    pagamento: Literal["dinheiro","credito","debito","pix","outros"]