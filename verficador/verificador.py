# Verificador para PokeScript

from utils.arbol import ArbolSintaxisAbstracta, NodoArbol, TipoNodo
from utils.tipo_datos import TipoDatos

TIPOS_POKEMON_VALIDOS = {"agua", "fuego", "planta", "hielo"}

class TablaSimbolos:
    def __init__(self):
        self.profundidad = 0
        self.simbolos = []

    def abrir_bloque(self):
        self.profundidad += 1

    def cerrar_bloque(self):
        self.simbolos = [s for s in self.simbolos if s['profundidad'] != self.profundidad]
        self.profundidad -= 1

    def nuevo_registro(self, nodo):
        tipo_extra = None
        if hasattr(nodo, 'atributos') and 'tipo' in nodo.atributos:
            tipo_extra = nodo.atributos['tipo']

        self.simbolos.append({
            'nombre': nodo.contenido,
            'profundidad': self.profundidad,
            'referencia': nodo,
            'tipo_dato': tipo_extra
        })

    def verificar_existencia(self, nombre):
        for registro in reversed(self.simbolos):
            if registro['nombre'] == nombre:
                return registro
        raise Exception(f"Error semántico: '{nombre}' no ha sido declarado")

    def verificar_tipo_valido(self, tipo):
        if tipo not in TIPOS_POKEMON_VALIDOS:
            raise Exception(f"Tipo de Pokémon inválido: '{tipo}'")

class VisitantePokeScript:
    def __init__(self, tabla_simbolos):
        self.ts = tabla_simbolos

    def visitar(self, nodo: NodoArbol):
        metodo = getattr(self, f"_visitar_{nodo.tipo.name.lower()}", None)
        if metodo:
            metodo(nodo)
        for hijo in nodo.nodos:
            self.visitar(hijo)

    def _visitar_asignacion(self, nodo):
        ident, tipo, valor = nodo.nodos
        self.ts.verificar_tipo_valido(tipo.contenido)
        self.ts.nuevo_registro(ident)
        self.visitar(valor)
        ident.atributos['tipo'] = tipo.contenido
        nodo.atributos['tipo'] = tipo.contenido

    def _visitar_identificador(self, nodo):
        reg = self.ts.verificar_existencia(nodo.contenido)
        nodo.atributos['tipo'] = reg.get('tipo_dato', TipoDatos.CUALQUIERA)

    def _visitar_expresion(self, nodo):
        for n in nodo.nodos:
            self.visitar(n)
        tipos = [n.atributos.get('tipo') for n in nodo.nodos if n.atributos.get('tipo')]
        if len(set(tipos)) == 1:
            nodo.atributos['tipo'] = tipos[0]
        else:
            raise Exception("Tipos incompatibles en expresión")

    def _visitar_funcion(self, nodo):
        ident, parametros, bloque = nodo.nodos
        self.ts.nuevo_registro(ident)
        self.ts.abrir_bloque()
        for param in parametros.nodos:
            self.ts.nuevo_registro(param)
        self.visitar(bloque)
        self.ts.cerrar_bloque()
        nodo.atributos['tipo'] = bloque.atributos.get('tipo', TipoDatos.NINGUNO)

    def _visitar_invocacion(self, nodo):
        ident = nodo.nodos[0]
        reg = self.ts.verificar_existencia(ident.contenido)
        if reg['referencia'].tipo != TipoNodo.FUNCION:
            raise Exception(f"'{ident.contenido}' no es una función")
        nodo.atributos['tipo'] = reg['referencia'].atributos.get('tipo', TipoDatos.CUALQUIERA)

    def _visitar_comparacion(self, nodo):
        self.visitar(nodo.nodos[0])
        self.visitar(nodo.nodos[2])
        nodo.atributos['tipo'] = TipoDatos.BOOLEANO

    def _visitar_condicion(self, nodo):
        for comp in nodo.nodos:
            self.visitar(comp)
        nodo.atributos['tipo'] = TipoDatos.BOOLEANO

    def _visitar_retorno(self, nodo):
        if nodo.nodos:
            self.visitar(nodo.nodos[0])
            nodo.atributos['tipo'] = nodo.nodos[0].atributos.get('tipo', TipoDatos.CUALQUIERA)
        else:
            nodo.atributos['tipo'] = TipoDatos.NINGUNO

    def _visitar_bloque_instrucciones(self, nodo):
        self.ts.abrir_bloque()
        for instr in nodo.nodos:
            self.visitar(instr)
        self.ts.cerrar_bloque()
        tipos = [n.atributos.get('tipo') for n in nodo.nodos if n.atributos.get('tipo') != TipoDatos.NINGUNO]
        nodo.atributos['tipo'] = tipos[-1] if tipos else TipoDatos.NINGUNO

class Verificador:
    def __init__(self, asa: ArbolSintaxisAbstracta):
        self.asa = asa
        self.tabla = TablaSimbolos()
        self.visitante = VisitantePokeScript(self.tabla)
        self._cargar_ambiente_estandar()

    def _cargar_ambiente_estandar(self):
        funciones = [
            ('capturar', TipoDatos.BOOLEANO),
            ('ResetearStats', TipoDatos.NINGUNO),
            ('huir', TipoDatos.BOOLEANO),
        ]
        for nombre, tipo in funciones:
            nodo = NodoArbol(TipoNodo.FUNCION, contenido=nombre, atributos={'tipo': tipo})
            self.tabla.nuevo_registro(nodo)

    def verificar(self):
        self.visitante.visitar(self.asa.raiz)

    def imprimir_asa(self):
        if self.asa.raiz:
            self.asa.imprimir_preorden()
        else:
            print("El ASA está vacío")
