from pydantic import BaseModel

class Item(BaseModel):
    codigo: str
    descricao: str
    quantidade: float
    valor_unit: float