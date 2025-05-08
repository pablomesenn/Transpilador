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
    #BLOQUE_INSTRUCCIONES = auto()
    STRING = auto()
    BOOLEANOS = auto()
    COMPARADOR = auto()
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

    def __init__(self, tipo, contenido = None, nodos = [], atributos= {}):

        self.tipo = tipo
        self.contenido = contenido
        self.nodos = nodos
        self.atributos = copy.deepcopy(atributos)

    """ 
    NO IMPLEMENTADO AÚN

    def visitar(self, visitador):
        return visitador.visitar(self)
    """

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

    def imprimir_preorden(self):
        self.__preorden(self.raiz)

    def __preorden(self, nodo):

        print(nodo)

        if nodo is not None:
            for nodo in nodo.nodos:
                self.__preorden(nodo)
