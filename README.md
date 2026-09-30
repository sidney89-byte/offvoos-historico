# offvoos-historico

Histórico dos **últimos 60 dias** de voos offshore publicados em [offvoos.com.br](https://offvoos.com.br),
todas as bases e unidades. O site só mostra cerca de 1 semana; este repositório guarda o resto.

- `dados/voos_60d.csv` — tabela dos últimos 60 dias (uma linha por voo, mais recente primeiro)
- `dados/historico.json` — os mesmos dados, um registro por dia
- `vigia.py` — o coletor; roda às 07:00 e às 19:00 (Brasília) pelo GitHub Actions

Colunas do CSV: `data, numero, programado, decolagem, status, origem, destinos, aeronave, empresa, id`.
`programado` é o horário que o site mostra como esperado; `decolagem` é a hora real (vazia se não decolou).

Os dados são os mesmos que o offvoos exibe publicamente. Não há dado pessoal.
