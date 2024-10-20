# Algoritmo Genético para el Problema de las N-Reinas

Este proyecto implementa un algoritmo genético para resolver el clásico problema de las n-reinas. El objetivo es encontrar una disposición en la que N reinas puedan ubicarse en un tablero de NxN sin atacarse entre sí.

## Descripción

El algoritmo evalúa la "aptitud" (fitness) de cada configuración del tablero mediante el conteo de colisiones entre las reinas y busca minimizar este número. Se seleccionan los individuos con mejor aptitud para producir nuevas generaciones mediante cruzamiento y mutación, hasta que se encuentra una solución o se alcanza el número de generaciones especificado.

### Estructura del código

1. **`fitness(tablero, n)`**: Calcula la cantidad de colisiones en un tablero y determina la aptitud de un individuo.
2. **`select(mejores, poblacion)`**: Selecciona los 6 mejores individuos basados en su aptitud.
3. **`cruzamiento(mejores, porcentajeMutacion, porcentajeCruzamiento)`**: Realiza el proceso de cruzamiento y mutación para generar nuevos individuos.
4. **`printTablero(tablero)`**: Imprime el tablero con la solución encontrada.


## Instrucciones de Uso

1. **Clonar el repositorio** o descargar los archivos del proyecto.

2. **Ejecutar el código** con los siguientes parámetros:

   ```bash
   python nombreArchivo.py <semilla> <n> <generaciones> <poblacionInicial> <porcentajeMutacion> <porcentajeCruzamiento>

## Ejemplo de ejecución
Este ejemplo muestra una solución para una solución de un tablero de 20x20

    ```bash
    python n_reinas.py 35 20 1000 30 50 90

## Salida
El programa imprimirá información sobre las generaciones, la selección de los mejores individuos, y finalmente, cuando se encuentre una solución, mostrará el tablero con la disposición de las reinas.

Si no se encuentra una solución, se imprimirá un mensaje indicando que no se logró encontrar una solución.

## Notas

- Según lo probado el este algoritmo funciona mejor cuando se ingresan porcentajes de mutacion entre 20% y 50%  y porcentajes de cruzamiento superiores al 90% para valores de n mas altos.

- Igualmente si se ingresan valores mas bajos de mutacion como 5% encuentra soluciones pero quizas sea necesario probar con diferentes semillas para encontrar resultados. 

- Segun lo probado tambien al usar 100% de pocentaje de cruzamiento hay aun más efectividad a la hora de encontrar soluciones.


## Estudiantes: 

- Javier Pino Herrera
- Dan Ocampo Castillo
- Felipe Gerbier Gerbier