"""Agente de linha de base — Laboratório 06 (D2-E4).

Agente reativo-com-estado, SEM modelo de linguagem: percepção (o registro),
decisão (regras explícitas com limiares), ação (a recomendação) e medida
(fração de decisões iguais ao rótulo, sobre 30 casos). É o número de linha
de base contra o qual o agente de D10 será comparado.

Conjunto usado: `d2/lab6/casos-de-reserva.csv` (reserva do curso, 30 casos
de manutenção industrial inventados pela coordenação — ver
`d2/lab6/FONTE.md`). O projeto AMS usa o AI4I2020 como dataset de
referência (ver `agent-spec-modelo.md`), mas esse conjunto não traz uma
ação corretiva rotulada caso a caso — por isso a linha de base deste
laboratório foi medida sobre a reserva, conforme autorizado pelo enunciado
(`d2/lab6/COMO-USAR-A-RESERVA.pdf`).

Métrica primária: acerto da decisão — casos com decisão igual à rotulada,
sobre o total. Valor sobre a reserva: 25/30 = 0.8333.

Uso:
    python -m ams.baseline
"""

from __future__ import annotations

import csv
from collections import Counter
from datetime import date as _date
from pathlib import Path

CAMINHO_DOS_CASOS = Path(__file__).resolve().parents[2] / "d2" / "lab6" / "casos-de-reserva.csv"

LIMITE_VIBRACAO = 7.0          # mm/s — acima disso, para
LIMITE_TEMPERATURA = 78.0      # °C   — acima disso, para
FALHAS_PARA_INSPECAO = 2       # falhas observadas da família → inspecionar
JANELA_DIAS = 7                # "recentes" = dentro desta janela


class EstadoDaFrota:
    """O que o agente já observou: falhas por família, dentro da janela."""

    def __init__(self, janela_dias: int = JANELA_DIAS) -> None:
        self._janela = janela_dias
        self._falhas: list[tuple[str, _date]] = []
        self._ultima_data: _date | None = None

    def falhas_recentes(self, familia: str) -> int:
        """Quantas falhas desta família o agente viu, dentro da janela."""
        if self._ultima_data is None:
            return 0
        limite = self._ultima_data.toordinal() - self._janela
        return sum(
            1 for familia_vista, dia in self._falhas
            if familia_vista == familia and dia.toordinal() >= limite)

    def registrar_desfecho(self, registro: dict) -> None:
        """O ambiente revela o desfecho do caso — a percepção do próximo
        ciclo é maior do que a do anterior (parcialmente observável)."""
        self._ultima_data = _date.fromisoformat(registro["data"])
        if int(registro.get("falhou_depois", 0)) == 1:
            self._falhas.append(
                (registro["tipo_maquina"], self._ultima_data))


def decidir(registro: dict, estado: EstadoDaFrota) -> str:
    """Uma rodada: percepção entra, ação sai. A primeira condição que casar
    decide — a reativa (limiares do registro atual) vem antes da que
    consulta o estado interno (falhas recentes da família)."""
    if registro["vibracao_mm_s"] > LIMITE_VIBRACAO or \
            registro["temperatura_c"] > LIMITE_TEMPERATURA:
        return "parar_para_manutencao"
    if estado.falhas_recentes(registro["tipo_maquina"]) >= FALHAS_PARA_INSPECAO:
        return "inspecionar_antes_de_operar"
    return "seguir_operando"


def carregar_casos(caminho: str | Path) -> list[dict]:
    """Lê o CSV de casos rotulados, em ordem cronológica — a ordem importa,
    porque o estado interno se acumula caso a caso."""
    with Path(caminho).open(encoding="utf-8-sig", newline="") as arquivo:
        casos = list(csv.DictReader(arquivo))
    casos.sort(key=lambda registro: registro["data"])
    for registro in casos:
        registro["idade_meses"] = int(registro["idade_meses"])
        registro["temperatura_c"] = float(registro["temperatura_c"])
        registro["vibracao_mm_s"] = float(registro["vibracao_mm_s"])
        registro["horas_desde_manutencao"] = float(
            registro["horas_desde_manutencao"])
        registro["falhou_depois"] = int(registro["falhou_depois"])
    return casos


def medir(caminho: str | Path = CAMINHO_DOS_CASOS) -> dict:
    """Roda o agente sobre os casos e devolve a métrica primária, o valor e
    o conjunto — as três informações do slide 28 — mais onde ele erra."""
    casos = carregar_casos(caminho)
    estado = EstadoDaFrota()
    acertos = 0
    erros: list[dict] = []
    for registro in casos:
        decisao = decidir(registro, estado)
        correta = registro["acao_correta"]
        if decisao == correta:
            acertos += 1
        else:
            erros.append({"id_caso": registro["id_caso"],
                          "decidiu": decisao, "correta": correta})
        estado.registrar_desfecho(registro)
    total = len(casos)
    return {
        "caminho": str(caminho),
        "total": total,
        "acertos": acertos,
        "valor": acertos / total if total else 0.0,
        "distribuicao": dict(Counter(r["acao_correta"] for r in casos)),
        "erros": erros,
    }


if __name__ == "__main__":
    resultado = medir()
    print("Métrica primária: acerto da decisão "
          "(casos com decisão igual à rotulada, sobre o total)")
    print(f"Valor: {resultado['acertos']}/{resultado['total']} = "
          f"{round(resultado['valor'], 4)}")
    print(f"Conjunto: {resultado['caminho']} — {resultado['total']} casos "
          f"rotulados {resultado['distribuicao']}")
