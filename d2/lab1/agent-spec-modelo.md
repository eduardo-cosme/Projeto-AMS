# agent-spec.md — modelo do meu agente

<!--
Este arquivo é para preencher, não para ler e devolver. As perguntas de cada
seção estão em comentário como este: elas não aparecem na pré-visualização,
aparecem no editor. Responda ABAIXO de cada seção, apagando nada delas.

As seções que ainda não foram vistas em aula ficam de pé, com a linha
"quando se preenche" dizendo o encontro em que isso acontece. O documento
cresce a cada laboratório — o de hoje é o primeiro.

Preencha com exemplos concretos do SEU domínio. Uma linha que funcionaria
para qualquer empresa é uma linha genérica — o exemplo do seu segmento
(agente-spec-exemplo.pdf, no mesmo pacote) mostra o contraste.
-->

**Domínio:** Gestão de Ordens de Serviço de Manutenção
**Autor(a):** Eduardo Boaventura  · **Última revisão:** 10/10/2026

---

## 1. PEAS

<!-- Perguntas que guiam o preenchimento:
  - Performance: o que conta como sucesso, em uma fórmula? Sobre o quê se
    conta, sobre qual conjunto, quanto é sucesso? Qual termo impede a
    trapaça mais óbvia (fechar rápido sem resolver)?
  - Environment: onde o agente opera? O que existe lá — sistemas, pessoas,
    documentos, ruído? Cite elementos concretos.
  - Actuators: o que o agente pode FAZER? Inclua comunicar e escalar:
    informar a decisão é uma ação, e passar adiante também é.
  - Sensors: o que o agente consegue PERCEBER? Só o que ele enxerga existe
    para ele.
  Um PEAS que menciona tecnologia de solução (banco vetorial, nome de modelo)
  está descrevendo a solução — o PEAS descreve o problema.
-->
**Quando se preenche:** no Laboratório 01, hoje. Refinado na Atividade Orientada.

**Performance:**
A fração de ordens de serviço em que o nível de risco de falha previsto
(baixo/médio/alto) bate com o desfecho real da máquina
se ela de fato falhou ou não, conforme o rótulo de falha do AI4I 2020 dividida pelo
total de ordens do conjunto de avaliação.
Sucesso: o agente deverá acertar mais de 85% na identificação dos dois tipos de situação: máquinas que apresentam falhas e máquinas que não apresentam falhas.
O termo contra a trapaça óbvia: como falhas são raras no dataset (cerca de 3,4% dos 10.000 registros), um agente que sempre responde "baixo risco" já acerta ~97% das ordens sem nunca ter avaliado nada — por isso o que conta não é a taxa de acerto simples, e sim a deteção de falha real: toda máquina que falhou e foi classificada como baixo risco é contada como erro grave, mesmo que a taxa de acerto geral pareça boa.

**Environment:**
Fábrica com máquinas monitoradas por sensores de temperatura, rotação, torque e desgaste, utilizando o dataset AI4I 2020 para análise de falhas. O sistema consulta ordens de serviço e normas de segurança (NR-10, NR-12 e NR-35). O técnico de manutenção utiliza as recomendações para apoiar suas decisões, enquanto o supervisor de segurança verifica os resultados. Os principais desafios são as variações dos sensores e as descrições incompletas ou ambíguas das intervenções.

**Actuators:**
Emitir a classificação do nível de risco de falha da máquina (baixo / médio/ alto), anexada à ordem de serviço; apontar as normas regulamentares aplicáveis à intervenção (NR-10, NR-12, NR-35); sinalizar se a intervenção exige bloqueio e etiquetagem (LOTO) antes de começar; comunicar ao técnico a recomendação de forma curta, justificada e auditável — o agente não decide por ele, só informa; escalar ao supervisor de segurança os casos de risco
alto ou de classificação ambígua, para auditoria antes ou depois da intervenção.

**Sensors:**
A leitura atual dos sensores da máquina informada na ordem de serviço (temperatura, rotação, torque e desgaste de ferramenta); o texto da descrição da intervenção escrito pelo técnico; o identificador e o histórico de falhas da máquina registrado no dataset AI4I 2020; o texto
das normas regulamentares (NR-10, NR-12, NR-35) disponível para busca.
O que não está nesses canais não existe para o agente:
ele não vê a máquina, não ouve nem sente o que o técnico percebe no local, e se a descrição da intervenção omitir um detalhe relevante, esse detalhe simplesmente não entra na decisão.

---

## 2. O ambiente em sete dimensões

