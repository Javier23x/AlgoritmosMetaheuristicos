import sys
import random
import numpy as np
import pandas as pd

def generarRutaHormiga(matrizFeromonas, matrizHeuristica, n_ciudades, alpha, beta, q0):
    ruta = []
    ciudades_no_visitadas = list(range(n_ciudades)) #Inicializamos las ciudades no visitadas
    actual = random.choice(ciudades_no_visitadas) #La hormiga empieza en una ciudad aleatoria
    ruta.append(actual) 
    ciudades_no_visitadas.remove(actual) #Quitamos la ciudad actual de las no visitadas

    while ciudades_no_visitadas:
        siguienteCiudad = elegirSiguienteCiudad(matrizFeromonas, matrizHeuristica, ciudades_no_visitadas, actual, alpha, beta, q0) #Elegir sgte ciudad
        ruta.append(siguienteCiudad)
        ciudades_no_visitadas.remove(siguienteCiudad) #Quitamos la ciudad actual de las no visitadas
        actual = siguienteCiudad 
    
    return ruta

def generarRutasColonia(matrizFeromonas, matrizHeuristica, n_ciudades, n_hormigas, alpha, beta, q0):
    # Creamos una matriz vacía de tamaño n_hormigas x n_ciudades con valor -1
    colonia = np.full((n_hormigas, n_ciudades), -1)

    for i in range(n_hormigas):
        # Generamos una ruta para esta hormiga
        ruta = generarRutaHormiga(matrizFeromonas, matrizHeuristica, n_ciudades, alpha, beta, q0)
        # Guardamos la ruta generada en la fila i de la colonia
        colonia[i, :] = ruta

    return colonia


def calcularCosto(matrizDistancia, solucion, n_ciudades):
    costo = 0

    #Sumar la distancia de todos los puntos actuales de la solucion
    for i in range(n_ciudades - 1):
        costo += matrizDistancia[solucion[i]][solucion[i + 1]]
    costo += matrizDistancia[solucion[n_ciudades - 1]][solucion[0]]
    return costo

def elegirSiguienteCiudad(matrizFeromonas, matrizHeuristica, ciudades_no_visitadas, actual, alpha, beta, q0):
    #Paso 1: Explotación vs exploración
    if random.random() < q0: #Generar un random entre 0 y 1
        #Explotación
        siguienteCiudad = max(ciudades_no_visitadas, key=lambda ciudad: (matrizFeromonas[actual][ciudad]) * (matrizHeuristica[actual][ciudad] ** beta))
    else:
        #Exploración
        probabilidades = [] #Generar lista de probabilidades para la ruleta
        
        #Paso 1: Generar lista de valores matrizFeromonas * matrizHeuristica**beta
        for ciudad in ciudades_no_visitadas:
            valor = (matrizFeromonas[actual][ciudad]) * (matrizHeuristica[actual][ciudad] ** beta)
            probabilidades.append(valor)
        
        #Paso 2: Dividir cada valor por la sumatoria total de las probabilidades para normalizar
        sumatoria = sum(probabilidades)
        probabilidades = [i/sumatoria for i in probabilidades]

        #Paso 3: Elegimos la siguiente ciudad en base a las probabilidades
        siguienteCiudad = random.choices(ciudades_no_visitadas, probabilidades)[0]

    return siguienteCiudad

def calcularMejorRuta(colonia, matrizDistancias, n_ciudades):
    mejor_ruta = None
    menor_costo = float('inf')  #Inicializamos el menor costo con un valor infinito

    #Recorremos cada ruta en la colonia
    for ruta in colonia:
        #Calculamos el costo de la ruta actual
        costo = calcularCosto(matrizDistancias, ruta, n_ciudades)
        
        #Comprobamos si el nuevo costo es menor al anterior
        if costo < menor_costo:
            menor_costo = costo
            mejor_ruta = ruta

    return mejor_ruta, menor_costo

def actualizarFeromonaLocal(colonia, alpha, t0, matrizFeromonas):
    # Recorremos cada ruta en la colonia
    for ruta in colonia:
        #Recorremos cada ciudad en la ruta (excepto la ultima)
        for i in range(len(ruta) - 1):  
            ciudad_actual = ruta[i]
            ciudad_siguiente = ruta[i + 1]

            #Actualizamos la feromona
            t = (1 - alpha) * matrizFeromonas[ciudad_actual][ciudad_siguiente] + alpha * t0
            matrizFeromonas[ciudad_actual][ciudad_siguiente] = t
            matrizFeromonas[ciudad_siguiente][ciudad_actual] = t  #Simétrico

        #Conectar la última ciudad con la primera para completar el ciclo
        ciudad_actual = ruta[-1] #Ultima ciudad
        ciudad_siguiente = ruta[0]

        #Actualizamos la feromona
        t = (1 - alpha) * matrizFeromonas[ciudad_actual][ciudad_siguiente] + alpha * t0
        matrizFeromonas[ciudad_actual][ciudad_siguiente] = t
        matrizFeromonas[ciudad_siguiente][ciudad_actual] = t  #Simétrico

