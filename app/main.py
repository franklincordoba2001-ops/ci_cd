"""Punto de entrada de la aplicación."""

import os
import sys

# Asegurar que el directorio raíz esté en sys.path para importaciones locales
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.calculator import add, divide, multiply, subtract  # noqa: E402


def run():
    """Ejecuta una demostración de la calculadora."""
    print("=== Demostración CI/CD con Python ===")
    num1, num2 = 10, 5

    print(f"{num1} + {num2} = {add(num1, num2)}")
    print(f"{num1} - {num2} = {subtract(num1, num2)}")
    print(f"{num1} * {num2} = {multiply(num1, num2)}")
    print(f"{num1} / {num2} = {divide(num1, num2)}")
    print("=== Pipeline ejecutado exitosamente ===")


if __name__ == "__main__":
    run()
