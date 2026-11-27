# O meu dado, com rigor — relatório do Laboratório 03

Conjunto: `casos-ams-60.csv` · 60 linhas · 9 variáveis

Medidas geradas pelo `medidas.py`: desvio padrão amostral (ddof=1),
quartis por interpolação linear, extremos pela regra da amplitude
interquartil — fora de 1,5 × a caixa (slide 24). As medidas são do
programa; as decisões são SUAS. Preencha todos os blocos `R:` e
confira com `python teste.py`.

## Medidas por variável

| variável | tipo | n | faltantes | média | mediana | desvio | Q1 | Q3 | AIQ | mín | máx |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| id_caso | categórica (60 valores; moda: C41) | 60 | 0 | — | — | — | — | — | — | — | — |
| data | categórica (30 valores; moda: 2026-03-18) | 60 | 0 | — | — | — | — | — | — | — | — |
| tipo_maquina | categórica (4 valores; moda: TORNO) | 60 | 0 | — | — | — | — | — | — | — | — |
| idade_meses | numérica | 60 | 0 | 52.1833 | 53.0000 | 28.3067 | 36.0000 | 64.0000 | 28.0000 | 3.0000 | 216.0000 |
| temperatura_c | numérica | 60 | 0 | 65.7617 | 63.0000 | 7.1741 | 61.0000 | 66.6250 | 5.6250 | 58.0000 | 83.0000 |
| vibracao_mm_s | numérica | 60 | 0 | 4.3892 | 3.6500 | 1.9195 | 3.0000 | 5.5750 | 2.5750 | 2.0000 | 8.6000 |
| horas_desde_manutencao | numérica | 60 | 0 | 118.9667 | 107.5000 | 51.7399 | 85.0000 | 152.5000 | 67.5000 | 20.0000 | 230.0000 |
| acao_correta | categórica (3 valores; moda: seguir_operando) | 60 | 0 | — | — | — | — | — | — | — | — |
| falhou_depois | numérica | 60 | 0 | 0.3333 | 0.0000 | 0.4754 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 |

## Extremos marcados (fora de 1,5 × a caixa — slide 24)

### Extremos de `idade_meses` — 1 valor(es), limites [-6.0000; 106.0000]

| linha | valor |
|---:|---:|
| 12 | 216.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: **Manter** (1 valor: C12, 216 meses). É o único candidato a erro de digitação (o seguinte é 80 meses), mas 18 anos é plausível para uma prensa e a regra de decisão do agente **não usa `idade_meses`**, então o valor não afeta nenhuma métrica da AO1. Remover sem evidência de erro seria omissão (slide 25). Pendência: confirmar no registro da máquina antes de qualquer análise que use idade.

### Extremos de `temperatura_c` — 10 valor(es), limites [52.5625; 75.0625]

| linha | valor |
|---:|---:|
| 2 | 81.5000 |
| 6 | 77.5000 |
| 13 | 79.2000 |
| 17 | 76.0000 |
| 21 | 80.0000 |
| 27 | 82.5000 |
| 34 | 79.5000 |
| 41 | 83.0000 |
| 43 | 79.0000 |
| 53 | 81.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: **Manter os 10.** Oito têm rótulo `parar_para_manutencao` (temperatura acima de 78 °C é o motivo da parada) e dois (C06 = 77,5 °C e C17 = 76,0 °C) são `seguir_operando`, controles logo abaixo do limite da regra. São sinal, não erro: removê-los tiraria do conjunto os casos que testam a regra de temperatura. Sem eles (50 casos) o acerto da linha de base iria de 0,783 para 0,740: o número mudaria, mas porque o conjunto deixaria de ter o fenômeno, não porque ficou mais verdadeiro.

## Faltantes (os três mecanismos do slide 26)

Nenhuma variável tem valores faltantes.

## As quatro perguntas do slide 29

**1. Média e mediana se separam em alguma variável? Em qual?**

R: Sim, em `vibracao_mm_s`: média 4,39 contra mediana 3,65 (a média é ~20% maior), por causa da cauda de 14 casos entre 6,8 e 8,6 mm/s. `horas_desde_manutencao` (119,0 contra 107,5) e `temperatura_c` (65,8 contra 63,0) também puxam para cima, pelos extremos de temperatura. `idade_meses` (52,2 contra 53,0) não se separa, mesmo com o valor de 216: a média sozinha não denunciaria esse extremo. Em `vibracao_mm_s` o 1,5×AIQ não marca nada (limite superior 9,44 mm/s, máximo 8,6): a cauda é real, não aberrante.

**2. Quantos extremos foram marcados, e quantos você decidiu manter?**

R: 11 marcados (1 em `idade_meses`, 10 em `temperatura_c`; nenhum em vibração). **Mantive os 11**, pelos motivos acima. Regra adotada: só removo com evidência de erro de medição (sensor travado, unidade errada, valor impossível); aqui não há.

**3. Algum faltante parece do terceiro mecanismo?**

R: Não há faltantes: 0 células vazias nas 9 variáveis. Isso decorre de os casos serem sintéticos (coordenação do curso), não de o sensor real nunca falhar. Em produção, a hipótese que mais preocupa é o terceiro mecanismo (MNAR): um sensor que satura ou desliga justamente com vibração muito alta perderia o dado no caso crítico. Nessa hipótese descartar ou imputar pela média esconderia o alerta; a regra deveria tratar "sem leitura de vibração" como `inspecionar_antes_de_operar`, nunca como `seguir_operando`.

**4. O que a análise da D1 não tinha visto?**

R: **1.** Que a distribuição de vibração tem dois blocos separados por um vazio (5,8 a 6,8 mm/s) e que o limiar de 7,0 mm/s da regra cai dentro da cauda, não ao lado dela: 9 dos 60 casos ficam entre 7,0 e 7,6 mm/s, justamente onde o rótulo correto muda entre parar e inspecionar. **2.** Que o conjunto é desbalanceado em favor de `seguir_operando` (33 de 60, 55%): sempre responder "seguir" já daria 55%, esse é o piso a bater. **3.** Que a taxa de acerto só é interpretável com intervalo: 47/60 = 0,783, IC95% [0,683; 0,883] (notebook).

## Comparação com a análise exploratória da D1

O que mudou de lá para cá — o que a análise de lá não tinha visto,
e o que estas decisões escritas mudam no conjunto que a D5 vai usar:

R: A D1 explorou o AI4I (taxa de falha por tipo, desgaste da ferramenta) e concluiu que a falha é rara (~3-4%) e que acurácia alta ali é fácil e enganosa. Este conjunto de 60 casos é outro objeto: rotula a *decisão correta* e não só o desfecho, e tem 33% de casos com `falhou_depois` = 1, bem acima dos 3,4% do AI4I. Isso muda o que a D5 pode usar: a taxa de base de falha **não** é a do AI4I, e qualquer modelo treinado nele precisa de um conjunto de decisão próprio. As decisões escritas aqui (manter os extremos, não há faltantes, vibração como cauda real) são o que a D5 herda: nenhum extremo foi removido, então o conjunto segue com os 60 casos.
