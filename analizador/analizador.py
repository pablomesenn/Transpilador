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
            
            """
            EL BUCLE ANALIZA LA PARTE: (Comentario | Asignación | Función | Equipo)*
            """

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

        pass

    def analizar_funcion(self):

        pass

    def analizar_equipo(self):
        pass

    def analizar_principal(self):
        pass

    def __pasar_siguiente_componente(self):

        self.posicion += 1

        if self.posicion >= self.cantidad_componentes:
            return
    