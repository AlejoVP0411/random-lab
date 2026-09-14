"""Generador no congruencial de productos medios."""

from dataclasses import dataclass


@dataclass
class MiddleProductConfig:
    seed_a: int
    seed_b: int
    digits: int
    count: int


def generate(config: MiddleProductConfig) -> list[float]:
    """Generate values by extracting the central digits of successive products."""
    if config.digits < 2 or config.digits > 8:
        raise ValueError("Los dígitos deben estar entre 2 y 8.")
    if config.count < 1 or config.count > 10_000:
        raise ValueError("La cantidad debe estar entre 1 y 10.000.")

    width = config.digits
    limit = 10 ** width
    x0, x1 = config.seed_a % limit, config.seed_b % limit
    values: list[float] = []
    for _ in range(config.count):
        product = f"{x0 * x1:0{width * 2}d}"
        start = (len(product) - width) // 2
        middle = int(product[start:start + width])
        values.append(middle / limit)
        x0, x1 = x1, middle
    return values
