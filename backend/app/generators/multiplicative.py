"""Generador congruencial multiplicativo."""

from dataclasses import dataclass


@dataclass
class MultiplicativeConfig:
    seed: int
    multiplier: int
    modulus: int
    count: int


def generate(config: MultiplicativeConfig) -> list[float]:
    """Return U(0,1) approximations using X[n+1] = a * X[n] mod m."""
    if config.modulus <= 1:
        raise ValueError("El módulo debe ser mayor que 1.")
    if config.count < 1 or config.count > 10_000:
        raise ValueError("La cantidad debe estar entre 1 y 10.000.")
    if config.multiplier <= 0:
        raise ValueError("El multiplicador debe ser mayor que 0.")

    state = config.seed
    values: list[float] = []
    for _ in range(config.count):
        state = (config.multiplier * state) % config.modulus
        values.append(state / (config.modulus-1))
    return values
