# Laboratório 04 — as quatro buscas, medidas

Formulação usada: `../lab3/meu_problema.py:MEU_PROBLEMA` — subproblema
"Consultas" (lab-03) adaptado ao domínio de Gestão de Ordens de Serviço de
Manutenção. Estado: fatos já levantados sobre a OS. Ação: consultar uma
fonte. Objetivo: reunir os quatro fatos que a seção 1 (Sensors) do
agent-spec.md exige antes de classificar o risco de falha.

## A tabela

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| largura | 20.0 | 1 | 6 | 25 | 2 | 0.0001 |
| custo_uniforme | 8.0 | 3 | 39 | 55 | 4 | 0.0001 |
| profundidade_limitada(limite=32) | 8.5 | 4 | 5 | 10 | 4 | 0.0 |
| aprofundamento_iterativo(limite=32) | 20.0 | 1 | 7 | 5 | 1 | 0.0 |

## Conclusão escrita

**Sim — o custo uniforme achou caminho mais barato que a largura** (8.0
contra 20.0, uma redução de 60%), e a profundidade limitada também achou um
caminho mais barato (8.5), embora não o ótimo.

