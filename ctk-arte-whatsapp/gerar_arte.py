#!/usr/bin/env python3
"""
Arte final CTK Seguros — 1080x1350 PNG @ 300 DPI
QR Code REAL (biblioteca qrcode) → Segfy
Botão WhatsApp visual com número (link wa.me no HTML auxiliar)
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUTPUT = ROOT / "output"

W, H = 1080, 1350
DPI = 300
MARGIN = 32  # borda igual

NAVY = (8, 28, 58)
NAVY_DEEP = (3, 16, 38)
NAVY_MID = (16, 48, 92)
GOLD = (201, 162, 39)
GOLD_LIGHT = (232, 201, 98)
GOLD_DARK = (148, 112, 18)
WHITE = (255, 255, 255)
GREEN = (37, 211, 102)
GREEN_DARK = (18, 140, 70)

QR_URL = (
    "https://gestao.segfy.com/Publico/Segurados/Orcamentos/"
    "SolicitarCotacao?e=bq3pqK5O9i3fuSp4u7Wy9w%3D%3D"
)
WA_URL = "https://wa.me/5511941947162"
WA_LABEL = "+55 11 94194-7162"

FONT_REG = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Bold.ttf"


def F(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def text_size(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0], b[3] - b[1]


def center_text(draw, text, y, font, fill):
    tw, th = text_size(draw, text, font)
    draw.text(((W - tw) // 2, y), text, font=font, fill=fill)
    return th


def rounded(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def make_bg() -> Image.Image:
    img = Image.new("RGB", (W, H), NAVY_DEEP)
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        # leve gradiente + vinheta horizontal
        r = int(NAVY_DEEP[0] * (1 - t * 0.15) + NAVY_MID[0] * t * 0.25)
        g = int(NAVY_DEEP[1] * (1 - t * 0.15) + NAVY_MID[1] * t * 0.25)
        b = int(NAVY_DEEP[2] * (1 - t * 0.15) + NAVY_MID[2] * t * 0.25)
        for x in range(W):
            edge = min(x, W - 1 - x, y, H - 1 - y)
            dark = max(0, 28 - edge) / 28.0 * 0.35
            px[x, y] = (
                max(0, int(r * (1 - dark))),
                max(0, int(g * (1 - dark))),
                max(0, int(b * (1 - dark))),
            )
    return img


def draw_borders(draw):
    m = MARGIN
    draw.rectangle([m, m, W - m - 1, H - m - 1], outline=GOLD, width=3)
    draw.rectangle([m + 10, m + 10, W - m - 11, H - m - 11], outline=GOLD_LIGHT, width=1)
    c = m + 20
    arm = 26
    for x0, y0, sx, sy in (
        (c, c, 1, 1),
        (W - c - 1, c, -1, 1),
        (c, H - c - 1, 1, -1),
        (W - c - 1, H - c - 1, -1, -1),
    ):
        draw.line([(x0, y0), (x0 + sx * arm, y0)], fill=GOLD, width=3)
        draw.line([(x0, y0), (x0, y0 + sy * arm)], fill=GOLD, width=3)


def load_logo(max_w: int = 300) -> Image.Image:
    """Fundo branco → transparente; navy → branco; gold permanece."""
    logo = Image.open(ASSETS / "ctk-logo.png").convert("RGBA")
    arr = np.array(logo).astype(np.int16)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    # branco / near-white → transparente
    white = (r > 230) & (g > 230) & (b > 230)
    # gold: R alto, G médio, B baixo
    gold = (~white) & (r > 140) & (g > 90) & (r - b > 40)
    # resto com tinta (navy escuro) → branco brilhante
    ink = (~white) & (~gold) & ((r + g + b) < 520)

    out = arr.copy()
    out[white, 3] = 0
    out[gold, 0] = GOLD[0]
    out[gold, 1] = GOLD[1]
    out[gold, 2] = GOLD[2]
    out[gold, 3] = 255
    out[ink, 0] = 255
    out[ink, 1] = 255
    out[ink, 2] = 255
    out[ink, 3] = 255
    logo = Image.fromarray(out.astype(np.uint8), "RGBA")
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)
    ratio = max_w / logo.width
    return logo.resize((max_w, max(1, int(logo.height * ratio))), Image.Resampling.LANCZOS)


def circular_photo(size: int = 220) -> Image.Image:
    src = Image.open(ASSETS / "corretora-portrait.png").convert("RGBA")
    side = min(src.width, src.height)
    left = (src.width - side) // 2
    top = (src.height - side) // 2
    src = src.crop((left, top, left + side, top + side)).resize(
        (size, size), Image.Resampling.LANCZOS
    )
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((1, 1, size - 2, size - 2), fill=255)
    face = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    face.paste(src, (0, 0), mask)

    ring_pad = 12
    canvas = Image.new("RGBA", (size + ring_pad * 2, size + ring_pad * 2), (0, 0, 0, 0))
    rd = ImageDraw.Draw(canvas)
    rd.ellipse((0, 0, size + ring_pad * 2 - 1, size + ring_pad * 2 - 1), outline=GOLD, width=7)
    rd.ellipse((5, 5, size + ring_pad * 2 - 6, size + ring_pad * 2 - 6), outline=GOLD_LIGHT, width=2)
    canvas.paste(face, (ring_pad, ring_pad), face)
    return canvas


def icon_tile(size: int, kind: str) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((1, 1, size - 2, size - 2), fill=NAVY_MID, outline=GOLD, width=3)
    cx = cy = size / 2
    s = size * 0.26
    c = GOLD_LIGHT
    w = 3

    if kind == "auto":
        d.rounded_rectangle((cx - s * 1.15, cy - s * 0.1, cx + s * 1.15, cy + s * 0.65), 5, outline=c, width=w)
        d.polygon(
            [(cx - s * 0.8, cy - s * 0.1), (cx - s * 0.3, cy - s * 0.8), (cx + s * 0.4, cy - s * 0.8), (cx + s * 0.9, cy - s * 0.1)],
            outline=c,
            width=w,
        )
        d.ellipse((cx - s * 0.8, cy + s * 0.4, cx - s * 0.3, cy + s * 0.9), outline=c, width=w)
        d.ellipse((cx + s * 0.3, cy + s * 0.4, cx + s * 0.8, cy + s * 0.9), outline=c, width=w)
    elif kind == "casa":
        d.polygon([(cx, cy - s), (cx - s, cy), (cx + s, cy)], outline=c, width=w)
        d.rectangle((cx - s * 0.72, cy, cx + s * 0.72, cy + s * 0.9), outline=c, width=w)
        d.rectangle((cx - s * 0.2, cy + s * 0.25, cx + s * 0.2, cy + s * 0.9), outline=c, width=w)
    elif kind == "vida":
        pts = [
            (cx, cy - s),
            (cx - s * 0.9, cy - s * 0.35),
            (cx - s * 0.8, cy + s * 0.5),
            (cx, cy + s),
            (cx + s * 0.8, cy + s * 0.5),
            (cx + s * 0.9, cy - s * 0.35),
        ]
        d.polygon(pts, outline=c, width=w)
        d.ellipse((cx - s * 0.4, cy - s * 0.2, cx - 2, cy + s * 0.2), outline=c, width=2)
        d.ellipse((cx + 2, cy - s * 0.2, cx + s * 0.4, cy + s * 0.2), outline=c, width=2)
        d.polygon([(cx - s * 0.38, cy + 2), (cx, cy + s * 0.5), (cx + s * 0.38, cy + 2)], outline=c, width=2)
    elif kind == "saude":
        d.rounded_rectangle((cx - s * 0.26, cy - s, cx + s * 0.26, cy + s), 4, fill=c)
        d.rounded_rectangle((cx - s, cy - s * 0.26, cx + s, cy + s * 0.26), 4, fill=c)
    elif kind == "empresa":
        d.rectangle((cx - s * 0.85, cy - s * 0.15, cx + s * 0.85, cy + s * 0.9), outline=c, width=w)
        d.rectangle((cx - s * 0.5, cy - s * 0.9, cx + s * 0.5, cy - s * 0.15), outline=c, width=w)
        for i in (-0.5, 0, 0.5):
            for j in (0.15, 0.5):
                d.rectangle((cx + s * i - 5, cy + s * j - 5, cx + s * i + 5, cy + s * j + 5), outline=c, width=2)
    else:  # odonto
        d.ellipse((cx - s * 0.65, cy - s * 0.8, cx + s * 0.65, cy + s * 0.3), outline=c, width=w)
        d.line([(cx - s * 0.45, cy + s * 0.1), (cx - s * 0.3, cy + s * 0.85)], fill=c, width=w)
        d.line([(cx, cy + s * 0.25), (cx, cy + s * 0.7)], fill=c, width=w)
        d.line([(cx + s * 0.45, cy + s * 0.1), (cx + s * 0.3, cy + s * 0.85)], fill=c, width=w)
    return img


def make_qr(pixel: int = 236) -> Image.Image:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(QR_URL)
    qr.make(fit=True)
    raw = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return raw.resize((pixel, pixel), Image.Resampling.NEAREST)


def wa_glyph(size: int = 44) -> Image.Image:
    """Ícone WhatsApp estilo vetorial (círculo + balão)."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((0, 0, size - 1, size - 1), fill=WHITE)
    # balão
    m = int(size * 0.16)
    d.ellipse((m, int(m * 0.7), size - m, size - int(m * 1.15)), fill=GREEN)
    d.polygon(
        [
            (int(size * 0.26), int(size * 0.72)),
            (int(size * 0.14), int(size * 0.94)),
            (int(size * 0.44), int(size * 0.78)),
        ],
        fill=GREEN,
    )
    # handset hint
    d.arc(
        (int(size * 0.32), int(size * 0.30), int(size * 0.68), int(size * 0.66)),
        start=200,
        end=340,
        fill=WHITE,
        width=3,
    )
    return img


