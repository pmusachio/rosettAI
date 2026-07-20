"""Gera imagens fictícias de atestado médico para testar o fluxo de upload
localmente, sem depender de documentos reais. Todos os dados são inventados.

Uso: python scripts/generate_demo_assets.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "demo_assets"


def _font(size):
    for candidate in ("Arial.ttf", "DejaVuSans.ttf", "Helvetica.ttf"):
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _base_canvas():
    img = Image.new("RGB", (900, 650), color="white")
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (899, 649)], outline="black", width=2)
    draw.text((30, 20), "AMOSTRA FICTÍCIA — DADOS SINTÉTICOS PARA TESTE", font=_font(16), fill="red")
    return img, draw


def generate_complete_certificate():
    img, draw = _base_canvas()
    lines = [
        ("Clínica Vida Plena", 24),
        ("", 12),
        ("ATESTADO MÉDICO", 22),
        ("", 20),
        ("Paciente: Ana Pereira", 18),
        ("CPF: 321.654.987-33", 18),
        ("", 10),
        ("Médico: Dr. Bruno Tavares", 18),
        ("CRM: CRM-PR 11223", 18),
        ("", 10),
        ("CID: R51", 18),
        ("Necessita afastamento de 1 (um) dia a partir desta data.", 18),
        ("", 10),
        ("Data de emissão: 18/07/2026", 18),
    ]
    y = 90
    for text, size in lines:
        if text:
            draw.text((60, y), text, font=_font(size), fill="black")
        y += size + 14
    path = OUTPUT_DIR / "atestado_completo_ana_pereira.png"
    img.save(path)
    return path


def generate_partial_certificate():
    img, draw = _base_canvas()
    lines = [
        ("UPA Central", 24),
        ("", 12),
        ("DECLARAÇÃO DE COMPARECIMENTO", 20),
        ("", 20),
        ("Paciente: Fernando Rocha", 18),
        ("", 10),
        ("Médico: [assinatura ilegível]", 18),
        ("CRM: [não identificado]", 18),
        ("", 10),
        ("CID: [não informado]", 18),
        ("Necessita de afastamento por [ilegível] dia(s).", 18),
        ("", 10),
        ("Data de emissão: 17/07/2026", 18),
    ]
    y = 90
    for text, size in lines:
        if text:
            draw.text((60, y), text, font=_font(size), fill="black")
        y += size + 14
    path = OUTPUT_DIR / "atestado_parcial_fernando_rocha.png"
    img.save(path)
    return path


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    p1 = generate_complete_certificate()
    p2 = generate_partial_certificate()
    print(f"Gerado: {p1}")
    print(f"Gerado: {p2}")
