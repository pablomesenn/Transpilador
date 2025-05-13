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

def test_invocaciones():
    """
    Prueba el análisis de invocaciones de funciones
    """
    print("\n=== TEST DE INVOCACIONES ===")
    
    ejemplos = [
        "teElijo calcularDano(pikachu, 10)",
        "teElijo sanarPokemon(charizard)",
        "teElijo batalla()",
        "teElijo sumarStats(ataque, defensa, velocidad)"
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
                
            # Análisis sintáctico
            analizador = AnalizadorLexico(componentes)
            
            # Probamos la invocación
            nodo_invocacion = analizador.analizar_invocacion()
            
            # Mostrar ASA resultante
            print("\nÁrbol de Sintaxis Abstracta para la invocación:")
            print(nodo_invocacion.nodeToStr())
            for nodo in nodo_invocacion.nodos:
                print(f"  ├─ {nodo.nodeToStr()}")
                for subnodo in nodo.nodos:
                    if subnodo:
                        print(f"  │  └─ {subnodo.nodeToStr()}")
            
            print("\n✅ Análisis exitoso")
        
        except Exception as e:
            print(f"\n❌ Error durante el análisis: {e}")
            import traceback
            traceback.print_exc()

def test_funciones():
    """
    Prueba el análisis de declaraciones de funciones
    """
    print("\n=== TEST DE FUNCIONES ===")
    
    ejemplos = [
        "batalla calcularDano(pokemon, poder) { resultado fuego = pokemon ataque poder retirada resultado }",
        "batalla sanarPokemon(pokemon) { pokemon fuego = pokemon ataque 20 retirada pokemon }",
        """batalla combatir(atacante, defensor) { 
            dano fuego = teElijo calcularDano(atacante, 10)
            defensor fuego = defensor ataque dano
            retirada defensor 
        }"""
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
                
            # Análisis sintáctico
            analizador = AnalizadorLexico(componentes)
            
            # Probamos la función
            nodo_funcion = analizador.analizar_funcion()
            
            # Mostrar ASA resultante
            print("\nÁrbol de Sintaxis Abstracta para la función:")
            print(nodo_funcion.nodeToStr())
            for nodo in nodo_funcion.nodos:
                print(f"  ├─ {nodo.nodeToStr()}")
                for subnodo in nodo.nodos:
                    if subnodo:
                        print(f"  │  └─ {subnodo.nodeToStr()}")
                        for subsubnodo in subnodo.nodos:
                            if subsubnodo:
                                print(f"  │     └─ {subsubnodo.nodeToStr()}")
            
            print("\n✅ Análisis exitoso")
        
        except Exception as e:
            print(f"\n❌ Error durante el análisis: {e}")
            import traceback
            traceback.print_exc()

def test_equipos():
    """
    Prueba el análisis de declaraciones de equipos
    """
    print("\n=== TEST DE EQUIPOS ===")
    
    ejemplos = [
        "equipo MiE { Pikachu {100, 5.5} }",
        "equipo Elite { Charizard {150, 7,8} Blastoise {145, 6.9} Venusaur {140, 6.5} }",
        "equipo Completo { Pikachu {100, 5,5} Charizard {150, 7.8} Blastoise {145, 6,9} Venusaur {140, 6.5} Snorlax {200, 8.0} Gengar {130, 7.2} }"
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

            # Análisis sintáctico
            analizador = AnalizadorLexico(componentes)
            
            # Probamos el equipo
            nodo_equipo = analizador.analizar_equipo()
            
            # Mostrar ASA resultante
            print("\nÁrbol de Sintaxis Abstracta para el equipo:")
            print(nodo_equipo.nodeToStr())
            for nodo in nodo_equipo.nodos:
                print(f"  ├─ {nodo.nodeToStr()}")
                for subnodo in nodo.nodos:
                    if subnodo:
                        print(f"  │  └─ {subnodo.nodeToStr()}")
            
            print("\n✅ Análisis exitoso")
        
        except Exception as e:
            print(f"\n❌ Error durante el análisis: {e}")
            import traceback
            traceback.print_exc()

def test_repeticiones():
    """
    Prueba el análisis de estructuras de repetición (turnos)
    """
    print("\n=== TEST DE REPETICIONES ===")
    
    ejemplos = [
        "turnos (contador paralizar 10) { contador fuego = contador ataque 1 }",
        """turnos (hp energia 0) { 
            hp fuego = hp ataque 1 
            energia fuego = energia ataque 1
        }"""
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
                
            # Análisis sintáctico
            analizador = AnalizadorLexico(componentes)
            
            # Probamos la repetición
            nodo_repeticion = analizador.analizar_repeticion()
            
            # Mostrar ASA resultante
            print("\nÁrbol de Sintaxis Abstracta para la repetición:")
            print(nodo_repeticion.nodeToStr())
            for nodo in nodo_repeticion.nodos:
                print(f"  ├─ {nodo.nodeToStr()}")
                for subnodo in nodo.nodos:
                    if subnodo:
                        print(f"  │  └─ {subnodo.nodeToStr()}")
            
            print("\n✅ Análisis exitoso")
        
        except Exception as e:
            print(f"\n❌ Error durante el análisis: {e}")
            import traceback
            traceback.print_exc()

def test_bifurcaciones():
    """
    Prueba el análisis de estructuras de bifurcación (si/sinnoh)
    """
    print("\n=== TEST DE BIFURCACIONES ===")
    
    ejemplos = [
        "si (hp paralizar 0) { retirada capturado }",
        """si (hp paralizador 0) { 
            retirada capturado 
        } sinnoh { 
            hp fuego = hp ataque 10 
        }"""
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
                
            # Análisis sintáctico
            analizador = AnalizadorLexico(componentes)
            
            # Probamos la bifurcación
            nodo_bifurcacion = analizador.analizar_bifurcacion()
            
            # Mostrar ASA resultante
            print("\nÁrbol de Sintaxis Abstracta para la bifurcación:")
            print(nodo_bifurcacion.nodeToStr())
            for nodo in nodo_bifurcacion.nodos:
                print(f"  ├─ {nodo.nodeToStr()}")
                for subnodo in nodo.nodos:
                    if subnodo:
                        print(f"  │  └─ {subnodo.nodeToStr()}")
                        for subsubnodo in subnodo.nodos:
                            if subsubnodo:
                                print(f"  │     └─ {subsubnodo.nodeToStr()}")
            
            print("\n✅ Análisis exitoso")
        
        except Exception as e:
            print(f"\n❌ Error durante el análisis: {e}")
            import traceback
            traceback.print_exc()

def test_condiciones():
    """
    Prueba el análisis de condiciones
    """
    print("\n=== TEST DE CONDICIONES ===")
    
    ejemplos = [
        "hp paralizar 0",
        "ataque paralizar defensa",
        "x ataque y and z paralizador w",
        "a ataque b or c paralizador d"
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
                
            # Análisis sintáctico
            analizador = AnalizadorLexico(componentes)
            
            # Probamos la condición
            nodo_condicion = analizador.analizar_condicion()
            
            # Mostrar ASA resultante
            print("\nÁrbol de Sintaxis Abstracta para la condición:")
            print(nodo_condicion.nodeToStr())
            for nodo in nodo_condicion.nodos:
                print(f"  ├─ {nodo.nodeToStr()}")
                for subnodo in nodo.nodos:
                    if subnodo:
                        print(f"  │  └─ {subnodo.nodeToStr()}")
            
            print("\n✅ Análisis exitoso")
        
        except Exception as e:
            print(f"\n❌ Error durante el análisis: {e}")
            import traceback
            traceback.print_exc()

def test_retorno():
    """
    Prueba el análisis de retornos
    """
    print("\n=== TEST DE RETORNOS ===")
    
    ejemplos = [
        "retirada resultado",
        "retirada 10",
        "retirada \"Victoria\"",
        "retirada capturado"
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
                
            # Análisis sintáctico
            analizador = AnalizadorLexico(componentes)
            
            # Probamos el retorno
            nodo_retorno = analizador.analizar_retorno()
            
            # Mostrar ASA resultante
            print("\nÁrbol de Sintaxis Abstracta para el retorno:")
            print(nodo_retorno.nodeToStr())
            for nodo in nodo_retorno.nodos:
                print(f"  ├─ {nodo.nodeToStr()}")
            
            print("\n✅ Análisis exitoso")
        
        except Exception as e:
            print(f"\n❌ Error durante el análisis: {e}")
            import traceback
            traceback.print_exc()

def test_programa_completo():
    """
    Prueba el análisis de un programa completo
    """
    print("\n=== TEST DE PROGRAMA COMPLETO ===")
    
    # Un ejemplo de programa completo
    programa = """
    pika Definición de variables globales
    ataque fuego = 10
    defensa agua = 8
    
    pika Definición de una función
    batalla calcularDano(pokemon, poder) {
        resultado fuego = pokemon ataque poder
        retirada resultado
    }
    
    pika Definición de un equipo
    equipo MiEquipo {
        Pikachu {100, 5.5}
        Charizard {150, 7.8}
    }
    
    pika Función principal
    teReto! {
        pika Asignaciones
        hp fuego = 100
        energia agua = 50
        
        pika Bifurcación
        si (hp paralizar 20) {
            mensaje planta = "Pokémon débil"
        } sinnoh {
            pika Repetición
            turnos (contador paralizar 3) {
                hp fuego = hp ataque 10
                contador fuego = contador ataque 1
            }
        }
        
        pika Invocación de función
        resultado fuego = teElijo calcularDano(hp, ataque)
    }
    """
    
    try:
        # Análisis léxico
        explorador = ExploradorPokeScript(programa)
        componentes = explorador.explorar()

        if explorador.errores:
            print("Errores léxicos encontrados:")
            for error in explorador.errores:
                print(f"  - {error}")
            return
        
        # Mostrar componentes léxicos (solo los primeros 10 para no saturar)
        print("Algunos componentes léxicos (primeros 10):")
        for i, comp in enumerate(componentes[:10]):
            print(f"  {comp}")
        print("  ...")
            
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
    while True:
        # Menú de pruebas
        print("===== PRUEBAS DEL ANALIZADOR LÉXICO Y SINTÁCTICO DE POKESCRIPT =====")
        print("Seleccione una opción para probar:")
        print("1. Asignaciones")
        print("2. Expresiones")
        print("3. Invocaciones")
        print("4. Funciones")
        print("5. Equipos")
        print("6. Repeticiones")
        print("7. Bifurcaciones")
        print("8. Condiciones")
        print("9. Retornos")
        print("10. Programa completo (ejemplo en memoria)")
        print("11. Programa desde archivo")
        print("12. Ejecutar todas las pruebas")
        print("0. Salir")
        opcion = input("\nIngrese el número de la prueba: ")
        
        if opcion == "1":
            test_asignaciones()
        elif opcion == "2":
            test_expresiones()
        elif opcion == "3":
            test_invocaciones()
        elif opcion == "4":
            test_funciones()
        elif opcion == "5":
            test_equipos()
        elif opcion == "6":
            test_repeticiones()
        elif opcion == "7":
            test_bifurcaciones()
        elif opcion == "8":
            test_condiciones()
        elif opcion == "9":
            test_retorno()
        elif opcion == "10":
            test_programa_completo()
        elif opcion == "11":
            ruta = input("Ingrese la ruta al archivo .poke: ")
            test_archivo_completo(ruta)
        elif opcion == "12":
            test_asignaciones()
            test_expresiones()
            test_invocaciones()
            test_funciones()
            test_equipos()
            test_repeticiones()
            test_bifurcaciones()
            test_condiciones()
            test_retorno()
            test_programa_completo()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida.")