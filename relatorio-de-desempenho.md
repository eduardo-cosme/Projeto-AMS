# Relatório de desempenho da linha de base — AMS

**Projeto:** AMS — Assistente de Manutenção Segura · **Data:** 17/11/2026

## 1. A métrica primária

A métrica principal é o percentual de acerto das decisões do agente. Ela mede quantas vezes a ação corretiva escolhida pelo agente, por meio do método decidir() em src/ams/baseline.py, corresponde à ação correta definida no conjunto de dados (acao_correta).

O cálculo é realizado dividindo o número de decisões corretas pelo total de casos avaliados:
Acerto = acertos / total de casos

## 2. O valor

A métrica primária foi calculada comparando a decisão tomada pelo agente com a ação corretiva esperada para cada caso.
Resultado: o agente acertou 25 dos 30 casos avaliados, alcançando uma taxa de acerto de 83,33%.

Métrica primária: acerto da decisão
Acertos: 25
Total de casos: 30
Valor: 25/30 = 0,8333 (83,33%)

## 3. O conjunto

A avaliação foi realizada utilizando o conjunto de reserva do D2-06 (d2/lab6/casos-de-reserva.csv), conforme autorizado pelo enunciado (d2/lab6/COMO-USAR-A-RESERVA.pdf).

O conjunto contém 30 casos de manutenção industrial, cada um com uma ação corretiva esperada (acao_correta). Os casos foram processados em ordem cronológica, pois o estado interno do agente (EstadoDaFrota) é atualizado a cada caso e influencia as decisões seguintes.

O dataset AI4I 2020, foi utilizado como referência no projeto AMS, informando apenas se houve falha na máquina, mas não especifica qual ação corretiva deve ser tomada. Por isso, não permite calcular diretamente a métrica de acerto da decisão. O conjunto de reserva do D2-06 supre essa necessidade, fornecendo ações corretivas rotuladas para cada caso.

Distribuição das ações corretivas:
  -seguir_operando: 16 casos
  -parar_para_manutencao: 7 casos
  -inspecionar_antes_de_operar: 7 casos

## 4. Onde o agente erra

Onde erra (o rótulo que o agente não deu):
  caso C07: decidiu seguir_operando, correto era inspecionar_antes_de_operar
  caso C08: decidiu seguir_operando, correto era inspecionar_antes_de_operar
  caso C10: decidiu inspecionar_antes_de_operar, correto era seguir_operando
  caso C11: decidiu parar_para_manutencao, correto era inspecionar_antes_de_operar
  caso C22: decidiu parar_para_manutencao, correto era inspecionar_antes_de_operar

**O padrão dos erros.**
Os cinco erros identificados apresentam dois tipos principais de falha e um terceiro caso relacionado ao uso do histórico.

C07 e C08 são falsos negativos: as máquinas falharam posteriormente (falhou_depois=1), mas as leituras dos sensores estavam dentro dos limites considerados normais. Além disso, no momento de C07, ainda não havia falhas recentes registradas para aquela família na janela de sete dias. Assim, o agente não tinha informações suficientes no estado interno para identificar o risco.

C11 e C22 são falsos positivos: a vibração ultrapassou o limite de 7,0 mm/s por uma pequena margem (7,4 e 7,1 mm/s), levando o agente a recomendar parar_para_manutencao. Porém, a ação correta era inspecionar_antes_de_operar, pois as máquinas não falharam posteriormente.

Já C10 representa um erro causado pelo histórico compartilhado da família. Como a máquina era do tipo TORNO e foi avaliada após C07 e C08, o estado ainda registrava duas falhas recentes, levando o agente a recomendar inspecionar_antes_de_operar, embora essa máquina não tenha apresentado falha.

Esses resultados mostram que o agente precisa identificar falhas que não aparecem nas leituras instantâneas e, ao mesmo tempo, evitar que limites muito sensíveis ou históricos de outras máquinas provoquem alertas desnecessários.

**A hipótese.**
O agente apresenta erros nos dois sentidos porque suas decisões se baseiam em duas informações limitadas: os limites fixos das leituras dos sensores e o histórico de falhas agrupado por família de máquinas.

Essa abordagem pode deixar de identificar falhas que não aparecem nas leituras do momento, como nos casos C07 e C08. Também pode gerar decisões excessivamente rígidas, tratando valores de vibração muito próximos, como 7,4 e 6,9 mm/s, de forma diferente apenas por estarem em lados opostos do limite estabelecido.

Além disso, o histórico compartilhado por família não permite distinguir se a falha ocorreu na própria máquina ou em outra do mesmo tipo. Isso pode fazer com que alertas gerados por C07 e C08 influenciem indevidamente a decisão de C10.

Portanto, a hipótese é que a combinação de limites fixos e histórico compartilhado por família reduz a precisão das decisões, causando tanto falhas não identificadas quanto alertas desnecessários.

## 5. A tabela comparativa de busca (item 4 da N2)

Formulação usada: `d2/lab3/meu_problema.py:MEU_PROBLEMA`
subproblema "Consultas" (lab-03), domínio de Gestão de Ordens de Serviço de Manutenção.
Estado: fatos já levantados sobre a OS.
Ação: consultar uma fonte.
Objetivo: reunir os quatro fatos que a seção 1 (Sensors) do
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

**A pergunta do item 4.**
O algoritmo A* com heurística admissível encontrou a solução de menor custo (8,0), igual ao custo da busca de custo uniforme e inferior ao resultado da busca em largura (20,0). Além disso, expandiu apenas 25 nós, contra 39 do custo uniforme, reduzindo a exploração em aproximadamente 36%, sem perder a solução ótima.

Isso demonstra que a heurística ajuda a direcionar a busca para os caminhos mais promissores, evitando explorar tantas possibilidades desnecessárias.

Já a heurística inadmissível encontrou uma solução com apenas 2 nós expandidos, mas com custo maior (20,0). Isso aconteceu porque ela superestimou os custos das consultas restantes e priorizou o atendimento humano, que resolve todas as informações de uma vez, mas é mais caro do que combinar fontes específicas.

Portanto, o A* com heurística admissível apresentou o melhor equilíbrio entre eficiência na busca e qualidade da solução, encontrando o menor custo com menos nós explorados.

**Ressalva de contagem.**
A busca em profundidade limitada expandiu apenas 5 nós e gerou 10, mas esse resultado depende diretamente do limite de profundidade escolhido (32).
Se o limite fosse menor, a busca poderia não encontrar uma solução. Se fosse maior, poderia explorar caminhos desnecessários.
Portanto, a quantidade reduzida de nós não significa necessariamente maior eficiência, pois é resultado do parâmetro configurado para a busca.
