# Análise — AMS (Gestão de Ordens de Serviço de Manutenção)

## O que torna o problema difícil

A observabilidade parcial não é rótulo aqui: a linha de base perdeu os
casos **C07 e C08** porque a falha intermitente não aparece na leitura
do instante — temperatura (60–61 °C) e vibração (3,0–3,1 mm/s) estavam
dentro da faixa normal exatamente nos casos em que a máquina (TORNO)
falhou logo depois, e como nenhuma falha da família ainda estava
registrada dentro da janela de 7 dias, o estado interno também não tinha
de onde desconfiar. A informação que decide — o desgaste acumulado que
antecede a falha — simplesmente não está em nenhum dos dois canais que
o agente enxerga (leitura pontual, histórico por família). Em segundo
lugar, a dimensão discreto/contínuo cobra um preço direto: vibração é
uma grandeza contínua, mas a regra trata o limiar de 7,0 mm/s como uma
fronteira categórica. Isso produziu os erros opostos **C11 e C22**
(7,4 e 7,1 mm/s — só 0,1–0,4 mm/s acima do limite), classificados como
`parar_para_manutencao` quando o rótulo correto era a ação intermediária
`inspecionar_antes_de_operar`: a régua binária não tem onde colocar "um
pouco alto, mas não crítico". Por fim, o estado por família (não por
máquina individual) é a dimensão "número de agentes"/granularidade do
modelo que vaza informação entre casos: **C10** é uma máquina TORNO
diferente, processada logo depois de C07/C08, e herda o alerta de
`inspecionar_antes_de_operar` por pertencer à mesma família que acabou
de falhar duas vezes — mesmo estando, desta vez, bem. A tabela de busca
reforça o segundo ponto por outro ângulo: o espaço de estados do
subproblema de consultas é pequeno (A* admissível expandiu só 25 nós
contra 39 da busca cega), o que mostra que o difícil deste domínio não
está em *buscar os fatos* — está em *decidir* com os fatos que já tem,
quando esses fatos vêm de uma leitura pontual e discretizada.

## Que tipo de agente o problema realmente exige

Um reativo simples não basta: ele decidiria C07, C08 e C10 exatamente
como a linha de base decidiu (leitura pontual contra limiar), porque
não tem onde guardar o que já viu. É preciso estado interno — e a
granularidade dele é parte do problema, não um detalhe de implementação:
o estado atual (`EstadoDaFrota`, contagem de falhas por família dentro
de uma janela de 7 dias) já é obrigatório pela observabilidade parcial
(seção 2 do `agent-spec.md`), mas os erros C10/C11/C22 mostram que
*quanto* histórico guardar e *em que granularidade* (família inteira vs.
máquina individual) são decisões de projeto com consequência medida, não
neutras. O agente não precisa de busca nem de planejamento de
trajetória — a formulação por busca (seção 7) resolve um subproblema
auxiliar (reunir fatos), não a decisão de risco em si, e o domínio é
episódico (seção 2): cada OS é avaliada contra o desfecho daquela
máquina, não contra uma sequência de decisões futuras. O que a
classificação de "baseado em utilidade" (seção 3 do agent-spec) exige
aqui, e que a linha de base dispensa por ser determinística em suas
regras: avaliar a *probabilidade* de falha a partir de sinais parciais e
pesar o custo assimétrico (falha não detectada é pior que alarme falso)
em vez de aplicar um limiar único que trata todo excesso acima da linha
como a mesma categoria de risco.

## O que isto muda no projeto (fecho)

A D10 precisa de duas coisas que a linha de base não tem: (1) um sinal
contínuo de risco (uma probabilidade ou um escore), não um limiar
binário — para que vibração 7,1 mm/s e vibração 9,0 mm/s não caiam na
mesma ação; e (2) estado por máquina individual, não por família, para
não vazar o alerta de uma máquina para outra que só compartilha o tipo.
Nenhuma das duas exige um sensor novo — é reorganização do que já se
coleta. Dito isso, a linha de base é competitiva onde o problema é
realmente binário: os casos de vibração ou temperatura muito acima do
limiar (C02, C03, C13, C15, C21, C27, C28 — todos os `parar_para_
manutencao` verdadeiros) foram todos acertados, porque ali a leitura
pontual já contém toda a informação que decide. Isso não é fracasso da
linha de base — é a prova de que o valor do modelo em D10 está
concentrado exatamente na faixa intermediária de risco, não no
problema inteiro.
