# WhatsApp Disparos — CTK Seguros

Repositório dedicado a campanhas de WhatsApp da **CTK Corretora de Seguros**.

Não faz parte do case GCP/Yelp (`TesteGCP`). Aqui ficam apenas a arte de disparo e as ferramentas de campanha.

## O que tem neste repo

| Pasta / arquivo | Uso |
|-----------------|-----|
| `gerar_arte.py` | Gera a arte final 1080×1350 (PNG @ 300 DPI) com QR Segfy real |
| `assets/` | Logos e foto da corretora (substituíveis pelos originais) |
| `output/` | PNG final + HTML clicável |
| `disparos/` | Lista de contatos, mensagem padrão e gerador de links `wa.me` |

## Arte pronta

Arquivo principal: `output/CTK_Arte_WhatsApp_1080x1350.png`

| Spec | Valor |
|------|-------|
| Formato | PNG |
| Dimensões | **1080 × 1350 px** |
| DPI | **300** |
| QR | Segfy — cotação gratuita |
| WhatsApp | `+55 11 94194-7162` → `https://wa.me/5511941947162` |

### Links da campanha

| Elemento | Destino |
|----------|---------|
| QR Code | [Cotação Segfy](https://gestao.segfy.com/Publico/Segurados/Orcamentos/SolicitarCotacao?e=bq3pqK5O9i3fuSp4u7Wy9w%3D%3D) |
| Botão WhatsApp | [wa.me/5511941947162](https://wa.me/5511941947162) |

## Regenerar a arte

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 gerar_arte.py
```

## Preparar um disparo (lista de contatos)

1. Copie a planilha modelo:

```bash
cp disparos/contatos.exemplo.csv disparos/contatos.csv
```

2. Preencha `nome` e `telefone` (apenas dígitos com DDI, ex.: `5511999999999`).

3. Ajuste o texto em `disparos/mensagem_padrao.txt` se quiser.

4. Gere os links individuais:

```bash
python3 disparos/gerar_links.py
```

Isso cria `disparos/links_gerados.csv` com uma URL `wa.me` por contato (mensagem já preenchida). Abra no celular ou no WhatsApp Web para enviar um a um, ou importe a base no WhatsApp Business.

> Este repositório **não** usa a WhatsApp Cloud API / API oficial. O fluxo é arte + links prontos para disparo manual ou via WhatsApp Business.

## Como publicar este repositório no GitHub

O token do agente Cloud só tem acesso ao repositório antigo (`TesteGCP`) e **não consegue criar** um repositório novo na conta.

Faça assim (1 minuto):

1. No GitHub, logado como **KCANTAGALLI**, crie um repositório **vazio** chamado `whatsapp-disparos` (sem README).
2. Responda neste chat com a URL, por exemplo: `https://github.com/KCANTAGALLI/whatsapp-disparos`
3. O agente faz o push do código completo.

Ou, localmente, com o ZIP deste projeto:

```bash
unzip whatsapp-disparos.zip
cd whatsapp-disparos
git init
git add .
git commit -m "Initial commit: arte e disparos WhatsApp CTK"
git branch -M main
git remote add origin https://github.com/KCANTAGALLI/whatsapp-disparos.git
git push -u origin main
```

## Assets (trocar pelos originais da marca)

- `assets/ctk-crest-logo.png` — brasão CTK
- `assets/corretora-hero.png` — foto da corretora
- `assets/topspeed-logo.png` — parceira TopSpeed