<!--
Perguntas que guiam o preenchimento (uma por dimensão):
  - Observabilidade: existe algo que muda a decisão e o agente não mede?
  - Número de agentes: existe alguém cujas ações mudam o seu resultado?
    Um humano que reage ao agente conta.
  - Determinismo: a mesma ação no mesmo estado dá sempre o mesmo efeito?
  - Episódico ou sequencial: a decisão de agora afeta as decisões seguintes?
  - Estático ou dinâmico: o ambiente muda enquanto o agente delibera?
  - Discreto ou contínuo: estados e ações são contáveis?
  - Conhecido ou desconhecido: o agente sabe de antemão as regras? (Trata do
    que ele SABE, não do que ele VÊ.)
  Cada classificação vem com uma frase de justificativa — a etiqueta sozinha
  não vale nada.
-->
**Quando se preenche:** no Laboratório 02, no sábado (encontro 2).

| Dimensão | Classificação | Justificativa |
|---|---|---|
| Observabilidade | Parcial | As informações dos sensores e o relato do técnico podem não mostrar detalhes importantes percebidos no local, como barulhos, cheiros ou peças soltas, que podem mudar a classificação correta do problema. |
| Determinismo | Estocástico | Mesmo com as mesmas medições dos sensores, o resultado pode ser diferente, pois as falhas podem acontecer de forma imprevisível. Além disso, a descrição do técnico pode ser interpretada de maneiras diferentes em cada caso. |
| Número de agentes | Multiagente | O técnico decide se realiza o serviço com base na recomendação, enquanto o supervisor de segurança verifica os casos de risco ou dúvida e pode mudar a decisão, ambos reagem ao que o agente produziu. |
| Episódico ou sequencial | Episódico | Cada ordem de serviço é avaliada individualmente, considerando a situação da máquina naquele momento. Mesmo que o histórico de falhas seja utilizado, um erro em uma ordem não altera a classificação correta das próximas. |
| Estático ou dinâmico | Semidinâmico | As informações da ordem de serviço não mudam durante a análise, mas a demora no alerta pode fazer uma máquina de alto risco falhar antes de o técnico ser avisado. |
| Discreto ou contínuo | Contínuo | Temperatura, rotação, torque e desgaste de ferramenta variam sem degraus, o agente divide os valores dos sensores em três níveis de risco (baixo, médio e alto). Essa divisão é uma escolha do sistema, pois os valores reais variam continuamente. |
| Conhecido ou desconhecido | Conhecido, com ressalva | As normas de segurança e os dados de falhas ajudam o agente a identificar riscos, mas ele pode não reconhecer falhas diferentes das previstas no conjunto de dados utilizado. |

**O que a tabela de consequências obriga neste projeto:**
- *Não se aplicam* — o processo não exige planejamento sequencial nem exploração, pois cada ordem de serviço é avaliada individualmente com base no histórico e nas normas existentes.
- *Se aplicam* — o agente precisa considerar o histórico da máquina, comunicar-se com técnicos e supervisores, lidar com falhas imprevisíveis, respeitar prazos de resposta e definir limites numéricos para cada nível de risco.

---

## 3. Tipo de agente pretendido

<!--
Perguntas que guiam o preenchimento:
  - O tipo mais simples que resolve: reativo simples, baseado em modelo,
    baseado em objetivos, baseado em utilidade, ou um deles com aprendizagem?
  - A caracterização do ambiente (seção 2) é que decide — parcialmente
    observável elimina o reativo simples.
  - Justifique com a dimensão do ambiente que obriga a escolha.
-->
**Quando se preenche:** no sábado (encontro 2, manhã).

**Agente baseado em utilidade, com um modelo interno do estado da máquina.**
Observabilidade parcial (seção 2): descarta o agente reativo simples, pois ele precisa de um modelo interno para estimar o estado da máquina com base no histórico, já que as leituras atuais não fornecem todas as informações necessárias.

Ambiente estocástico e assimetria de custos (seção 1): como classificar incorretamente uma máquina com falha como de baixo risco é mais grave do que gerar um alarme falso, o agente deve considerar as probabilidades e os custos de cada decisão. Isso exige avaliar a utilidade das alternativas, em vez de apenas verificar se existe falha ou não.

Conclusão: a melhor escolha é um agente baseado em utilidade, apoiado em um modelo interno do ambiente, pois ele consegue lidar tanto com a falta de informações completas quanto com as diferentes consequências de cada decisão.

---

## 4. Medida de desempenho

<!--
Perguntas que guiam o preenchimento:
  - A fórmula do campo Performance, agora em definição operacional: como se
    calcula, passo a passo, sem ambiguidade?
  - Métrica primária e duas secundárias. As secundárias pegam o que a
    primária deixa passar (custo, latência, reabertura).
  - O conjunto de casos: de onde vêm, quantos são, de que período.
  - O limiar de sucesso e o valor de hoje.
