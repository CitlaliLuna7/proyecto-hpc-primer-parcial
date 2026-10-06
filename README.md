# EC. Primer Parcial — Proyecto Práctico HPC

## Análisis de Resultados

### 1. ¿La ejecución paralela fue más rápida que la secuencial?
Sí. Al incrementar el número de workers a 2 y 4, el cálculo de $f(x)$ se distribuyó entre múltiples núcleos del procesador, reduciendo el tiempo total de procesamiento en comparación con 1 worker.

### 2. ¿Qué número de workers obtuvo el menor tiempo?
La configuración con **4 workers** registró el menor tiempo de ejecución.

### 3. ¿Duplicar el número de workers duplicó el rendimiento? ¿Por qué?
No exactamente. Debido al **overhead de administración de procesos** (creación de procesos, división de rangos y comunicación IPC), la ganancia de velocidad no escala de manera lineal ideal (Ley de Amdahl).

### 4. ¿Por qué el problema seleccionado puede paralelizarse?
Porque es un problema **"embarazosamente paralelo"** (*Embarrassingly Parallel*). La evaluación de $f(x)$ en cada punto es independiente de las demás iteraciones, sin dependencias de datos ni necesidad de memoria compartida.

### 5. ¿En qué momento agregar más workers deja de ser beneficioso?
Cuando el número de workers supera la cantidad de núcleos físicos/lógicos de la CPU o cuando la carga de datos por worker es tan reducida que el costo de gestionar procesos sobrepasa el tiempo real de cómputo.

### 6. ¿Qué limitaciones tiene el hardware utilizado?
* Cantidad de núcleos físicos y hilos de procesamiento.
* Ancho de banda de memoria RAM al transferir arreglos a la caché de la CPU.
* Estrés térmico (*thermal throttling*) de la laptop.

### 7. ¿Este experimento representa HPC o solamente demuestra principios utilizados en HPC?
**Demuestra principios utilizados en HPC.** Implementa división de dominios, métricas de Speedup y Eficiencia. Sin embargo, un entorno de HPC formal utiliza clústeres multinodo distribuidos con redes de alta velocidad (InfiniBand), MPI y gestores de tareas como SLURM.

## Implementación secuencial

La versión secuencial del programa se encuentra en `src/secuencial.py`.

Esta implementación evalúa la función matemática de manera secuencial, procesando los elementos uno por uno:

f(x) = sqrt(x) + x² + sin(x) + cos(x) + log(x)

El tiempo de ejecución se mide utilizando `time.perf_counter()`, permitiendo posteriormente comparar el rendimiento de la ejecución secuencial con las versiones paralelas.

También se agregaron pruebas automatizadas en `tests/test_secuencial.py` utilizando pytest para verificar que la función matemática produce resultados correctos.
