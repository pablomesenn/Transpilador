from explorador.explorador import TipoComponente, ComponenteLexico
from utils.arbol import TipoNodo, NodoArbol, ArbolSintaxisAbstracta

class AnalizadorLexico:
    
    """
    Clase que representa el analizador léxico. 
    Se encarga de leer el código fuente y generar el árbol de sintáxis abstracto.
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
        Método principal que inicia el análisis siguiendo el esquema de
        análisis por descenso recursivo
        """

        self.asa.raiz = self.__analizar_programa()

    def __analizar_programa(self):

        """
        Programa ::= (Comentario | Asignación | Función | Equipo )* Principal
        """

        nodos_nuevos = []

        while True:
            tipo = self.componente_actual.tipo
            texto = self.componente_actual.texto

            if tipo == TipoComponente.IDENTIFICADOR:
                nodos_nuevos.append(self.__analizar_asignacion())

            elif tipo == TipoComponente.FUNCION:
                nodos_nuevos.append(self.__analizar_funcion())

            else:
                break

        return NodoArbol(TipoNodo.PROGRAMA, nodos=nodos_nuevos)

    #def __analizar_asignacion(self):

    #def __analizar_funcion(self):

    #def __analizar_equipo(self): ?

    def __pasar_siguiente_componente(self):

        self.posicion += 1

        if self.posicion >= self.cantidad_componentes:
            return