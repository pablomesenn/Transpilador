from explorador.explorador import TipoComponente, ComponenteLexico
from utils.arbol import TipoNodo, NodoArbol, ArbolSintaxisAbstracta

class AnalizadorLexico:
    
    """
    Clase que representa el analizador léxico. 
    Se encarga de procesar los componentes léxicos y generar el ASA.
    """

    componentes_lexicos: list
    cantidad_componentes: int
    posicion_componente_actual: int
    componente_actual: ComponenteLexico

    def __init__(self, lista_componentes: list):

        self.posicion_componente_actual = 0
        self.asa = ArbolSintaxisAbstracta()
        self.componentes_lexicos = lista_componentes
        self.cantidad_componentes = len(lista_componentes)
        self.componente_actual = lista_componentes[0] if lista_componentes else None

    def imprimir_asa(self):

        """
        Imprime el árbol de sintaxis abstracta.
        """
        
        if self.componente_actual is None:
            self.asa.imprimir_preorden
        else:
            print([])

    def analizar(self):

        """
        Método principal que inicia el análisis siguiendo el algoritmo de
        análisis por descenso recursivo
        """

        self.asa.raiz = self.__analizar_programa()

    def __analizar_programa(self):

        """
        Programa ::= (Comentario | Asignación | Función | Equipo )* Principal
        """

        # El explorador no está procesando los comentarios? no tiene que procesarlos

        nodos_nuevos = []

        while True:
            
            # EL BUCLE ANALIZA LA PARTE: (Comentario | Asignación | Función | Equipo)*
            print("Tipo: " + self.componente_actual.tipo)
            # ASIGNACIÓN
            if self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:
                nodos_nuevos.append(self.analizar_asignacion()) 
            
            # FUNCION
            elif self.componente_actual.tipo == TipoComponente.FUNCION:
                nodos_nuevos.append(self.analizar_funcion())

            # EQUIPO
            elif self.componente_actual.texto == "equipo":
                nodos_nuevos.append(self.analizar_equipo())

            else:
                break
        
        # PRINCIPAL
        if self.componente_actual.texto == "teReto!":
            nodos_nuevos.append(self.analizar_principal())
            
        else:
            raise Exception("Error de sintaxis: Se esperaba 'principal'")

        return NodoArbol(TipoNodo.PROGRAMA, nodos=nodos_nuevos) 

    def analizar_asignacion(self):
        
        """
        Asignacion ::= Identificador Tipo = (Literal | Expresión | Invocación)
        """
        
        nodos_nuevos = []

        # El identificador es obligatorio al inicio
        identificador = self.verificar_identificador()
        nodos_nuevos.append(identificador)

        # Verificar el tipo
        tipo = self.verificar_tipo()
        nodos_nuevos.append(tipo)

        # Verificar el signo de igual
        self.verificar("=")
        self.__pasar_siguiente_componente()

        # Analizar el lado derecho de la asignación: (Literal | Expresión | Invocación)
        # Verificamos qué tipo de valor tenemos a la derecha
        
        # Caso 1: Literal (String, Entero, Flotante, Booleano)
        if (self.componente_actual.tipo == TipoComponente.STRING or 
            self.componente_actual.tipo == TipoComponente.ENTERO or 
            self.componente_actual.tipo == TipoComponente.FLOTANTE or 
            self.componente_actual.tipo == TipoComponente.BOOLEANO):
            
            # Crear nodo según el tipo de literal
            tipo_nodo = self._convertir_tipo_componente_a_tipo_nodo(self.componente_actual.tipo)
            valor = NodoArbol(tipo_nodo, contenido=self.componente_actual.texto)
            nodos_nuevos.append(valor)
            self.__pasar_siguiente_componente()
            
        # Caso 2: Invocación (teElijo Identificador (Parámetros))
        elif self.componente_actual.texto == "teElijo":
            nodos_nuevos.append(self.analizar_invocacion())
            
        # Caso 3: Expresión (puede ser identificador, paréntesis o parte de expresión compleja)
        else:
            nodos_nuevos.append(self.analizar_expresion())
        
        # Crear y devolver el nodo de asignación con todos sus componentes
        return NodoArbol(TipoNodo.ASIGNACION, nodos=nodos_nuevos)
    
    def _convertir_tipo_componente_a_tipo_nodo(self, tipo_componente):
        """
        Convierte un TipoComponente a un TipoNodo correspondiente para literales
        """
        mapa_conversion = {
            TipoComponente.STRING: TipoNodo.STRING,
            TipoComponente.ENTERO: TipoNodo.ENTERO,
            TipoComponente.FLOTANTE: TipoNodo.FLOTANTE,
            TipoComponente.BOOLEANO: TipoNodo.BOOLEANOS
        }
    
        return mapa_conversion.get(tipo_componente, None)
    
    def analizar_expresion(self):
        
        """
        Expresión simplificada ::= Término (Operador Término)*
        Término ::= Literal | Identificador | Invocación
        """
        
        # Analizamos el primer término
        termino_izquierdo = self.analizar_termino()
        
        # Nodo inicial de la expresión
        nodo_expresion = NodoArbol(TipoNodo.EXPRESION, nodos=[termino_izquierdo])
        
        # Si después del término hay un operador, continuamos analizando la expresión
        while (self.componente_actual and 
            self.componente_actual.tipo == TipoComponente.OPERADOR):
            
            # Crear nodo para el operador
            operador = NodoArbol(TipoNodo.OPERADOR, contenido=self.componente_actual.texto)
            self.__pasar_siguiente_componente()
            
            # Analizar el término derecho
            termino_derecho = self.analizar_termino()
            
            # Actualizar el nodo de expresión para incluir el operador y el término derecho
            nodo_expresion.nodos.append(operador)
            nodo_expresion.nodos.append(termino_derecho)

        return nodo_expresion    
        
    def analizar_termino(self):
            """
            Término ::= Literal | Identificador | Invocación
            """
            # Caso 1: Si es un identificador
            if self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:
                return self.verificar_identificador()
            
            # Caso 2: Si es un literal (entero, flotante, string, booleano)
            elif (self.componente_actual.tipo == TipoComponente.STRING or 
                self.componente_actual.tipo == TipoComponente.ENTERO or 
                self.componente_actual.tipo == TipoComponente.FLOTANTE or 
                self.componente_actual.tipo == TipoComponente.BOOLEANO):
                
                tipo_nodo = self._convertir_tipo_componente_a_tipo_nodo(self.componente_actual.tipo)
                literal = NodoArbol(tipo_nodo, contenido=self.componente_actual.texto)
                self.__pasar_siguiente_componente()
                return literal
            
            # Caso 3: Invocación
            elif self.componente_actual.texto == "teElijo":
                return self.analizar_invocacion()
            
            else:
                raise Exception(f"Error de sintaxis: Se esperaba un término válido, pero se encontró '{self.componente_actual.texto}'")

    def analizar_invocacion(self):
        
        """
        Invocación ::= teElijo Identificador (Parámetros)
        """

        # Verificar que comience con "teElijo"
        self.verificar("teElijo")
        self.__pasar_siguiente_componente()
        
        # Obtener el identificador
        identificador = self.verificar_identificador()
        
        # Verificar el paréntesis de apertura
        self.verificar("(")
        self.__pasar_siguiente_componente()
        
        # Analizar los parámetros
        parametros = self.analizar_parametros()
        
        # Verificar el paréntesis de cierre
        self.verificar(")")
        self.__pasar_siguiente_componente()
        
        # Crear y devolver el nodo de invocación
        return NodoArbol(TipoNodo.INVOCACION, nodos=[identificador, parametros])

    def analizar_parametros(self):
        
        """
        Parámetros ::= Valor (',' Valor)*
        """
        
        parametros = []
        
        # Si no hay parámetros (cierre inmediato)
        if self.componente_actual.texto == ")":
            return NodoArbol(TipoNodo.PARAMETROS, nodos=parametros)
        
        # Analizar el primer valor
        parametros.append(self.analizar_valor())
        
        # Mientras encontremos comas, analizar más valores
        while self.componente_actual.texto == ",":
            self.__pasar_siguiente_componente()  # Consumir ','
            parametros.append(self.analizar_valor())
        
        return NodoArbol(TipoNodo.PARAMETROS, nodos=parametros)

    def analizar_valor(self):
        """
        Valor ::= (Identificador | Literal)
        """
        # Si es un identificador
        if self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:
            return self.verificar_identificador()
        
        # Si es un literal (entero, flotante, string, booleano)
        elif (self.componente_actual.tipo == TipoComponente.STRING or 
            self.componente_actual.tipo == TipoComponente.ENTERO or 
            self.componente_actual.tipo == TipoComponente.FLOTANTE or 
            self.componente_actual.tipo == TipoComponente.BOOLEANO):
            
            tipo_nodo = self._convertir_tipo_componente_a_tipo_nodo(self.componente_actual.tipo)
            valor = NodoArbol(tipo_nodo, contenido=self.componente_actual.texto)
            self.__pasar_siguiente_componente()
            return valor
        
        else:
            raise Exception(f"Error de sintaxis: Se esperaba un identificador o un literal, pero se encontró '{self.componente_actual.texto}'")
        
    def analizar_funcion(self):

        """
        Función ::= batalla Identificador (Parámetros) { Instruccion*}
        """
        nodos_nuevos = []

        self.verificar("batalla")
        nodos_nuevos.append(self.verificar_identificador())
        self.verificar("(") 
        nodos_nuevos.append(self.analizar_parametros())
        self.verificar(")")
        nodos_nuevos.append(self.analizar_bloque_instrucciones())

        return NodoArbol(TipoNodo.FUNCION, nodos=nodos_nuevos)
        
    def analizar_equipo(self):
        """
        Equipo ::= equipo Identificador { Pokemon{1,6} }
        """

        nodos_nuevos = []

        # Palabra clave "equipo"
        self.verificar("equipo")

        # Nombre del equipo (identificador)
        nodos_nuevos.append(self.verificar_identificador())

        # Llave de apertura
        self.verificar("{")

        # Al menos 1 y como máximo 6 Pokémon
        cantidad_pokemones = 0
        while self.componente_actual.tipo == TipoComponente.NOMBRE_POKEMON:
            if cantidad_pokemones == 6:
                raise Exception("Error de sintaxis: Un equipo no puede tener más de 6 Pokémon.")
            
            nodos_nuevos.append(self.analizar_pokemon())
            cantidad_pokemones += 1

        if cantidad_pokemones == 0:
            raise Exception("Error de sintaxis: Se esperaba al menos un Pokémon.")

        # Llave de cierre
        self.verificar("}")

        return NodoArbol(TipoNodo.EQUIPO, nodos=nodos_nuevos)

    def analizar_pokemon(self):
        
        """
        Pokemon::= NombrePokemon {Entero, Float}
        """

        nodos_nuevos = []
        
        # Verificar el nombre del Pokémon
        self.verificar_tipo_componente(TipoComponente.NOMBRE_POKEMON)
        nodos_nuevos.append(NodoArbol(TipoNodo.NOMBRE_POKEMON, contenido=self.componente_actual.texto))
        self.__pasar_siguiente_componente()

        self.verificar("{")
        
        nodos_nuevos.append(self.verificar_enteros())
        nodos_nuevos.append(self.verificar_flotantes())
        
        self.verificar("}")

        return NodoArbol(TipoNodo.POKEMON, nodos=nodos_nuevos)
    
    def analizar_principal(self):
        
        """
        Principal ::= teReto! BloqueInstrucciones
        """

        nodos_nuevos = []

        # Verificar el token "teReto!"
        self.verificar('teReto!')

        nodos_nuevos.append(self.analizar_bloque_instrucciones())

        return NodoArbol(TipoNodo.PRINCIPAL, nodos=nodos_nuevos)

    def analizar_bloque_instrucciones(self):    
        
        """
        Para factorizar código, viene como sugerencia en el analizador del profesor
        
        BloqueInstrucciones ::= { Instrucción* }
        """
        
        nodos_nuevos = []

        # Verificar el token '{'
        self.verificar("{")

        # Instrucciones dentro del bloque, pueden ser 0 o más
        while self.componente_actual.texto in ['turnos', 'si', 'sinnoh', 'retirada'] or self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:
            nodos_nuevos.append(self.analizar_instruccion())

        # Verificar el token '}'
        self.verificar("}")

        return NodoArbol(TipoNodo.BLOQUE_INSTRUCCIONES, nodos=nodos_nuevos)

    def analizar_instruccion(self):

        """
        Instrucción ::= (Repetición | Bifurcación | Asignación | Invoación | Retorno) 
        """

        nodos_nuevos = []

        # Repetición
        if self.componente_actual.texto == "turnos":
            nodos_nuevos.append(self.analizar_repeticion())

        # Bifurcación
        elif self.componente_actual.texto == "si":
            nodos_nuevos.append(self.analizar_bifurcacion())

        # Asignación
        elif self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:
            nodos_nuevos.append(self.analizar_asignacion())

        # Invocación
        elif self.componente_actual.texto == "teElijo":
            nodos_nuevos.append(self.analizar_invocacion())

        # Retorno
        elif self.componente_actual.texto == "retirada":
            nodos_nuevos.append(self.analizar_retorno())

        # Porta a mi los comentarios xD

        #TODO: Aquí podría agregarse el nodo nodos_nuevos[0]
        return NodoArbol(TipoNodo.INSTRUCCION, nodos=nodos_nuevos)

    def analizar_repeticion(self):
        
        """
        Repetición ::= turnos (Condición) BloqueInstrucciones
        """

        nodos_nuevos = []

        # Verificar el token "turnos"
        self.verificar("turnos")
        # Verificar token "("
        self.verificar("(")
        # Verificar la condición    
        nodos_nuevos.append(self.analizar_condicion())
        # Verificar token ")"
        self.verificar(")")

        # Analizar el bloque de instrucciones
        nodos_nuevos.append(self.analizar_bloque_instrucciones())

        return NodoArbol(TipoNodo.REPETICION, nodos=nodos_nuevos)

    def analizar_bifurcacion(self):
        
        """
        Bifurcación ::= Si (Sinnoh)?
        """

        nodos_nuevos = []

        # La regla "si" es obligatorio
        nodos_nuevos.append(self.analizar_si())
        # Si hay un "sinnoh" opcional
        if self.componente_actual.texto == "sinnoh":
            nodos_nuevos.append(self.analizar_sinnoh())

        return NodoArbol(TipoNodo.BIFURCACION, nodos=nodos_nuevos)

    def analizar_si(self):
        
        """
        Si ::= si (Condición) BloqueInstrucciones
        """

        nodos_nuevos = []

        # Verificar el token "si"
        self.verificar("si")
        # Verificar token "("
        self.verificar("(")
        # Verificar la condición    
        nodos_nuevos.append(self.analizar_condicion())
        # Verificar token ")"
        self.verificar(")")

        # Analizar el bloque de instrucciones
        nodos_nuevos.append(self.analizar_bloque_instrucciones())

        return NodoArbol(TipoNodo.SI, nodos=nodos_nuevos)

    def analizar_sinnoh(self):
        """
        Sinnoh ::= sinnoh BloqueInstrucciones
        """

        nodos_nuevos = []

        # Verificar el token "sinnoh"
        self.verificar("sinnoh")

        # Analizar el bloque de instrucciones
        nodos_nuevos.append(self.analizar_bloque_instrucciones())

        return NodoArbol(TipoNodo.SINNOH, nodos=nodos_nuevos)

    def analizar_condicion(self):
        
        """
        Condición ::= Comparación (OperadorLógico Comparación)*
        """

        nodos_nuevos = []

        # Verificar la comparación
        nodos_nuevos.append(self.analizar_comparacion())
        
        # Verificar el operador lógico
        while self.componente_actual.tipo == TipoComponente.OPERADOR_LOGICO:
            
            nodos_nuevos.append(self.analizar_operador_logico())
            # Verificar la comparación
            nodos_nuevos.append(self.analizar_comparacion())
        
        return NodoArbol(TipoNodo.CONDICION, nodos=nodos_nuevos)

    def analizar_comparacion(self):
        
        """
        Comparación ::= Valor Comparador Valor
        """ 
        
        nodos_nuevos = []

        # Verificar el primer valor
        nodos_nuevos.append(self.analizar_valor)
        # Verificar el comparador
        nodos_nuevos.append(self.analizar_comparador())
        # Verificar el segundo valor
        nodos_nuevos.append(self.analizar_valor())

        return NodoArbol(TipoNodo.COMPARACION, nodos=nodos_nuevos)

    def analizar_operador_logico(self):
        
        """
        OperadorLógico ::= and | or
        """

        # Verificar el operador lógico
        self.verificar_tipo_componente(TipoComponente.OPERADOR_LOGICO)

        # Agregar el nodo al árbol
        nodo = NodoArbol(TipoNodo.OPERADOR_LOGICO, contenido=self.componente_actual.texto)

        # Pasar al siguiente componente
        self.__pasar_siguiente_componente()

        return nodo

    #TODO: Tal vez haga falta manejar los literales como lo hace victor en analizar_asignacion()

    def analizar_literal(self):
        
        """
        Literal ::= Entero | Flotante | String | Booleano 
        """

        if self.componente_actual.tipo == TipoComponente.ENTERO:
            return self.verificar_enteros()

        elif self.componente_actual.tipo == TipoComponente.FLOTANTE:
            return self.verificar_flotantes()
        
        elif self.componente_actual.tipo == TipoComponente.STRING:
            return self.verificar_string()
        
        elif self.componente_actual.tipo == TipoComponente.BOOLEANO:
            return self.verificar_booleano()
        
        else:
            raise Exception(f"Error de sintaxis: Se esperaba un literal, pero se encontró '{self.componente_actual.texto}'")

    def analizar_comparador(self):
        
        """
        Comparador ::= '==' | '!=' | '<' | '>' | '<=' | '>='
        """

        # Verificar el comparador
        self.verificar_tipo_componente(TipoComponente.COMPARADOR)

        # Agregar el nodo al árbol
        nodo = NodoArbol(TipoNodo.COMPARADOR, contenido=self.componente_actual.texto)

        # Pasar al siguiente componente
        self.__pasar_siguiente_componente()

        return nodo
    
    def analizar_retorno(self):

        """
        Retorno ::= retirada Valor
        """
        
        nodos_nuevos = []

        # Verificar el token "retirada"
        self.verificar("retirada")
        # Verificar el valor
        nodos_nuevos.append(self.analizar_valor())
        # Crear y devolver el nodo de retorno
        return NodoArbol(TipoNodo.RETORNO, nodos=nodos_nuevos)

    def verificar_identificador(self):
        
        """
        Verifica que el componente actual sea un identificador.
        Si no lo es, lanza una excepción.
        """

        self.verificar_tipo_componente(TipoComponente.IDENTIFICADOR)

        # Agregar el nodo al árbol
        nodo = NodoArbol(TipoNodo.IDENTIFICADOR, contenido = self.componente_actual.texto)

        # Pasar al siguiente componente
        self.__pasar_siguiente_componente()

        return nodo

    def verificar_tipo(self):
        
        """
        Verifica que el componente actual sea un tipo.
        Si no lo es, lanza una excepción.
        """

        self.verificar_tipo_componente(TipoComponente.TIPO)

        # Agregar el nodo al árbol
        nodo = NodoArbol(TipoNodo.TIPO, contenido = self.componente_actual.texto)

        # Pasar al siguiente componente
        self.__pasar_siguiente_componente()

        return nodo

    # FUNCIONES AUXILIARES

    def verificar_string(self):

        """
        Verifica que el componente actual sea un string.
        Si no lo es, lanza una excepción.
        """

        self.verificar_tipo_componente(TipoComponente.STRING)

        # Agregar el nodo al árbol
        nodo = NodoArbol(TipoNodo.STRING, contenido = self.componente_actual.texto)

        # Pasar al siguiente componente
        self.__pasar_siguiente_componente()

        return nodo
    
    def verificar_booleano(self):

        """
        Verifica que el componente actual sea un booleano.
        Si no lo es, lanza una excepción.
        """

        self.verificar_tipo_componente(TipoComponente.BOOLEANO)

        # Agregar el nodo al árbol
        nodo = NodoArbol(TipoNodo.BOOLEANO, contenido = self.componente_actual.texto)

        # Pasar al siguiente componente
        self.__pasar_siguiente_componente()

        return nodo

    def verificar_enteros(self):
        """
        Verifica que el componente actual sea un entero.
        Si no lo es, lanza una excepción.
        """

        self.verificar_tipo_componente(TipoComponente.ENTERO)

        # Agregar el nodo al árbol
        nodo = NodoArbol(TipoNodo.ENTERO, contenido = self.componente_actual.texto)

        # Pasar al siguiente componente
        self.__pasar_siguiente_componente()

        return nodo
    
    def verificar_flotantes(self):
        """
        Verifica que el componente actual sea un flotante.
        Si no lo es, lanza una excepción.
        """

        self.verificar_tipo_componente(TipoComponente.FLOTANTE)

        # Agregar el nodo al árbol
        nodo = NodoArbol(TipoNodo.FLOTANTE, contenido = self.componente_actual.texto)

        # Pasar al siguiente componente
        self.__pasar_siguiente_componente()

        return nodo

    def verificar(self, string: str):

        """
        Verifica si el texto del componente léxico actual corresponde con
        el esperado cómo argumento
        """
        if self.componente_actual is None:
            raise Exception(f"Error de sintaxis: Se esperaba '{string}', pero se llegó al final del archivo")
            
        if self.componente_actual.texto != string:
            raise Exception(f"Error de sintaxis: Se esperaba '{string}', pero se encontró '{self.componente_actual.texto}'")
        
    def verificar_tipo_componente(self, tipo: TipoComponente):
        """
        Verifica que el componente actual sea del tipo esperado.
        Si no lo es, lanza una excepción.
        """

        if self.componente_actual is None:
            raise Exception(f"Error de sintaxis: Se esperaba un componente de tipo '{tipo}', pero se llegó al final del archivo")
        
        if self.componente_actual.tipo != tipo:
            raise Exception(f"Error de sintaxis: Se esperaba un componente de tipo '{tipo}', pero se encontró '{self.componente_actual.texto}'") 

    def __pasar_siguiente_componente(self):

        """
        Avanza al siguiente componente léxico.
        """
        self.posicion_componente_actual += 1
        if self.posicion_componente_actual < self.cantidad_componentes:
            self.componente_actual = self.componentes_lexicos[self.posicion_componente_actual]
        else:
            self.componente_actual = None