#!/usr/bin/env python3
"""
Arte final CTK — layout da referência (navy + painel branco + footer)
1080x1350 PNG @ 300 DPI | QR REAL (qrcode) | WhatsApp + telefone
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter, PngImagePlugin

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUTPUT = ROOT / "output"

W, H = 1080, 1350
DPI = 300

NAVY = (10, 28, 64)
NAVY_DEEP = (6, 18, 48)
NAVY_SOFT = (20, 45, 95)
GOLD = (201, 162, 39)
GOLD_LIGHT = (230, 200, 95)
GOLD_DARK = (150, 115, 20)
WHITE = (255, 255, 255)
GREEN = (37, 211, 102)
GREEN_DARK = (18, 140, 70)
GREEN_TEXT = (22, 163, 74)
BLACK = (20, 20, 20)
GRAY = (70, 80, 100)

QR_URL = (
    "https://gestao.segfy.com/Publico/Segurados/Orcamentos/"
    "SolicitarCotacao?e=bq3pqK5O9i3fuSp4u7Wy9w%3D%3D"
)
WA_URL = "https://wa.me/5511941947162"
WA_PHONE = "+55 11 94194-7162"

FONT_R = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Regular.ttf"
FONT_B = "/usr/share/fonts/truetype/noto/NotoSansDisplay-Bold.ttf"
FONT_BI = "/usr/share/fonts/truetype/noto/NotoSansDisplay-BoldItalic.ttf"


def F(size: int, bold=False, italic=False):
    if italic and bold:
        path = FONT_BI
    elif bold:
        path = FONT_B
    else:
        path = FONT_R
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def ts(draw, text, font):
    b = draw.textbbox((0, 0), text, font=font)
    return b[2] - b[0], b[3] - b[1]


def round_rect(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def remove_white(img: Image.Image, thresh=240) -> Image.Image:
    arr = np.array(img.convert("RGBA"))
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    white = (r > thresh) & (g > thresh) & (b > thresh)
    arr[white, 3] = 0
    out = Image.fromarray(arr, "RGBA")
    bbox = out.getbbox()
    return out.crop(bbox) if bbox else out


def load_logo_crest(max_h=130) -> Image.Image:
    logo = remove_white(Image.open(ASSETS / "ctk-crest-logo.png"), 248)
    ratio = max_h / logo.height
    return logo.resize((int(logo.width * ratio), max_h), Image.Resampling.LANCZOS)


def load_topspeed(max_w=160) -> Image.Image:
    logo = remove_white(Image.open(ASSETS / "topspeed-logo.png"), 248)
    ratio = max_w / logo.width
    return logo.resize((max_w, max(1, int(logo.height * ratio))), Image.Resampling.LANCZOS)


def load_hero(size=(420, 520)) -> Image.Image:
    src = Image.open(ASSETS / "corretora-hero.png").convert("RGB")
    # cover crop
    tw, th = size
    scale = max(tw / src.width, th / src.height)
    nw, nh = int(src.width * scale), int(src.height * scale)
    src = src.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = max(0, (nh - th) // 2 - 20)
    src = src.crop((left, top, left + tw, top + th))
    # rounded mask
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, tw - 1, th - 1), radius=28, fill=255)
    out = Image.new("RGBA", size, (0, 0, 0, 0))
    out.paste(src, (0, 0))
    out.putalpha(mask)
    # gold border
    border = Image.new("RGBA", size, (0, 0, 0, 0))
    bd = ImageDraw.Draw(border)
    bd.rounded_rectangle((1, 1, tw - 2, th - 2), radius=28, outline=GOLD, width=4)
    return Image.alpha_composite(out, border)


def make_qr(px=150) -> Image.Image:
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=1,
    )
    qr.add_data(QR_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img.resize((px, px), Image.Resampling.NEAREST)


def icon_circle(kind: str, size=72) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((1, 1, size - 2, size - 2), fill=WHITE, outline=GOLD, width=3)
    m = 7
    d.ellipse((m, m, size - m - 1, size - m - 1), fill=NAVY)
    cx = cy = size / 2
    s = size * 0.22
    c = WHITE  # ícones brancos sobre navy (como na referência)
    w = 2

    if kind == "auto":
        d.rounded_rectangle((cx - s * 1.1, cy - s * 0.1, cx + s * 1.1, cy + s * 0.55), 3, outline=c, width=w)
        d.polygon(
            [(cx - s * 0.75, cy - s * 0.1), (cx - s * 0.25, cy - s * 0.7), (cx + s * 0.35, cy - s * 0.7), (cx + s * 0.85, cy - s * 0.1)],
            outline=c, width=w,
        )
        d.ellipse((cx - s * 0.75, cy + s * 0.35, cx - s * 0.3, cy + s * 0.8), outline=c, width=w)
        d.ellipse((cx + s * 0.3, cy + s * 0.35, cx + s * 0.75, cy + s * 0.8), outline=c, width=w)
    elif kind == "moto":
        d.ellipse((cx - s * 0.95, cy + s * 0.15, cx - s * 0.25, cy + s * 0.85), outline=c, width=w)
        d.ellipse((cx + s * 0.25, cy + s * 0.15, cx + s * 0.95, cy + s * 0.85), outline=c, width=w)
        d.line([(cx - s * 0.4, cy + s * 0.35), (cx + s * 0.15, cy - s * 0.55)], fill=c, width=w + 1)
        d.line([(cx + s * 0.15, cy - s * 0.55), (cx + s * 0.55, cy + s * 0.35)], fill=c, width=w + 1)
        d.arc((cx - s * 0.1, cy - s * 0.9, cx + s * 0.7, cy - s * 0.1), 200, 340, fill=c, width=w)
    elif kind == "truck":
        d.rectangle((cx - s * 1.05, cy - s * 0.35, cx + s * 0.15, cy + s * 0.55), outline=c, width=w)
        d.rectangle((cx + s * 0.15, cy - s * 0.05, cx + s * 0.95, cy + s * 0.55), outline=c, width=w)
        d.ellipse((cx - s * 0.7, cy + s * 0.35, cx - s * 0.25, cy + s * 0.8), outline=c, width=w)
        d.ellipse((cx + s * 0.35, cy + s * 0.35, cx + s * 0.8, cy + s * 0.8), outline=c, width=w)
    elif kind == "casa":
        d.polygon([(cx, cy - s * 0.85), (cx - s * 0.9, cy - s * 0.05), (cx + s * 0.9, cy - s * 0.05)], outline=c, width=w)
        d.rectangle((cx - s * 0.65, cy - s * 0.05, cx + s * 0.65, cy + s * 0.8), outline=c, width=w)
        d.rectangle((cx - s * 0.18, cy + s * 0.15, cx + s * 0.18, cy + s * 0.8), outline=c, width=w)
    elif kind == "vida":
        d.ellipse((cx - s * 0.85, cy - s * 0.55, cx - 1, cy + s * 0.25), outline=c, width=w)
        d.ellipse((1 + cx, cy - s * 0.55, cx + s * 0.85, cy + s * 0.25), outline=c, width=w)
        d.polygon([(cx - s * 0.82, cy + s * 0.05), (cx, cy + s * 0.9), (cx + s * 0.82, cy + s * 0.05)], outline=c, width=w)
        d.ellipse((cx - s * 0.35, cy - s * 0.15, cx - s * 0.1, cy + s * 0.1), fill=c)
        d.ellipse((cx + s * 0.1, cy - s * 0.15, cx + s * 0.35, cy + s * 0.1), fill=c)
    elif kind == "empresa":
        d.rectangle((cx - s * 0.75, cy - s * 0.15, cx + s * 0.75, cy + s * 0.8), outline=c, width=w)
        d.rectangle((cx - s * 0.4, cy - s * 0.85, cx + s * 0.4, cy - s * 0.15), outline=c, width=w)
        for i in (-0.4, 0, 0.4):
            d.rectangle((cx + s * i - 4, cy + s * 0.15, cx + s * i + 4, cy + s * 0.4), outline=c, width=1)
    else:  # consorcio $
        d.ellipse((cx - s * 0.75, cy - s * 0.75, cx + s * 0.75, cy + s * 0.75), outline=c, width=w + 1)
        f = F(int(size * 0.38), True)
        d.text((cx - size * 0.12, cy - size * 0.22), "$", font=f, fill=c)
    return img


def gold_shield(size=28) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pts = [
        (size * 0.5, 1),
        (size - 2, size * 0.28),
        (size - 3, size * 0.62),
        (size * 0.5, size - 1),
        (3, size * 0.62),
        (2, size * 0.28),
    ]
    d.polygon(pts, fill=GOLD)
    # check
    d.line([(size * 0.28, size * 0.48), (size * 0.45, size * 0.65), (size * 0.72, size * 0.32)], fill=NAVY_DEEP, width=3)
    return img


def heart_icon(size=22) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = GOLD_LIGHT
    d.ellipse((1, 2, size * 0.55, size * 0.6), outline=c, width=2)
    d.ellipse((size * 0.45, 2, size - 2, size * 0.6), outline=c, width=2)
    d.polygon([(2, size * 0.4), (size / 2, size - 2), (size - 2, size * 0.4)], outline=c, width=2)
    return img


def benefit_icon(kind: str, size=46) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = GOLD
    w = 2
    cx = cy = size / 2
    s = size * 0.32
    if kind == "handshake":
        d.arc((cx - s, cy - s * 0.4, cx + s * 0.2, cy + s * 0.8), 20, 200, fill=c, width=w)
        d.arc((cx - s * 0.2, cy - s * 0.4, cx + s, cy + s * 0.8), -20, 160, fill=c, width=w)
        d.line([(cx - s * 0.6, cy), (cx + s * 0.6, cy)], fill=c, width=w)
    elif kind == "search":
        d.ellipse((cx - s, cy - s, cx + s * 0.4, cy + s * 0.4), outline=c, width=w)
        d.line([(cx + s * 0.25, cy + s * 0.25), (cx + s * 0.9, cy + s * 0.9)], fill=c, width=w + 1)
    elif kind == "people":
        for dx in (-0.55, 0, 0.55):
            d.ellipse((cx + s * dx - 4, cy - s * 0.7, cx + s * dx + 4, cy - s * 0.2), outline=c, width=w)
            d.arc((cx + s * dx - 8, cy - s * 0.1, cx + s * dx + 8, cy + s * 0.9), 200, 340, fill=c, width=w)
    elif kind == "headset":
        d.arc((cx - s, cy - s * 0.7, cx + s, cy + s * 0.5), 200, 340, fill=c, width=w)
        d.rounded_rectangle((cx - s * 1.1, cy - s * 0.1, cx - s * 0.55, cy + s * 0.55), 3, outline=c, width=w)
        d.rounded_rectangle((cx + s * 0.55, cy - s * 0.1, cx + s * 1.1, cy + s * 0.55), 3, outline=c, width=w)
    else:  # star
        pts = []
        import math
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            r = s if i % 2 == 0 else s * 0.45
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        d.polygon(pts, outline=c, width=w)
    return img


def wa_bubble(size=56) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((0, 0, size - 1, size - 1), fill=GREEN)
    m = int(size * 0.18)
    d.ellipse((m, int(m * 0.7), size - m, size - int(m * 1.15)), fill=WHITE)
    d.polygon(
        [(int(size * 0.28), int(size * 0.72)), (int(size * 0.16), int(size * 0.94)), (int(size * 0.46), int(size * 0.78))],
        fill=WHITE,
    )
    return img


def phone_icon(size=28) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((size * 0.3, 1, size * 0.7, size - 1), 4, outline=WHITE, width=2)
    d.ellipse((size * 0.42, size * 0.78, size * 0.58, size * 0.9), fill=WHITE)
    return img


def wrap_text(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        tw, _ = ts(draw, trial, font)
        if tw <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def compose() -> Image.Image:
    base = Image.new("RGB", (W, H), NAVY_DEEP)
    # subtle top gradient
    px = base.load()
    for y in range(520):
        t = y / 520
        r = int(NAVY_DEEP[0] + (NAVY[0] - NAVY_DEEP[0]) * t)
        g = int(NAVY_DEEP[1] + (NAVY[1] - NAVY_DEEP[1]) * t)
        b = int(NAVY_DEEP[2] + (NAVY[2] - NAVY_DEEP[2]) * t)
        for x in range(W):
            px[x, y] = (r, g, b)

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    # ========== TOP LEFT BRAND ==========
    logo = load_logo_crest(118)
    layer.alpha_composite(logo, (42, 28))

    f_sub = F(13, True)
    draw.text((52, 28 + logo.height + 4), "CORRETORA DE SEGUROS", font=f_sub, fill=WHITE)

    # Parceira oficial TopSpeed
    y_p = 28 + logo.height + 28
    sh = gold_shield(26)
    layer.alpha_composite(sh, (52, y_p))
    f_p = F(12, True)
    draw.text((84, y_p + 4), "PARCEIRA OFICIAL", font=f_p, fill=GOLD_LIGHT)
    ts_logo = load_topspeed(130)
    layer.alpha_composite(ts_logo, (84, y_p + 22))

    # Tagline
    y_t = y_p + 70
    f_h1 = F(34, True)
    f_h2 = F(36, True)
    draw.text((48, y_t), "CUIDAMOS DO QUE", font=f_h1, fill=GOLD)
    draw.text((48, y_t + 40), "MAIS IMPORTA!", font=f_h2, fill=WHITE)

    # Experience capsule
    y_c = y_t + 95
    exp = "Há mais de 20 anos oferecendo soluções completas para proteger você, sua família e seu patrimônio."
    f_exp = F(13)
    lines = wrap_text(draw, exp, f_exp, 420)
    cap_h = 18 + len(lines) * 18 + 12
    round_rect(draw, (42, y_c, 520, y_c + cap_h), 22, fill=NAVY, outline=GOLD, width=2)
    ht = heart_icon(20)
    layer.alpha_composite(ht, (56, y_c + 14))
    ty = y_c + 12
    for line in lines:
        draw.text((84, ty), line, font=f_exp, fill=WHITE)
        ty += 18

    # ========== TOP RIGHT HERO ==========
    hero = load_hero((430, 500))
    hx, hy = 600, 24
    # soft shadow
    shadow = Image.new("RGBA", (hero.width + 20, hero.height + 20), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((8, 10, hero.width + 8, hero.height + 10), 28, fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    layer.alpha_composite(shadow, (hx - 8, hy - 2))
    layer.alpha_composite(hero, (hx, hy))

    # Badge overlapping photo
    badge = "ATUANDO NO RAMO DE SEGUROS HÁ 20 ANOS"
    f_badge = F(11, True)
    bw, bh = ts(draw, badge, f_badge)
    bx0 = hx + 18
    by0 = hy + hero.height - 70
    round_rect(draw, (bx0, by0, bx0 + bw + 50, by0 + 42), 10, fill=(12, 12, 18, 230), outline=GOLD, width=2)
    bsh = gold_shield(22)
    layer.alpha_composite(bsh, (bx0 + 10, by0 + 10))
    draw.text((bx0 + 38, by0 + 12), badge, font=f_badge, fill=GOLD_LIGHT)

    # ========== WHITE MIDDLE PANEL ==========
    panel_top = 545
    panel_bot = 1045
    round_rect(draw, (28, panel_top, W - 28, panel_bot), 28, fill=WHITE)

    # SOLUÇÕES capsule
    title = "SOLUÇÕES QUE OFERECEMOS"
    f_sol = F(16, True)
    tw, th = ts(draw, title, f_sol)
    sol_w = tw + 48
    sol_x = (W - sol_w) // 2
    sol_y = panel_top + 18
    round_rect(draw, (sol_x, sol_y, sol_x + sol_w, sol_y + 36), 18, fill=GOLD)
    draw.text(((W - tw) // 2, sol_y + 8), title, font=f_sol, fill=NAVY_DEEP)

    # 7 product icons
    products = [
        ("auto", "SEGURO\nAUTO"),
        ("moto", "SEGURO\nMOTO"),
        ("truck", "SEGURO\nCAMINHÃO"),
        ("casa", "SEGURO\nRESIDENCIAL"),
        ("vida", "SEGURO\nDE VIDA"),
        ("empresa", "SEGURO\nEMPRESARIAL"),
        ("money", "CONSÓRCIOS\nE MUITO MAIS"),
    ]
    icon_s = 64
    gap = 18
    total_w = 7 * icon_s + 6 * gap
    x0 = (W - total_w) // 2
    iy = sol_y + 52
    f_ilab = F(9, True)
    for i, (kind, label) in enumerate(products):
        ix = x0 + i * (icon_s + gap)
        ic = icon_circle(kind, icon_s)
        layer.alpha_composite(ic, (ix, iy))
        # multiline label centered
        for li, line in enumerate(label.split("\n")):
            lw, _ = ts(draw, line, f_ilab)
            draw.text((ix + (icon_s - lw) // 2, iy + icon_s + 4 + li * 12), line, font=f_ilab, fill=NAVY)

    # Cotação row: left text + right QR
    cy0 = iy + icon_s + 42
    # Left CTA text — highlighted
    f_cta1 = F(26, True)
    f_cta2 = F(26, True)
    draw.text((52, cy0), "FAÇA SUA", font=f_cta1, fill=NAVY)
    draw.text((52, cy0 + 32), "COTAÇÃO", font=f_cta2, fill=GOLD_DARK)
    draw.text((52, cy0 + 64), "GRATUITA!", font=f_cta2, fill=NAVY)

    f_desc = F(13)
    desc = "Seguro Auto, Moto e Caminhão: É só preencher o formulário e buscaremos a melhor opção para você!"
    for i, line in enumerate(wrap_text(draw, desc, f_desc, 480)):
        draw.text((52, cy0 + 105 + i * 17), line, font=f_desc, fill=GRAY)

    # Cotação 20 seguradoras
    y_seg = cy0 + 160
    layer.alpha_composite(gold_shield(24), (52, y_seg))
    f_seg = F(12, True)
    draw.text((82, y_seg + 4), "COTAÇÃO EM MAIS DE 20 SEGURADORAS", font=f_seg, fill=NAVY)

    # Right QR — enlarged & framed
    qr = make_qr(168)
    qx = W - 48 - qr.width - 14
    qy = cy0 + 2
    # gold frame pad
    pad = 12
    round_rect(draw, (qx - pad, qy - pad, qx + qr.width + pad, qy + qr.height + pad), 12, fill=WHITE, outline=GOLD, width=4)
    layer.paste(qr.convert("RGBA"), (qx, qy))

    # Gold button under QR — required copy, white text, centered
    btn1, btn2 = "ESCANEIE O QR CODE", "E FAÇA SUA COTAÇÃO"
    f_btn = F(12, True)
    w1, h1 = ts(draw, btn1, f_btn)
    w2, h2 = ts(draw, btn2, f_btn)
    btn_w = max(qr.width + pad * 2, max(w1, w2) + 24)
    btn_h = h1 + h2 + 18
    bx = qx + qr.width // 2 - btn_w // 2
    by = qy + qr.height + pad + 10
    round_rect(draw, (bx, by, bx + btn_w, by + btn_h), 10, fill=GOLD, outline=GOLD_DARK, width=1)
    draw.text((bx + (btn_w - w1) // 2, by + 7), btn1, font=f_btn, fill=WHITE)
    draw.text((bx + (btn_w - w2) // 2, by + 7 + h1 + 2), btn2, font=f_btn, fill=WHITE)

    # WhatsApp row inside white panel
    wa_y = panel_bot - 110
    # divider
    draw.line([(52, wa_y - 14), (W - 52, wa_y - 14)], fill=(230, 230, 235), width=2)

    bubble = wa_bubble(54)
    layer.alpha_composite(bubble, (48, wa_y))
    f_wa_t = F(13, True)
    wa_msg = "CONSÓRCIOS, PLANOS DE SAÚDE E DEMAIS SEGUROS? Fale conosco no WhatsApp e nossa equipe terá o maior prazer em te atender!"
    tx = 114
    for i, line in enumerate(wrap_text(draw, wa_msg, f_wa_t, 420)):
        draw.text((tx, wa_y + 2 + i * 16), line, font=f_wa_t, fill=GREEN_TEXT)

    # BIG green WhatsApp button (right) — larger, with phone
    gbw = 320
    gbh = 72
    gbx = W - 52 - gbw
    gby = wa_y - 4
    round_rect(draw, (gbx + 2, gby + 3, gbx + gbw + 2, gby + gbh + 3), 36, fill=(0, 0, 0, 60))
    round_rect(draw, (gbx, gby, gbx + gbw, gby + gbh), 36, fill=GREEN)
    # content: WA icon + phone + CTA
    mini = wa_bubble(32)
    layer.alpha_composite(mini, (gbx + 14, gby + 20))
    ph = phone_icon(22)
    layer.alpha_composite(ph, (gbx + 52, gby + 12))
    f_ph = F(13, True)
    draw.text((gbx + 78, gby + 12), WA_PHONE, font=f_ph, fill=WHITE)
    f_cta_wa = F(13, True)
    cta_wa = "SOLICITE SUA COTAÇÃO AGORA"
    cw, _ = ts(draw, cta_wa, f_cta_wa)
    draw.text((gbx + (gbw - cw) // 2 + 10, gby + 40), cta_wa, font=f_cta_wa, fill=WHITE)

    # ========== FOOTER NAVY ==========
    # already navy from base; ensure bottom solid
    draw.rectangle((0, panel_bot + 8, W, H), fill=NAVY_DEEP)

    benefits = [
        ("handshake", "ATENDIMENTO\nPERSONALIZADO"),
        ("search", "ANÁLISE DAS\nMELHORES SEGURADORAS"),
        ("people", "ACOMPANHAMENTO\nDO INÍCIO AO FIM"),
        ("headset", "SUPORTE TAMBÉM\nAPÓS A CONTRATAÇÃO"),
        ("star", "CLIENTES\nSATISFEITOS"),
    ]
    f_ben = F(9, True)
    b_s = 42
    b_gap = 28
    b_total = 5 * b_s + 4 * b_gap
    # Actually space by equal columns across width
    col_w = (W - 80) // 5
    by_icons = panel_bot + 28
    for i, (kind, label) in enumerate(benefits):
        cx = 40 + i * col_w + col_w // 2
        ic = benefit_icon(kind, b_s)
        layer.alpha_composite(ic, (cx - b_s // 2, by_icons))
        for li, line in enumerate(label.split("\n")):
            lw, _ = ts(draw, line, f_ben)
            draw.text((cx - lw // 2, by_icons + b_s + 6 + li * 12), line, font=f_ben, fill=WHITE)

    # Bottom strip
    strip_y = H - 78
    draw.line([(40, strip_y - 10), (W - 40, strip_y - 10)], fill=GOLD, width=1)
    layer.alpha_composite(gold_shield(28), (40, strip_y))
    f_foot = F(11, True)
    slogan = "PROTEGER HOJE É GARANTIR UM AMANHÃ TRANQUILO PARA VOCÊ, SUA FAMÍLIA E SEU PATRIMÔNIO."
    for i, line in enumerate(wrap_text(draw, slogan, f_foot, 620)):
        draw.text((76, strip_y + 2 + i * 14), line, font=f_foot, fill=WHITE)

    # TopSpeed again on right
    ts2 = load_topspeed(140)
    # recolor for dark: make black -> white
    arr = np.array(ts2)
    ink = arr[:, :, 3] > 20
    # keep red accents, whiten dark
    dark = ink & (arr[:, :, 0] < 80) & (arr[:, :, 1] < 80) & (arr[:, :, 2] < 80)
    arr[dark, 0] = 255
    arr[dark, 1] = 255
    arr[dark, 2] = 255
    ts2 = Image.fromarray(arr, "RGBA")
    layer.alpha_composite(ts2, (W - 40 - ts2.width, strip_y - 4))
    f_po = F(10, True)
    po = "PARCEIRA OFICIAL"
    pw, _ = ts(draw, po, f_po)
    draw.text((W - 40 - ts2.width + (ts2.width - pw) // 2, strip_y - 18), po, font=f_po, fill=GOLD_LIGHT)

    out = Image.alpha_composite(base.convert("RGBA"), layer)
    return out.convert("RGB")


def export(img: Image.Image) -> Path:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    out = OUTPUT / "CTK_Arte_WhatsApp_1080x1350.png"
    meta = PngImagePlugin.PngInfo()
    meta.add_text("Title", "CTK Corretora de Seguros — Cotação Gratuita")
    meta.add_text("Description", f"QR={QR_URL}; WhatsApp={WA_URL}")
    meta.add_text("Software", "qrcode+Pillow CTK generator v2")
    kwargs = dict(dpi=(DPI, DPI), optimize=False, compress_level=1, pnginfo=meta)
    img.save(out, "PNG", **kwargs)
    img.save("/opt/cursor/artifacts/CTK_Arte_WhatsApp_1080x1350.png", "PNG", **kwargs)

    # QR isolado
    make_qr(400).save(OUTPUT / "qrcode_segfy_real.png", "PNG", dpi=(DPI, DPI))

    (OUTPUT / "CTK_Arte_WhatsApp_clicavel.html").write_text(
        f"""<!DOCTYPE html>
<html lang="pt-BR"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>CTK — Cotação</title>
<style>
body{{margin:0;background:#061230;display:flex;justify-content:center;padding:12px}}
.wrap{{position:relative;width:min(1080px,100%)}}
img{{width:100%;display:block;border-radius:6px}}
a.qr{{position:absolute;left:68%;right:5%;top:52%;height:14%}}
a.wa{{position:absolute;left:62%;right:5%;top:68%;height:6%;border-radius:999px}}
</style></head><body>
<div class="wrap">
<img src="CTK_Arte_WhatsApp_1080x1350.png" alt="CTK"/>
<a class="qr" href="{QR_URL}" title="Cotação Segfy"></a>
<a class="wa" href="{WA_URL}" title="WhatsApp {WA_PHONE}"></a>
</div></body></html>
""",
        encoding="utf-8",
    )
    return out


def main():
    # fix load_hero typo guard
    img = compose()
    path = export(img)
    print(f"OK {path} {img.size} bytes={path.stat().st_size}")


if __name__ == "__main__":
    main()
