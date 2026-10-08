---
name: reformular-antes-de-insistir
description: Use ao ESCREVER código que decide ação/aviso/classificação, no PRIMEIRO erro ou reprovação de um conserto (antes de remendar), e antes de abrir um ciclo executor→revisor. Sinais: "mais um caso", "faltou cobrir", "e se vier escrito assim", regex sobre mensagem, o usuário perguntando "falta muito?" ou "seja mais inteligente".
---

# Reformular antes de insistir

Origem: outubro/2026 — seis rodadas de conserto tentando um painel adivinhar a causa de qualquer
falha pelo TEXTO da mensagem de erro. Cada revisão achava um caso novo. Resolveu ao perguntar que
DECISÃO a pessoa toma (só uma: "renovo o login ou o sistema resolve sozinho?") e ler a resposta de
onde ela já existia de forma confiável. Nada disto é invenção nossa — são princípios documentados.

## Cinco princípios

1. **Mensagem é para gente; código decide por tipo/código.** Nunca ramificar pelo texto de erro,
   corpo de resposta, observação ou nome. (Microsoft, diretrizes de exceção do .NET; RFC 9457: o
   cliente decide pelo `type`, o `detail` não deve ser interpretado.)
2. **Interpretar uma vez, na entrada; depois carregar o dado pronto** ("Parse, don't validate",
   A. King). Quem fez a operação grava a categoria/código; as outras camadas leem o campo — nunca
   montar texto para outra parte reler.
3. **Padrão seguro para o desconhecido** (Saltzer & Schroeder, *fail-safe defaults*): decida pela
   prova, não pela falta dela. O caso desconhecido nunca manda fazer a coisa errada nem esconde
   nada. Texto livre só pode SUBIR um alerta, nunca baixar.
4. **Eliminar a classe, não o caso** (Google *Safe Coding*; análise de variantes). No PRIMEIRO
   defeito: de que padrão ele é? Onde mais aparece? Conserte a causa em todos os lugares e, se der,
   torne o erro impossível de escrever (função que exige a categoria, tabela fechada, teste que
   reprova). Checklist é rede, não barreira.
5. **Uma regra, um lugar; tabela no lugar de cadeia de if.** Antes de escrever, procure se a
   decisão já existe e reaproveite (ou conserte a existente). Lista fechada `valor → resultado` com
   o padrão seguro no fim. Curto é menos caminhos, não linhas espremidas.

## Regras de domínio (o "negócio")

Cada projeto tem uma FONTE das regras de domínio (norma, lei, regulamento, contrato, documentação
oficial, decisões do dono registradas). Ordem: fonte → decisões registradas → perguntar ao dono,
dizendo onde procurou. Ler a fonte não basta:
- ANTES de codar, escreva a lista `decisão → item da fonte`; decisão sem item vira pergunta, não código;
- tabela de domínio no código leva um campo `ref` por linha, e um teste exige;
- regra que contraria a fonte é motivo de reprovação.

## Antes de remendar ou de abrir executor → revisor

Responda por escrito: (a) que decisão a pessoa toma? (b) onde a resposta já existe na origem?
(c) a lista de casos cabe numa tela? (d) qual o padrão seguro? Depois combine com executor E revisor:
- critério de pronto = lista FECHADA `entrada → resultado`, com um caso "desconhecido";
- fora do escopo (vira sugestão, não reprovação);
- testes escritos por quem NÃO fez o conserto — conserto que só passa nos próprios testes tende a
  "decorar" o teste (Smith et al. 2015, *Is the cure worse than the disease?*; mesmo achado com
  LLMs em 2025).

Se o conserto é "mais uma regex/palavra/formato", o desenho está errado: volte às perguntas.
Se o mesmo tema voltar por outro caminho, pare e reformule com o usuário.

## Pronto é no uso real

Aprovado pelo revisor não é resolvido. Se o conserto atravessa camadas, percorra o caminho real uma
vez (dado fiel, camada vizinha de verdade, confira na tela e no que foi gravado) antes de dizer
pronto. Em 07/10/2026 um lote aprovado com 3.528 testes verdes não resolveu nada: a causa era o
servidor. Ver regra 8 do `ORIENTACOES-SKILLS.md`.

## O que fazer com o trabalho já feito

Guarde o útil (a categoria antiga vira detalhe em "Ver detalhes"), mas tire dele o poder de decidir
a ação. Avise o usuário em uma frase: o que mudou de abordagem, por quê, e que o ciclo agora fecha.
