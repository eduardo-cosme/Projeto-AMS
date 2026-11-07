# O mapa do meu domínio — conferência (Laboratório 04)

Conjunto: manutencao · 384 dimensões antes da redução
Escolha registrada (slide 55): normalizado · semente da vizinhança: 20260901
Mapas: mapa-do-espaco-normalizado.png e mapa-do-espaco-sem-normalizar.png (componentes principais à esquerda, vizinhança à direita em cada um — slide 55) · pontos (do conjunto normalizado): mapa-pontos.csv

## Passo 4 — os três pares que escolhido no mapa (slide 52)

| par | cosseno original | a vizinhança visual |
|---|---|---|
| (35, 36) | +0.9780 | confirma |
| (30, 31) | +0.9426 | confirma |
| (60, 77) | +0.1228 | NÃO confirma |

## As quatro perguntas do slide 53

1. Os dois métodos produzem os mesmos agrupamentos?
R: Não exatamente. No PCA os 200 pontos formam uma nuvem quase homogênea,
sem fronteiras visuais claras entre grupos — a variância que as duas
primeiras componentes conseguem capturar de um espaço de 384 dimensões é
pequena, então a estrutura global aparece, mas "achatada". No t-SNE surgem
sub-grupos bem mais compactos e isolados (ex.: os pares (35,36) e (30,31)
ficam colados entre si e separados do resto). Os dois métodos concordam nos
pares mais óbvios — frases quase idênticas, como (35,36) e (30,31), ficam
próximas nos dois mapas — mas discordam no restante: o t-SNE separa em
grupos visuais nítidos conjuntos que no PCA aparecem misturados no meio da
nuvem.

2. Há grupo que só aparece em um deles?
R: Sim. O t-SNE forma pequenos aglomerados quase sobrepostos nas bordas do
mapa (ex.: os índices 33/34 e 136/137 ficam praticamente um em cima do
outro) que não têm equivalente no PCA — lá os mesmos índices aparecem
espalhados dentro da nuvem central, sem nenhum destaque. É o esperado pelo
slide 51: o PCA preserva a variância GLOBAL mas não força agrupamento local;
o t-SNE otimiza exatamente para manter vizinhos próximos, criando clusters
visuais que o PCA não desenha.

3. Os vizinhos visuais confirmam no cosseno original?
R: Dois dos três pares confirmam: (35,36) cos +0,9780 e (30,31) cos +0,9426
— ambas são frases quase idênticas com um verbo trocado pelo oposto
("aperte"/"afrouxe", "abra"/"feche"), então a proximidade visual é real. O
terceiro, (60,77), NÃO confirma: cos +0,1228, mesmo estando entre os vizinhos
mais próximos do mapa de vizinhança (separados por ~4,5 unidades numa
figura que se espalha por mais de 25). "O contato do contator K3 apresentou
soldagem dos contatos principais" e "As correntes da esteira transportadora
receberam lubrificação na terça-feira" não têm nenhuma relação semântica —
equipamentos e ações completamente diferentes.

4. O que aconteceria com um vetor novo, fora do conjunto?
R: Testado com o vetor 105 tratado como novo (`--novo 105`). No mapa de
componentes principais a posição sai na hora, porque a transformação é
FIXA: `(vetor − centro) @ componentes` devolveu (-0,195; 0,242) — exatamente
onde o ponto 105 já estava no mapa original (o teste.py confirma que
`posicionar_novo` reproduz o mapa inteiro, ponto a ponto). No mapa de
vizinhança (t-SNE) não existe essa opção: o método não define uma função de
projeção, então incluir um vetor novo exige refazer o mapa INTEIRO — e,
rodando de novo, as posições dos outros 200 pontos também podem mudar. É a
diferença prática mais importante para um sistema em produção: o PCA aceita
itens novos a custo baixo; a vizinhança, não.

## o caso do mapa (critério do slide 52)

Par e o que a figura sugeria, e o que o cosseno original disse:

R: Par (60, 77). No mapa de vizinhança os dois ficam entre os vizinhos mais
próximos da mesma região do gráfico (tsne=(-12,72; 1,34) e (-14,23; -2,94) —
visivelmente colados perto da borda esquerda, comparado ao espalhamento
total do mapa). A figura sugere que são frases parecidas. Mas o cosseno
original é +0,1228 — praticamente ortogonal: a frase 60 fala de um contator
elétrico que soldou os contatos; a 77 fala de lubrificação da corrente de
uma esteira transportadora. Nenhuma relação real de conteúdo — o t-SNE
colocou os dois próximos porque ambos são "sobras": frases sem vizinhos
semânticos fortes no restante do conjunto acabam empurradas para o mesmo
canto de baixa densidade, não porque sejam parecidas entre si. Confirma o
aviso dos slides 51/52: a vizinhança entre grupos (ou em regiões de baixa
densidade) do t-SNE não é confiável — só a distância DENTRO de um grupo bem
formado é informativa.
