# offvoos-historico

Histórico **completo e sem prazo** dos voos offshore publicados em [offvoos.com.br](https://offvoos.com.br),
todas as bases e unidades, desde 21/09/2026. O site só mostra cerca de 1 semana; este repositório guarda o resto.

- `dados/arquivo/AAAA-MM.csv` — **arquivo permanente**, um por mês (nunca é apagado; mês fechado não muda mais)
- `dados/voos_60d.csv` — tabela dos últimos 60 dias (mais recente primeiro), lida pelo Excel (Power Query) e pelo app
- `dados/historico.json` — os mesmos 60 dias, um registro por dia (área de trabalho do vigia)
- `vigia.py` — o coletor; roda às 07:00 e às 19:00 (Brasília) pelo GitHub Actions

Colunas dos CSV: `data, numero, programado, decolagem, status, origem, destinos, aeronave, empresa, id`.
`programado` é o horário que o site mostra como esperado; `decolagem` é a hora real (vazia se não decolou).
Voo transferido aparece em cada dia em que foi programado, com o mesmo `numero`.

Os dados são os mesmos que o offvoos exibe publicamente. Não há dado pessoal.
