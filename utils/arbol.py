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
    INSTRUCCION = auto()
    REPETICION = auto()
    BIFURCACION = auto()
    SI = auto()
    SINNOH = auto()
    OPERADOR_LOGICO = auto()
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

    def visitar(self, visitador):
        return visitador.visitar(self)

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
    
    def imprimir_preorden_decorado(self):
        def _walk(nd, lvl):
            if nd is None:
                return

            indent = "|   " * (lvl - 1) + ("-> " if lvl else "")
            s = f"{nd.tipo.name}"
            if nd.contenido is not None:
                s += f"('{nd.contenido}')"

            extras = []
            if "tipo" in nd.atributos:
                extras.append(f"tipo={nd.atributos['tipo'].name if hasattr(nd.atributos['tipo'], 'name') else nd.atributos['tipo']}")
            if extras:
                s += " [" + ", ".join(extras) + "]"

            if nd.tipo.name == "IDENTIFICADOR" and "def_pos" in nd.atributos:
                ln, col = nd.atributos["def_pos"]
                s += f"  ->  línea {ln}:{col}"

            print(indent + s)
            for h in nd.nodos:
                _walk(h, lvl + 1)

        _walk(self.raiz, 0)


# PRUEBAS 

if __name__ == '__main__':
    # construimos un arbol mini para ver la salida
    raiz  = NodoArbol(TipoNodo.PROGRAMA)
    ident = NodoArbol(TipoNodo.IDENTIFICADOR, "dinero",
                      atributos={"tipo":"NÚMERO", "def_pos": (4,1)})
    ent   = NodoArbol(TipoNodo.ENTERO, "1000", atributos={"tipo":"NÚMERO"})
    asig  = NodoArbol(TipoNodo.ASIGNACION, nodos=[ident, ent],
                      atributos={"tipo":"NÚMERO"})
    raiz.nodos.append(asig)

    asa = ArbolSintaxisAbstracta()
    asa.raiz = raiz

    print("\n=== pre-orden clásico ===")
    asa.imprimir_preorden()

    print("\n=== pre-orden decorado ===")
    asa.imprimir_preorden_decorado()
 