-->
**Quando se preenche:** a fórmula começa no Laboratório 01; a definição
operacional completa — primária, secundárias, conjunto e limiar — é item da
Atividade Orientada.

Métrica primária — Recall de falhas reais: mede a capacidade do agente de identificar máquinas que realmente apresentam falhas. A meta é identificar corretamente pelo menos 85% das falhas reais. O valor atual é 0%, pois a linha de base utilizada classifica todas as máquinas como de baixo risco, deixando de identificar qualquer falha.

Métrica secundária 1 — Taxa de falsos alarmes: mede a proporção de máquinas sem falhas reais que são classificadas incorretamente como apresentando risco. A meta é manter essa taxa em, no máximo, 15%. O valor atual é 0%, porque a linha de base nunca gera alertas. Isso demonstra que uma taxa baixa de falsos alarmes não significa que o agente seja eficiente: ele pode simplesmente deixar de identificar todas as falhas. Por isso, essa métrica deve ser avaliada em conjunto com o recall.

Métrica secundária 2 — Taxa de escalonamento correto ao supervisor: mede se o agente encaminha corretamente ao supervisor os casos que exigem avaliação humana, conforme a ação prevista na seção 1. A meta é 100% de encaminhamentos corretos, pois nenhum caso que exija supervisão deve deixar de ser encaminhado. O valor atual é não aplicável, porque essa regra de escalonamento ainda não foi implementada.

---

## 5. Restrições

<!--
Perguntas que guiam o preenchimento:
  - Latência aceitável: a partir de quantos segundos a resposta perde valor?
  - Custo aceitável: quanto pode custar cada resolução?
  - O que o agente jamais pode fazer: a ação irreversível que ele não executa
    sozinho. Esta linha vira política em D12.
  - A troca que você aceita: quanto de qualidade por quanto de custo?
    Um exemplo numérico vale mais que a fórmula.
-->
**Quando se preenche:** na Atividade Orientada.

Latência e custo: o tempo de resposta varia conforme o risco: até 60 segundos para risco alto, 5 minutos para risco médio e 15 minutos para risco baixo, processado em lote. O custo estimado é de R$ 0,05 por ordem, podendo aumentar em casos ambíguos ou de alto risco. Esses limites consideram que a situação da máquina pode mudar durante a análise.

Limites de autonomia e segurança: o agente nunca executa ou libera o bloqueio e etiquetagem de segurança (LOTO), nem encerra ordens de risco médio ou alto sem confirmação humana. Sua função é analisar os dados, identificar riscos e recomendar ações, sem substituir o responsável pela decisão.

Equilíbrio entre qualidade e custo: pode ser aceitável aumentar os falsos alarmes de 15% para 20% e triplicar o reprocessamento de ordens de alto risco para manter a resposta em até 60 segundos, desde que isso aumente a segurança e reduza falhas não detectadas. Essa escolha se justifica porque o custo de não identificar uma falha real é maior do que o de gerar um alarme falso.

---

## 6. Catálogo de ações

<!--
Perguntas que guiam o preenchimento:
  - Para cada ação: nome, entrada, saída, é reversível?, qual o risco se
    errar? As quatro colunas são obrigatórias — "baixo" não é descrição de
    risco.
  - Ações de leitura E de escrita: as que alteram o mundo são as que exigem
    cuidado, e são justamente as que mais ficam de fora.
  - Este catálogo é, literalmente, a lista de ferramentas que você vai
    implementar em D10.
-->
**Quando se preenche:** na Atividade Orientada — o pacote `D2-07` traz o
modelo da tabela e dois exemplos preenchidos.



---

## 7. Formulação por busca

<!--
Perguntas que guiam o preenchimento:
  - Qual fatia do problema é um espaço de estados? (Nem toda fatia é — e
    reconhecer a que não é vale tanto quanto formular a que é.)
  - Os cinco componentes: estado inicial, ações, modelo de transição, teste
    de objetivo, custo de caminho. Comece pelo teste de objetivo.
  - O estado descreve a SITUAÇÃO, não a história de como se chegou nela.
-->
**Quando se preenche:** no Laboratório 03, sábado à tarde (encontro 2).

- Estado: conjunto de fatos já levantados sobre a OS (tupla vazia no início).
- Ações: consultar uma de 5 fontes (telemetria, sistema de OS, prontuário completo, biblioteca de normas, atendimento humano).
- Objetivo: ter os 4 fatos que a seção 1 (Sensors) já exige — sensores, histórico AI4I 2020, descrição da intervenção, normas aplicáveis.
- Custo: latência de cada consulta, em segundos.
