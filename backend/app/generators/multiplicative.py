"""Generador congruencial multiplicativo."""

from dataclasses import dataclass


@dataclass
class MultiplicativeConfig:
    seed: int
    multiplier: int
    modulus: int
    count: int


def generate(config: MultiplicativeConfig) -> list[float]:
    """Genera números pseudoaleatorios mediante el método congruencial multiplicativo."""

    # ---------------------------------------------------------
    # VALIDACIÓN DE LA SEMILLA
    # X0 debe ser impar: X0 = 2n + 1
    # ---------------------------------------------------------
    if config.seed <= 0:
        raise ValueError("La semilla debe ser mayor que 0.")

    if config.seed % 2 == 0:
        raise ValueError(
            "La semilla debe ser impar, es decir, cumplir X0 = 2n + 1."
        )

    # ---------------------------------------------------------
    # VALIDACIÓN DEL MULTIPLICADOR
    # a debe cumplir:
    # a = 8t + 3  ó  a = 8t + 5
    #
    # Equivalente a:
    # a % 8 == 3 ó a % 8 == 5
    # ---------------------------------------------------------
    if config.multiplier <= 0:
        raise ValueError("El multiplicador debe ser mayor que 0.")

    if config.multiplier % 8 not in (3, 5):
        raise ValueError(
            "El multiplicador debe cumplir a = 8t + 3 o a = 8t + 5."
        )

    # ---------------------------------------------------------
    # VALIDACIÓN DEL MÓDULO
    # m debe ser una potencia de 2:
    # m = 2^k
    # ---------------------------------------------------------
    if config.modulus <= 1:
        raise ValueError("El módulo debe ser mayor que 1.")

    if (config.modulus & (config.modulus - 1)) != 0:
        raise ValueError(
            "El módulo debe ser una potencia de 2, es decir, m = 2^k."
        )

    # Calculamos k a partir del módulo.
    k = config.modulus.bit_length() - 1

    # ---------------------------------------------------------
    # VALIDACIÓN DE LA CANTIDAD
    #
    # N <= 2^(k-2)
    # ---------------------------------------------------------
    if k < 2:
        raise ValueError(
            "El módulo debe permitir calcular 2^(k-2)."
        )

    max_count = 2 ** (k - 2)

    if config.count < 1:
        raise ValueError("La cantidad debe ser como mínimo 1.")

    if config.count > max_count:
        raise ValueError(
            f"La cantidad de números no puede superar {max_count} "
            f"para un módulo de {config.modulus} (k = {k})."
        )

    # ---------------------------------------------------------
    # GENERACIÓN
    # X[n+1] = (a * X[n]) mod m
    # ---------------------------------------------------------
    state = config.seed
    values: list[float] = []

    for _ in range(config.count):
        state = (config.multiplier * state) % config.modulus
        values.append(state / (config.modulus - 1))

    return values