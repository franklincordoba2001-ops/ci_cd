"""Pruebas unitarias para app.calculator."""

import pytest
from app.calculator import add, divide, multiply, subtract


def test_add():
    """Verifica que la suma funcione correctamente."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    """Verifica que la resta funcione correctamente."""
    assert subtract(10, 4) == 6
    assert subtract(5, 10) == -5


def test_multiply():
    """Verifica que la multiplicación funcione correctamente."""
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    assert multiply(5, 0) == 0


def test_divide():
    """Verifica la división y el manejo de excepción por división entre cero."""
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3

    with pytest.raises(ValueError, match="No se puede dividir por cero"):
        divide(10, 0)
