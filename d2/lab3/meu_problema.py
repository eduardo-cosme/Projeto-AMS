"""Laboratório 03 — caminho padrão: subproblema 2 do catálogo (consultas),
adaptado para o domínio de Gestão de Ordens de Serviço de Manutenção.

A pergunta que o agente precisa responder antes de classificar o risco de
falha de uma máquina e recomendar uma ação: "que fatos eu ainda preciso
levantar sobre esta ordem de serviço?"

Estado: o conjunto de fatos já levantados sobre a ordem de serviço.
Ação: consultar uma fonte (sistema, base de dados ou pessoa).
Transição: os fatos que a fonte devolve se somam aos já sabidos.
Objetivo: ter todos os fatos que a seção 1 (Sensors) do agent-spec.md exige.
Custo: a latência da consulta (segundos).

Os dados trocam os do exemplo de férias pelos do domínio — a classe
`Consultas`, importada do catálogo, não muda uma linha.
"""

from __future__ import annotations

import sys
from pathlib import Path

_AQUI = Path(__file__).resolve().parent
for _pasta in (_AQUI, *_AQUI.parents):
    if (_pasta / "comum" / "busca.py").is_file():
        sys.path.insert(0, str(_pasta / "comum"))
        break

from problemas.consultas import Consultas, Fonte  # noqa: E402

# Os quatro fatos que a seção 1 (Sensors) do agent-spec.md já lista como o
# que o agente enxerga: sem eles, a classificação de risco não tem base.
FATOS_NECESSARIOS: frozenset[str] = frozenset({
    "leitura atual dos sensores da máquina",
    "histórico de falhas da máquina (AI4I 2020)",
    "descrição da intervenção escrita pelo técnico",
    "normas regulamentares aplicáveis (NR-10, NR-12, NR-35)",
})

FONTES: tuple[Fonte, ...] = (
    Fonte("painel de telemetria da máquina", 0.5,
          ("leitura atual dos sensores da máquina",)),
    Fonte("sistema de ordens de serviço — texto do técnico", 1.0,
          ("descrição da intervenção escrita pelo técnico",)),
    Fonte("prontuário completo da máquina", 4.0,
          ("leitura atual dos sensores da máquina",
           "histórico de falhas da máquina (AI4I 2020)")),
    Fonte("biblioteca de normas regulamentares (NR-10/12/35)", 3.0,
          ("normas regulamentares aplicáveis (NR-10, NR-12, NR-35)",)),
    Fonte("atendimento humano do engenheiro de segurança", 20.0,
          ("leitura atual dos sensores da máquina",
           "histórico de falhas da máquina (AI4I 2020)",
           "descrição da intervenção escrita pelo técnico",
           "normas regulamentares aplicáveis (NR-10, NR-12, NR-35)")),
)

MEU_PROBLEMA = Consultas(FATOS_NECESSARIOS, FONTES)


if __name__ == "__main__":
    import importlib.util

    teste = importlib.util.spec_from_file_location(
        "verificar-formulacao",
        Path(__file__).resolve().parent / "verificar-formulacao.py")
    modulo = importlib.util.module_from_spec(teste)
    sys.modules["verificar-formulacao"] = modulo
    teste.loader.exec_module(modulo)
    raise SystemExit(modulo.main([str(Path(__file__)) + ":MEU_PROBLEMA"]))
