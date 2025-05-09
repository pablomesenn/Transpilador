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

        # El explorador no está procesando los comentarios?

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
            nodos_nuevos.append(self.analizar_principal())
            
        else:
            raise Exception("Error de sintaxis: Se esperaba 'principal'")

        return NodoArbol(TipoNodo.PROGRAMA, nodos=nodos_nuevos) 

    def analizar_asignacion(self):

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
        
        # TODO: AHORA TOCA ANALIZAR EL LADO DERECHO DE LA ASIGNACIÓN: (Literal | Expresión | Invocación)
        # ! Hay que tener cuidado con la Expresión, tal vez sea necesario cambiarla



        pass


    def analizar_funcion(self):

        pass

    def analizar_equipo(self):
        pass

    def analizar_principal(self):
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