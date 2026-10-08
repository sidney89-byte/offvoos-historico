# Orientações: como as IAs devem trabalhar neste repositório

Este repositório usa um conjunto de skills (em `.claude/skills/`) para que a IA trabalhe como
um desenvolvedor sênior: com lógica, e não na força bruta.

## Por que (o que aprendemos)

Em outubro/2026, num projeto do mesmo dono, a IA passou seis rodadas de conserto tentando fazer um
painel adivinhar a causa de qualquer falha lendo o TEXTO da mensagem de erro. Cada revisão achava
um caso novo; cada conserto era "mais uma regex". O problema só fechou quando a pergunta mudou para
"que decisão a pessoa toma?" e a resposta foi lida de um dado confiável gravado na origem.

Lições, nas palavras do dono:
- *"As IAs muitas vezes tentam resolver os problemas de código na força bruta ao invés de buscar
  uma lógica."*
- *"No primeiro erro, a lógica é tentar encontrar um padrão logo. É assim que um ser humano faria."*
- *"Códigos mais inteligentes são mais curtos e mais estruturados. Mais à prova de futuro e mudanças."*
- As regras de negócio vêm da FONTE oficial (norma, lei, documentação), não da cabeça da IA.

Medimos depois: com critério fechado e revisor independente, nenhum ciclo passou de duas rodadas.
Mas a skill sozinha não mudou o hábito do executor — o que funcionou foi tornar o erro difícil de
escrever (tabela com referência por linha, plano antes do código, teste que reprova).

## As skills

| Skill | Quando usar |
|---|---|
| `reformular-antes-de-insistir` | ao escrever código que decide algo; no primeiro erro; antes de abrir ciclo executor → revisor |
| `writing-plans` | antes de mexer no código numa tarefa de vários passos |
| `systematic-debugging` | em todo defeito: causa raiz antes de conserto; 3 tentativas falhas = questionar o desenho |
| `verification-before-completion` | antes de dizer "pronto": rodar a verificação e mostrar a saída |
| `test-driven-development` | ao implementar recurso ou conserto: teste primeiro |
| `receiving-code-review` | ao receber revisão: conferir tecnicamente, não concordar por educação |

As cinco últimas vêm do projeto obra/superpowers v6.4.2 (MIT, `LICENSE-superpowers`), copiadas sem
alteração. A primeira é nossa.

## Regras curtas

1. **Texto livre não decide ação.** Decide o dado da origem (código, campo, categoria gravada).
2. **Caso desconhecido cai num padrão seguro** escrito antes; texto só sobe alerta, nunca baixa.
3. **No primeiro defeito, procure o padrão** e conserte a causa em todos os lugares.
4. **Uma regra, um lugar; tabela fechada no lugar de cadeia de if.**
5. **Regra de domínio vem da fonte oficial**, com a referência escrita no código; sem fonte = pergunta.
6. **Executor → revisor só com critério fechado** (entrada → resultado, fora do escopo, padrão seguro);
   o revisor testa com casos próprios.
7. **Plano antes do código; verificação antes de dizer pronto.**

Para atualizar as skills do Superpowers: copiar de novo de https://github.com/obra/superpowers e
registrar a versão aqui.
