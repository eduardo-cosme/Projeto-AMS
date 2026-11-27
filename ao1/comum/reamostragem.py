"""Intervalo de confiança por reamostragem — a função que o slide 19 do D3-E3 mostra.

Para que serve
--------------
Os laboratórios de inferência da disciplina (o lab-05 e o E4-B1) calculam com
ela o intervalo de confiança de qualquer métrica medida sobre um conjunto de
casos: taxa de acerto, custo médio, latência no percentil 95. É a mesma ideia
das oito linhas do slide 19 do D3-E3 — sortear com reposição, recalcular a
métrica, olhar os percentis 2,5 e 97,5 — com três compromissos a mais, que
são do kit e não do slide:

  - a SEMENTE é obrigatória (parâmetro só de palavra-chave, sem valor
    padrão): sem ela o professor não consegue conferir o que o aluno
    reportou (regra 11 do `ORDEM-DOS-BRIEFS`). Ela volta no resultado,
    para aparecer no relatório de quem chamou;
  - a estatística é um parâmetro: taxa de sucesso, custo médio e p95 saem
    do mesmo código, como o slide 22 do D3-E3 promete à turma.
    `estatistica=None` significa média, que é o caso do slide;
  - o resultado devolve também a DISTRIBUIÇÃO reamostrada, de que o
    laboratório do E4 precisa para o intervalo da diferença entre duas
    variantes.

Sem estado global: duas chamadas com a mesma semente devolvem o mesmo
resultado, em qualquer ordem. Depende só da biblioteca padrão e do NumPy.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

REPETICOES_PADRAO = 10_000
"""O número de reamostragens do slide 19, explicitado para constar no gabarito."""

Estatistica = Callable[[np.ndarray], float]


@dataclass(frozen=True)
class Intervalo:
    """O resultado de uma reamostragem.

    `inferior` e `superior` são os percentis da distribuição reamostrada
    nos limites do nível pedido; `estimativa` é a estatística calculada
    sobre os dados originais; `distribuicao` é o valor da estatística em
    cada reamostragem (um valor por sorteio); `semente` é a semente usada
    e volta no resultado para que o relatório do aluno a declare.
    """

    inferior: float
    superior: float
    nivel: float
    estimativa: float
    distribuicao: np.ndarray
    repeticoes: int
    semente: int

    @property
    def largura(self) -> float:
        """O quanto o intervalo ocupa — a medida que o lab-05 pede comparar."""
        return self.superior - self.inferior


def intervalo(
    dados,
    estatistica: Estatistica | None = None,
    repeticoes: int = REPETICOES_PADRAO,
    nivel: float = 0.95,
    *,
    semente: int,
) -> Intervalo:
    """O intervalo de confiança de `estatistica(dados)` por reamostragem.

    Recebe os dados (um valor observado por caso — por exemplo, o vetor de
    zeros e uns que o conjunto rotulado de cada aluno já tem), sorteia com
    reposição uma nova amostra do mesmo tamanho, recalcula a estatística e
    repete `repeticoes` vezes; os percentis da distribuição obtida formam
    o intervalo, ao nível `nivel` (0.95 devolve os percentis 2,5 e 97,5 do
    slide). `semente` é obrigatório e é o que torna o resultado conferível.

    Levanta `ValueError` com mensagem clara se a amostra for vazia, se o
    nível ficar fora de (0, 1) ou se o número de repetições for menor que 1.
    """
    dados = np.asarray(dados, dtype=float)
    if dados.size == 0:
        raise ValueError("a amostra está vazia — não há o que reamostrar")
    if estatistica is None:
        estatistica = np.mean
    if repeticoes < 1:
        raise ValueError(f"repeticoes precisa ser >= 1; recebi {repeticoes}")
    if not 0.0 < nivel < 1.0:
        raise ValueError(f"nivel precisa estar entre 0 e 1; recebi {nivel}")

    estimativa = float(estatistica(dados))
    rng = np.random.default_rng(semente)
    n = dados.size
    valores = np.empty(int(repeticoes), dtype=float)
    for i in range(int(repeticoes)):
        sorteio = rng.choice(dados, size=n, replace=True)
        valores[i] = estatistica(sorteio)

    cauda = (1.0 - nivel) / 2.0
    inferior, superior = np.percentile(valores, [100.0 * cauda, 100.0 * (1.0 - cauda)])
    return Intervalo(
        inferior=float(inferior),
        superior=float(superior),
        nivel=float(nivel),
        estimativa=estimativa,
        distribuicao=valores,
        repeticoes=int(repeticoes),
        semente=int(semente),
    )
