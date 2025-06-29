import random
import time
import os

# Configuración inicial
NUM_CARACOLES = 5
LONGITUD_META = 40
DORMIR = 0.2  # tiempo entre actualizaciones

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_carrera(caracoles):
    limpiar_pantalla()
    for i, posicion in enumerate(caracoles):
        pista = '-' * posicion + '@' + '-' * (LONGITUD_META - posicion)
        print(f"Caracol {i+1}: {pista}")

def carrera():
    caracoles = [0 for _ in range(NUM_CARACOLES)]
    ganador = None

    while ganador is None:
        for i in range(NUM_CARACOLES):
            avance = random.randint(0, 3)  # caracol avanza de 0 a 3 pasos
            caracoles[i] += avance
            if caracoles[i] >= LONGITUD_META:
                caracoles[i] = LONGITUD_META
                ganador = i
        mostrar_carrera(caracoles)
        time.sleep(DORMIR)

    print(f"\n🎉 ¡El caracol {ganador + 1} ha ganado la carrera! 🎉")

if __name__ == "__main__":
    carrera()