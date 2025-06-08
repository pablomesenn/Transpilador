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

        for reg in reversed(self.simbolos):
            if reg['nombre'] == nodo.contenido and reg['profundidad'] == self.profundidad:
                raise VariableYaDeclarada(nodo.contenido)

        self.simbolos.append({
            'nombre': nodo.contenido,
            'profundidad': self.profundidad,
            'referencia': nodo,
            'tipo': tipo_extra
        })

        print(f"[REGISTRO] {nodo.contenido} registrado con tipo {tipo_extra} en profundidad {self.profundidad}")

    def verificar_existencia(self, nombre):
        for registro in reversed(self.simbolos):
            if registro['nombre'] == nombre:
                return registro
        raise VariableNoDeclarada(nombre)

    def verificar_tipo_valido(self, tipo):
        if tipo not in TIPOS_POKEMON_VALIDOS:
            raise TipoNoReconocido(tipo)

    def buscar(self, nombre):
        for reg in reversed(self.simbolos):
            if reg['nombre'] == nombre:
                return {'tipo_dato': reg['tipo'], 'referencia': reg['referencia']}
        return None

class VisitantePokeScript:

    OPERADORES_VALIDOS = {"ataque", "curación", "poción"}  

    def __init__(self, tabla_simbolos):
        self.ts = tabla_simbolos

    def visitar(self, nodo: NodoArbol):
        metodo = getattr(self, f"_visitar_{nodo.tipo.name.lower()}", None)
        if metodo:
            metodo(nodo)
        else:
            for hijo in nodo.nodos:
                self.visitar(hijo)
        print(f"[VISITANDO] Nodo tipo: {nodo.tipo}, contenido: {getattr(nodo, 'contenido', '')}")

    def _visitar_principal(self, nodo):
        # El nodo contiene el bloque principal del programa
        self.visitar(nodo.nodos[0])
        nodo.atributos['tipo'] = nodo.nodos[0].atributos.get('tipo', TipoDatos.NINGUNO)

    def _visitar_repeticion(self, nodo):
        condicion, cuerpo = nodo.nodos
        self.visitar(condicion)
        if condicion.atributos.get('tipo') != TipoDatos.BOOLEANO:
            raise Exception("La condición del ciclo debe ser booleana")
        self.visitar(cuerpo)
        nodo.atributos['tipo'] = TipoDatos.NINGUNO
    
    def _visitar_bifurcacion(self, nodo):
        for hijo in nodo.nodos:
            self.visitar(hijo)
        nodo.atributos['tipo'] = TipoDatos.NINGUNO

    def _visitar_si(self, nodo):
        condicion, bloque = nodo.nodos
        self.visitar(condicion)
        if condicion.atributos.get('tipo') != TipoDatos.BOOLEANO:
            raise Exception("La condición del 'si' debe ser booleana")
        self.visitar(bloque)
        nodo.atributos['tipo'] = TipoDatos.NINGUNO
    
    def _visitar_sinnoh(self, nodo):
        self.visitar(nodo.nodos[0])  # Solo tiene el bloque
        nodo.atributos['tipo'] = TipoDatos.NINGUNO

    def _visitar_asignacion(self, nodo):
        """
        Asignación ::= Identificador Tipo? = (Literal | Expresión | Invocación)
        """
        if len(nodo.nodos) == 3:
            ident, tipo, valor = nodo.nodos

            # Validar que el tipo declarado sea válido (tipo Pokémon o semántico conocido)
            if tipo.contenido in TIPOS_POKEMON_VALIDOS:
                tipo_semantico = TipoDatos.NÚMERO
            elif tipo.contenido in [e.name for e in TipoDatos]:
                tipo_semantico = TipoDatos[tipo.contenido]
            else:
                raise Exception(f"Tipo no reconocido: '{tipo.contenido}'")

            # Registrar el identificador en la tabla
            ident.atributos['tipo'] = tipo_semantico
            self.ts.nuevo_registro(ident)

        elif len(nodo.nodos) == 2:
            ident, valor = nodo.nodos

            # Si no se declara tipo, tratamos de inferirlo más adelante
            tipo_semantico = None

            # Buscar si ya estaba registrado antes (para evitar sobrescribir)
            existente = self.ts.buscar(ident.contenido)
            if existente is None:
                # Si no estaba registrado, lo marcamos como cualquiera
                ident.atributos['tipo'] = TipoDatos.CUALQUIERA
                self.ts.nuevo_registro(ident)
            else:
                tipo_semantico = existente['tipo_dato']
                ident.atributos['tipo'] = tipo_semantico

        else:
            raise Exception("Asignación mal formada")

        # Visitar la expresión o valor asignado
        self.visitar(valor)

        # Verificar compatibilidad entre el tipo del valor y el tipo declarado
        tipo_valor = valor.atributos.get('tipo', TipoDatos.CUALQUIERA)

        if tipo_semantico and tipo_valor != TipoDatos.CUALQUIERA and tipo_valor != tipo_semantico:
            raise Exception(f"Tipo incompatible: se esperaba '{tipo_semantico}' pero se obtuvo '{tipo_valor}' en la asignación a '{ident.contenido}'")

        # Anotar el tipo en el nodo de asignación también
        nodo.atributos['tipo'] = tipo_semantico or tipo_valor

    def _visitar_identificador(self, nodo):
        reg = self.ts.verificar_existencia(nodo.contenido)
        nodo.atributos['tipo'] = reg.get('tipo', TipoDatos.CUALQUIERA)

    def _visitar_equipo(self, nodo):
        """
        Equipo ::= equipo Identificador { ... }
        """
        ident = nodo.nodos[0]  
        self.ts.nuevo_registro(ident)

    def _visitar_expresion(self, nodo):
        for n in nodo.nodos:
            self.visitar(n)

        for n in nodo.nodos:
            if n.tipo.name == "OPERADOR":
                if n.contenido not in self.OPERADORES_VALIDOS:
                    raise Exception(f"Operador no reconocido: '{n.contenido}'")

        tipos = [n.atributos.get('tipo') for n in nodo.nodos if 'tipo' in n.atributos]
        tipos_sin_cualquiera = [t for t in tipos if t != TipoDatos.CUALQUIERA]

        if not tipos_sin_cualquiera:
            nodo.atributos['tipo'] = TipoDatos.CUALQUIERA
        elif all(t == tipos_sin_cualquiera[0] for t in tipos_sin_cualquiera):
            nodo.atributos['tipo'] = tipos_sin_cualquiera[0]
        else:
            raise Exception("Tipos incompatibles en expresión")

    def _visitar_funcion(self, nodo):
        """
        Función ::= batalla Identificador (Parámetros) BloqueInstrucciones
        """
        ident, parametros, bloque = nodo.nodos

        ident.atributos['tipo'] = TipoDatos.FUNCION
        self.ts.nuevo_registro(ident)

        self.ts.abrir_bloque()
        for param in parametros.nodos:
            
            param.atributos['tipo'] = TipoDatos.CUALQUIERA
            self.ts.nuevo_registro(param)

        self.visitar(bloque)

        self.ts.cerrar_bloque()

        nodo.atributos['tipo'] = bloque.atributos.get('tipo', TipoDatos.NINGUNO)

    def _visitar_invocacion(self, nodo):
        ident = nodo.nodos[0]
        args = nodo.nodos[1:]

        reg = self.ts.verificar_existencia(ident.contenido)
        
        if reg['tipo'] != TipoDatos.FUNCION:
            raise Exception(f"'{ident.contenido}' no es una función")
        
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

    def _visitar_pokemon(self, nodo):
        nombre = nodo.nodos[0]
        atributos = nodo.nodos[1:]
        self.visitar(nombre)
        for attr in atributos:
            self.visitar(attr)
        nodo.atributos['tipo'] = TipoDatos.CUALQUIERA

    def _visitar_string(self, nodo):
        nodo.atributos['tipo'] = TipoDatos.TEXTO

    def _visitar_entero(self, nodo):
        nodo.atributos['tipo'] = TipoDatos.NÚMERO
    
    def _visitar_flotante(self, nodo):
        nodo.atributos['tipo'] = TipoDatos.FLOTANTE
    
    def _visitar_booleanos(self, nodo):
        nodo.atributos['tipo'] = TipoDatos.BOOLEANO
    

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
