# Anotações — Laboratório 02, a descida à mão

> O critério do slide 11: as quatro perguntas respondidas por escrito, com o
> número que sustenta cada resposta. Preencha a tabela rodando o esqueleto
> com as três taxas do slide 12 e copiando a última linha de cada execução.

## A última linha de cada taxa

| Taxa | Última linha da saída (perda, w, b) |
|---|---|
| 0,001 | passo  200 perda 22462.1 w 215.016 b -17.7381 |
| 0,1 | passo  200 perda 0.752176 w 300.008 b 4.91185 |
| 1,5 | passo  200 perda inf w -3.12216e+190 b 4.826e+189 |

## As quatro perguntas do slide 11

**1. A perda está caindo a cada passo, ou oscilando?**

R: Depende da taxa. Com taxa 0,1 a perda cai a cada passo sem oscilar —
284802 no passo 1, 36734,6 no passo 2, 5450 no passo 3, caindo de forma
monotônica até 0,752176 no passo 200. Com taxa 0,001 também cai de forma
monotônica, só que devagar (284802 → 281149 → 277543 nos três primeiros
passos). Com taxa 1,5 não oscila: cresce de forma monotônica e explosiva
(284802 no passo 1 para 2,14e+07 já no passo 2).

**2. Ela estabiliza, ou continua descendo até o fim?**

R: Com taxa 0,1 ela estabiliza bem antes do passo 200 — do passo 198 ao 200
a perda fica parada em 0,752176 (três casas decimais iguais). Com taxa 0,001
ela ainda está caindo no passo 200 (22462,1), sem ter estabilizado — é a
taxa "baixa demais" do slide 12. Com taxa 1,5 ela não estabiliza: diverge até
virar `inf` no passo 161.

**3. Os pesos encontrados batem com os que geraram os dados?**

R: Só com taxa 0,1: w=300,008 e b=4,91185 ficam muito perto dos verdadeiros
w=300 e b=5. Com taxa 0,001 os pesos ficam longe (w=215,016, b=-17,7381) —
200 passos não foram suficientes. Com taxa 1,5 os pesos não batem com nada:
w=-3,12e+190 e b=4,83e+189 são artefatos do estouro numérico, não uma
estimativa.

**4. Se algo divergiu, qual foi o primeiro passo estranho?**

R: Com taxa 1,5, a perda já nasce estranha no passo 1 (284802, igual ao
primeiro passo das outras taxas) mas dobra de tamanho a cada passo em vez de
cair: 2,14e+07 no passo 2, 1,63e+09 no passo 3, 1,23e+11 no passo 4 — um
crescimento exponencial claro desde o início. O primeiro passo em que ela
deixa de ser um número finito é o passo 161, onde a perda vira `inf`;
rodando com `--passos 350`, o primeiro `nan` da coluna aparece no passo 326.
