# Relatório de desempenho da linha de base — AMS

**Projeto:** AMS — Assistente de Manutenção Segura · **Data:** 17/11/2026

## 1. A métrica primária

Acerto da decisão: fração de casos em que a ação decidida pelo agente
(`decidir()` em `src/ams/baseline.py`) é igual à ação corretiva
rotulada no conjunto (`acao_correta`), sobre o total de casos —
`acertos / total`.

## 2. O valor

```
Métrica primária: acerto da decisão (casos com decisão igual à rotulada, sobre o total)
Valor: 25/30 = 0.8333
```

## 3. O conjunto

Conjunto de reserva do D2-06 (`d2/lab6/casos-de-reserva.csv`), conforme
autorizado pelo enunciado (`d2/lab6/COMO-USAR-A-RESERVA.pdf`): 30 casos
de manutenção industrial com ação corretiva rotulada caso a caso,
processados em ordem cronológica (a ordem importa porque o estado
interno do agente — `EstadoDaFrota` — se acumula caso a caso).

Declaração: o AI4I 2020, dataset de referência do projeto AMS, informa
apenas se a máquina falhou ou não, sem indicar qual ação corretiva
deveria ser aplicada — por isso não permite medir esta métrica sem uma
etapa adicional de classificação manual. A reserva do D2-06 supre essa
lacuna.

Distribuição dos rótulos: `{'seguir_operando': 16, 'parar_para_manutencao': 7, 'inspecionar_antes_de_operar': 7}`.

## 4. Onde o agente erra

```
Onde erra (o rótulo que o agente não deu):
  caso C07: decidiu seguir_operando, correto era inspecionar_antes_de_operar
  caso C08: decidiu seguir_operando, correto era inspecionar_antes_de_operar
  caso C10: decidiu inspecionar_antes_de_operar, correto era seguir_operando
  caso C11: decidiu parar_para_manutencao, correto era inspecionar_antes_de_operar
  caso C22: decidiu parar_para_manutencao, correto era inspecionar_antes_de_operar
```

**O padrão dos erros.** Os cinco erros se dividem em dois tipos opostos,
não um só. C07 e C08 são falsos negativos: a máquina (TORNO) falhou
depois (`falhou_depois=1`), mas os sensores daquele instante estavam
dentro da faixa normal (temperatura 60–61 °C, vibração 3,0–3,1 mm/s,
ambos abaixo dos limiares de 78 °C e 7,0 mm/s) e, no momento de C07, o
histórico da família ainda não tinha nenhuma falha registrada dentro da
janela de 7 dias — o estado não tinha matéria-prima para desconfiar. Já
C11 e C22 são falsos positivos pelo lado oposto: a vibração cruzou o
limiar por pouco (7,4 e 7,1 mm/s contra o limite de 7,0), disparando a
condição reativa de `parar_para_manutencao`, quando o rótulo correto era
a ação intermediária (`inspecionar_antes_de_operar`) — nenhuma das duas
máquinas de fato falhou depois. C10 é um terceiro padrão: por ser do
mesmo tipo (TORNO) e vir logo depois de C07/C08, a família ainda carrega
2 falhas dentro da janela quando C10 é processado, e a condição de
estado dispara `inspecionar_antes_de_operar` para uma máquina que, desta
vez, estava de fato bem.

**A hipótese.** O agente erra nos dois sentidos pelo mesmo motivo: ele
só enxerga dois tipos de evidência — o limiar fixo da leitura instantânea
e a contagem de falhas por *família* de máquina, não por máquina
individual. Isso produz (a) cegueira a falhas intermitentes que não
elevam a leitura no instante da OS (C07/C08), (b) uma fronteira rígida
no limiar contínuo de vibração que trata 7,4 e 6,9 mm/s como
categoricamente diferentes quando a diferença real é pequena (C11/C22),
e (c) contaminação do histórico: o estado não distingue "esta máquina
específica já falhou" de "uma máquina qualquer desta família falhou" —
por isso o alerta de C07/C08 vaza para C10, uma máquina diferente da
mesma família.

## 5. A tabela comparativa de busca (item 4 da N2)

Formulação usada: `d2/lab3/meu_problema.py:MEU_PROBLEMA` — subproblema
"Consultas" (lab-03), domínio de Gestão de Ordens de Serviço de
Manutenção. Estado: fatos já levantados sobre a OS. Ação: consultar uma
fonte. Objetivo: reunir os quatro fatos que a seção 1 (Sensors) do
`agent-spec.md` exige antes de classificar o risco de falha.

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

**A pergunta do item 4.** O A* com a heurística admissível manteve o
custo ótimo (8.0 — igual ao custo uniforme, e menor que os 20.0 da
largura) e expandiu **25 nós contra 39** do custo uniforme, uma economia
de 36% sem abrir mão da otimalidade. Isso diz que o espaço de estados
deste subproblema é pequeno e pouco ramificado (a heurística admissível
— menor latência entre as fontes que ainda faltam — já corta boa parte
da busca cega), mas que mesmo assim a informação da heurística vale a
pena: ela guia a expansão para o lado certo da árvore em vez de
explorá-la em largura. A heurística inadmissível chega a uma solução
mais rápido (2 nós) mas mais cara (20.0, a mesma da busca cega sem
informação) — ela superestima o custo de cada consulta faltante e acaba
escolhendo cedo demais o atendimento humano (fonte mais lenta, mas que
resolve tudo de uma vez), perdendo a combinação mais barata de fontes
específicas.

**Ressalva de contagem.** A profundidade limitada expande só 5 nós e
gera 10, mas esse número depende inteiramente do limite escolhido
(32) — um limite menor faria a busca falhar sem achar solução alguma, e
um limite maior exploraria fundo demais sem necessidade; o número
"bonito" de nós aqui é consequência do parâmetro, não da eficiência do
algoritmo.
