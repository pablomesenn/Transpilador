from utils.arbol import ArbolSintaxisAbstracta, NodoArbol, TipoNodo

class VisitanteGenerador:

    def __init__(self):
        self.tabuladores = 0

    def visitar(self, nodo: NodoArbol):
        """
        Método que se llama para visitar un nodo del árbol.
        """
        if nodo is None:
            return ""

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
            resultado = self.__visitar_operador_logico(nodo)
        elif nodo.tipo == TipoNodo.CONDICION:
            resultado = self.__visitar_condicion(nodo)
        elif nodo.tipo == TipoNodo.COMPARACION:
            resultado = self.__visitar_comparacion(nodo)
        elif nodo.tipo == TipoNodo.RETORNO:
            resultado = self.__visitar_retorno(nodo)
        elif nodo.tipo == TipoNodo.PRINCIPAL:
            resultado = self.__visitar_principal(nodo)
        elif nodo.tipo == TipoNodo.BLOQUE_INSTRUCCIONES:
            resultado = self.__visitar_bloque_instrucciones(nodo)
        elif nodo.tipo == TipoNodo.OPERADOR:
            resultado = self.__visitar_operador(nodo)
        elif nodo.tipo == TipoNodo.STRING:
            resultado = self.__visitar_string(nodo)
        elif nodo.tipo == TipoNodo.BOOLEANOS:
            resultado = self.__visitar_booleanos(nodo)
        elif nodo.tipo == TipoNodo.ENTERO:
            resultado = self.__visitar_entero(nodo)
        elif nodo.tipo == TipoNodo.FLOTANTE:
            resultado = self.__visitar_flotante(nodo)
        elif nodo.tipo == TipoNodo.IDENTIFICADOR:
            resultado = self.__visitar_identificador(nodo)
        elif nodo.tipo == TipoNodo.COMPARADOR:
            resultado = self.__visitar_comparador(nodo)
        elif nodo.tipo == TipoNodo.EQUIPO:
            resultado = self.__visitar_equipo(nodo)
        elif nodo.tipo == TipoNodo.POKEMON:
            resultado = self.__visitar_pokemon(nodo)
        elif nodo.tipo == TipoNodo.NOMBRE_POKEMON:
            resultado = self.__visitar_nombre_pokemon(nodo)
        elif nodo.tipo == TipoNodo.ERROR:
            resultado = "# ERROR EN EL CÓDIGO"
                
        return resultado

    def __obtener_indentacion(self):
        """Retorna la indentación actual basada en el nivel de tabuladores"""
        return "    " * self.tabuladores

    def __visitar_programa(self, nodo: NodoArbol):
        """
        Programa ::= (Comentario | Asignación | Función | Equipo)* Principal
        """
        instrucciones = []

        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado and resultado.strip() and not resultado.startswith("# Error"):
                instrucciones.append(resultado)

        return '\n'.join(instrucciones)

    def __visitar_asignacion(self, nodo: NodoArbol):
        """
        Asignación ::= Identificador Tipo = (Literal | Expresión | Invocación)
        """
        instrucciones = []

        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            instrucciones.append(resultado)

        # Filtrar elementos vacíos y obtener solo los valores significativos
        valores_significativos = [inst for inst in instrucciones if inst and inst.strip()]
        
        if len(valores_significativos) >= 2:
            # El primer valor es el identificador, el último es el valor asignado
            identificador = valores_significativos[0]
            valor = valores_significativos[-1]
            return f"{self.__obtener_indentacion()}{identificador} = {valor}"
        else:
            return f"{self.__obtener_indentacion()}# Error en asignación - valores insuficientes"

    def __visitar_tipo(self, nodo: NodoArbol):
        """
        Tipo ::= planta | fuego | agua | hielo
        """
        return ''  # No se usa directamente en el código generado

    def __visitar_expresion(self, nodo: NodoArbol):
        """
        ExpresiónSimplificada ::= Término (Operador Término)*
        """
        instrucciones = []

        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado:
                instrucciones.append(resultado)

        return ' '.join(instrucciones)
        
    def __visitar_funcion(self, nodo: NodoArbol):
        """
        Función ::= batalla Identificador (Parámetros) BloqueInstrucciones
        """
        instrucciones = []

        for nodo_hijo in nodo.nodos:
            instrucciones.append(self.visitar(nodo_hijo))

        # instrucciones[0] es el identificador, instrucciones[1] son los parámetros, instrucciones[2] es el bloque
        nombre = instrucciones[0] if len(instrucciones) > 0 else "funcion_sin_nombre"
        parametros = instrucciones[1] if len(instrucciones) > 1 else ""
        bloque = instrucciones[2] if len(instrucciones) > 2 else "    pass"
        
        return f"def {nombre}({parametros}):\n{bloque}"

    def __visitar_invocacion(self, nodo: NodoArbol):
        """
        Invocación ::= teElijo Identificador (Parámetros)
        """
        instrucciones = []

        for nodo_hijo in nodo.nodos:
            instrucciones.append(self.visitar(nodo_hijo))

        # instrucciones[0] es el identificador, instrucciones[1] son los parámetros
        nombre = instrucciones[0] if len(instrucciones) > 0 else "funcion_sin_nombre"
        parametros = instrucciones[1] if len(instrucciones) > 1 else ""
        
        return f"{nombre}({parametros})"

    def __visitar_parametros(self, nodo: NodoArbol):
        """
        Parámetros ::= Valor (',' Valor)*
        """
        parametros = []

        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado:
                parametros.append(resultado)

        return ', '.join(parametros) if parametros else ''

    def __visitar_instruccion(self, nodo: NodoArbol):
        """
        Instrucción ::= (Repetición | Bifurcación | Asignación | Invocación | Retorno)
        """
        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado:
                return resultado
        return ""

    def __visitar_repeticion(self, nodo: NodoArbol):
        """
        Repetición ::= turnos (Condición) BloqueInstrucciones
        """
        instrucciones = []

        for nodo_hijo in nodo.nodos:
            instrucciones.append(self.visitar(nodo_hijo))

        condicion = instrucciones[0] if len(instrucciones) > 0 else "True"
        bloque = instrucciones[1] if len(instrucciones) > 1 else "    pass"
        
        return f"{self.__obtener_indentacion()}while {condicion}:\n{bloque}"

    def __visitar_bifurcacion(self, nodo: NodoArbol):
        """
        Bifurcación ::= Si (Sinnoh)?
        """
        instrucciones = []

        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado:
                instrucciones.append(resultado)

        # Unir el if y el else si existe
        return ''.join(instrucciones)

    def __visitar_si(self, nodo: NodoArbol):
        """
        Si ::= si (Condición) BloqueInstrucciones
        """
        instrucciones = []

        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado:
                instrucciones.append(resultado)

        condicion = instrucciones[0] if len(instrucciones) > 0 else "True"
        bloque = instrucciones[1] if len(instrucciones) > 1 else f"{self.__obtener_indentacion()}    pass"
        
        return f"{self.__obtener_indentacion()}if {condicion}:\n{bloque}"

    def __visitar_sinnoh(self, nodo: NodoArbol):
        """
        Sinnoh ::= sinnoh BloqueInstrucciones
        """
        instrucciones = []

        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado:
                instrucciones.append(resultado)

        bloque = instrucciones[0] if len(instrucciones) > 0 else f"{self.__obtener_indentacion()}    pass"
        
        return f"\n{self.__obtener_indentacion()}else:\n{bloque}"

    def __visitar_operador_logico(self, nodo: NodoArbol):
        """
        OperadorLógico ::= and | or
        """
        return nodo.contenido if nodo.contenido else "and"

    def __visitar_condicion(self, nodo: NodoArbol):
        """
        Condición ::= Comparación (OperadorLógico Comparación)*
        """
        elementos = []

        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado:
                elementos.append(resultado)

        return ' '.join(elementos)

    def __visitar_comparacion(self, nodo: NodoArbol):
        """
        Comparación ::= Valor Comparador Valor
        """
        elementos = []

        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado:
                elementos.append(resultado)

        if len(elementos) >= 3:
            return f"{elementos[0]} {elementos[1]} {elementos[2]}"
        else:
            return "True"  # Condición por defecto

    def __visitar_retorno(self, nodo: NodoArbol):
        """
        Retorno ::= retirada Valor
        """
        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado:
                return f"{self.__obtener_indentacion()}return {resultado}"
        
        return f"{self.__obtener_indentacion()}return"

    def __visitar_principal(self, nodo: NodoArbol):
        """
        Principal ::= teReto BloqueInstrucciones
        """
        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado:
                return f"if __name__ == '__main__':\n{resultado}"
        
        return "if __name__ == '__main__':\n    pass"

    def __visitar_bloque_instrucciones(self, nodo: NodoArbol):
        """
        BloqueInstrucciones ::= { Instrucción* }
        """
        self.tabuladores += 1
        instrucciones = []

        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado and resultado.strip():
                instrucciones.append(resultado)

        self.tabuladores -= 1

        if not instrucciones:
            return f"{self.__obtener_indentacion()}    pass"
        
        return '\n'.join(instrucciones)

    def __visitar_operador(self, nodo: NodoArbol):
        """
        Operador ::= (ataque | poción | fortalecer | golpecritrico)
        """
        mapeo_operadores = {
            "ataque": "+",
            "poción": "-", 
            "fortalecer": "*",
            "golpecritrico": "//"
        }
        
        return mapeo_operadores.get(nodo.contenido, "+")

    def __visitar_string(self, nodo: NodoArbol):
        """
        String ::= "(\w(\s\w))"
        """
        if not nodo.contenido:
            return '""'
        
        # Si el string ya tiene comillas, no las agregamos
        contenido = str(nodo.contenido)
        if contenido.startswith('"') and contenido.endswith('"'):
            return contenido
        elif contenido.startswith("'") and contenido.endswith("'"):
            return contenido
        else:
            # Si no tiene comillas, las agregamos
            return f'"{contenido}"'

    def __visitar_booleanos(self, nodo: NodoArbol):
        """
        Booleanos ::= capturado | escapó
        """
        mapeo_booleanos = {
            "capturado": "True",
            "escapó": "False",
            "escapo": "False"  # Variante sin tilde
        }
        
        contenido = str(nodo.contenido).lower() if nodo.contenido else ""
        return mapeo_booleanos.get(contenido, "True")

    def __visitar_entero(self, nodo: NodoArbol):
        """
        Entero ::= -?[0-9]+
        """
        return str(nodo.contenido) if nodo.contenido else "0"

    def __visitar_flotante(self, nodo: NodoArbol):
        """
        Flotante ::= -?[0-9]+','[0-9]+
        """
        # Convertir la coma decimal a punto decimal para Python
        if nodo.contenido:
            return str(nodo.contenido).replace(',', '.')
        return "0.0"

    def __visitar_identificador(self, nodo: NodoArbol):
        """
        Identificador ::= [A-Za-z_][A-Za-z0-9_]*
        """
        return str(nodo.contenido) if nodo.contenido else "variable"

    def __visitar_comparador(self, nodo: NodoArbol):
        """
        Comparador ::= '==' | '!=' | '<' | '>' | '<=' | '>='
        """
        return str(nodo.contenido) if nodo.contenido else "=="

    def __visitar_equipo(self, nodo: NodoArbol):
        """
        Equipo ::= equipo Identificador {Pokemon{1,6}}
        """
        elementos = []

        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado:
                elementos.append(resultado)

        if len(elementos) >= 2:
            nombre_equipo = elementos[0]
            pokemones = elementos[1:]
            lista_pokemones = '[' + ', '.join(pokemones) + ']'
            return f"{self.__obtener_indentacion()}{nombre_equipo} = {lista_pokemones}"
        
        return f"{self.__obtener_indentacion()}# Error en definición de equipo"

    def __visitar_pokemon(self, nodo: NodoArbol):
        """
        Pokemon ::= NombrePokemon {Entero, Float}
        """
        elementos = []

        for nodo_hijo in nodo.nodos:
            resultado = self.visitar(nodo_hijo)
            if resultado:
                elementos.append(resultado)

        if len(elementos) >= 3:
            nombre = elementos[0]
            nivel = elementos[1]
            hp = elementos[2]
            return f'{{"nombre": "{nombre}", "nivel": {nivel}, "hp": {hp}}}'
        elif len(elementos) >= 1:
            nombre = elementos[0]
            return f'{{"nombre": "{nombre}", "nivel": 1, "hp": 100.0}}'
        
        return '{"nombre": "pokemon_sin_nombre", "nivel": 1, "hp": 100.0}'

    def __visitar_nombre_pokemon(self, nodo: NodoArbol):
        """
        NombrePokemon ::= poke[A-Za-z][A-Za-z0-9_-]+
        """
        return str(nodo.contenido) if nodo.contenido else "pokemon_sin_nombre"