# Anotações — Laboratório 02, a descida à mão

> O critério do slide 11: as quatro perguntas respondidas por escrito, com o
> número que sustenta cada resposta. Preencha a tabela rodando o esqueleto
> com as três taxas do slide 12 e copiando a última linha de cada execução.

## A última linha de cada taxa

| Taxa | Última linha da saída (perda, w, b) |
|---|---|
| 0,001 | passo  200 perda 22462.1 w 215.016 b -17.7381 |
| 0,1   |   passo  200 perda 0.752176 w 300.008 b 4.91185 |
| 1,5   |   passo  200 perda inf w -3.12216e+190 b 4.826e+189 |

## As quatro perguntas do slide 11

**1. A perda está caindo a cada passo, ou oscilando?**

Taxa 0,1: a perda diminui continuamente, sem apresentar oscilações. Começa em 284.802 no passo 1, cai para 36.734,6 no passo 2 e 5.450 no passo 3, chegando a 0,752176 no passo 200. Isso indica uma convergência rápida e estável.

Taxa 0,001: a perda também diminui continuamente, sem oscilações, mas em um ritmo muito mais lento. Nos três primeiros passos, os valores passam de 284.802 para 281.149 e depois para 277.543. Isso indica uma convergência mais gradual.

Taxa 1,5: a perda não apresenta oscilações, mas cresce de maneira contínua e explosiva. Parte de 284.802 no passo 1 e chega a aproximadamente 21,4 milhões já no passo 2. Isso indica que a taxa de aprendizagem está muito alta, fazendo com que o algoritmo se afaste da solução em vez de convergir.

**2. Ela estabiliza, ou continua descendo até o fim?**

O comportamento da perda depende da taxa de aprendizagem utilizada:

Taxa 0,1: estabiliza antes do passo 200, mantendo a perda em aproximadamente 0,752176. Isso indica que o algoritmo chegou à convergência.

Taxa 0,001: continua diminuindo até o passo 200, mas ainda não estabilizou, pois a taxa de aprendizagem é muito baixa.

Taxa 1,5: não estabiliza. A perda cresce descontroladamente até atingir inf (infinito) no passo 161, indicando que o algoritmo divergiu.

Ou seja, a taxa 0,1 apresenta o melhor resultado, pois alcança a estabilização rapidamente. A taxa 0,001 é lenta demais e a taxa 1,5 é alta demais, causando divergência.

**3. Os pesos encontrados batem com os que geraram os dados?**

Taxa 0,1: sim. Os valores encontrados (w=300,008 e b=4,91185) são muito próximos dos valores reais (w=300 e b=5).

Taxa 0,001: não. Os valores ainda estão distantes dos reais, pois 200 passos não foram suficientes para chegar à convergência.

Taxa 1,5: não. Os valores encontrados são resultados de instabilidade numérica causada pela taxa de aprendizagem excessiva.

Ou seja, somente a taxa 0,1 conseguiu encontrar pesos próximos dos valores reais.

**4. Se algo divergiu, qual foi o primeiro passo estranho?**

R: Com taxa 1,5, a perda começa a aumentar drasticamente já no passo 2. Enquanto o esperado seria diminuir a cada passo, ela passa de 284.802 no passo 1 para 21,4 milhões no passo 2, 1,63 bilhão no passo 3 e 123 bilhões no passo 4. Esse crescimento acelerado continua até atingir inf (infinito) no passo 161, demonstrando que a taxa de aprendizagem está muito alta e faz o algoritmo divergir.
