from enum import Enum, auto
import copy

class TipoNodo(Enum):

    """
    Describe los tipos de nodo presentes en el ASA 
    """

    PROGRAMA = auto()
    ASIGNACION  = auto()
    ASIGNACION_GLOBAL = auto()
    TIPO = auto()
    EXPRESION = auto()
    OPERADOR = auto()
    FUNCION = auto()
    INVOCACION = auto()
    PARAMETROS = auto()
    #PARAMETROS_INVOCACION = auto()
    INSTRUCCION = auto()
    REPETICION = auto()
    BIFURCACION = auto()
    SI = auto()
    SINNOH = auto()
    #OPERADOR_LOGICO = auto()
    PRINCIPAL = auto()
    CONDICION = auto()
    COMPARACION = auto()
    RETORNO = auto()
    ERROR = auto()
    BLOQUE_INSTRUCCIONES = auto()
    STRING = auto()
    BOOLEANOS = auto()
    ENTERO = auto()
    FLOTANTE = auto()
    IDENTIFICADOR = auto()
    COMPARADOR = auto()
    EQUIPO = auto()
    POKEMON = auto()
    NOMBRE_POKEMON = auto()
    

class NodoArbol():
    
    """
    Nodos de los arboles propiamente, contiene su tipo
    """

    tipo : TipoNodo
    contenido : str
    atributos : dict

    def __init__(self, tipo, contenido=None, nodos=None, atributos=None):
        self.tipo = tipo
        self.contenido = contenido
        self.nodos = nodos if nodos is not None else []
        self.atributos = copy.deepcopy(atributos if atributos is not None else {})

    def nodeToStr(self):
        resultado = '{:30}\t'.format(self.tipo)
        
        if self.contenido is not None:
            resultado += '{:10}\t'.format(self.contenido)
        else:
            resultado += '{:10}\t'.format('')


        if self.atributos != {}:
            resultado += '{:38}'.format(str(self.atributos))
        else:
            resultado += '{:38}\t'.format('')

        if self.nodos != []:
            resultado += '<'

            # Imprime los tipos de los nodos del nivel siguiente
            for nodo in self.nodos[:-1]:
                if nodo is not None:
                    resultado += '{},'.format(nodo.tipo)

            resultado += '{}'.format(self.nodos[-1].tipo)
            resultado += '>'

        return resultado


class ArbolSintaxisAbstracta:
    
    raiz : NodoArbol
    
    def __init__(self):
        
        """
        Inicializa el árbol sintáctico abstracto.
        """
        
        self.raiz = None

    def insertar_nodo(self, nodo_padre: NodoArbol, nuevo_nodo: NodoArbol):
        
        """
        Inserta un nodo como hijo de otro nodo.
        Si el nodo raíz aún no existe, se establece como la raíz.
        """

        if self.raiz is None:
            self.raiz = nuevo_nodo
        elif nodo_padre:
            nodo_padre.nodos.append(nuevo_nodo)

    def imprimir_preorden(self):
        self.__preorden(self.raiz, nivel=0)

    def __preorden(self, nodo, nivel):
        if nodo is not None:
            print("  " * nivel + nodo.nodeToStr())
            for hijo in nodo.nodos:
                self.__preorden(hijo, nivel + 1)

# PRUEBAS 

if __name__ == '__main__':
    raiz = NodoArbol(TipoNodo.PROGRAMA, "Inicio")
    hijo1 = NodoArbol(TipoNodo.ASIGNACION, "x = 1")
    hijo2 = NodoArbol(TipoNodo.ASIGNACION, "y = 2")
    hijo3 = NodoArbol(TipoNodo.EXPRESION, "x + y")
    hijo4 = NodoArbol(TipoNodo.BOOLEANOS, "1")
    hijo5 = NodoArbol(TipoNodo.COMPARACION, "2")
    hijo6 = NodoArbol(TipoNodo.COMPARADOR, "3")

    arbol = ArbolSintaxisAbstracta()
    arbol.insertar_nodo(None, raiz)
    arbol.insertar_nodo(raiz, hijo1)
    arbol.insertar_nodo(raiz, hijo2)
    arbol.insertar_nodo(raiz, hijo3)
    arbol.insertar_nodo(hijo1, hijo4)
    arbol.insertar_nodo(hijo2, hijo5)
    arbol.insertar_nodo(hijo3, hijo6)

    arbol.imprimir_preorden()
 