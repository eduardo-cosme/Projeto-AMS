**Domínio:** Gestão de Ordens de Serviço de Manutenção
**Autor(a):** Eduardo Boaventura  · **Última revisão:** 17/11/2026

> **Nota de revisão (fecho da N2):** releitura completa das sete seções
> antes da entrega. Não há devolutiva registrada do E3 sobre este
> documento até esta data; por isso as linhas "o que mudou e por quê"
> abaixo registram só o que mudou nesta revisão por causa da medição da
> linha de base (N2), e declaram "sem alteração" onde nada mudou. Se a
> devolutiva do E3 chegar depois da entrega, ela entra aqui como próxima
> revisão.

---

## 1. PEAS

**Performance:**
A fração de ordens de serviço em que o nível de risco de falha previsto
(baixo/médio/alto) bate com o desfecho real da máquina — se ela de fato
falhou ou não, conforme o rótulo de falha do AI4I 2020 — dividida pelo
total de ordens do conjunto de avaliação.
Sucesso: o agente deverá acertar mais de 85% na identificação dos dois
tipos de situação: máquinas que apresentam falhas e máquinas que não
apresentam falhas.
O termo contra a trapaça óbvia: como falhas são raras no dataset (cerca
de 3,4% dos 10.000 registros), um agente que sempre responde "baixo
risco" já acerta ~97% das ordens sem nunca ter avaliado nada — por isso
o que conta não é a taxa de acerto simples, e sim a deteção de falha
real: toda máquina que falhou e foi classificada como baixo risco é
contada como erro grave, mesmo que a taxa de acerto geral pareça boa.

**Environment:**
Fábrica com máquinas monitoradas por sensores de temperatura, rotação,
torque e desgaste, utilizando o dataset AI4I 2020 para análise de
falhas. O sistema consulta ordens de serviço e normas de segurança
(NR-10, NR-12 e NR-35). O técnico de manutenção utiliza as
recomendações para apoiar suas decisões, enquanto o supervisor de
segurança verifica os resultados. Os principais desafios são as
variações dos sensores e as descrições incompletas ou ambíguas das
intervenções.

**Actuators:**
Emitir a classificação do nível de risco de falha da máquina (baixo /
médio / alto), anexada à ordem de serviço; apontar as normas
regulamentares aplicáveis à intervenção (NR-10, NR-12, NR-35);
sinalizar se a intervenção exige bloqueio e etiquetagem (LOTO) antes de
começar; comunicar ao técnico a recomendação de forma curta, justificada
e auditável — o agente não decide por ele, só informa; escalar ao
supervisor de segurança os casos de risco alto ou de classificação
ambígua, para auditoria antes ou depois da intervenção.

**Sensors:**
A leitura atual dos sensores da máquina informada na ordem de serviço
(temperatura, rotação, torque e desgaste de ferramenta); o texto da
descrição da intervenção escrito pelo técnico; o identificador e o
histórico de falhas da máquina registrado no dataset AI4I 2020; o texto
das normas regulamentares (NR-10, NR-12, NR-35) disponível para busca.
O que não está nesses canais não existe para o agente: ele não vê a
máquina, não ouve nem sente o que o técnico percebe no local, e se a
descrição da intervenção omitir um detalhe relevante, esse detalhe
simplesmente não entra na decisão.

> **O que mudou e por quê:**

## 2. O ambiente em sete dimensões

| Dimensão | Classificação | Justificativa |
|---|---|---|
| Observabilidade | Parcial | As informações dos sensores e o relato do técnico podem não mostrar detalhes importantes percebidos no local, como barulhos, cheiros ou peças soltas, que podem mudar a classificação correta do problema. |
| Determinismo | Estocástico | Mesmo com as mesmas medições dos sensores, o resultado pode ser diferente, pois as falhas podem acontecer de forma imprevisível. Além disso, a descrição do técnico pode ser interpretada de maneiras diferentes em cada caso. |
| Número de agentes | Multiagente | O técnico decide se realiza o serviço com base na recomendação, enquanto o supervisor de segurança verifica os casos de risco ou dúvida e pode mudar a decisão, ambos reagem ao que o agente produziu. |
| Episódico ou sequencial | Episódico | Cada ordem de serviço é avaliada individualmente, considerando a situação da máquina naquele momento. Mesmo que o histórico de falhas seja utilizado, um erro em uma ordem não altera a classificação correta das próximas. |
| Estático ou dinâmico | Semidinâmico | As informações da ordem de serviço não mudam durante a análise, mas a demora no alerta pode fazer uma máquina de alto risco falhar antes de o técnico ser avisado. |
| Discreto ou contínuo | Contínuo | Temperatura, rotação, torque e desgaste de ferramenta variam sem degraus; o agente divide os valores dos sensores em três níveis de risco (baixo, médio e alto). Essa divisão é uma escolha do sistema, pois os valores reais variam continuamente. |
| Conhecido ou desconhecido | Conhecido, com ressalva | As normas de segurança e os dados de falhas ajudam o agente a identificar riscos, mas ele pode não reconhecer falhas diferentes das previstas no conjunto de dados utilizado. |

