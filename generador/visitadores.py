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
        """
        Programa ::= (Comentario | Asignación | Función | Equipo)* Principal
        """
        
        pass

    def __visitar_asignacion(self, nodo: NodoArbol):
        """
        Asignación ::= Identificador Tipo = (Literal | Expresión | Invocación)
        """

        pass

    def __visitar_tipo(self, nodo: NodoArbol):
        """
        Tipo ::= planta | fuego | agua | hielo
        """

        pass

    def __visitar_expresion(self, nodo: NodoArbol):
        """
        ExpresiónSimplificada ::= Término (Operador Término)*
        """

        pass

        
    def __visitar_funcion(self, nodo: NodoArbol):
        """
        Función ::= batalla Identificador (Parámetros) BloqueInstrucciones
        """
        
        pass

    def __visitar_invocacion(self, nodo: NodoArbol):
        """
        Invocación ::= teElijo Identificador (Parámetros)
        """
        
        pass

    def __visitar_parametros(self, nodo: NodoArbol):
        """
        Parámetros ::= Valor (',' Valor)*
        """

        pass

    def __visitar_instruccion(self, nodo: NodoArbol):
        """
        Instrucción ::= (Repetición 
                    | Bifurcación 
                    | Asignación 
                    | Invocación
                    | Retorno) 
        """
        
        pass

    def __visitar_repeticion(self, nodo: NodoArbol):
        """
        Repetición ::= turnos (Condición) BloqueInstrucciones
        """

        pass

    def __visitar_bifurcacion(self, nodo: NodoArbol):
        """
        Bifurcación ::= Si (Sinnoh)?
        """

        pass

    def __visitar_si(self, nodo: NodoArbol):
        """
        Si ::= si (Condición) BloqueInstrucciones
        """

        pass

    def __visitar_sinnoh(self, nodo: NodoArbol):
        """
        Sinnoh ::= Sinnoh BloqueInstrucciones
        """

        pass

    def __visitar_operador_logico(self, nodo: NodoArbol):
        """
        OperadorLógico ::= and | or
        """

        pass

    def __visitar_condicion(self, nodo: NodoArbol):
        """
        Condición ::= Comparación (OperadorLógico Comparación)*
        """

        pass

    def __visitar_comparacion(self, nodo: NodoArbol):
        """
        Comparación ::= Valor Comparador Valor
        """
        
        pass

    def __visitar_retorno(self, nodo: NodoArbol):
        """
        Retorno ::= retirada Valor
        """

        pass

    def __visitar_principal(self, nodo: NodoArbol):
        """
        Principal ::= teReto BloqueInstrucciones
        """

        pass

    def __visitar_bloque_instrucciones(self, nodo: NodoArbol):
        """
        BloqueInstrucciones ::= { Instrucción* }
        """

        pass

    def __visitar_operador(self, nodo: NodoArbol):
        """ 
        Operador ::= (ataque | poción | fortalecer | golpecritrico)
        """

        pass

    def __visitar_string(self, nodo: NodoArbol):
        """
        String ::= "(\w(\s\w))"
        """

        pass

    def __visitar_booleanos(self, nodo: NodoArbol):
        """
        Booleanos ::= capturado | escapó
        """

        pass

    def __visitar_entero(self, nodo: NodoArbol):
        """
        Entero ::= -?[0-9]+
        """

        pass

    def __visitar_flotante(self, nodo: NodoArbol):
        """
        Flotante ::= -?[0-9]+','[0-9]+
        """

        pass

    def __visitar_identificador(self, nodo: NodoArbol):
        """
        Identificador ::= [A-Za-z_][A-Za-z0-9_]*
        """

        pass

    def __visitar_comparador(self, nodo: NodoArbol):
        """
        Comparador ::= '==' | '!=' | '<' | '>' | '<=' | '>='
        """

        pass

    def __visitar_equipo(self, nodo: NodoArbol):
        """
        Equipo ::= equipo Identificador {Pokemon{1,6}}
        """

        pass

    def __visitar_pokemon(self, nodo: NodoArbol):
        """
        Pokemon ::= NombrePokemon {Entero, Float}
        """

        pass

    def __visitar_nombre_pokemon(self, nodo: NodoArbol):
        """
        NombrePokemon ::= poke[A-Za-z][A-Za-z0-9_-]+  
        """

        pass