# Laboratório 05 — a estrela e a comparação

Formulação usada: `../lab3/meu_problema.py:MEU_PROBLEMA` — a mesma do
lab-04 (subproblema "Consultas", domínio de Gestão de Ordens de Serviço de
Manutenção). Heurísticas: as do catálogo (`comum/problemas/consultas.py`),
já prontas e comentadas — caminho padrão.

## A tabela completa (lab-04 + lab-05)

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| largura | 20.0 | 1 | 6 | 25 | 2 | 0.0001 |
| custo_uniforme | 8.0 | 3 | 39 | 55 | 4 | 0.0001 |
| profundidade_limitada(limite=32) | 8.5 | 4 | 5 | 10 | 4 | 0.0 |
| aprofundamento_iterativo(limite=32) | 20.0 | 1 | 7 | 5 | 1 | 0.0 |
| gulosa[admissivel] | 20.0 | 1 | 2 | 5 | 1 | 0.0001 |
| a_estrela[admissivel] | 8.0 | 3 | 25 | 50 | 3 | 0.0001 |
| gulosa[inadmissivel] | 20.0 | 1 | 2 | 5 | 1 | 0.0 |
| a_estrela[inadmissivel] | 20.0 | 1 | 2 | 5 | 1 | 0.0 |

As duas heurísticas vêm de `comum/problemas/consultas.py`:

**Admissível (heuristica_admissivel)** — considera a menor latência entre as consultas que fornecem algum fato faltante. É admissível porque, enquanto houver fatos faltantes, será necessária pelo menos uma consulta útil, cujo custo não pode ser menor que essa estimativa.

**Inadmissível (heuristica_inadmissivel)** — multiplica a quantidade de fatos faltantes pela maior latência do catálogo. Superestima o custo, pois assume que cada fato exige uma consulta separada à fonte mais lenta, ignorando que uma única consulta pode fornecer vários fatos.
**Conclusão:** a admissível economiza tempo sem perder a solução ótima; a inadmissível pode ser mais rápida, mas corre o risco de encontrar uma solução pior.

## O parágrafo da dominância

**Dominância entre heurísticas:** uma heurística domina outra quando estima um custo maior, sem ultrapassar o custo real, permitindo explorar menos caminhos sem perder a garantia de encontrar a solução mais barata.

No meu exemplo, a heurística admissível expandiu 25 nós e encontrou a solução ótima (custo 8,0), reduzindo a exploração em 36% em relação à busca cega (39 nós).

Já a inadmissível expandiu apenas 2 nós, mas encontrou uma solução mais cara (20,0), pois escolheu rapidamente o caminho do “atendimento humano” sem considerar alternativas melhores.

**Conclusão:** a admissível economiza tempo sem perder a solução ótima; a inadmissível pode ser mais rápida, mas corre o risco de encontrar uma solução pior.