def phone_emoji(size: int = 36) -> Image.Image:
    """Ícone 📱 vetorial (branco) — legível no botão verde."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # corpo do celular
    x0, y0 = size * 0.28, size * 0.06
    x1, y1 = size * 0.72, size * 0.94
    d.rounded_rectangle((x0, y0, x1, y1), radius=size * 0.12, outline=WHITE, width=max(2, size // 14))
    # tela
    d.rounded_rectangle(
        (x0 + size * 0.08, y0 + size * 0.14, x1 - size * 0.08, y1 - size * 0.22),
        radius=size * 0.04,
        outline=WHITE,
        width=max(1, size // 18),
    )
    # botão home
    cx, cy = size / 2, y1 - size * 0.11
    r = size * 0.06
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE)
    return img


def compose() -> Image.Image:
    base = make_bg().convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw_borders(draw)

    # Escala vertical compacta para caber tudo com bordas
    y = MARGIN + 22

    logo = load_logo(240)
    layer.alpha_composite(logo, ((W - logo.width) // 2, y))
    y += logo.height + 10

    photo = circular_photo(200)
    layer.alpha_composite(photo, ((W - photo.width) // 2, y))
    y += photo.height + 10

    y += center_text(draw, "CTK CORRETORA DE SEGUROS", y, F(22, True), GOLD_LIGHT) + 6
    y += center_text(draw, "Proteção completa para você e sua família", y, F(17), WHITE) + 12

    draw.line([(W // 2 - 70, y), (W // 2 + 70, y)], fill=GOLD, width=2)
    y += 16

    # Ícones 2x3
    products = [
        ("auto", "AUTO"),
        ("casa", "RESIDENCIAL"),
        ("vida", "VIDA"),
        ("saude", "SAÚDE"),
        ("empresa", "EMPRESARIAL"),
        ("odonto", "ODONTOLÓGICO"),
    ]
    icon_s = 70
    gap_x = 36
    cols = 3
    row_w = cols * icon_s + (cols - 1) * gap_x
    x0 = (W - row_w) // 2
    f_icon = F(13, True)
    label_h = 18

    for i, (kind, label) in enumerate(products):
        row, col = divmod(i, cols)
        ix = x0 + col * (icon_s + gap_x)
        iy = y + row * (icon_s + label_h + 16)
        ic = icon_tile(icon_s, kind)
        layer.alpha_composite(ic, (ix, iy))
        tw, _ = text_size(draw, label, f_icon)
        draw.text((ix + (icon_s - tw) // 2, iy + icon_s + 5), label, font=f_icon, fill=WHITE)

    y += 2 * (icon_s + label_h + 16) + 6

    # CTA DESTACADO — faixa dourada sólida, sem artefatos
    cta = "FAÇA SUA COTAÇÃO GRATUITA"
    f_cta = F(28, True)
    tw, th = text_size(draw, cta, f_cta)
    cta_h = 74
    cta_m = 72
    # sombra suave abaixo
    rounded(draw, (cta_m + 2, y + 6, W - cta_m + 2, y + cta_h + 6), 18, fill=(0, 0, 0, 100))
    rounded(draw, (cta_m, y, W - cta_m, y + cta_h), 18, fill=GOLD)
    rounded(draw, (cta_m, y, W - cta_m, y + cta_h), 18, outline=GOLD_LIGHT, width=3)
    draw.text(((W - tw) // 2, y + (cta_h - th) // 2 - 1), cta, font=f_cta, fill=NAVY_DEEP)
    y += cta_h + 18

    # QR maior e enquadrado (uma moldura limpa)
    qr = make_qr(252)
    qx = (W - qr.width) // 2
    box_pad = 10
    rounded(
        draw,
        (qx - box_pad, y - box_pad, qx + qr.width + box_pad, y + qr.height + box_pad),
        12,
        fill=WHITE,
        outline=GOLD,
        width=4,
    )
    layer.paste(qr, (qx, y))
    y += qr.height + box_pad + 14

    # Botão dourado (duas linhas, branco, centralizado)
    t1, t2 = "ESCANEIE O QR CODE", "E FAÇA SUA COTAÇÃO"
    f_btn = F(18, True)
    w1, h1 = text_size(draw, t1, f_btn)
    w2, h2 = text_size(draw, t2, f_btn)
    btn_w = max(w1, w2) + 56
    btn_h = h1 + h2 + 28
    bx = (W - btn_w) // 2
    rounded(draw, (bx, y, bx + btn_w, y + btn_h), 12, fill=GOLD, outline=GOLD_LIGHT, width=2)
    draw.text(((W - w1) // 2, y + 10), t1, font=f_btn, fill=WHITE)
    draw.text(((W - w2) // 2, y + 10 + h1 + 4), t2, font=f_btn, fill=WHITE)
    y += btn_h + 16

    # BOTÃO WHATSAPP GRANDE
    wa_h = 82
    wa_m = 86
    rounded(draw, (wa_m + 3, y + 4, W - wa_m + 3, y + wa_h + 4), 41, fill=(0, 0, 0, 120))
    rounded(draw, (wa_m, y, W - wa_m, y + wa_h), 41, fill=GREEN, outline=(180, 255, 210), width=3)

    icon = wa_glyph(48)
    phone = phone_emoji(36)
    f_wa = F(28, True)
    label = WA_LABEL
    tw, th = text_size(draw, label, f_wa)
    gap = 10
    total = icon.width + gap + phone.width + 10 + tw
    start = (W - total) // 2
    iy = y + (wa_h - icon.height) // 2
    layer.alpha_composite(icon, (start, iy))
    layer.alpha_composite(phone, (start + icon.width + gap, y + (wa_h - phone.height) // 2))
    draw.text(
        (start + icon.width + gap + phone.width + 10, y + (wa_h - th) // 2 - 1),
        label,
        font=f_wa,
        fill=WHITE,
    )

    # Garantir que cabemos na borda inferior
    assert y + wa_h < H - MARGIN - 16, f"overflow: bottom={y + wa_h} limit={H - MARGIN - 16}"

    out = Image.alpha_composite(base, layer)
    return out.convert("RGB")


def export(img: Image.Image) -> Path:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    out = OUTPUT / "CTK_Arte_WhatsApp_1080x1350.png"
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Title", "CTK Corretora de Seguros — Cotação Gratuita")
    meta.add_text("Description", f"QR={QR_URL}; WhatsApp={WA_URL}")
    meta.add_text("Software", "qrcode+Pillow CTK generator")
    kwargs = dict(dpi=(DPI, DPI), optimize=False, compress_level=1, pnginfo=meta)
    img.save(out, "PNG", **kwargs)
    img.save("/opt/cursor/artifacts/CTK_Arte_WhatsApp_1080x1350.png", "PNG", **kwargs)

    # QR isolado + preview crop
    make_qr(400).save(OUTPUT / "qrcode_segfy_real.png", "PNG", dpi=(DPI, DPI))

    (OUTPUT / "CTK_Arte_WhatsApp_clicavel.html").write_text(
        f"""<!DOCTYPE html>
<html lang="pt-BR"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>CTK — Cotação</title>
<style>
body{{margin:0;background:#041226;display:flex;justify-content:center;padding:12px}}
.wrap{{position:relative;width:min(1080px,100%)}}
img{{width:100%;display:block;border-radius:6px}}
a.qr{{position:absolute;left:28%;right:28%;top:58%;height:20%}}
a.wa{{position:absolute;left:8%;right:8%;bottom:4.2%;height:6.2%;border-radius:999px}}
</style></head><body>
<div class="wrap">
<img src="CTK_Arte_WhatsApp_1080x1350.png" alt="CTK"/>
<a class="qr" href="{QR_URL}" title="Cotação Segfy"></a>
<a class="wa" href="{WA_URL}" title="WhatsApp {WA_LABEL}"></a>
</div></body></html>
""",
        encoding="utf-8",
    )
    return out


def main():
    img = compose()
    path = export(img)
    print(f"OK {path} {img.size} dpi={DPI} bytes={path.stat().st_size}")
    # Validar payload do QR gerado pela lib
    qr = qrcode.QRCode()
    qr.add_data(QR_URL)
    qr.make(fit=True)
    print("QR modules:", qr.modules_count, "data OK")


if __name__ == "__main__":
    main()
