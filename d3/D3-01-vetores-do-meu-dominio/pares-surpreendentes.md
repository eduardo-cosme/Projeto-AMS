# Pares que surpreenderam — Laboratório 01

> O slide 19 do D3-E1 pede DOIS casos anotados: um par PRÓXIMO sem razão
> aparente e um par DISTANTE que deveria estar junto. Eles voltam na D7,
> quando a turma montar o próprio índice de recuperação — escreva aqui e
> guarde este arquivo no seu repositório.

## Um par PRÓXIMO sem razão aparente

- Índices do par: (15, 102)
- As duas frases:
  - primeira: "A pista externa do rolamento do ventilador apresenta pitting avançado."
  - segunda: "O ventilador exaustor da cabine de pintura opera abaixo da vazão de projeto."
- Cosseno medido: 0,7675

Resp: Apesar da alta similaridade (9º entre os dez resultados), os equipamentos e problemas são completamente diferentes: um apresenta desgaste mecânico (pitting no rolamento), enquanto o outro tem vazão de ar abaixo do especificado em um exaustor de pintura. A semelhança parece estar apenas na palavra “ventilador”, indicando que o embedding considera mais a semelhança entre os termos do que o contexto técnico dos problemas. 

## Um par DISTANTE que deveria estar junto

- Índices do par: (143, 145)
- As duas frases:
  - primeira: "O líquido penetrante nas soldas do tanque não revelou indicações relevantes."
  - segunda: "O ensaio por ultrassom das juntas soldadas do vaso cobriu dez por cento do comprimento."
- Cosseno medido: 0,1266

Resp: As duas frases deveriam apresentar alta similaridade, pois descrevem ensaios não destrutivos (END) em juntas soldadas de vasos e tanques, utilizando técnicas diferentes: líquido penetrante e ultrassom. Porém, o cosseno foi muito baixo (0,1266), indicando pouca similaridade. Isso sugere que o embedding valoriza mais os termos específicos de cada técnica do que o contexto técnico em comum: inspeção de soldas por ensaios não destrutivos.

## O que a comparação com NORMALIZAR = True mudou

Resp:
1. Alguma ordem mudou? De qual par?

Nos dez pares mais semelhantes e nos dez mais distantes, nenhuma posição mudou. Na lista completa, a primeira troca aparece apenas na 1746ª colocação, entre os pares (50, 93) e (88, 98), que possuem cossenos praticamente iguais (0,38618). Essa alteração ocorre por diferenças mínimas de arredondamento (aproximadamente 1e-7), sem impacto real na similaridade.

2. O que muda com a normalização?

A normalização não altera significativamente a similaridade de cosseno, mas muda o comportamento da distância euclidiana. Com os vetores normalizados, as duas métricas mantêm a mesma ordem de classificação. Sem normalização, a distância euclidiana também considera a magnitude dos vetores, podendo gerar resultados diferentes. Por exemplo, os pares 1 e 3 do ranking apresentam cossenos próximos (0,9426 e 0,9348), mas distâncias euclidianas diferentes (1,3691 e 1,4036).
