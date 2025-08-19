from datetime import datetime

def gerar_chave(numero: int, serie: int) -> str:
    # Chave mock de 44 dígitos
    base = f"35{datetime.now().strftime('%y%m')}{numero:09d}{serie:03d}"
    return base.ljust(44, "0")
