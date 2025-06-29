from utils.arbol import ArbolSintaxisAbstracta, NodoArbol, TipoNodo

class VisitanteGenerador:

    tabuladores = 0

    def visitar(self, nodo: NodoArbol):
        """
        Método que se llama para visitar un nodo del árbol.
        """

        resultado = ""

        if nodo.tipo == TipoNodo.PROGRAMA:
            resultado = self.__visitar_programa(nodo)

        elif nodo.tipo == TipoNodo.ASIGNACION:
            resultado = self.__visitar_asignacion(nodo)
        
        elif nodo.tipo == TipoNodo.TIPO:
            resultado = self.__visitar_tipo(nodo)
        
        elif nodo.tipo == TipoNodo.EXPRESION:
            resultado = self.__visitar_expresion(nodo)
        
        elif nodo.tipo == TipoNodo.FUNCION:
            resultado = self.__visitar_funcion(nodo)
        
        elif nodo.tipo == TipoNodo.INVOCACION:
            resultado = self.__visitar_invocacion(nodo)
        
        elif nodo.tipo == TipoNodo.PARAMETROS:
            resultado = self.__visitar_parametros(nodo)
        
        elif nodo.tipo == TipoNodo.INSTRUCCION:
            resultado = self.__visitar_instruccion(nodo)
        
        elif nodo.tipo == TipoNodo.REPETICION:
            resultado = self.__visitar_repeticion(nodo)
        
        elif nodo.tipo == TipoNodo.BIFURCACION:
            resultado = self.__visitar_bifurcacion(nodo)
        
        elif nodo.tipo == TipoNodo.SI: 
            resultado = self.__visitar_si(nodo)
        
        elif nodo.tipo == TipoNodo.SINNOH:
            resultado = self.__visitar_sinnoh(nodo)
        
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

        instrucciones = []

        for nodo_hijo in nodo.nodos:
            instrucciones.append(nodo_hijo.visitar(self)) 

        return '\n'.join(instrucciones)

    def __visitar_asignacion(self, nodo: NodoArbol):
        """
        Asignación ::= Identificador Tipo = (Literal | Expresión | Invocación)
        """

        resultado = """{} = {}"""

        instrucciones = []

        for nodo_hijo in nodo.nodos:
            instrucciones.append(nodo_hijo.visitar(self))

        return resultado.format(instrucciones[0], instrucciones[2]) # instrucciones[1] es el tipo    

    def __visitar_tipo(self, nodo: NodoArbol):
        """
        Tipo ::= planta | fuego | agua | hielo
        """

        return ''  # No se usa directamente en el código generado

    def __visitar_expresion(self, nodo: NodoArbol):
        """
        ExpresiónSimplificada ::= Término (Operador Término)*
        Término ::= Literal | Identificador | Invocación
        """

        instrucciones = []

        for nodo_hijo in nodo.nodos:
            instrucciones.append(nodo_hijo.visitar(self))

        return ' '.join(instrucciones)
        
    def __visitar_funcion(self, nodo: NodoArbol):
        """
        Función ::= batalla Identificador (Parámetros) BloqueInstrucciones
        """
        
        resultado = """\ndef {}({}):\n{}"""

        instrucciones = []

        for nodo_hijo in nodo.nodos:
            instrucciones.append(nodo_hijo.visitar(self))

        # instrucciones[0] es el identificador, instrucciones[1] son los parámetros, instrucciones[2] es el bloque de instrucciones
        return resultado.format(instrucciones[0], instrucciones[1], instrucciones[2])

    def __visitar_invocacion(self, nodo: NodoArbol):
        """
        Invocación ::= teElijo Identificador (Parámetros)
        """
        
        resultado = "{}({})"

        instrucciones = []

        for nodo_hijo in nodo.nodos:
            instrucciones.append(nodo_hijo.visitar(self))

        # instrucciones[0] es el identificador, instrucciones[1] son los parámetros
        return resultado.format(instrucciones[0], instrucciones[1])

    def __visitar_parametros(self, nodo: NodoArbol):
        """
        Parámetros ::= Valor (',' Valor)*
        """

        parametros = []

        for nodo_hijo in nodo.nodos:
            parametros.append(nodo_hijo.visitar(self))

        if len(parametros) > 0:
            return ','.join(parametros)

        else:
            return ''   

    def __visitar_instruccion(self, nodo: NodoArbol):
        """
        Instrucción ::= (Repetición 
                    | Bifurcación 
                    | Asignación 
                    | Invocación
                    | Retorno) 
        """
        
        valor = ""

        for nodo_hijo in nodo.nodos:
            valor += nodo_hijo.visitar(self)

        return valor

    def __visitar_repeticion(self, nodo: NodoArbol):
        """
        Repetición ::= turnos (Condición) BloqueInstrucciones
        """

        resultado = """while {}:\n{}"""

        instrucciones = []

        for nodo_hijo in nodo.nodos:
            instrucciones.append(nodo_hijo.visitar(self))

        # instrucciones[0] es la condición, instrucciones[1] es el bloque de instrucciones 
        return resultado.format(instrucciones[0], instrucciones[1])   

    def __visitar_bifurcación(self, nodo_actual):
        """
        Bifurcación ::= Si (Sinnoh)?
        """

        resultado = """{}{}"""

        instrucciones = []

        for nodo in nodo_actual.nodos:
            instrucciones.append(nodo.visitar(self))

        # Se asegura que haya dos elementos en la lista
        if len(instrucciones) == 1:
            instrucciones.append('')  # sinnoh no existe

        return resultado.format(instrucciones[0], instrucciones[1])

    def __visitar_si(self, nodo: NodoArbol):
        """
        Si ::= si (Condición) BloqueInstrucciones
        """

        resultado = """if {}:\n{}"""

        instrucciones = []

        for nodo_hijo in nodo.nodos:
            instrucciones.append(nodo_hijo.visitar(self))

        # instrucciones[0] es la condición, instrucciones[1] es el bloque de instrucciones
        return resultado.format(instrucciones[0], instrucciones[1])  

    def __visitar_sinnoh(self, nodo: NodoArbol):
        """
        Sinnoh ::= Sinnoh BloqueInstrucciones
        """

        resultado = """else:\n{}"""

        instrucciones = []

        for nodo_hijo in nodo.nodos:
            instrucciones.append(nodo_hijo.visitar(self))

        # instrucciones[0] es el bloque de instrucciones
        return resultado.format(instrucciones[0])

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