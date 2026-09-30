#!/usr/bin/env python3
"""Vigia de voos offshore: guarda os últimos 60 dias do offvoos.com.br (todas as unidades).

O offvoos só guarda ~1 semana — para data mais antiga ele devolve os voos de outro dia.
Este vigia roda 2x por dia no GitHub Actions, busca os dias que o site ainda tem e acumula:
  dados/historico.json  — um registro por dia (fonte da verdade)
  dados/voos_60d.csv    — tabela plana dos últimos 60 dias, lida pelo Power Query do Excel
Só usa a biblioteca padrão do Python.
"""
import csv
import datetime as dt
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = "https://offvoos.com.br"
UA = "Mozilla/5.0 (compatible; offvoos-historico/1.0; +https://github.com/sidney89-byte/offvoos-historico)"
DADOS = Path(__file__).resolve().parent / "dados"
HISTORICO = DADOS / "historico.json"
CSV = DADOS / "voos_60d.csv"
DIAS_NO_SITE = 8      # o site só devolve ~1 semana; mais antigo que isso não adianta pedir
DIAS_GUARDAR = 60
BRT = ZoneInfo("America/Sao_Paulo")
COLUNAS = ["data", "numero", "programado", "decolagem", "status", "origem", "destinos",
           "aeronave", "empresa", "id"]


def baixar(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def texto(fragmento):
    return html.unescape(re.sub(r"<[^>]+>", "", fragmento)).strip()


def voos_do_dia(dia):
    pagina = baixar(f"{BASE}/voos?d={dia.isoformat()}")
    if 'class="flight-row"' not in pagina and "flight" not in pagina:
        raise RuntimeError("página sem a tabela de voos (bloqueio do Cloudflare?)")
    voos = []
    for m in re.finditer(r'<tr class="flight-row"(.*?)</tr>', pagina, re.S):
        tr = m.group(1)

        def um(padrao):
            x = re.search(padrao, tr, re.S)
            return texto(x.group(1)) if x else ""
        # data verdadeira da linha: para data antiga o site devolve voos de outro dia
        iso = re.search(r'data-scheduled-iso="(\d{4}-\d\d-\d\d)', tr)
        if not iso or iso.group(1) != dia.isoformat():
            continue
        voos.append({
            "id": re.search(r'data-flight-id="([^"]+)"', tr).group(1),
            "numero": um(r'class="col-flight">#?(.*?)</td>'),
            "data": dia.isoformat(),
            "programado": um(r'class="time-main">(.*?)</div>'),
            "decolagem": um(r'class="time-actual">\s*✓?\s*(.*?)</div>'),
            "status": um(r'class="status-pill[^"]*">(.*?)</span>'),
            "origem": um(r'class="origin"[^>]*>(.*?)</span>'),
            "destinos": " / ".join(texto(c) for c in re.findall(r'<span class="code">(.*?)</span>', tr, re.S)),
            "aeronave": (um(r'class="reg">(.*?)</div>') + " " + um(r'class="model">(.*?)</div>')).strip(),
            "empresa": um(r'class="company">(.*?)</div>'),
        })
    return voos


def main():
    hist = json.loads(HISTORICO.read_text()) if HISTORICO.exists() else {}
    hoje = dt.datetime.now(BRT).date()
    agora = dt.datetime.now(BRT).isoformat(timespec="minutes")
    falhas = 0
    for i in range(-1, DIAS_NO_SITE + 1):  # amanhã até 8 dias atrás
        dia = hoje - dt.timedelta(days=i)
        chave = dia.isoformat()
        if chave in hist and i > 2 and hist[chave]["voos"]:
            continue  # dia fechado e já guardado
        try:
            voos = voos_do_dia(dia)
        except Exception as e:
            falhas += 1
            print(f"{chave}: falhou ({e})")
            continue
        if not voos and hist.get(chave, {}).get("voos"):
            print(f"{chave}: site sem dados; mantido o histórico")
            continue
        hist[chave] = {"coletado_em": agora, "voos": voos}
        print(f"{chave}: {len(voos)} voos")
        time.sleep(1)
    if falhas >= DIAS_NO_SITE:
        sys.exit("todas as buscas falharam — o site pode estar bloqueando o GitHub")

    limite = (hoje - dt.timedelta(days=DIAS_GUARDAR)).isoformat()
    hist = {k: v for k, v in sorted(hist.items()) if k >= limite}
    DADOS.mkdir(exist_ok=True)
    HISTORICO.write_text(json.dumps(hist, ensure_ascii=False, indent=1) + "\n")

    linhas = [v for reg in hist.values() for v in reg["voos"]]
    linhas.sort(key=lambda v: (v["data"], v["programado"], v["numero"]), reverse=True)
    with CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS, extrasaction="ignore")
        w.writeheader()
        w.writerows(linhas)
    print(f"histórico: {len(hist)} dias ({min(hist)} a {max(hist)}), {len(linhas)} voos")


if __name__ == "__main__":
    main()
