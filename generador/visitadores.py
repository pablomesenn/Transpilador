from utils.arbol import ArbolSintaxisAbstracta, NodoArbol, TipoNodo

class VisitanteGenerador:

    tabuladores = 0

    def visitar(self, nodo: NodoArbol):
        """
        Método que se llama para visitar un nodo del árbol.
        """

        resultado = ""

        if nodo.tipo == TipoNodo.PROGRAMA:
            return

        elif nodo.tipo == TipoNodo.ASIGNACION:
            return
        
        elif nodo.tipo == TipoNodo.TIPO:
            return
        
        elif nodo.tipo == TipoNodo.EXPRESION:
            return
        
        elif nodo.tipo == TipoNodo.FUNCION:
            return
        
        elif nodo.tipo == TipoNodo.INVOCACION:
            return
        
        elif nodo.tipo == TipoNodo.PARAMETROS:
            return
        
        elif nodo.tipo == TipoNodo.INSTRUCCION:
            return
        
        elif nodo.tipo == TipoNodo.REPETICION:
            return
        
        elif nodo.tipo == TipoNodo.BIFURCACION:
            return
        
        elif nodo.tipo == TipoNodo.SI: 
            return
        
        elif nodo.tipo == TipoNodo.SINNOH:
            return
        
        elif nodo.tipo == TipoNodo.OPERADOR_LOGICO:
            return
        
        elif nodo.tipo == TipoNodo.CONDICION:
            return
        
        elif nodo.tipo == TipoNodo.COMPARACION:
            return
        
        elif nodo.tipo == TipoNodo.RETORNO:
            return
        
        elif nodo.tipo == TipoNodo.ERROR:
            return
                
        elif nodo.tipo == TipoNodo.PRINCIPAL:
            return

        elif nodo.tipo == TipoNodo.BLOQUE_INSTRUCCIONES:
            return

        elif nodo.tipo == TipoNodo.OPERADOR:
            return
        
        elif nodo.tipo == TipoNodo.STRING:
            return
        
        elif nodo.tipo == TipoNodo.BOOLEANOS:
            return
        
        elif nodo.tipo == TipoNodo.ENTERO:
            return
        
        elif nodo.tipo == TipoNodo.FLOTANTE:
            return
        
        elif nodo.tipo == TipoNodo.IDENTIFICADOR:
            return
        
        elif nodo.tipo == TipoNodo.COMPARADOR:
            return
        
        elif nodo.tipo == TipoNodo.EQUIPO:
            return
        
        elif nodo.tipo == TipoNodo.POKEMON:
            return
        
        elif nodo.tipo == TipoNodo.NOMBRE_POKEMON:
            return
        
        return resultado
    
    def __visitar_programa(self, nodo: NodoArbol):
        pass

    def __visitar_asignacion(self, nodo: NodoArbol):
        pass

    def __visitar_tipo(self, nodo: NodoArbol):
        pass

    def __visitar_expresion(self, nodo: NodoArbol):
        pass

    def __visitar_funcion(self, nodo: NodoArbol):
        pass

    def __visitar_invocacion(self, nodo: NodoArbol):
        pass

    def __visitar_parametros(self, nodo: NodoArbol):
        pass

    def __visitar_instruccion(self, nodo: NodoArbol):
        pass

    def __visitar_repeticion(self, nodo: NodoArbol):
        pass

    def __visitar_bifurcacion(self, nodo: NodoArbol):
        pass

    def __visitar_si(self, nodo: NodoArbol):
        pass

    def __visitar_sinnoh(self, nodo: NodoArbol):
        pass

    def __visitar_operador_logico(self, nodo: NodoArbol):
        pass

    def __visitar_condicion(self, nodo: NodoArbol):
        pass

    def __visitar_comparacion(self, nodo: NodoArbol):
        pass

    def __visitar_retorno(self, nodo: NodoArbol):
        pass

    def __visitar_error(self, nodo: NodoArbol):
        pass

    def __visitar_principal(self, nodo: NodoArbol):
        pass

    def __visitar_bloque_instrucciones(self, nodo: NodoArbol):
        pass

    def __visitar_operador(self, nodo: NodoArbol):
        pass

    def __visitar_string(self, nodo: NodoArbol):
        pass

    def __visitar_booleanos(self, nodo: NodoArbol):
        pass

    def __visitar_entero(self, nodo: NodoArbol):
        pass

    def __visitar_flotante(self, nodo: NodoArbol):
        pass

    def __visitar_identificador(self, nodo: NodoArbol):
        pass

    def __visitar_comparador(self, nodo: NodoArbol):
        pass

    def __visitar_equipo(self, nodo: NodoArbol):
        pass

    def __visitar_pokemon(self, nodo: NodoArbol):
        pass

    def __visitar_nombre_pokemon(self, nodo: NodoArbol):
        pass