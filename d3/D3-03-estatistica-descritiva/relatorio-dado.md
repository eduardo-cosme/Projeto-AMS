# O meu dado, com rigor — relatório do Laboratório 03

Conjunto: `..\..\data\amostra\ai4i2020.csv` · 200 linhas · 14 variáveis

Medidas geradas pelo `medidas.py`: desvio padrão amostral (ddof=1),
quartis por interpolação linear, extremos pela regra da amplitude
interquartil — fora de 1,5 × a caixa (slide 24). As medidas são do
programa; as decisões são SUAS. Preencha todos os blocos `R:` e
confira com `python teste.py`.

## Medidas por variável

| variável | tipo | n | faltantes | média | mediana | desvio | Q1 | Q3 | AIQ | mín | máx |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| UDI | numérica | 200 | 0 | 5027.1950 | 5014.5000 | 2837.9039 | 2779.7500 | 7459.5000 | 4679.7500 | 138.0000 | 9998.0000 |
| Product ID | categórica (200 valores; moda: L51324) | 200 | 0 | — | — | — | — | — | — | — | — |
| Type | categórica (3 valores; moda: L) | 200 | 0 | — | — | — | — | — | — | — | — |
| Air temperature [K] | numérica | 200 | 0 | 300.1115 | 300.2000 | 2.0807 | 298.3000 | 301.8000 | 3.5000 | 295.6000 | 304.2000 |
| Process temperature [K] | numérica | 200 | 0 | 310.0475 | 310.1000 | 1.5444 | 308.8000 | 311.1000 | 2.3000 | 306.1000 | 313.8000 |
| Rotational speed [rpm] | numérica | 200 | 0 | 1528.5300 | 1472.0000 | 201.5680 | 1410.5000 | 1611.5000 | 201.0000 | 1278.0000 | 2678.0000 |
| Torque [Nm] | numérica | 200 | 0 | 41.4785 | 43.1000 | 10.6072 | 33.4000 | 49.0500 | 15.6500 | 10.7000 | 66.7000 |
| Tool wear [min] | numérica | 200 | 0 | 112.7750 | 115.0000 | 66.3876 | 57.5000 | 171.5000 | 114.0000 | 0.0000 | 240.0000 |
| Machine failure | numérica | 200 | 0 | 0.0400 | 0.0000 | 0.1965 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| TWF | numérica | 200 | 0 | 0.0150 | 0.0000 | 0.1219 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| HDF | numérica | 200 | 0 | 0.0050 | 0.0000 | 0.0707 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| PWF | numérica | 200 | 0 | 0.0100 | 0.0000 | 0.0997 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| OSF | numérica | 200 | 0 | 0.0150 | 0.0000 | 0.1219 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| RNF | numérica | 200 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Extremos marcados (fora de 1,5 × a caixa — slide 24)

### Extremos de `Rotational speed [rpm]` — 8 valor(es), limites [1109.0000; 1913.0000]

| linha | valor |
|---:|---:|
| 4 | 2678.0000 |
| 54 | 2355.0000 |
| 59 | 2025.0000 |
| 86 | 2009.0000 |
| 91 | 1927.0000 |
| 114 | 2370.0000 |
| 122 | 1931.0000 |
| 133 | 2595.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Mantendo os 8 valores. São rotações fisicamente plausíveis (1927 a 2678
rpm, dentro da faixa de operação do equipamento) e não há indício de erro de
digitação. A análise da D1 já havia concluído que torque e
rotação são inversamente relacionados (potência aproximadamente constante) e
que as falhas se aglomeram nos "cantos extremos" dessa curva, é exatamente
isso que estes 8 pontos registram.
Só a linha 4 (rotação 2678, a mais extrema) coincide com uma falha registrada (Machine failure=1, modo PWF); as outras 7 têm rotação extrema sem falha, o que confirma a conclusão da D1
de que a variável carrega sinal mas não garante falha sozinha.

Remover esses pontos jogaria fora justamente os casos mais informativos
sobre risco, o que vai precisar para bater a regra do desgaste.

### Extremos de `Machine failure` — 8 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 4 | 1.0000 |
| 9 | 1.0000 |
| 23 | 1.0000 |
| 77 | 1.0000 |
| 83 | 1.0000 |
| 89 | 1.0000 |
| 132 | 1.0000 |
| 168 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Mantenho os 8 valores. `Machine failure` é uma variável binária rara (4%
dos registros, exatamente a taxa que a Pergunta 1 da D1 mediu): como mais de
75% das linhas valem 0, Q1 e Q3 colapsam em 0 e a regra da amplitude
interquartil (1,5 × uma caixa de tamanho zero) marca qualquer "1" como
extremo. Isso é um artefato de aplicar uma regra pensada para variáveis
contínuas a uma variável 0/1 — não é erro de dado nem indício de problema de
coleta. Esses "1" são justamente os casos de falha que o projeto existe para
prever; removê-los descartaria a classe de interesse (e infla
artificialmente a acurácia do "nunca falha" que a Pergunta 1 da D1 já alertou
ser enganosa).

### Extremos de `TWF` — 3 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 23 | 1.0000 |
| 83 | 1.0000 |
| 168 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Mantendo os 3 valores, pelo mesmo motivo da `Machine failure` acima: é um
indicador binário de modo de falha (desgaste da ferramenta), ainda mais raro
(1,5% dos registros) — a regra do AIQ aplicada a uma 0/1 marca a minoria como
"extrema" por construção, não por anomalia. As três linhas (23, 83, 168) têm
exatamente um modo marcado cada (só TWF), sem sobreposição com outro modo —
consistente com a Pergunta 5 da D1, que já descrevia os cinco modos como
mecanismos distintos.

