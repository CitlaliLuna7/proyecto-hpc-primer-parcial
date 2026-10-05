import math
import time
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt
import numpy as np

def evaluar_funcion(x):
    return math.sqrt(x) + (x ** 2) + math.sin(x) + math.cos(x) + math.log(x)

def evaluar_bloque(inicio, fin):
    return [evaluar_funcion(x) for x in range(inicio, fin)]

def ejecucion_paralela(n_elementos, num_workers):
    t0 = time.perf_counter()
    tamano_bloque = n_elementos // num_workers
    rangos = []
    for i in range(num_workers):
        inicio = 1 + i * tamano_bloque
        fin = 1 + (i + 1) * tamano_bloque if i < num_workers - 1 else n_elementos + 1
        rangos.append((inicio, fin))
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(evaluar_bloque, inicio, fin) for inicio, fin in rangos]
        _ = [f.result() for f in futures]
        
    return time.perf_counter() - t0

if __name__ == '__main__':
    N = 5_000_000
    WORKERS_LIST = [1, 2, 4]
    REPETICIONES = 3

    print(f"=== INICIANDO EXPERIMENTO HPC (N = {N:,} elementos) ===")
    tiempos = {w: [] for w in WORKERS_LIST}
    promedios = {}

    for w in WORKERS_LIST:
        print(f"\nEvaluando con {w} worker(s)...")
        for i in range(REPETICIONES):
            t = ejecucion_paralela(N, w)
            tiempos[w].append(t)
            print(f"  Prueba {i+1}: {t:.4f} s")
        promedios[w] = np.mean(tiempos[w])
        print(f"  -> Tiempo promedio: {promedios[w]:.4f} s")

    T1 = promedios[1]
    speedups = {w: T1 / promedios[w] for w in WORKERS_LIST}
    eficiencias = {w: speedups[w] / w for w in WORKERS_LIST}

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))

    axes[0].plot(WORKERS_LIST, [promedios[w] for w in WORKERS_LIST], 'ro-', linewidth=2)
    axes[0].set_title("Workers vs. Tiempo de Ejecución")
    axes[0].set_xlabel("Número de Workers")
    axes[0].set_ylabel("Tiempo Promedio (s)")
    axes[0].grid(True)

    axes[1].plot(WORKERS_LIST, [speedups[w] for w in WORKERS_LIST], 'bs-', linewidth=2, label="Speedup Real")
    axes[1].plot(WORKERS_LIST, WORKERS_LIST, 'g--', label="Speedup Ideal (Lineal)")
    axes[1].set_title("Workers vs. Speedup ($S_p$)")
    axes[1].set_xlabel("Número de Workers")
    axes[1].set_ylabel("Speedup ($T_1 / T_p$)")
    axes[1].legend()
    axes[1].grid(True)

    axes[2].plot(WORKERS_LIST, [eficiencias[w] * 100 for w in WORKERS_LIST], 'g^-', linewidth=2)
    axes[2].set_title("Workers vs. Eficiencia ($E_p$)")
    axes[2].set_xlabel("Número de Workers")
    axes[2].set_ylabel("Eficiencia (%)")
    axes[2].grid(True)

    plt.tight_layout()
    plt.savefig("graficas_rendimiento.png", dpi=300)
    print("\n[+] Gráficas generadas y guardadas como 'graficas_rendimiento.png'")
