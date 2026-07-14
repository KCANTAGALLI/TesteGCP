# Arte Final CTK — WhatsApp / Instagram / Facebook / Impressão

## Arquivo principal

`output/CTK_Arte_WhatsApp_1080x1350.png`

- Formato: PNG
- Dimensões: **1080 × 1350 px**
- DPI: **300**
- QR Code **real** (biblioteca `qrcode`) → Segfy
- Botão WhatsApp com **📱 +55 11 94194-7162**

## Links embutidos

| Elemento | Destino |
|----------|---------|
| QR Code | https://gestao.segfy.com/Publico/Segurados/Orcamentos/SolicitarCotacao?e=bq3pqK5O9i3fuSp4u7Wy9w%3D%3D |
| Botão WhatsApp (HTML auxiliar) | https://wa.me/5511941947162 |

> Em disparo de imagem no WhatsApp Business, o QR abre a cotação ao escanear. O HTML `CTK_Arte_WhatsApp_clicavel.html` adiciona áreas clicáveis para web / link na bio.

## Regenerar

```bash
pip install -r requirements.txt
python3 gerar_arte.py
```

## Assets

- `assets/ctk-logo.png` — logo CTK
- `assets/corretora-portrait.png` — foto da corretora (substitua pelo arquivo original para fidelidade total)
