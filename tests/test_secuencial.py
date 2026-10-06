import math

from src.secuencial import evaluar_funcion


def test_evaluar_funcion():
    x = 5

    esperado = (
        math.sqrt(x)
        + (x ** 2)
        + math.sin(x)
        + math.cos(x)
        + math.log(x)
    )

    resultado = evaluar_funcion(x)

    assert math.isclose(resultado, esperado, rel_tol=1e-9)