**O que a tabela de consequências obriga neste projeto:**
- *Não se aplicam* — o processo não exige planejamento sequencial nem
  exploração, pois cada ordem de serviço é avaliada individualmente com
  base no histórico e nas normas existentes.
- *Se aplicam* — o agente precisa considerar o histórico da máquina,
  comunicar-se com técnicos e supervisores, lidar com falhas
  imprevisíveis, respeitar prazos de resposta e definir limites
  numéricos para cada nível de risco.

**O que mudou e por quê:** 

## 3. Tipo de agente pretendido

**Agente baseado em utilidade, com um modelo interno do estado da máquina.**
Observabilidade parcial (seção 2): descarta o agente reativo simples,
pois ele precisa de um modelo interno para estimar o estado da máquina
com base no histórico, já que as leituras atuais não fornecem todas as
informações necessárias.

Ambiente estocástico e assimetria de custos (seção 1): como classificar
incorretamente uma máquina com falha como de baixo risco é mais grave
do que gerar um alarme falso, o agente deve considerar as
probabilidades e os custos de cada decisão. Isso exige avaliar a
utilidade das alternativas, em vez de apenas verificar se existe falha
ou não.

Conclusão: a melhor escolha é um agente baseado em utilidade, apoiado
em um modelo interno do ambiente, pois ele consegue lidar tanto com a
falta de informações completas quanto com as diferentes consequências
de cada decisão.

**Relação com a linha de base medida nesta entrega:**
O arquivo src/ams/baseline.py (item 2) implementa uma versão mais simples de um agente baseado em modelo, que utiliza estado interno e limites fixos para tomar decisões, mas não considera a probabilidade de falha nem o custo das consequências.

Essa implementação serve como referência inicial para avaliar o desempenho do agente. A diferença entre essa versão e um agente baseado em utilidade é justamente o que será analisado no item 5 (analise.md): quais melhorias são necessárias para que o agente deixe de apenas reagir aos sinais e ao histórico e passe a considerar a probabilidade de falha e as consequências de cada decisão.


**O que mudou e por quê:**
Foi acrescentada a observação sobre a relação com a linha de base (baseline.py) para esclarecer que o código implementa uma versão mais simples de agente baseado em modelo, que utiliza estado interno, mas ainda não considera a probabilidade de falha nem o custo das decisões.

Essa observação evita uma possível contradição entre a especificação do projeto e o código implementado. A escolha do tipo de agente continua a mesma; apenas foi esclarecida a diferença entre a versão atual e o modelo de agente baseado em utilidade que se pretende alcançar.

## 4. Medida de desempenho

Métrica primária — Recall de falhas reais: mede a capacidade do agente
de identificar máquinas que realmente apresentam falhas. A meta é
identificar corretamente pelo menos 85% das falhas reais. O valor atual
é 0%, pois a linha de base utilizada classifica todas as máquinas como
de baixo risco, deixando de identificar qualquer falha.

Métrica secundária 1 — Taxa de falsos alarmes: mede a proporção de
máquinas sem falhas reais que são classificadas incorretamente como
apresentando risco. A meta é manter essa taxa em, no máximo, 15%. O
valor atual é 0%, porque a linha de base nunca gera alertas. Isso
demonstra que uma taxa baixa de falsos alarmes não significa que o
agente seja eficiente: ele pode simplesmente deixar de identificar
todas as falhas. Por isso, essa métrica deve ser avaliada em conjunto
com o recall.

Métrica secundária 2 — Taxa de escalonamento correto ao supervisor:
mede se o agente encaminha corretamente ao supervisor os casos que
exigem avaliação humana, conforme a ação prevista na seção 1. A meta é
100% de encaminhamentos corretos, pois nenhum caso que exija supervisão
deve deixar de ser encaminhado. O valor atual é não aplicável, porque
essa regra de escalonamento ainda não foi implementada.

A linha de base (src/ams/baseline.py) foi avaliada utilizando o conjunto de reserva do D2-06 (casos-de-reserva.csv), que contém 30 casos com suas respectivas ações corretivas esperadas.

A métrica utilizada foi o acerto da decisão, que mede quantas vezes a ação escolhida pelo agente corresponde à ação correta definida no conjunto de dados. Os resultados estão apresentados no arquivo relatorio-de-desempenho.md.

O AI4I 2020 não possui ações corretivas classificadas individualmente, informando apenas se houve falha ou não na máquina. Por isso, não permite calcular diretamente essa métrica, mas pode ser utilizado para medir o recall de falhas, que é a métrica considerada para avaliar o produto final do projeto.

**O que mudou e por quê:**
Foi acrescentada uma observação para esclarecer qual métrica foi utilizada na avaliação da linha de base. A medição utilizou o acerto da decisão no conjunto de reserva do D2-06, pois o AI4I 2020 não informa qual ação corretiva deve ser aplicada em cada caso.
As métricas de recall e falsos alarmes continuam sendo utilizadas para avaliar o produto final do projeto, não a linha de base do laboratório.

---

## 5. Restrições

