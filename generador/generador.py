from utils.arbol import ArbolSintaxisAbstracta, NodoArbol, TipoNodo
from generador.visitadores import VisitanteGenerador

class Generador: 

    def __init__(self, asa: ArbolSintaxisAbstracta):
        self.asa = asa
        self.visitador = VisitanteGenerador()

        # Ambiente estándar con funciones útiles para el lenguaje Pokémon
        self.ambiente_estandar = """# Código generado automáticamente desde el lenguaje Pokémon
# Funciones auxiliares del ambiente estándar

def mostrar(mensaje):
    \"\"\"Función para mostrar mensajes en pantalla\"\"\"
    print(mensaje)

def capturar_pokemon(nombre, nivel=1, hp=100.0):
    \"\"\"Función para crear un nuevo Pokémon\"\"\"
    return {"nombre": nombre, "nivel": nivel, "hp": hp}

def entrenar_pokemon(pokemon, incremento_nivel=1):
    \"\"\"Función para entrenar un Pokémon\"\"\"
    if isinstance(pokemon, dict) and "nivel" in pokemon:
        pokemon["nivel"] += incremento_nivel
        pokemon["hp"] += incremento_nivel * 10
    return pokemon

# Inicio del código del usuario
"""

    def imprimir_asa(self):
        """
        Imprime el árbol de sintaxis abstracta
        """
        if self.asa.raiz is None:
            print("El árbol sintáctico abstracto está vacío.")
            return
        else:
            self.asa.imprimir_preorden()
            
    def generar_codigo(self):
        """
        Genera el código fuente a partir del árbol de sintaxis abstracta.
        """
        if self.asa.raiz is None:
            print("El árbol sintáctico abstracto está vacío.")
            return ""
        
        resultado = self.visitador.visitar(self.asa.raiz)
        
        codigo_completo = self.ambiente_estandar
        if resultado and resultado.strip():
            codigo_completo += "\n" + resultado
        
        return codigo_completo
    
    def generar_y_guardar(self, nombre_archivo="codigo_generado.py"):
        """
        Genera el código y lo guarda en un archivo Python
        """
        codigo = self.generar_codigo()
        
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(codigo)
            print(f"Código generado exitosamente en: {nombre_archivo}")
            return True
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")
            return False
    
    def generar_y_mostrar(self):
        """
        Genera el código y lo muestra en consola
        """
        codigo = self.generar_codigo()
        print("=" * 50)
        print("CÓDIGO PYTHON GENERADO:")
        print("=" * 50)
        print(codigo)
        print("=" * 50)
        return codigo