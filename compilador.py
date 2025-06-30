import sys
from explorador.explorador import ExploradorPokeScript
from analizador.analizador import AnalizadorLexico
from verificador.verificador import Verificador
from generador.generador import Generador

def main():
    if len(sys.argv) != 2:
        print("Uso: python nombre_del_script.py <archivo.poke>")
        sys.exit(1)
    
    archivo_poke = sys.argv[1]
    
    try:
        # 1. Leer código fuente
        with open(archivo_poke, "r", encoding="utf-8") as archivo:
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

        generador = Generador(analizador.asa)
        generador.generar_y_mostrar()

        # Guardar en archivo (mismo nombre pero con extensión .py)
        archivo_salida = archivo_poke.replace('.poke', '.py')
        generador.generar_y_guardar(archivo_salida)

        # 5. Si todo está bien:
        print("Verificación semántica completada sin errores.")
        print(f"Archivo generado: {archivo_salida}")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo_poke}")
    except Exception as e:
        print(f"Error durante la ejecución: {str(e)}")

if __name__ == "__main__":
    main()