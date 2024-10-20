#El calculo del fitnees consiste en revisar la cantidad de colisiones que existen en el tablero y calcular la diferencia con el numero de maximas
#Colisiones posibles por tablero (n*(n-1)/2). Luego se seleccionan los 6 mejores individuos por poblacion basados en los que tengan mejor fitness,
#para luego cruzar estos inidividuos y seleccionar una nueva poblacion del numero ingresado de poblacionInicial. Para el proceso de cruzamiento dividimos losindividuos a la mitad y los
#mezclamos con la mitad de otro individuo, en el proceso se aplica mutacion a uno de los numeros (seleccionado aleatoriamente) de el individuo cambiandolo por otro
#aleatorio.

# Estudiantes : Javier Pino Herrera, Dan Ocampo Castillo, Felipe Gerbier Gerbier

import random
import math
import sys

def fitness(tablero, n):
  acumulador = 0
  size = len(tablero)
  columna_i = 0
  #Se cuentan las coliciones entre las reinas y se asignan al acumulador
  for i in tablero:
    for j in range(columna_i + 1, size):
      if i == tablero[j]:
        acumulador = acumulador + 1
      if int(tablero[j]) + (j - columna_i) == int(i) or int(
          tablero[j]) - (j - columna_i) == int(i):
        acumulador = acumulador + 1
    columna_i = columna_i + 1
  #n*(n-1)/3 es el maximo de colisiones que se pueden dar para un tablero de tamaño n asi que se le resta el acumulador para obtener el colisiones
  return (n * (n - 1) / 2) - acumulador


def select(mejores, poblacion):
  #Se seleccionan los que tengan menos colisiones
  for i in range(6):
    aux2 = 0
    aux = 0
    for j in range(poblacionInicial):
      if colisiones[j] > aux:
        aux = colisiones[j]
        aux2 = j
        #colisiones[j] = 0
      else:
        pass
    mejores.append(poblacion[aux2])
  return mejores


def cruzamiento(mejores, porcentajeMutacion, porcentajeCruzamiento, max_intentos=10):
    heads = []
    tails = []
    hijos = []
    
    for i in range(len(mejores)):
        lista = mejores[i]
        aux = math.ceil(len(lista) / 2)
        aux2 = [lista[i:i + aux] for i in range(0, len(lista), aux)]

        for j in range(len(aux2)):
            if random.randint(1, 100) <= porcentajeMutacion:
                columna = random.randint(1, math.floor((n / 2) - 1))
                fila = random.randint(1, n)
                
                # Verifica si la mutación resulta en un conflicto
                while aux2[j][columna] == str(fila):
                    fila = random.randint(1, n)  # Cambia de fila si está en conflicto
                
                aux2[j][columna] = str(fila)
            else:
                pass
        
        heads.append(aux2[0])
        tails.append(aux2[1])

    # Intentos de cruzar padres
    intentos = 0
    while len(hijos) < len(mejores) and intentos < max_intentos:
        for i in range(len(heads)):
            for j in range(len(tails)):
                if i != j:
                    # Probabilidad de cruzar estos padres
                    if random.randint(1, 100) <= porcentajeCruzamiento:
                        hijos.append(heads[i] + tails[j])
        intentos += 1

    # Si no se logró generar suficientes hijos, completar con los mejores
    if len(hijos) == 0:
        return mejores
    else:
        return hijos




def printTablero(tablero):  #Display de tablero
  size = len(tablero)
  for i in range(size):
    aux = ""
    for j in tablero:
      if int(j) == i + 1:
        aux = aux + " # "
      else:
        aux = aux + " '' "
    print(aux)

#-----------------------------------------------------------------------------------------------INICIO DEL CODIGO-----------------------------------------------------------------------------------------------

if len(sys.argv) != 7:
    print("Error, prodcure ingresar correctamente los parametros al ejecutar el archivo, ejemplo:\n")
    print("python nombreArchivo.py semilla n generaciones poblacionInicial porcentajeMutacion porcentajeCruzamiento")
else:
    
    random.seed(int(sys.argv[1])) #Semilla

    n = int(sys.argv[2])
    generaciones = int(sys.argv[3])
    poblacionInicial = int(sys.argv[4])
    porcentajeMutacion = int(sys.argv[5])
    porcentajeCruzamiento = int(sys.argv[6])

    poblacion = []
    mejores = []
    colisiones = []
    solucion = 0

    #Genera una poblacion inicial aleatoria
    for i in range(poblacionInicial):

      aux = " "

      for j in range(n):

        aux = str(aux) + str(random.randint(1, n)) + " "

      poblacion.append(list(aux.split()))


#----------------------------Ciclo principal de tamaño de generaciones-----------------------------------------

solucion_encontrada = False  # Variable de control

for a in range(generaciones):
    print(f"Generación: {a+1}")

    # Calcula y se guarda en colisiones el fitness de la población inicial
    for i in range(len(poblacion)):  
        colisiones.append(fitness(poblacion[i], n))   

    aux = 0
    for i in range(len(poblacion)):  
        if colisiones[i] == (n * (n - 1) / 2):  # Verifica si se encontró la solución
            solucion = poblacion[i]
            print("SOLUCION = " + str(solucion) + "\n")
            print("Tablero:")
            printTablero(solucion)
            solucion_encontrada = True  # Cambia la variable de control a True
            break  # Rompe el ciclo de evaluación de colisiones

        elif colisiones[i] > aux:
            aux = colisiones[i]
        else:
            pass    

    # Si la solución fue encontrada, sal del ciclo principal
    if solucion_encontrada:
        break  # Sale del ciclo de generaciones

    # Selecciona los 6 mejores de la población
    mejores = select(mejores, poblacion)

    print(f"Cantidad de Mejores individuos seleccionados: {len(mejores)}")
    print(f"Mejores individuos seleccionados: {(mejores)}")

    # Limpiar las variables para la siguiente generación
    poblacion.clear()

    # Realizar el cruzamiento y mutación
    poblacion = cruzamiento(mejores, porcentajeMutacion, porcentajeCruzamiento)

    print(f"Población después del cruzamiento: {len(poblacion)}")

    # Asegurarse de que la nueva población tenga el tamaño de poblacionInicial
    while len(poblacion) < poblacionInicial:
        poblacion.append(random.choice(mejores))

    print(f"Población final de la generación: {len(poblacion)}")
    print("") #Espaciado entre generaciones

    colisiones.clear()  # Limpia la variable para reutilizar en la siguiente generación
    mejores.clear()  # Limpia la variable para reutilizar en la siguiente generación

# Si no se encontró la solución imprime un mensaje
if not solucion_encontrada:
    print("No se ha encontrado solución\n")



