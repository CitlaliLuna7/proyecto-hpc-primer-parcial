import statistics
import sys
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import proyecto_hpc


WORKERS = [1, 2, 4]
REPETICIONES = 3
N_ELEMENTOS = 5_000_000

RESULTADOS_DIR = ROOT / "resultados"


def ejecutar_benchmark():
    RESULTADOS_DIR.mkdir(exist_ok=True)

    resultados = {}

    print("=== BENCHMARK HPC ===")
    print(f"Número de elementos: {N_ELEMENTOS:,}")
    print()

    for workers in WORKERS:
        tiempos = []

        print(f"Evaluando con {workers} worker(s)...")

        for prueba in range(REPETICIONES):
            tiempo = proyecto_hpc.ejecucion_paralela(
                N_ELEMENTOS,
                workers
            )

            tiempos.append(tiempo)

            print(
                f"  Prueba {prueba + 1}: "
                f"{tiempo:.6f} segundos"
            )

        resultados[workers] = tiempos
        print()

    promedios = {
        workers: statistics.mean(tiempos)
        for workers, tiempos in resultados.items()
    }

    tiempo_base = promedios[1]

    metricas = {}

    print("=== MÉTRICAS DE RENDIMIENTO ===")
    print()

    for workers in WORKERS:
        promedio = promedios[workers]
        speedup = tiempo_base / promedio
        eficiencia = speedup / workers

        metricas[workers] = {
            "tiempo": promedio,
            "speedup": speedup,
            "eficiencia": eficiencia
        }

        print(f"Workers: {workers}")
        print(f"Tiempo promedio: {promedio:.6f} segundos")
        print(f"Speedup: {speedup:.4f}")
        print(f"Eficiencia: {eficiencia * 100:.2f}%")
        print()

    # Guardar resultados en archivo
    archivo_resultados = RESULTADOS_DIR / "benchmark.txt"

    with open(archivo_resultados, "w", encoding="utf-8") as archivo:
        archivo.write("=== BENCHMARK HPC ===\n")
        archivo.write(f"Número de elementos: {N_ELEMENTOS:,}\n")
        archivo.write(f"Repeticiones por configuración: {REPETICIONES}\n\n")

        for workers in WORKERS:
            archivo.write(f"Workers: {workers}\n")
            archivo.write(
                f"Tiempo promedio: "
                f"{metricas[workers]['tiempo']:.6f} segundos\n"
            )
            archivo.write(
                f"Speedup: "
                f"{metricas[workers]['speedup']:.4f}\n"
            )
            archivo.write(
                f"Eficiencia: "
                f"{metricas[workers]['eficiencia'] * 100:.2f}%\n"
            )
            archivo.write("\n")

    # Datos para las gráficas
    tiempos = [metricas[w]["tiempo"] for w in WORKERS]
    speedups = [metricas[w]["speedup"] for w in WORKERS]
    eficiencias = [
        metricas[w]["eficiencia"] * 100
        for w in WORKERS
    ]

    # Gráfica de tiempo
    plt.figure()
    plt.plot(WORKERS, tiempos, marker="o")
    plt.xlabel("Número de workers")
    plt.ylabel("Tiempo promedio (segundos)")
    plt.title("Workers vs Tiempo de ejecución")
    plt.grid(True)
    plt.savefig(
        RESULTADOS_DIR / "workers_vs_tiempo.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    # Gráfica de speedup
    plt.figure()
    plt.plot(WORKERS, speedups, marker="o")
    plt.xlabel("Número de workers")
    plt.ylabel("Speedup")
    plt.title("Workers vs Speedup")
    plt.grid(True)
    plt.savefig(
        RESULTADOS_DIR / "workers_vs_speedup.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    # Gráfica de eficiencia
    plt.figure()
    plt.plot(WORKERS, eficiencias, marker="o")
    plt.xlabel("Número de workers")
    plt.ylabel("Eficiencia (%)")
    plt.title("Workers vs Eficiencia")
    plt.grid(True)
    plt.savefig(
        RESULTADOS_DIR / "workers_vs_eficiencia.png",
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

    print("Resultados guardados en:")
    print(archivo_resultados)

    print("\nGráficas generadas:")
    print("  resultados/workers_vs_tiempo.png")
    print("  resultados/workers_vs_speedup.png")
    print("  resultados/workers_vs_eficiencia.png")


if __name__ == "__main__":
    ejecutar_benchmark()
