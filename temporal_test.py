from explorador.explorador import ExploradorPokeScript
from analizador.analizador import AnalizadorLexico
from verificador.verificador import Verificador

# 1. Leer código fuente
with open("pruebas/Tienda_pokemon.poke", "r", encoding="utf-8") as archivo:
    codigo = archivo.read()

# 2. Análisis léxico
explorador = ExploradorPokeScript(codigo)
tokens = explorador.explorar()

# 3. Análisis sintáctico
analizador = AnalizadorLexico(tokens)
analizador.analizar()

# 4. Verificación semántica
verificador = Verificador(analizador.asa)
verificador.verificar()

analizador.asa.imprimir_preorden_decorado()

# 5. Si todo está bien:
print("Verificación semántica completada sin errores.")
