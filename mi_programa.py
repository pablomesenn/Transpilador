# Código generado automáticamente desde el lenguaje Pokémon
# Funciones auxiliares del ambiente estándar
import random

def mostrar(mensaje):
    """Función para mostrar mensajes en pantalla"""
    print(mensaje)

def capturar_pokemon(nombre, nivel=1, hp=100.0):
    """Función para crear un nuevo Pokémon"""
    return {"nombre": nombre, "nivel": nivel, "hp": hp}

def entrenar_pokemon(pokemon, incremento_nivel=1):
    """Función para entrenar un Pokémon"""
    if isinstance(pokemon, dict) and "nivel" in pokemon:
        pokemon["nivel"] += incremento_nivel
        pokemon["hp"] += incremento_nivel * 10
    return pokemon

def numero_aleatorio(minimo=1, maximo=10):
    """Función para generar un número aleatorio"""
    return random.randint(minimo, maximo)


# Inicio del código del usuario

nivel = 5
experiencia = 0
expNecesaria = 100.01
def ganarExperiencia(nivActual):
    expGanada = nivActual + 10
    return expGanada
EquipoNovato = [{"nombre": "pokeBulbasaur", "nivel": 15, "hp": 6.0}]
if __name__ == '__main__':
    contador = 0
    while contador < 3:
        expGanada =         ganarExperiencia(nivel)
        experiencia = experiencia + expGanada
        contador = contador + 1
    if experiencia >= expNecesaria:
        nivel = nivel + 1
        experiencia = experiencia - expNecesaria