### Extremos de `HDF` — 1 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 89 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Mantendo o único valor. Mesmo motivo estrutural das demais variáveis
binárias de modo de falha: `HDF` é o modo mais raro da amostra (0,5% dos
registros), então o seu único "1" sempre vai cair fora da caixa degenerada
[0; 0]. A linha 89 não aparece em nenhum outro modo marcado nem entre os
extremos de rotação, então é um caso de HDF "puro" — condizente com a
Pergunta 4 da D1, que liga HDF ao limiar de diferença de temperatura.

### Extremos de `PWF` — 2 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 4 | 1.0000 |
| 77 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Mantendo os 2 valores, mesmo motivo estrutural das demais binárias. Vale
registrar o que a conferência cruzada mostrou: a linha 4 é justamente a
rotação mais extrema da amostra (2678 rpm, o maior valor marcado em
`Rotational speed [rpm]`) — a confirmação mais direta, nesta amostra, da
física apontada na Pergunta 3 da D1 (PWF nasce no canto extremo da curva
potência-constante). Já a linha 77 tem PWF e OSF marcados ao mesmo tempo,
é o caso concreto de "dois modos simultâneos" que a Pergunta 5 da D1 citava
de forma agregada, sem apontar a linha.

### Extremos de `OSF` — 3 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 9 | 1.0000 |
| 77 | 1.0000 |
| 132 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Mantendo os 3 valores, mesmo motivo estrutural das demais binárias de modo
de falha. A linha 77 repete o caso de sobreposição com `PWF` já registrado
acima (dois modos simultâneos); as linhas 9 e 132 têm só OSF marcado. Nenhuma
das três coincide com os extremos de rotação, o que é consistente com OSF
("overstrain failure") depender também do torque e do desgaste acumulado, não
só da rotação isolada.


## Faltantes (os três mecanismos do slide 26)

Nenhuma variável tem valores faltantes.

## As quatro perguntas do slide 29

**1. Média e mediana se separam em alguma variável? Em qual?**

R: A diferença mais significativa entre média e mediana aparece na variável Rotational speed [rpm]: a média é 1.528,53 rpm e a mediana é 1.472,00 rpm, uma diferença de aproximadamente 56,5 rpm (4%).
Isso indica uma distribuição com cauda à direita, em que valores de rotação muito elevados, principalmente os 8 extremos que chegam a 2.678 rpm, puxam a média para cima.
Nas demais variáveis contínuas, a diferença entre média e mediana é inferior a 2%. Já nas variáveis binárias, essa diferença é esperada, pois representam eventos raros, com predominância de valores 0.

Conclusão: Rotational speed [rpm] apresenta a diferença mais relevante, influenciada pelos valores elevados de rotação.

**2. Quantos extremos foram marcados, e quantos você decidiu manter?**

R: Foram identificados 25 valores extremos, distribuídos da seguinte forma:
8 em Rotational speed [rpm], 8 em Machine failure, 3 em TWF, 1 em HDF, 2 em PWF e 3 em OSF.
Decidi manter todos os 25 registros, sem remover nenhum. Os 8 valores de rotação representam condições reais de funcionamento da máquina, enquanto os outros 17 estão relacionados às variáveis binárias de falhas, classificadas como extremas devido à baixa frequência desses eventos.

Conclusão: Todos os registros foram mantidos por serem dados válidos e relevantes para a análise e a previsão de falhas.

**3. Algum faltante parece do terceiro mecanismo?**

R: Não há como avaliar — esta amostra de 200 linhas não tem nenhuma célula
faltante (0 em todas as 14 variáveis). Isso é esperado: o `FONTE.md` descreve
esta amostra como o fallback offline do curso, uma versão já validada e
versionada; o dataset completo (10.000 linhas, baixado por`scripts/baixar-dados.py`) pode ter faltantes que esta amostra reduzida nãocaptura, então esta resposta vale só para os 200 registros analisados aqui.

**4. O que a análise da D1 não tinha visto?**

R: (1) os números exatos e as linhas de cada extremo — a D1 falou em "cantos extremos" da
curva potência-constante em termos de gráfico de dispersão, mas não listou
linhas; aqui a linha 4 (rotação 2678, `Machine failure`=1, modo PWF) é a
confirmação pontual daquela conclusão.
(2) o caso concreto de dois modos simultâneos que a Pergunta 5 da D1 mencionava de forma agregada agora tem
uma linha exata (77: PWF e OSF juntos).
(3) o artefato metodológico de que a regra do AIQ, pensada para variáveis contínuas, marca automaticamente a minoria de qualquer indicador 0/1 como "extremo" — a D1 nunca aplicou essa
regra às variáveis binárias, então esse ponto é novo aqui.

## Comparação com a análise exploratória da D1

O que mudou de lá para cá — o que a análise de lá não tinha visto,
e o que estas decisões escritas mudam no conjunto que a D5 vai usar:

R: A D1 apresentou uma análise mais geral, utilizando gráficos e distribuições para identificar padrões, como falhas raras, desgaste, valores extremos e modos de falha simultâneos. Já esta análise aplicou critérios estatísticos (quartis e AIQ) para identificar os extremos com maior precisão, apontando os registros específicos.
A principal mudança para a D5 é a decisão de manter os 25 valores extremos, pois representam informações reais de funcionamento ou ocorrências de falhas. Removê-los automaticamente poderia eliminar dados importantes para o treinamento do modelo e prejudicar a previsão de falhas.
