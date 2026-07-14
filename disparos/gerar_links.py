#!/usr/bin/env python3
"""Gera links wa.me individuais a partir de uma lista CSV de contatos."""

from __future__ import annotations

import csv
import re
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTATOS = ROOT / "contatos.csv"
EXEMPLO = ROOT / "contatos.exemplo.csv"
MENSAGEM = ROOT / "mensagem_padrao.txt"
SAIDA = ROOT / "links_gerados.csv"


def apenas_digitos(telefone: str) -> str:
    return re.sub(r"\D+", "", telefone or "")


def carregar_mensagem() -> str:
    return MENSAGEM.read_text(encoding="utf-8").strip()


def carregar_contatos() -> list[dict[str, str]]:
    fonte = CONTATOS if CONTATOS.exists() else EXEMPLO
    with fonte.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader if (row.get("telefone") or "").strip()]


def main() -> None:
    template = carregar_mensagem()
    contatos = carregar_contatos()
    if not contatos:
        raise SystemExit("Nenhum contato encontrado. Preencha disparos/contatos.csv")

    with SAIDA.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "telefone", "link_whatsapp"])
        writer.writeheader()
        for row in contatos:
            nome = (row.get("nome") or "").strip() or "cliente"
            telefone = apenas_digitos(row.get("telefone", ""))
            if not telefone:
                continue
            texto = template.replace("{nome}", nome)
            link = f"https://wa.me/{telefone}?text={urllib.parse.quote(texto)}"
            writer.writerow(
                {"nome": nome, "telefone": telefone, "link_whatsapp": link}
            )

    fonte = CONTATOS if CONTATOS.exists() else EXEMPLO
    print(f"Fonte: {fonte.name}")
    print(f"Gerado: {SAIDA} ({len(contatos)} contatos)")


if __name__ == "__main__":
    main()
