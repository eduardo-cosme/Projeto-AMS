# Laboratório 06 — linha de base: medição e análise

O Laboratório 06 realiza a medição e análise de desempenho do sistema utilizando uma base de dados de reserva (casos-de-reserva.csv), que possui casos com ações corretivas identificadas. Essa escolha permite avaliar se as decisões tomadas pelo sistema estão corretas. Já a base AI4I2020, utilizada anteriormente no projeto AMS, informa apenas se ocorreu ou não uma falha, sem indicar qual ação corretiva deveria ser aplicada. Por isso, não permite medir a precisão das decisões sem uma etapa adicional de classificação manual.

Tipo de agente: baseado em modelo (reativo com estado). O agente utiliza a estrutura EstadoDaFrota para armazenar o histórico de falhas recentes de cada família de máquina, considerando um período de 7 dias. Isso é necessário porque o ambiente é parcialmente observável: uma única leitura não permite identificar se uma máquina já apresenta falhas recorrentes. Ao considerar esse histórico, o método decidir() consegue avaliar a repetição das falhas e tomar decisões mais adequadas, em vez de analisar cada ocorrência isoladamente.


## Métrica, valor e conjunto (slide 28)
 Resultado obtido: 25 acertos em 30 casos analisados, correspondendo a 83,33% de precisão.
Base de dados utilizada: casos-de-reserva.csv, composta por 30 situações de manutenção industrial, distribuídas em três tipos de decisão:
- 16 casos: seguir_operando (continuar a operação).
- 7 casos: parar_para_manutencao (interromper a máquina para manutenção).
- 7 casos: inspecionar_antes_de_operar (realizar uma inspeção antes de continuar a operação).

## Onde o agente erra, e por quê
Não identifica falhas intermitentes (C07 e C08): nesses casos, os sensores de vibração e temperatura apresentaram valores normais no momento da leitura. Como não havia registro de falhas anteriores, o agente não conseguiu identificar o problema. Ou seja, a limitação está na leitura dos sensores, e não nas regras de decisão.
