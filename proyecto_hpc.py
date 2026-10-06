import math
import time
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt
import numpy as np


def evaluar_funcion(x):
    return math.sqrt(x) + (x ** 2) + math.sin(x) + math.cos(x) + math.log(x)


def evaluar_bloque(inicio, fin):
    return [evaluar_funcion(x) for x in range(inicio, fin)]


def ejecucion_secuencial(n_elementos):
    inicio = time.perf_counter()

    for x in range(1, n_elementos + 1):
        evaluar_funcion(x)

    return time.perf_counter() - inicio


def ejecucion_paralela(n_elementos, num_workers):
    inicio = time.perf_counter()

    tamano_bloque = n_elementos // num_workers
    rangos = []

    for i in range(num_workers):
        inicio_bloque = 1 + i * tamano_bloque

        if i < num_workers - 1:
            fin_bloque = 1 + (i + 1) * tamano_bloque
        else:
            fin_bloque = n_elementos + 1

        rangos.append((inicio_bloque, fin_bloque))

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(evaluar_bloque, inicio_bloque, fin_bloque)
            for inicio_bloque, fin_bloque in rangos
        ]

        for future in futures:
            future.result()

    return time.perf_counter() - inicio


if __name__ == "__main__":

    N = 5_000_000
    WORKERS_LIST = [1, 2, 4]
    REPETICIONES = 3

    print("=" * 60)
    print("COMPARACIÓN SECUENCIAL VS. PARALELA")
    print(f"Número de elementos: {N:,}")
    print("=" * 60)

    # ---------------------------------------------------------
    # EJECUCIÓN SECUENCIAL
    # ---------------------------------------------------------

    tiempos_secuencial = []

    print("\nEjecutando versión secuencial...")

    for i in range(REPETICIONES):
        tiempo = ejecucion_secuencial(N)
        tiempos_secuencial.append(tiempo)

        print(f"  Prueba {i + 1}: {tiempo:.4f} segundos")

    tiempo_secuencial = np.mean(tiempos_secuencial)

    print(f"\nTiempo secuencial promedio: {tiempo_secuencial:.4f} segundos")

    # ---------------------------------------------------------
    # EJECUCIÓN PARALELA
    # ---------------------------------------------------------

    tiempos = {workers: [] for workers in WORKERS_LIST}
    promedios = {}

    print("\nEjecutando versión paralela...")

    for workers in WORKERS_LIST:

        print(f"\nEvaluando con {workers} worker(s)...")

        for i in range(REPETICIONES):

            tiempo = ejecucion_paralela(N, workers)

            tiempos[workers].append(tiempo)

            print(
                f"  Prueba {i + 1}: "
                f"{tiempo:.4f} segundos"
            )

        promedios[workers] = np.mean(tiempos[workers])

        print(
            f"  Tiempo promedio: "
            f"{promedios[workers]:.4f} segundos"
        )

    # ---------------------------------------------------------
    # SPEEDUP Y EFICIENCIA
    # ---------------------------------------------------------

    speedups = {}
    eficiencias = {}

    for workers in WORKERS_LIST:

        speedups[workers] = (
            tiempo_secuencial / promedios[workers]
        )

        eficiencias[workers] = (
            speedups[workers] / workers
        )

    # ---------------------------------------------------------
    # TABLA DE RESULTADOS
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("RESULTADOS")
    print("=" * 70)

    print(
        f"{'Configuración':<18}"
        f"{'Tiempo (s)':<15}"
        f"{'Speedup':<15}"
        f"{'Eficiencia':<15}"
    )

    print("-" * 70)

    print(
        f"{'Secuencial':<18}"
        f"{tiempo_secuencial:<15.4f}"
        f"{'1.00':<15}"
        f"{'100.00%':<15}"
    )

    for workers in WORKERS_LIST:

        print(
            f"{workers} workers{'':<9}"
            f"{promedios[workers]:<15.4f}"
            f"{speedups[workers]:<15.2f}"
            f"{eficiencias[workers] * 100:<15.2f}%"
        )

    print("=" * 70)

    # ---------------------------------------------------------
    # GRÁFICA 1: TIEMPO SECUENCIAL VS. PARALELO
    # ---------------------------------------------------------

    configuraciones = ["Secuencial", "1 worker", "2 workers", "4 workers"]

    tiempos_grafica = [
        tiempo_secuencial,
        promedios[1],
        promedios[2],
        promedios[4]
    ]

    plt.figure(figsize=(9, 5))

    plt.bar(configuraciones, tiempos_grafica)

    plt.title("Comparación de tiempo: secuencial vs. paralelo")
    plt.xlabel("Configuración")
    plt.ylabel("Tiempo promedio (segundos)")

    plt.grid(axis="y")

    plt.tight_layout()

    plt.savefig(
        "comparacion_secuencial_paralelo.png",
        dpi=300
    )

    plt.show()

    # ---------------------------------------------------------
    # GRÁFICA 2: SPEEDUP
    # ---------------------------------------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(
        WORKERS_LIST,
        [speedups[w] for w in WORKERS_LIST],
        "o-",
        label="Speedup real"
    )

    plt.plot(
        WORKERS_LIST,
        WORKERS_LIST,
        "--",
        label="Speedup ideal"
    )

    plt.title("Speedup de la ejecución paralela")
    plt.xlabel("Número de workers")
    plt.ylabel("Speedup")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    plt.savefig(
        "speedup.png",
        dpi=300
    )

    plt.show()

    print("\nExperimento terminado correctamente.")
    print("Se generaron las gráficas:")
    print("- comparacion_secuencial_paralelo.png")
    print("- speedup.png")
