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

            # ASIGNACIÓN
            if self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:
                nodos_nuevos.append([self.analizar_asignacion()]) 
            
            # FUNCION
            elif self.componente_actual.tipo == TipoComponente.FUNCION:
                nodos_nuevos.append([self.analizar_funcion()])

            # EQUIPO
            elif self.componente_actual.texto == "equipo":
                nodos_nuevos.append([self.analizar_equipo()])

            else:
                break
        
        # PRINCIPAL
        if self.componente_actual.texto == "teReto!":
            nodos_nuevos.append([self.analizar_principal()])
            
        else:
            raise Exception("Error de sintaxis: Se esperaba 'principal'")

        return NodoArbol(TipoNodo.PROGRAMA, nodos=nodos_nuevos) 

    def analizar_asignacion(self):
        #! falta testear

        """
        Asignacion ::= Identificador Tipo = (Literal | Expresión | Invocación)
        """

        nodos_nuevos = []

        # El identificador es obligatorio al incio
        nodos_nuevos.append([self.verificar_identificador()])

        # Verificar el tipo
        nodos_nuevos.append([self.verificar_tipo()])
        
        # Verificar el signo de igual
        self.verificar("=")

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

    def analizar_expresion(self):
        # ! Esta implementacion es para darnos una idea, aun falta testearla, puede ocupar cambios en la gramatica
        """
        Expresión ::= Expresión Operador Expresión
                | (Expresión) 
                | Literal
                | Identificador
                | Invocación
            """
        
        # Caso simple: Si es un identificador
        if self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:
            identificador = self.verificar_identificador()
            return NodoArbol(TipoNodo.EXPRESION, nodos=[identificador])
        
        # Caso simple: Si es un literal (entero, flotante, string, booleano)
        elif (self.componente_actual.tipo == TipoComponente.STRING or 
            self.componente_actual.tipo == TipoComponente.ENTERO or 
            self.componente_actual.tipo == TipoComponente.FLOTANTE or 
            self.componente_actual.tipo == TipoComponente.BOOLEANO):
            
            tipo_nodo = self._convertir_tipo_componente_a_tipo_nodo(self.componente_actual.tipo)
            literal = NodoArbol(tipo_nodo, contenido=self.componente_actual.texto)
            self.__pasar_siguiente_componente()
            return NodoArbol(TipoNodo.EXPRESION, nodos=[literal])
        
        # Caso expresión entre paréntesis
        elif self.componente_actual.texto == "(":
            self.__pasar_siguiente_componente()  # Consumir '('
            expresion = self.analizar_expresion()
            
            if self.componente_actual.texto != ")":
                raise Exception(f"Error de sintaxis: Se esperaba ')', pero se encontró '{self.componente_actual.texto}'")
            
            self.__pasar_siguiente_componente()  # Consumir ')'
            return expresion
        
        # Caso invocación
        elif self.componente_actual.texto == "teElijo":
            invocacion = self.analizar_invocacion()
            return NodoArbol(TipoNodo.EXPRESION, nodos=[invocacion])
        
        # En un analizador más completo, aquí se manejaría la precedencia de operadores
        # y la construcción de expresiones complejas
        else:
            raise Exception(f"Error de sintaxis: Expresión inválida iniciando con '{self.componente_actual.texto}'")
    
    
    def analizar_funcion(self):
        pass

    def analizar_equipo(self):
        pass

    def analizar_principal(self):
        
        """
        Principal ::= teReto! BloqueInstrucciones
        """

        nodos_nuevos = []

        # Verificar el token "teReto!"
        self.verificar('teReto!')

        nodos_nuevos.append([self.analizar_bloque_instrucciones()])

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
            nodos_nuevos.append([self.analizar_instruccion()])

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
            nodos_nuevos.append([self.analizar_repeticion()])

        # Bifurcación
        elif self.componente_actual.texto == "si":
            nodos_nuevos.append([self.analizar_bifurcacion()])

        # Asignación
        elif self.componente_actual.tipo == TipoComponente.IDENTIFICADOR:
            nodos_nuevos.append([self.analizar_asignacion()]) #! analizar_asignacion() o está en proceso, faltan pruebas

        # Invocación
        elif self.componente_actual.texto == "teElijo":
            nodos_nuevos.append([self.analizar_invocacion()])

        # Retorno
        elif self.componente_actual.texto == "retirada":
            nodos_nuevos.append([self.analizar_retirada()])

        # Porta a mi los comentarios xD

        #TODO: Aquí podría agregarse el nodo nodos_nuevos[0]
        return NodoArbol(TipoNodo.INSTRUCCION, nodos=nodos_nuevos)

    def analizar_repeticion(self):
        
        """
        turnos (Condición | Entero) BloqueInstrucciones
        """

        nodos_nuevos = []

        # Verificar el token "turnos"
        self.verificar("turnos")
        # Verificar token "("
        self.verificar("(")
        # Verificar la condición    
        #if self.componente_actual.tipo == 

    def analizar_bifurcacion(self):
        
        nodos_nuevos = []
        pass

    def analizar_invocacion(self):
        
        nodos_nuevos = []
        pass

    def analizar_retirada(self):
        
        nodos_nuevos = []
        pass

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

    def verificar(self, string: str):

        """
        Verifica si el texto del componente léxico actual corresponde con
        el esperado cómo argumento
        """

        if self.componente_actual.texto != string:
            raise Exception(f"Error de sintaxis: Se esperaba '{string}', pero se encontró '{self.componente_actual.texto}'")

        self.__pasar_siguiente_componente()

    def verificar_tipo_componente(self, tipo: TipoComponente):
        """
        Verifica que el componente actual sea del tipo esperado.
        Si no lo es, lanza una excepción.
        """

        if self.componente_actual.tipo != tipo:
            raise Exception(f"Error de sintaxis: Se esperaba un componente de tipo '{tipo}', pero se encontró '{self.componente_actual.texto}'")

    def __pasar_siguiente_componente(self):

        self.posicion += 1

        if self.posicion >= self.cantidad_componentes:
            return