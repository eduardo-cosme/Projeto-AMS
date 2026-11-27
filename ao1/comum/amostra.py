"""Tamanho de amostra e poder — a conta por trás do slide 33 do D3-E3.

Duas perguntas, nos dois desenhos:

  - QUANTOS CASOS para detectar uma diferença de tamanho dado, com poder e
    significância dados — no desenho pareado (as duas versões sobre os
    mesmos casos, o teste de McNemar) e no não pareado (grupos de casos
    diferentes). É `casos_para_diferenca`, e o slide 33 compara os dois
    desenhos lado a lado;
  - QUE PODER um número de casos compram para detectar uma diferença dada.
    É `poder_para` — é esta que o aluno usa para descobrir o que os
    sessenta casos dele compram (D3-E4, a conclusão "não sei ainda").

A tabela do slide 33 do D3-E3 é a saída de `casos_para_diferenca` com
taxa de base 0,70 (poder 80%, significância 5%, correlação 0,70). A taxa
de base é parâmetro do DOMÍNIO — a taxa de acerto do agente que se está
avaliando —, não constante do curso; por isso ela é argumento
obrigatório aqui, sem valor padrão: quem chama a função declara a taxa
que mede.

Fórmulas (as padrão da literatura, com as contas à vista):

  - grupos independentes, n casos por versão, taxas p0 (base) e p1 = p0+δ:

        n = [ z(1−α/2)·√(2·p̄·q̄) + z(1−β)·√(p0·q0 + p1·q1) ]² / δ²

    com p̄ = (p0+p1)/2 (Montgomery & Runger, caps. 9–10 — a referência do
    deck; Fleiss, Statistical Methods for Rates and Proportions). O slide
    33 conta AVALIAÇÕES: o total é 2n.

  - pareado (McNemar), n pares de casos:

        n = [ z(1−α/2)·√(pd) + z(1−β)·√(pd − δ²) ]² / δ²

    com pd a proporção de pares discordantes, derivada da correlação r
    entre as respostas das duas versões (Connett et al., 1987; Connor,
    1987 — a família que a pesquisa P02 cita). O padrão `correlacao=0.70`
    é o valor usado pela P02.

As inversas da normal vêm de `statistics.NormalDist` (biblioteca padrão),
para a conta ficar reproduzível sem dependência além do próprio Python.

Sem estado global. Não há rede aqui — nada deste módulo chama nada de fora.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import NormalDist

CORRELACAO_PADRAO = 0.70
"""A correlação entre as respostas das duas versões nos mesmos casos, com que
a P02 dimensionou a coluna pareada do slide 33."""


@dataclass(frozen=True)
class Dimensionamento:
    """O que um salto de desempenho exige, nos dois desenhos.

    `casos_independentes` é por VERSÃO; `avaliacoes_independentes` é o
    total de invocações (2n) — a unidade que a coluna "casos independentes"
    do slide 33 reporta. `casos_pareados` são os casos partilhados pelas
    duas versões, cada caso produzindo um par. `discordantes_esperados`
    é o número de discordâncias que a correlação declarada prediz entre os
    casos pareados — o regime em que o teste exato do `comparar` vai rodar.
    """

    diferenca: float
    taxa_base: float
    poder: float
    significancia: float
    correlacao: float
    casos_independentes: int
    casos_pareados: int
    discordantes_esperados: float

    @property
    def avaliacoes_independentes(self) -> int:
        return 2 * self.casos_independentes

    @property
    def economia_do_pareamento(self) -> float:
        """Quanto o pareamento economiza de invocações, na leitura do slide 33."""
        return 1.0 - self.casos_pareados / self.avaliacoes_independentes


def casos_para_diferenca(
    diferenca: float,
    taxa_base: float,
    poder: float = 0.80,
    significancia: float = 0.05,
    correlacao: float = CORRELACAO_PADRAO,
) -> Dimensionamento:
    """Quantos casos para detectar `diferenca` com o poder pedido, nos dois desenhos.

    `diferenca` é o salto absoluto de taxa a detectar (0.05 = cinco pontos
    percentuais), a partir de `taxa_base`. `significancia` é bilateral.
    Arredonda para cima: número de casos é inteiro, e faltar caso custa
    poder. Levanta `ValueError` com mensagem clara para argumentos fora de
    faixa (diferença não positiva, taxa base fora de (0, 1), poder ou
    significância fora de (0, 1), correlação fora de [0, 1) ou
    incompatível com a diferença pedida).
    """
    _validar(diferenca, taxa_base, poder, significancia, correlacao)
    p0 = taxa_base
    p1 = p0 + diferenca
    z_alfa = NormalDist().inv_cdf(1.0 - significancia / 2.0)
    z_beta = NormalDist().inv_cdf(poder)

    p_barra = (p0 + p1) / 2.0
    q_barra = 1.0 - p_barra
    var_nula = 2.0 * p_barra * q_barra
    var_alternativa = p0 * (1.0 - p0) + p1 * (1.0 - p1)
    soma = z_alfa * math.sqrt(var_nula) + z_beta * math.sqrt(var_alternativa)
    independentes = math.ceil(soma**2 / diferenca**2)

    discordancia = _proporcao_discordante(p0, diferenca, correlacao)
    soma_pareada = z_alfa * math.sqrt(discordancia) + z_beta * math.sqrt(
        discordancia - diferenca**2
    )
    pareados = math.ceil(soma_pareada**2 / diferenca**2)

    return Dimensionamento(
        diferenca=diferenca,
        taxa_base=p0,
        poder=poder,
        significancia=significancia,
        correlacao=correlacao,
        casos_independentes=independentes,
        casos_pareados=pareados,
        discordantes_esperados=discordancia * pareados,
    )


def poder_para(
    casos: int,
    diferenca: float,
    taxa_base: float,
    significancia: float = 0.05,
    correlacao: float = CORRELACAO_PADRAO,
    *,
    desenho: str = "pareado",
) -> float:
    """Que poder `casos` compram para detectar `diferenca`, no desenho pedido.

    `desenho` é `"pareado"` (o padrão da disciplina: `casos` são os casos
    partilhados, um par por caso) ou `"independente"` (`casos` são os
    casos de CADA versão, grupos diferentes). Devolve a probabilidade de o
    teste do desenho rejeitar a igualdade quando o salto verdadeiro é
    `diferenca`. É a conta que responde "o que os sessenta casos compram".
    """
    _validar(diferenca, taxa_base, 0.5, significancia, correlacao)
    if casos < 1:
        raise ValueError(f"casos precisa ser >= 1; recebi {casos}")
    if desenho not in ("pareado", "independente"):
        raise ValueError(
            f"desenho é 'pareado' ou 'independente'; recebi {desenho!r}"
        )
    p0 = taxa_base
    p1 = p0 + diferenca
    z_alfa = NormalDist().inv_cdf(1.0 - significancia / 2.0)
    raiz_n = math.sqrt(casos)

    if desenho == "pareado":
        discordancia = _proporcao_discordante(p0, diferenca, correlacao)
        desvio = math.sqrt(discordancia - diferenca**2)
        numerador = diferenca * raiz_n - z_alfa * math.sqrt(discordancia)
    else:
        p_barra = (p0 + p1) / 2.0
        desvio = math.sqrt(p0 * (1.0 - p0) + p1 * (1.0 - p1))
        numerador = diferenca * raiz_n - z_alfa * math.sqrt(2.0 * p_barra * (1.0 - p_barra))
    return NormalDist().cdf(numerador / desvio)


def _proporcao_discordante(p0: float, diferenca: float, correlacao: float) -> float:
    """A fração de pares discordantes que a correlação r prediz.

    Da correlação entre as respostas das duas versões sai a proporção de
    casos em que ambas acertam; o resto se decompõe nas duas casas de
    discordância. Sem discordância não há teste — se a correlação pedida
    tornar o desenho impossível (ela não cabe dentro de [0, 1) ou deixa as
    casas negativas), o erro é explícito, nunca silencioso.
    """
    if not 0.0 <= correlacao < 1.0:
        raise ValueError(
            f"correlacao precisa estar em [0, 1); recebi {correlacao}"
        )
    p1 = p0 + diferenca
    covariancia = correlacao * math.sqrt(p0 * (1.0 - p0) * p1 * (1.0 - p1))
    ambos_acertam = p0 * p1 + covariancia
    # dentro do que as margens permitem
    ambos_acertam = min(ambos_acertam, p0, p1)
    ambos_acertam = max(ambos_acertam, max(0.0, p0 + p1 - 1.0), 0.0)
    so_b = p1 - ambos_acertam
    so_a = p0 - ambos_acertam
    discordancia = so_a + so_b
    if discordancia <= diferenca**2:
        raise ValueError(
            f"a correlacao {correlacao} deixa o desenho sem variação para o "
            f"teste (proporção discordante {discordancia:.4f} com diferença "
            f"{diferenca}); declare uma correlação menor"
        )
    return discordancia


def _validar(
    diferenca: float,
    taxa_base: float,
    poder: float,
    significancia: float,
    correlacao: float,
) -> None:
    if not 0.0 < diferenca:
        raise ValueError(
            f"diferenca é o salto a detectar, em pontos, e precisa ser > 0; "
            f"recebi {diferenca}"
        )
    if not 0.0 < taxa_base < 1.0 or not 0.0 < taxa_base + diferenca < 1.0:
        raise ValueError(
            f"a taxa base e a base+diferença precisam estar em (0, 1); "
            f"recebi taxa_base={taxa_base} e diferenca={diferenca}"
        )
    if not 0.0 < poder < 1.0:
        raise ValueError(f"poder precisa estar em (0, 1); recebi {poder}")
    if not 0.0 < significancia < 1.0:
        raise ValueError(
            f"significancia precisa estar em (0, 1); recebi {significancia}"
        )
    if not 0.0 <= correlacao < 1.0:
        raise ValueError(
            f"correlacao precisa estar em [0, 1); recebi {correlacao}"
        )
