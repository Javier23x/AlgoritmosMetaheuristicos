# Colonia de Hormigas para el Problema del Viajero Viajero (TSP)

Este proyecto implementa el algoritmo de la colonia de hormigas (Ant Colony Optimization, ACO) para resolver el Problema del Vendedor Viajero (Traveling Salesman Problem, TSP). El código genera rutas optimizadas que minimizan la distancia total recorrida para visitar todas las ciudades exactamente una vez.

## Cómo ejecutar el programa

### Requisitos:
- Python 3.x
- Librerías: `numpy`, `pandas`

### Instalación de dependencias:

```bash
pip install numpy pandas
```

### Compilación y Ejecución:

El programa se ejecuta desde la línea de comandos con los siguientes parámetros:

```
python nombreArchivo.py semilla tamañoColonia númeroIteraciones tasaEvaporacion pesoHeuristica Q0 archivoEntrada
```

- **semilla**: Valor para inicializar el generador aleatorio.
- **tamañoColonia**: Número de hormigas en la colonia.
- **númeroIteraciones**: Cantidad de iteraciones a ejecutar.
- **tasaEvaporacion (alpha)**: Factor de evaporación de feromonas.
- **pesoHeuristica (beta)**: Peso de la heurística en la elección de la siguiente ciudad.
- **Q0**: Valor entre 0 y 1 que controla la proporción de explotación vs exploración.
- **archivoEntrada**: Archivo de entrada con las coordenadas de las ciudades en formato TXT.

### Ejemplo de Ejecución:
```bash
python hormigas.py 1 50 100 0.1 2.5 0.9 berlin52.txt
```

Este comando usa la semilla `1`, una colonia de `50` hormigas, `100` iteraciones, una tasa de evaporación de `0.1`, un peso heurístico de `2.5`, una probabilidad de explotación de `0.9`, y el archivo `berlin52.txt` como entrada.

## Lógica del Algoritmo

El algoritmo se basa en el comportamiento de las hormigas para encontrar caminos óptimos en gráficos. La lógica principal es la siguiente:

1. **Inicialización**: Se genera una solución inicial aleatoria y se establecen las matrices de distancias, heurística y feromonas.
2. **Generación de Rutas**: Para cada iteración, las hormigas eligen sus rutas basadas en la probabilidad determinada por la combinación de la cantidad de feromonas y la distancia a la siguiente ciudad (heurística).
3. **Actualización de Feromonas**: Después de que todas las hormigas hayan completado sus rutas, las feromonas se actualizan localmente y globalmente para favorecer las mejores rutas.
4. **Búsqueda del Óptimo**: Se elige la mejor ruta de todas las hormigas y se guarda como solución óptima.
5. **Evaporación de Feromonas**: A medida que avanza el algoritmo, la feromona depositada en los caminos se evapora para permitir la exploración de nuevas rutas.

### Salida
Al finalizar, el programa imprime:
- La mejor ruta encontrada.
- El costo (distancia total) de la mejor ruta.

## Archivo de Entrada

El archivo de entrada esta incluido en la carpeta con nombre berlin52.txt.