def actualizarFeromonaGlobal(matrizFeromonas, mejorRuta, mejorCosto, alpha):
    delta = 1 / mejorCosto #Calcular delta

    #Recorrer cada ciudad de la ruta (Excepto la última)
    for i in range(len(mejorRuta) - 1):
        ciudad_actual = mejorRuta[i]
        ciudad_siguiente = mejorRuta[i + 1]
        
        #Actualizamos la feromona
        t = (1 - alpha) * matrizFeromonas[ciudad_actual][ciudad_siguiente] + alpha * delta
        matrizFeromonas[ciudad_actual][ciudad_siguiente] = t
        matrizFeromonas[ciudad_siguiente][ciudad_actual] = t

    #Ultima y primera ciudad
    ciudad_final = mejorRuta[-1]
    ciudad_inicial = mejorRuta[0]

    #Actualizamos la feromona
    t = (1 - alpha) * matrizFeromonas[ciudad_final][ciudad_inicial] + alpha * delta
    matrizFeromonas[ciudad_final][ciudad_inicial] = t
    matrizFeromonas[ciudad_inicial][ciudad_final] = t

def coloniaHormigas():
    pass


#--------------------------------------------------INICIO--------------------------------------------------------

if len(sys.argv) != 8:
    print("Error, procure ingresar correctamente los parametros de entrada al ejecutar el archivo, ejemplo:\n")
    print("python nombreArchivo.py semilla TamañoColonia NumeroIteraciones TasaEvaporacion PesoHeuristica Q0 archivoEntrada")
else:
    random.seed(int(sys.argv[1])) #Semilla
    n_hormigas = int(sys.argv[2]) #Tamaño de colonia
    iteraciones = int(sys.argv[3]) #Numero de iteraciones
    alpha = float(sys.argv[4]) #Factor de evaporación
    beta = float(sys.argv[5]) #Peso heuristica
    q0 = float(sys.argv[6]) #Probabilidad explotación vs exploración
    entrada = sys.argv[7] #Nombre del archivo de entrada

solucionIdeal = [
    1 - 1, 49 - 1, 32 - 1, 45 - 1, 19 - 1, 41 - 1, 8 - 1, 9 - 1, 10 - 1, 43 - 1,
    33 - 1, 51 - 1, 11 - 1, 52 - 1, 14 - 1, 13 - 1, 47 - 1, 26 - 1, 27 - 1, 28 - 1,
    12 - 1, 25 - 1, 4 - 1, 6 - 1, 15 - 1, 5 - 1, 24 - 1, 48 - 1, 38 - 1, 37 - 1,
    40 - 1, 39 - 1, 36 - 1, 35 - 1, 34 - 1, 44 - 1, 46 - 1, 16 - 1, 29 - 1, 50 - 1,
    20 - 1, 23 - 1, 30 - 1, 2 - 1, 7 - 1, 42 - 1, 21 - 1, 17 - 1, 3 - 1, 18 - 1,
    31 - 1, 22 - 1
]

# Leer archivo de entrada y pasarlo a matriz de coordenadas
matrizCoordenadas = pd.read_table(entrada, header=None, sep=r'\s+', skiprows=6, skipfooter=1, engine='python')
matrizCoordenadas = matrizCoordenadas.drop(columns=0, axis=1).to_numpy()
n_ciudades = matrizCoordenadas.shape[0]

matrizDistancias = np.zeros((n_ciudades, n_ciudades))

#Generar la matriz de distancia
for i in range(n_ciudades):
    for j in range(n_ciudades):
        if i != j:
            # Calcular la distancia euclidiana entre la ciudad i y la ciudad j
            matrizDistancias[i][j] = np.sqrt((matrizCoordenadas[j][0] - matrizCoordenadas[i][0]) ** 2 +
            (matrizCoordenadas[j][1] - matrizCoordenadas[i][1]) ** 2)

#Generar la matriz de heuristica
with np.errstate(divide='ignore', invalid='ignore'):
    matrizHeuristica = np.where(matrizDistancias != 0, 1 / matrizDistancias, 0)
np.fill_diagonal(matrizHeuristica, 0)

#Generar una solucion inicial de forma aleatoria
solucionInicial = list(range(n_ciudades))
random.shuffle(solucionInicial)

mejorCosto = calcularCosto(matrizDistancias, solucionInicial, n_ciudades) #Establecemos un mejor costo inicial
t0 = 1/(n_ciudades*(mejorCosto)) #Calcular t0 inicial

#Se llena la matriz de feromonas con los valores de t0 y 0's en la diagonal
matrizFeromonas = np.full((n_ciudades, n_ciudades), t0)
np.fill_diagonal(matrizFeromonas, 0)

#Ciclo principal
for iteracion in range(iteraciones):
    
    #Obtenemos nuestra primera colonia de hormigas con sus rutas correspondientes
    colonia = generarRutasColonia(matrizFeromonas, matrizHeuristica, n_ciudades, n_hormigas, alpha, beta, q0)
    actualizarFeromonaLocal(colonia, alpha, t0, matrizFeromonas) #Actualizamos localmente la matriz de feromonas

    #Obtenemos la mejor ruta con su costo asociado de la función calcularMejorRuta
    mejorRutaActual, mejorCostoActual = calcularMejorRuta(colonia, matrizDistancias, n_ciudades) 
    
    #Confirmar si la nueva mejor ruta es mejor a la anterior
    if mejorCostoActual < mejorCosto:
        mejorRuta = mejorRutaActual
        mejorCosto = mejorCostoActual
    
    actualizarFeromonaGlobal(matrizFeromonas, mejorRuta, mejorCosto, alpha) #Actualización global de feromonas
   
   #Depuración
    print(f"Iteración {iteracion + 1}/{iteraciones}, Mejor costo actual: {mejorCosto}")

#Resultado
print("Mejor ruta encontrada:", mejorRuta)
print("Costo de la mejor ruta:", mejorCosto)

