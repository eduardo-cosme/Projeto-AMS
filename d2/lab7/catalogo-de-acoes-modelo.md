# Catálogo de ações — modelo para preencher

<!--
Este arquivo é para preencher: uma linha por ação que o SEU agente vai
poder executar. As perguntas de cada coluna estão aqui em comentário.

As quatro perguntas que decidem se uma linha está boa:
  - Ação de ESCRITA também? As que alteram o mundo são as que exigem
    cuidado — e são justamente as que mais ficam de fora.
  - COMUNICAR é ação? Avisar, escalar, transferir, pedir confirmação:
    entram com entrada, saída e risco como as outras.
  - "É reversível?" pergunta se o efeito pode ser DESFEITO sem custo
    maior que o da própria ação.
  - O risco diz risco DE QUÊ — "baixo" não é descrição; "paga duas vezes
    uma nota que já estava paga" é.

Este catálogo é, literalmente, a lista de ferramentas que você vai
implementar em D10. Cada linha vira uma função com contrato.
-->

| Ação | Entrada | Saída | É reversível? | Risco se errar |
|---|---|---|---|---|
| Consultar os sensores atuais da máquina | Identificador da máquina (da OS) | Leituras de temperatura, rotação, torque e desgaste de ferramenta | Sim (somente leitura) | Dados incorretos geram classificação errada e reavaliação. |
| Consultar o histórico de falhas da máquina no AI4I 2020 | Identificador da máquina | Registros de falhas anteriores (TWF, HDF, PWF, OSF) e padrão de ocorrência | Sim — só lê | Histórico incompleto pode subestimar o risco |
| Ler a descrição da intervenção escrita pelo técnico | Texto livre da ordem de serviço | Sintoma, componente envolvido | Sim | Descrição incompleta faz o agente decidir com menos informação do que o técnico tem no local |
| Consultar a biblioteca de normas regulamentares (NR-10, NR-12, NR-35) | Categoria da intervenção (elétrica, mecânica, altura etc.) | Trechos aplicáveis da norma e exigências de segurança | Sim | Norma desatualizada pode gerar orientações de segurança incorretas. |
| Classificar o nível de risco de falha e anexar a classificação à OS | Sensores, histórico e descrição da intervenção | Nível de risco (baixo/médio/alto) anexado à ordem de serviço | Sim (pode ser revisado) | Falso negativo atrasa a correção; falso positivo gera parada desnecessária |


**Quem executa cada ação** (o agente sozinho? com confirmação humana? só
humano?):
O agente executa sozinho as consultas aos sensores, histórico de falhas, descrição da intervenção, normas de segurança e classificação do risco, pois são atividades de leitura e análise.

Já as recomendações de LOTO (bloqueio e etiquetagem) e a comunicação das orientações são geradas pelo agente, mas a execução do bloqueio e a decisão de realizar a intervenção cabem exclusivamente ao técnico.

O escalonamento ao supervisor é feito pelo agente, porém a decisão final — aprovar, solicitar mais informações ou reclassificar o risco — é sempre humana.

Em resumo: o agente analisa e recomenda; o técnico e o supervisor tomam as decisões e executam as ações. O agente não substitui a responsabilidade humana, conforme definido na seção 5 do PEAS.

**O que o agente JAMAIS executa sozinho:**
O agente nunca realiza nem libera o bloqueio e etiquetagem de segurança (LOTO), apenas identifica a necessidade e recomenda o procedimento. O bloqueio e a liberação da máquina são responsabilidades exclusivas do técnico ou responsável humano.

Também não pode encerrar sozinho ordens de serviço classificadas como risco médio ou alto, sendo obrigatória a confirmação humana.

Em resumo: o agente identifica riscos e recomenda ações, mas nunca executa procedimentos físicos de segurança nem toma decisões finais sem autorização humana, conforme definido na seção 5 (Restrições) do agent-spec.
