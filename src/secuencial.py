import math
import time


def evaluar_funcion(x):
    """
    Evalúa la función matemática utilizada en el proyecto.

    f(x) = sqrt(x) + x^2 + sin(x) + cos(x) + log(x)
    """
    return (
        math.sqrt(x)
        + (x ** 2)
        + math.sin(x)
        + math.cos(x)
        + math.log(x)
    )


def ejecutar_secuencial(n_elementos):
    """
    Procesa n_elementos de manera secuencial y devuelve
    los resultados junto con el tiempo de ejecución.
    """
    inicio = time.perf_counter()

    resultados = [
        evaluar_funcion(x)
        for x in range(1, n_elementos + 1)
    ]

    tiempo = time.perf_counter() - inicio

    return resultados, tiempo


if __name__ == "__main__":
    N = 5_000_000

    resultados, tiempo = ejecutar_secuencial(N)

    print("=== EJECUCIÓN SECUENCIAL ===")
    print(f"Elementos procesados: {N:,}")
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos")
