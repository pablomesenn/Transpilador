# Importamos las clases necesarias
from explorador.explorador import ExploradorPokeScript
from analizador.analizador import AnalizadorLexico, TipoComponente

def test_asignaciones():
    """
    Prueba el análisis de asignaciones simples y expresiones
    """
    print("\n=== TEST DE ASIGNACIONES ===")
    
    ejemplos = [
        # Asignaciones simples
        "pikachu fuego = 10",
        "charizard agua = \"Hola Mundo\"",
        "squirtle planta = capturado",
        
        # Asignaciones con expresiones
        "hp fuego = vida ataque energia",
        "ataque hielo = poder fortalecer resistencia",
        
        # Asignaciones con invocaciones
        "resultado fuego = teElijo calcularDano(pikachu, 10)",
    ]
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n--- Ejemplo {i}: '{ejemplo}' ---")
        try:
            # Análisis léxico
            explorador = ExploradorPokeScript(ejemplo)
            componentes = explorador.explorar()

            if explorador.errores:
                print("Error léxico encontrado:")
                for error in explorador.errores:
                    print(f"  - {error}")
                continue
            
            # Mostrar componentes léxicos
            print("Componentes léxicos:")
            for comp in componentes:
                print(f"  {comp}")
                
            # Análisis sintáctico (solo de la asignación)
            analizador = AnalizadorLexico(componentes)
            
            # Solo probamos la asignación
            nodo_asignacion = analizador.analizar_asignacion()
            
            # Mostrar ASA resultante
            print("\nÁrbol de Sintaxis Abstracta para la asignación:")
            print(nodo_asignacion.nodeToStr())
            for nodo in nodo_asignacion.nodos:
                print(f"  ├─ {nodo.nodeToStr()}")
                for subnodo in nodo.nodos:
                    if subnodo:
                        print(f"  │  └─ {subnodo.nodeToStr()}")
            
            print("\n✅ Análisis exitoso")
        
        except Exception as e:
            print(f"\n❌ Error durante el análisis: {e}")
            import traceback
            traceback.print_exc()

def test_expresiones():
    """
    Prueba específicamente el análisis de expresiones
    """
    print("\n=== TEST DE EXPRESIONES ===")
    
    ejemplos = [
        "10 ataque 20",
        "variable",
        "teElijo funcion(a, b)",
        "x ataque y golpecritrico z",
    ]
    
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n--- Ejemplo {i}: '{ejemplo}' ---")
        try:
            # Análisis léxico
            explorador = ExploradorPokeScript(ejemplo)
            componentes = explorador.explorar()
            explorador.imprimir_componentes()

            if explorador.errores:
                print("Error léxico encontrado:")
                for error in explorador.errores:
                    print(f"  - {error}")
                continue
            
            # Análisis sintáctico (solo de la expresión)
            analizador = AnalizadorLexico(componentes)
            
            # Solo probamos la expresión
            nodo_expresion = analizador.analizar_expresion()
            
            # Mostrar ASA resultante
            print("\nÁrbol de Sintaxis Abstracta para la expresión:")
            print(nodo_expresion.nodeToStr())
            for nodo in nodo_expresion.nodos:
                print(f"  ├─ {nodo.nodeToStr()}")
                for subnodo in nodo.nodos:
                    if subnodo:
                        print(f"  │  └─ {subnodo.nodeToStr()}")
            
            print("\n✅ Análisis exitoso")
        
        except Exception as e:
            print(f"\n❌ Error durante el análisis: {e}")
            import traceback
            traceback.print_exc()

def test_archivo_completo(ruta_archivo):
    """
    Prueba el análisis de un archivo completo
    """
    print(f"\n=== TEST DE ARCHIVO COMPLETO: {ruta_archivo} ===")
    
    try:
        # Leer el archivo
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Análisis léxico
        explorador = ExploradorPokeScript(contenido)
        componentes = explorador.explorar()
        
        if explorador.errores:
            print("Errores léxicos encontrados:")
            for error in explorador.errores:
                print(f"  - {error}")
        
        # Análisis sintáctico
        analizador = AnalizadorLexico(componentes)

        
        # Analizar todo el programa
        analizador.analizar()
        
        # Mostrar ASA resultante
        print("\nÁrbol de Sintaxis Abstracta para el programa completo:")
        analizador.imprimir_asa()
        
        print("\n✅ Análisis exitoso")
    
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ejecutar pruebas
    test_asignaciones()
    test_expresiones()
    
    # Descomenta para probar con un archivo
    # test_archivo_completo("ruta/al/archivo.poke")