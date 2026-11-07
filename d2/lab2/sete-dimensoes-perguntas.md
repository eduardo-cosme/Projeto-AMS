# Sete dimensões — perguntas para o meu ambiente

<!--
Este arquivo é o formulário do Laboratório 02: preencha DENTRO dele, na
seção do seu domínio, no fim. As perguntas por dimensão estão em comentário
como este — aparecem no editor, não na pré-visualização.

Em cada dimensão, a resposta tem duas partes obrigatórias: a classificação
e UMA FRASE de justificativa. A justificativa é o que a rubrica pontua — a
etiqueta sozinha não vale nada (slide 32). Quando a resposta honesta for
"depende", escreva de que depende e em que situação cada resposta se
aplica: isso é caracterização melhor, não pior.

Copie a tabela preenchida para a seção 2 do seu agent-spec.md ao terminar.
-->

## As sete perguntas (as mesmas do slide 22)

| Dimensão | A pergunta que ela faz |
|---|---|
| Observabilidade | O agente enxerga tudo o que precisa para decidir? |
| Número de agentes | Existe outro agente cujas ações afetam o resultado? |
| Determinismo | A mesma ação no mesmo estado dá sempre o mesmo efeito? |
| Episódico ou sequencial | A decisão de agora afeta as decisões seguintes? |
| Estático ou dinâmico | O ambiente muda enquanto o agente delibera? |
| Discreto ou contínuo | Estados e ações são contáveis ou variam sem degraus? |
| Conhecido ou desconhecido | O agente sabe de antemão as regras do ambiente? |

## O que prestar atenção em cada uma

- **Observabilidade** — o teste que decide: existe algo que muda a decisão
  correta e que o agente não mede? Se existe, é parcialmente observável,
  e o projeto precisa de estado interno. Quase todo domínio real é
  parcialmente observável; a resposta honesta aqui costuma ser "parcial".
- **Número de agentes** — um humano operador conta, se ele reage ao que o
  agente faz. Se a sua resposta for multiagente, a D11 será central para
  o seu projeto, e não periférica.
- **Determinismo** — é sobre o efeito das ações, não sobre a observação.
  E atenção: qualquer sistema que chame um modelo de linguagem tem uma
  ação estocástica no meio.
- **Episódico ou sequencial** — classificar um lote é episódico; conduzir
  um atendimento é sequencial. A consequência prática é o custo de
  avaliação: episódico avalia casos independentes, sequencial exige
  avaliar trajetórias inteiras.
- **Estático ou dinâmico** — dinâmico impõe prazo: resposta tardia é
  resposta errada. O caso do meio tem nome: semidinâmico, quando o
  ambiente não muda mas a nota do agente cai com a espera.
- **Discreto ou contínuo** — busca funciona sobre enumeração; contínuo
  precisa ser discretizado antes, e toda discretização perde informação.
  Se você discretizar, a granularidade é decisão declarada, com custo dos
  dois lados.
- **Conhecido ou desconhecido** — a distinção que mais confunde: trata do
  que o agente SABE sobre as regras, e não do que ele VÊ. Sistema legado
  sem documentação é ambiente desconhecido, mesmo que se enxergue tudo
  nele.

## As respostas do meu domínio

**Domínio:** Gestão de Ordens de Serviço de Manutenção (risco de falha de máquina)

| Dimensão | Minha classificação | Justificativa (uma frase) |
|---|---|---|
| Observabilidade | Parcial | As leituras de sensor e a descrição escrita do técnico não capturam o que só se percebe no local (ruído, cheiro, folga mecânica) nem um detalhe que o técnico tenha deixado de registrar, e esse detalhe pode ser justamente o que muda a classificação correta. |
| Número de agentes | Multiagente | O técnico decide executar ou não a intervenção a partir da recomendação, e o supervisor de segurança audita e pode reverter os casos de risco alto ou ambíguos — ambos reagem ao que o agente produziu, e a classificação ambígua do agente precisa antecipar como o supervisor vai julgá-la. |
| Determinismo | Estocástico | A mesma leitura de sensores não garante o mesmo desfecho real (o próprio AI4I 2020 simula falha como processo probabilístico, não determinado só pelos quatro parâmetros medidos), e a interpretação da descrição textual da intervenção varia de caso para caso. |
| Episódico ou sequencial | Episódico | Cada ordem de serviço é avaliada contra o desfecho daquela máquina naquele momento; classificar uma OS errado não muda o que é a resposta certa para a próxima OS, mesmo que o histórico de falhas da máquina entre como dado de entrada. |
| Estático ou dinâmico | Semidinâmico | As leituras registradas na OS não mudam enquanto o agente classifica, mas a demanda tem prazo: se a emissão da recomendação demora, uma máquina em risco alto pode falhar antes de a sinalização de LOTO chegar ao técnico. |
| Discreto ou contínuo | Contínuo  | Temperatura, rotação, torque e desgaste de ferramenta são grandezas reais que variam sem degraus; O agente divide os valores dos sensores em três níveis de risco (baixo, médio e alto). Essa divisão é uma escolha do sistema, pois os valores reais variam continuamente. |
| Conhecido ou desconhecido | Conhecido | As normas de segurança e os dados de falhas ajudam o agente a identificar riscos, mas ele pode não reconhecer falhas diferentes das previstas no conjunto de dados utilizado. |

**O que a tabela de consequências obriga no meu projeto** (conferir no
`tabela-de-consequencias.pdf` e colar aqui as linhas que se aplicam):

- **Não se aplicam (e isso já economiza trabalho):**
  - Não é sequencial → não preciso de planejamento nem de avaliação de trajetória inteira: cada OS é um caso independente, e a Performance (seção 4) pode ser medida por conjunto de casos, não por sequência de decisões.
  - Não é totalmente desconhecido → não preciso de uma fase de exploração formal; o aprendizado vem do histórico rotulado do AI4I 2020 e das normas já documentadas.

- **Se aplicam (viram exigência declarada):**
  - Parcialmente observável → preciso de estado interno: guardar o histórico de falhas da máquina e o contexto de OS anteriores dela, não só a leitura pontual dos sensores.
  - Multiagente → preciso de um protocolo de comunicação com o técnico e o supervisor (como a recomendação é formatada, o que dispara escalonamento) e de antecipar a reação deles — por exemplo, calibrar o limiar de "ambíguo" sabendo que o supervisor vai revisar esses casos.
  - Estocástico → preciso trabalhar com valor esperado e não com certeza binária: a classificação de risco é uma estimativa de probabilidade de falha, não uma previsão garantida, e o critério de sucesso (seção 1) já reflete isso ao aceitar <15% de erro, não 0%.
  - Semidinâmico → preciso declarar um prazo de resposta aceitável (quanto tempo entre a leitura dos sensores e a recomendação chegar ao técnico) e o que conta como resposta parcial aceitável se o agente não conseguir classificar a tempo.
  - Contínuo na entrada → preciso declarar a granularidade da discretização: os limiares numéricos de sensor que definem baixo/médio/alto, e justificar por que três faixas (e não mais) bastam para a decisão do técnico.
