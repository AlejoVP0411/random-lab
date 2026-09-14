"""Prueba de póker usando grupos de cinco decimales."""

from collections import Counter
from math import comb


def _category(digits: str) -> str:
    counts = sorted(Counter(digits).values(), reverse=True)
    if counts == [5]:
        return "Quintilla"
    if counts == [4, 1]:
        return "Póker"
    if counts == [3, 2]:
        return "Full house"
    if counts == [3, 1, 1]:
        return "Tercia"
    if counts == [2, 2, 1]:
        return "Dos pares"
    if counts == [2, 1, 1, 1]:
        return "Un par"
    return "Todos distintos"


def run(values: list[float]) -> dict:
    categories = ["Todos distintos", "Un par", "Dos pares", "Tercia", "Full house", "Póker", "Quintilla"]
    probabilities = {
        "Todos distintos": 0.3024,
        "Un par": 0.5040,
        "Dos pares": 0.1080,
        "Tercia": 0.0720,
        "Full house": 0.0090,
        "Póker": 0.0045,
        "Quintilla": 0.0001,
    }
    observed = Counter(_category(f"{value:.5f}".split(".")[1]) for value in values)
    n = len(values)
    rows = []
    chi_square = 0.0
    for category in categories:
        expected = n * probabilities[category]
        actual = observed[category]
        contribution = ((actual - expected) ** 2 / expected) if expected else 0
        chi_square += contribution
        rows.append({"category": category, "observed": actual, "expected": round(expected, 3), "contribution": round(contribution, 4)})
    # 6 grados de libertad; valor crítico aproximado para alfa 0.05.
    critical = 12.592
    return {
        "name": "Prueba de Póker",
        "statistic": round(chi_square, 4),
        "critical_value": critical,
        "alpha": 0.05,
        "passed": chi_square < critical,
        "message": "No se rechaza la hipótesis de aleatoriedad." if chi_square < critical else "Se rechaza la hipótesis de aleatoriedad.",
        "details": rows,
    }
