from arbol import NodoArbol, TipoNodo, ArbolSintaxisAbstracta

def test_insercion_simple():
    arbol = ArbolSintaxisAbstracta()
    
    # Nodo raíz tipo PROGRAMA
    raiz = NodoArbol(TipoNodo.PROGRAMA, "main")
    arbol.insertar_nodo(None, raiz)

    # Nodo hijo tipo ASIGNACION
    nodo_asignacion = NodoArbol(TipoNodo.ASIGNACION, "x")
    arbol.insertar_nodo(raiz, nodo_asignacion)

    # Nodo hijo tipo EXPRESION
    nodo_expr = NodoArbol(TipoNodo.EXPRESION, "5")
    arbol.insertar_nodo(nodo_asignacion, nodo_expr)

    print("=== Recorrido Preorden ===")
    arbol.imprimir_preorden()


def test_insercion_multiple():
    arbol = ArbolSintaxisAbstracta()

    raiz = NodoArbol(TipoNodo.FUNCION, "suma")
    arbol.insertar_nodo(None, raiz)

    parametros = NodoArbol(TipoNodo.PARAMETROS)
    cuerpo = NodoArbol(TipoNodo.INSTRUCCION)
    retorno = NodoArbol(TipoNodo.RETORNO, "resultado")

    arbol.insertar_nodo(raiz, parametros)
    arbol.insertar_nodo(raiz, cuerpo)
    arbol.insertar_nodo(cuerpo, retorno)

    print("\n=== Recorrido Preorden (función) ===")
    arbol.imprimir_preorden()


test_insercion_simple()
print("======================================================")
test_insercion_multiple()