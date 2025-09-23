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

    # Cabeçalho DANFE NFC-e padrão brasileiro
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20*mm, altura - 18*mm, "DANFE NFC-e - Documento Auxiliar da Nota Fiscal de Consumidor Eletrônica")
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, altura - 26*mm, f"Nº: {dados.get('numero', '---')}  Série: {dados.get('serie', '---')}  Modelo: {dados.get('modelo', '65')}")
    c.drawString(20*mm, altura - 32*mm, f"Data/Hora Emissão: {dados.get('dhEmi', '---')}")
    c.drawString(20*mm, altura - 38*mm, f"Chave de Acesso: {chave}")
    c.drawString(20*mm, altura - 44*mm, f"Protocolo: {dados.get('protocolo', '---')}")
    c.drawString(20*mm, altura - 50*mm, f"Status: {dados.get('status', '---')}")
    c.drawString(20*mm, altura - 56*mm, f"Total: R$ {dados.get('total', 0):.2f}")

    # Emitente
    emitente = dados.get('emitente', {})
    c.setFont("Helvetica-Bold", 11)
    c.drawString(20*mm, altura - 64*mm, f"Emitente: {emitente.get('razao_social', '---')}")
    c.setFont("Helvetica", 9)
    c.drawString(20*mm, altura - 70*mm, f"CNPJ: {emitente.get('cnpj', '---')}  IE: {emitente.get('ie', '---')}")
    c.drawString(20*mm, altura - 76*mm, f"Endereço: {emitente.get('endereco', '---')}")

    # Destinatário (opcional)
    destinatario = dados.get('destinatario', {})
    if destinatario:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(20*mm, altura - 84*mm, f"Destinatário: {destinatario.get('nome', '---')}")
        c.setFont("Helvetica", 9)
        c.drawString(20*mm, altura - 90*mm, f"CPF/CNPJ: {destinatario.get('cpf_cnpj', '---')}")
        c.drawString(20*mm, altura - 96*mm, f"Endereço: {destinatario.get('endereco', '---')}")
        y_itens = altura - 104*mm
    else:
        y_itens = altura - 84*mm

    # QR Code
    qr = qrcode.make(dados["qr"])
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    img = ImageReader(buffer)
    c.drawImage(img, largura - 60*mm, altura - 70*mm, 40*mm, 40*mm)

    # Itens
    c.setFont("Helvetica-Bold", 11)
    c.drawString(20*mm, y_itens, "Itens da Venda:")
    y = y_itens - 8*mm
    c.setFont("Helvetica", 9)
    c.drawString(20*mm, y, "Cód  Descrição                    Qtd  V. Unit  V. Total")
    y -= 6*mm
    for item in dados["pedido"]["itens"]:
        v_total = item['quantidade'] * item['valor_unit']
        linha = f"{item['codigo']:<4} {item['descricao'][:20]:<22} {item['quantidade']:>4} {item['valor_unit']:>7.2f} {v_total:>8.2f}"
        c.drawString(20*mm, y, linha)
        y -= 6*mm
        if y < 30*mm:
            c.showPage()
            y = altura - 20*mm

    # Forma de pagamento
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20*mm, y-4*mm, f"Pagamento: {dados['pedido'].get('pagamento', '---').upper()}")

    c.showPage()
    c.save()
    return nome_arquivo
