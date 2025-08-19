from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import qrcode
from io import BytesIO

def gerar_danfe(chave, dados):
    nome_arquivo = f"DANFE_{chave}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    # Cabeçalho
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20*mm, altura - 20*mm, "DANFCE - Documento Auxiliar da Nota Fiscal do Consumidor Eletrônica")
    
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, altura - 30*mm, f"Chave de Acesso: {chave}")
    c.drawString(20*mm, altura - 40*mm, f"Protocolo: {dados['protocolo']}")
    c.drawString(20*mm, altura - 50*mm, f"Status: {dados['status']}")
    c.drawString(20*mm, altura - 60*mm, f"Total: R$ {dados['total']:.2f}")

    # QR Code
    qr = qrcode.make(dados["qr"])
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    
    img = ImageReader(buffer) 
    c.drawImage(img, largura - 60*mm, altura - 70*mm, 40*mm, 40*mm)

    # Itens
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20*mm, altura - 80*mm, "Itens da Venda:")

    y = altura - 90*mm
    c.setFont("Helvetica", 10)
    for item in dados["pedido"]["itens"]:
        linha = f"{item['descricao']}  x{item['quantidade']}  R$ {item['valor_unit']:.2f}"
        c.drawString(20*mm, y, linha)
        y -= 10*mm

    c.showPage()
    c.save()
    return nome_arquivo