Latência e custo: o tempo de resposta varia conforme o risco: até 60
segundos para risco alto, 5 minutos para risco médio e 15 minutos para
risco baixo, processado em lote. O custo estimado é de R$ 0,05 por
ordem, podendo aumentar em casos ambíguos ou de alto risco. Esses
limites consideram que a situação da máquina pode mudar durante a
análise.

Limites de autonomia e segurança: o agente nunca executa ou libera o
bloqueio e etiquetagem de segurança (LOTO), nem encerra ordens de risco
médio ou alto sem confirmação humana. Sua função é analisar os dados,
identificar riscos e recomendar ações, sem substituir o responsável
pela decisão.

Equilíbrio entre qualidade e custo: pode ser aceitável aumentar os
falsos alarmes de 15% para 20% e triplicar o reprocessamento de ordens
de alto risco para manter a resposta em até 60 segundos, desde que isso
aumente a segurança e reduza falhas não detectadas. Essa escolha se
justifica porque o custo de não identificar uma falha real é maior do
que o de gerar um alarme falso.

**O que mudou e por quê:**
Não houve alterações nesta revisão. As restrições relacionadas à latência, ao custo e ao nível de autonomia do agente foram mantidas, pois a linha de base não realizou testes que permitissem avaliar esses aspectos ou justificar mudanças nos requisitos.

---

## 6. Catálogo de ações

| Ação | Entrada | Saída | É reversível? | Risco se errar |
|---|---|---|---|---|
| Consultar os sensores atuais da máquina | Identificador da máquina (da OS) | Leituras de temperatura, rotação, torque e desgaste de ferramenta | Sim (somente leitura) | Dados incorretos geram classificação errada e reavaliação. |
| Consultar o histórico de falhas da máquina no AI4I 2020 | Identificador da máquina | Registros de falhas anteriores (TWF, HDF, PWF, OSF) e padrão de ocorrência | Sim — só lê | Histórico incompleto pode subestimar o risco |
| Ler a descrição da intervenção escrita pelo técnico | Texto livre da ordem de serviço | Sintoma, componente envolvido | Sim | Descrição incompleta faz o agente decidir com menos informação do que o técnico tem no local |
| Consultar a biblioteca de normas regulamentares (NR-10, NR-12, NR-35) | Categoria da intervenção (elétrica, mecânica, altura etc.) | Trechos aplicáveis da norma e exigências de segurança | Sim | Norma desatualizada pode gerar orientações de segurança incorretas. |
| Classificar o nível de risco de falha e anexar a classificação à OS | Sensores, histórico e descrição da intervenção | Nível de risco (baixo/médio/alto) anexado à ordem de serviço | Sim (pode ser revisado) | Falso negativo atrasa a correção; falso positivo gera parada desnecessária |

**Quem executa cada ação** (o agente sozinho? com confirmação humana? só
humano?):
O agente executa sozinho as consultas aos sensores, histórico de
falhas, descrição da intervenção, normas de segurança e classificação
do risco, pois são atividades de leitura e análise.

Já as recomendações de LOTO (bloqueio e etiquetagem) e a comunicação
das orientações são geradas pelo agente, mas a execução do bloqueio e a
decisão de realizar a intervenção cabem exclusivamente ao técnico.

O escalonamento ao supervisor é feito pelo agente, porém a decisão
final — aprovar, solicitar mais informações ou reclassificar o risco —
é sempre humana.

Em resumo: o agente analisa e recomenda; o técnico e o supervisor tomam
as decisões e executam as ações. O agente não substitui a
responsabilidade humana, conforme definido na seção 5 do PEAS.

**O que o agente JAMAIS executa sozinho:**
O agente nunca realiza nem libera o bloqueio e etiquetagem de segurança
(LOTO), apenas identifica a necessidade e recomenda o procedimento. O
bloqueio e a liberação da máquina são responsabilidades exclusivas do
técnico ou responsável humano.

Também não pode encerrar sozinho ordens de serviço classificadas como
risco médio ou alto, sendo obrigatória a confirmação humana.

Em resumo: o agente identifica riscos e recomenda ações, mas nunca
executa procedimentos físicos de segurança nem toma decisões finais sem
autorização humana, conforme definido na seção 5 (Restrições) do
agent-spec.

**O que mudou e por quê:**
sem alteração nesta revisão, o catálogo de ações continua o mesmo; a linha de base decide entre três ações corretivas rotuladas, que são um recorte do uso do agente, não uma troca do catálogo.

---

## 7. Formulação por busca

- Estado: conjunto de fatos já levantados sobre a OS (tupla vazia no
  início).
- Ações: consultar uma de 5 fontes (telemetria, sistema de OS,
  prontuário completo, biblioteca de normas, atendimento humano).
- Objetivo: ter os 4 fatos que a seção 1 (Sensors) já exige — sensores,
  histórico AI4I 2020, descrição da intervenção, normas aplicáveis.
- Custo: latência de cada consulta, em segundos.

**O que mudou e por quê:**
Não houve alterações nesta revisão. A formulação por busca continua a mesma apresentada na tabela do relatório (relatorio-de-desempenho.md, item 4). Os resultados obtidos não indicaram necessidade de modificar os estados, as ações disponíveis, o objetivo ou os custos utilizados na busca.
