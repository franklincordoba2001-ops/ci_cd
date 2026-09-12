"""Módulo de calculadora con operaciones matemáticas básicas."""


def add(a: float, b: float) -> float:
    """Calcula la suma de dos números."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Calcula la resta de dos números."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Calcula la multiplicación de dos números."""
    return a * b


def divide(a: float, b: float) -> float:
    """Calcula la división de dos números. Lanza ValueError si b es 0."""
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b
