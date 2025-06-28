from utils.arbol import ArbolSintaxisAbstracta, NodoArbol, TipoNodo
from generador.visitadores import VisitanteGenerador

class Generador: 

    asa : ArbolSintaxisAbstracta
    visitador : VisitanteGenerador

    ambiente_estandar = """


    """

    def __init__(self, asa: ArbolSintaxisAbstracta, visitador: str):
        self.asa = asa
        self.visitador = VisitanteGenerador()

    def imprimir_asa(self):
        """
        Imprime el arbol de sintaxis abstracta
        """
        if self.asa.raiz is None:
            print("El árbol sintáctico abstracto está vacío.")
            return
        else:
            self.asa.imprimir_preorden(self.asa.raiz)
            
    def generar_codigo(self):
        """
        Genera el código fuente a partir del árbol de sintaxis abstracta.
        """
        if self.asa.raiz is None:
            print("El árbol sintáctico abstracto está vacío.")
            return
        
        resultado = self.visitador.visitar(self.asa.raiz)
        
        print(self.ambiente_estandar)  # Imprime el ambiente estándar
        if resultado:
            print(resultado)  
        
        