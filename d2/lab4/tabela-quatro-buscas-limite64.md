# Laboratório 04 — as quatro buscas, medidas (LIMITE = 64)

Foi mudado a constante `LIMITE` do `esqueleto.py`, de 32 para 64, nas duas
buscas com limite (profundidade limitada e aprofundamento iterativo).

## A tabela

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| largura | 20.0 | 1 | 6 | 25 | 2 | 0.0005 |
| custo_uniforme | 8.0 | 3 | 39 | 55 | 4 | 0.0001 |
| profundidade_limitada(limite=64) | 8.5 | 4 | 5 | 10 | 4 | 0.0 |
| aprofundamento_iterativo(limite=64) | 20.0 | 1 | 7 | 5 | 1 | 0.0 |

## Conclusão escrita
Como a profundidade da solução é muito menor que os limites 32 e 64, aumentar o limite não altera o resultado. Por isso, os custos e os números de nós permanecem iguais.

