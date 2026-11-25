# Análise — AMS (Gestão de Ordens de Serviço de Manutenção)

## O que torna o problema difícil

O problema é difícil porque o agente inteligente possui observabilidade parcial, ou seja, ele não consegue enxergar todas as informações necessárias para identificar o estado real da máquina.

Nos casos C07 e C08, a máquina (TORNO) apresentou uma falha intermitente, mas os sensores não indicaram nenhuma condição anormal no momento da leitura. A temperatura estava entre 60 e 61 °C, e a vibração entre 3,0 e 3,1 mm/s, valores considerados dentro da faixa normal.

Além disso, não havia registro de falhas da mesma família de máquinas no histórico dos últimos 7 dias. Dessa forma, o agente não possuía informações suficientes para suspeitar que uma falha estava prestes a acontecer.

O principal problema é que a falha foi causada por um desgaste acumulado que não podia ser identificado apenas pelas leituras instantâneas de temperatura e vibração, nem pelo histórico disponível.

Portanto, o agente tomou sua decisão com base nas informações que conseguia observar, mas essas informações eram incompletas. Isso demonstra que, em ambientes com obs

## Que tipo de agente o problema realmente exige

O problema exige um agente com estado interno, pois um agente reativo simples considera apenas as leituras atuais dos sensores, sem levar em conta o histórico da máquina. Isso poderia fazer com que repetisse os erros identificados nos casos C07, C08 e C10.

O estado interno permite armazenar informações sobre falhas anteriores, considerando tanto a família quanto a máquina individualmente. Além disso, um mecanismo baseado em utilidade permite avaliar a probabilidade de falha e as consequências de cada decisão, considerando que não identificar uma falha real é mais grave do que gerar um alarme falso.

Portanto, a solução mais adequada é um agente com estado interno e decisão baseada em utilidade, capaz de combinar informações atuais e históricas para avaliar os riscos de forma mais precisa.

## O que isto muda no projeto (fecho)

Na minha opinão o projeto precisa de duas melhorias: primeiro, utilizar uma escala contínua de risco, em vez de uma classificação baseada apenas em limites fixos, permitindo diferenciar situações com níveis distintos de gravidade. Segundo, manter um histórico individual por máquina, evitando que o alerta de uma máquina influencie outra apenas por pertencerem à mesma família.

Essas melhorias não exigem novos sensores, apenas um melhor aproveitamento das informações já coletadas. A linha de base continua sendo eficiente nos casos em que a decisão é claramente binária, tendo acertado os sete casos de parada para manutenção. Portanto, o principal ganho do modelo está na avaliação dos riscos intermediários, onde considerar o histórico e a intensidade dos sinais permite decisões mais precisas.
