import math
import os 
import time 
import numpy as np
#Aplicacion Modelo de Co-ocurrencias
d1 = ["hola"," mundo", "como"]
d2 = ["caballo","perro",'gato']
d3 = ["caballo", "gato", "perro", "minino"]
d4 = ["caballo", "gato", "perro", "minino", "comadreja","animal"]
d5 = ["caballo", "gato", "perro", "minino", "gato", "conejo","tigresita", "zorrito"]
docs = [d1,d2,d3,d4,d5]
biblioteca = docs
def calculo_matriz_coorrelacion(biblioteca):
    for i in range(0,len(biblioteca)):
            print(f"distancia de  de fila {i+1}, {max(map(len, biblioteca[i]))}")
            

def calculo_frecuencia_diagonal(terminos, biblioteca):
    frecuencia = set()
    contador = 0
    resultado = [ ]
    for lista in biblioteca:
        for palabra in lista:
            if palabra in lista:
                contador = contador + 1
            resultado.append(contador)
    return resultado
            
def calculo_frecuencia(lista):
    pass

def ordenar_total(arreglo):
  resultado = []
  for subarreglo in arreglo:
    resultado.extend(subarreglo)
  resultado = sorted(resultado)
  return resultado

def eliminar_repetidas(lista):
  unicas = set()
  resultado = []
  for palabra in lista:
    if palabra not in unicas:
      unicas.add(palabra)
      resultado.append(palabra)
  return resultado

if __name__ == '__main__':   
    start = time.time_ns()
    #print(len(biblioteca[-1][3]))
    for fila in biblioteca:
  # Aplicar la función eliminar_repetidas a cada fila y mostrar el resultado

        print(eliminar_repetidas(fila))
        print(calculo_frecuencia_diagonal(fila))
    #calculo_matriz_coorrelacion(docs);
    final = time.time_ns() - start
    print(f"{final/10**8}")



