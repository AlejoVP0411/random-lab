"""Prueba de corridas arriba y abajo (runs up/down)."""

from math import sqrt


def run(values: list[float]) -> dict:
    n = len(values)
    if n < 2:
        raise ValueError("La prueba de corridas requiere al menos 2 números.")
    runs = 1
    directions = []
    for previous, current in zip(values, values[1:]):
        direction = current > previous
        directions.append(direction)
    for previous, current in zip(directions, directions[1:]):
        if current != previous:
            runs += 1
    expected = (2 * n - 1) / 3
    variance = (16 * n - 29) / 90
    z = (runs - expected) / sqrt(variance)
    critical = 1.96
    return {
        "name": "Corridas arriba y abajo",
        "statistic": round(z, 4),
        "critical_value": critical,
        "alpha": 0.05,
        "passed": abs(z) < critical,
        "message": "No se rechaza la hipótesis de aleatoriedad." if abs(z) < critical else "Se rechaza la hipótesis de aleatoriedad.",
        "details": [{"category": "Corridas observadas", "observed": runs, "expected": round(expected, 3), "contribution": round(z, 4)}],
    }
