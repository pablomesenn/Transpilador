# Verificador para PokeScript

from utils.arbol import ArbolSintaxisAbstracta, NodoArbol, TipoNodo
from utils.tipo_datos import TipoDatos

TIPOS_POKEMON_VALIDOS = {"agua", "fuego", "planta","hielo"}

MAPEO_TIPO = {
    "fuego"  : TipoDatos.NÚMERO,     # enteros
    "agua"   : TipoDatos.TEXTO,      # strings
    "planta" : TipoDatos.FLOTANTE,   # números con punto
    "hielo"  : TipoDatos.BOOLEANO,   # capturado / escapo
}

OPERADORES_NUMERICOS = {"ataque", "poción"}

class TablaSimbolos:
    """
    Estructura de soporte para el análisis semántico.
    Mantiene la pila de entornos y permite registrar / consultar símbolos.
    Imprime “instantáneas” cada vez que cambia.
    """

    def __init__(self):
        self.profundidad: int = 0          # nivel del bloque actual
        self.simbolos:   list = []         # todos los registros (cada uno es un dict)

    # ------------------------------------------------------------------ utilidades internas
    def _dump(self, encabezado: str) -> None:
        """Imprime la tabla completa (o un mensaje) después de cada operación."""
        print(f'\n{encabezado}')
        print(f'   PROF  NOMBRE            TIPO')
        print(f'   ----  ----------------  ----------------')

        for reg in self.simbolos:
            tipo = reg["tipo"].name if reg["tipo"] else "?"
            print(f'   {reg["profundidad"]:<4}  {reg["nombre"]:<16}  {tipo}')

    # ------------------------------------------------------------------ manejo de bloques
    def abrir_bloque(self) -> None:
        self.profundidad += 1
        self._dump(f'=== Abro bloque  (profundidad {self.profundidad})')

    def cerrar_bloque(self) -> None:
        # elimina símbolos de la profundidad actual
        self.simbolos = [s for s in self.simbolos if s["profundidad"] != self.profundidad]
        self._dump(f'=== Cierro bloque (profundidad {self.profundidad})')
        self.profundidad -= 1

    # ------------------------------------------------------------------ registro y consultas
    def nuevo_registro(self, nodo) -> None:
        tipo_extra = nodo.atributos.get('tipo') if hasattr(nodo, 'atributos') else None

        entrada = {
            'nombre'     : nodo.contenido,
            'profundidad': self.profundidad,
            'referencia' : nodo,
            'tipo'       : tipo_extra,
            'decl_linea'  : getattr(nodo, 'linea', None),
            'decl_col'    : getattr(nodo, 'columna', None)
        }
        if 'parametros' in nodo.atributos:
            entrada['parametros'] = nodo.atributos['parametros']

        # Verificar redeclaración en el mismo nivel
        for reg in self.simbolos:
            if reg['nombre'] == entrada['nombre'] and reg['profundidad'] == self.profundidad:
                raise Exception(f"Redeclaración de '{entrada['nombre']}' en el mismo bloque")

        self.simbolos.append(entrada)
        self._dump(f'+++ Nuevo símbolo -> {entrada["nombre"]}:{tipo_extra.name if tipo_extra else "?"}')

    def verificar_existencia(self, nombre: str) -> dict:
        for reg in reversed(self.simbolos):
            if reg['nombre'] == nombre:
                return reg
        raise Exception(f"Error semántico: '{nombre}' no ha sido declarado")

    def verificar_tipo_valido(self, lexema_tipo: str, conjunto_validos) -> None:
        if lexema_tipo not in conjunto_validos:
            raise Exception(f"Tipo de Pokémon inválido: '{lexema_tipo}'")


class VisitantePokeScript:
    def __init__(self, tabla_simbolos):
        self.ts = tabla_simbolos

    def visitar(self, nodo: NodoArbol):
        metodo = getattr(self, f"_visitar_{nodo.tipo.name.lower()}", None)
        if metodo:
            metodo(nodo)
        else:
            for hijo in nodo.nodos:
                self.visitar(hijo)
        

    def _visitar_asignacion(self, nodo: NodoArbol) -> None:
        """
        Maneja:
            Identificador PalabraTipo = (Literal | Expresión | Invocación)
            ó
            Identificador = (Literal | Expresión | Invocación)
        Valida que el valor coincida con la semántica fijada por la 'PalabraTipo'.
        """

        
        if len(nodo.nodos) == 3:
            ident_node, tipo_token, valor_node = nodo.nodos

            
            if tipo_token.contenido not in MAPEO_TIPO:
                raise Exception(f"Tipo desconocido: '{tipo_token.contenido}'")

            tipo_semantico = MAPEO_TIPO[tipo_token.contenido]        

            self.visitar(valor_node)
            tipo_valor = valor_node.atributos.get("tipo", TipoDatos.CUALQUIERA)

            if tipo_valor not in (TipoDatos.CUALQUIERA, tipo_semantico):
                raise Exception(
                    f"Tipo incompatible: '{ident_node.contenido}' es '{tipo_token.contenido}' "
                    f"({tipo_semantico.name}) pero se le asigna {tipo_valor.name}"
                )

            ident_node.atributos["tipo"] = tipo_semantico
            self.ts.nuevo_registro(ident_node)
            nodo.atributos["tipo"] = tipo_semantico
            return

        
        if len(nodo.nodos) == 2:
            ident_node, valor_node = nodo.nodos

            
            self.visitar(valor_node)
            tipo_valor = valor_node.atributos.get("tipo", TipoDatos.CUALQUIERA)

            
            try:
                reg = self.ts.verificar_existencia(ident_node.contenido)
                tipo_semantico = reg.get("tipo", TipoDatos.CUALQUIERA)
            except Exception:
            
                tipo_semantico = tipo_valor
                ident_node.atributos["tipo"] = tipo_semantico
                self.ts.nuevo_registro(ident_node)

            if tipo_valor not in (TipoDatos.CUALQUIERA, tipo_semantico):
                raise Exception(
                    f"Tipo incompatible: '{ident_node.contenido}' era {tipo_semantico.name} "
                    f"y se le intenta asignar {tipo_valor.name}"
                )

            nodo.atributos["tipo"] = tipo_semantico
            return

        raise Exception("Asignación mal formada")
    

    def _visitar_identificador(self, nodo):
        reg = self.ts.verificar_existencia(nodo.contenido)
        nodo.atributos['tipo'] = reg.get('tipo', TipoDatos.CUALQUIERA)
        nodo.atributos["def_pos"] = (reg["decl_linea"], reg["decl_col"])

    def _visitar_equipo(self, nodo):
        """
        Equipo ::= equipo Identificador { Pokemon{1,6} }
        Cada Pokémon viene como nodo TipoNodo.POKEMON
                ├─ IDENTIFICADOR (nombre)
                ├─ ENTERO        (vida)
                └─ FLOTANTE      (peso)
        """
        # registrar el nombre del equipo
        ident_equipo = nodo.nodos[0]
        self.ts.nuevo_registro(ident_equipo)

        # recorrer los miembros
        for miembro in nodo.nodos[1:]:
            if miembro.tipo != TipoNodo.POKEMON:
                raise Exception("Se esperaba un nodo POKEMON dentro del equipo")

            if len(miembro.nodos) != 3:
                raise Exception(
                    f"Miembro del equipo mal formado: se esperaban 3 nodos "
                    f"(nombre, vida, peso) pero se obtuvieron {len(miembro.nodos)}"
                )

            # nombre, vida, peso
            nombre_poke = miembro.nodos[0]          # IDENTIFICADOR
            vida_poke   = miembro.nodos[1]          # ENTERO
            peso_poke   = miembro.nodos[2]          # FLOTANTE

            # visitar sus literales para anotar tipos
            self.visitar(vida_poke)
            self.visitar(peso_poke)

            # opcional: guardar la ficha del Pokémon en la tabla si te interesa
            nombre_poke.atributos['tipo'] = TipoDatos.CUALQUIERA
            self.ts.nuevo_registro(nombre_poke)

        # nada que devolver: el nodo EQUIPO no produce valor
        nodo.atributos['tipo'] = TipoDatos.NINGUNO

    def _visitar_expresion(self, nodo: NodoArbol) -> None:
        """
        Expresión ::= término ( OPERADOR término )*
        Solo se admiten operadores numéricos ('ataque', 'poción').
        El tipo resultante se propaga; si aparece CUALQUIERA, el
        resultado se mantiene como CUALQUIERA hasta que se resuelva.
        """
        # -- evaluar primer término
        self.visitar(nodo.nodos[0])
        current_type = nodo.nodos[0].atributos.get("tipo", TipoDatos.CUALQUIERA)

        i = 1
        while i < len(nodo.nodos):
            op_node   = nodo.nodos[i]
            term_node = nodo.nodos[i + 1]

            self.visitar(term_node)
            right_type = term_node.atributos.get("tipo", TipoDatos.CUALQUIERA)
            op         = op_node.contenido

            # ── solo 'ataque' y 'poción' son válidos
            if op not in ("ataque", "poción"):
                raise Exception(f"Operador no reconocido: '{op}'")

            # ── ambos lados deben ser numéricos o CUALQUIERA
            permitidos = (TipoDatos.NÚMERO, TipoDatos.FLOTANTE, TipoDatos.CUALQUIERA)
            if current_type not in permitidos or right_type not in permitidos:
                raise Exception(
                    f"Operador '{op}' solo admite números "
                    f"(izq={current_type.name}, der={right_type.name})"
                )

            # ── determinar tipo resultante
            if TipoDatos.CUALQUIERA in (current_type, right_type):
                current_type = TipoDatos.CUALQUIERA
            elif TipoDatos.FLOTANTE in (current_type, right_type):
                current_type = TipoDatos.FLOTANTE
            else:
                current_type = TipoDatos.NÚMERO

            i += 2  # avanzar al siguiente operador

        nodo.atributos["tipo"] = current_type

    def _visitar_funcion(self, nodo):
        ident, parametros, bloque = nodo.nodos

        ident.atributos['tipo'] = TipoDatos.FUNCION
        
        ident.atributos['parametros'] = [p.contenido for p in parametros.nodos]
        self.ts.nuevo_registro(ident)

        self.ts.abrir_bloque()
        for param in parametros.nodos:
            param.atributos['tipo'] = TipoDatos.CUALQUIERA
            self.ts.nuevo_registro(param)

        self.visitar(bloque)
        self.ts.cerrar_bloque()

        nodo.atributos['tipo'] = bloque.atributos.get('tipo', TipoDatos.NINGUNO)

    def _visitar_invocacion(self, nodo: NodoArbol) -> None:
        """
        Invocación ::= teElijo IDENTIFICADOR (arg1, arg2, ...)
        Estructura del ASA:
            nodo.nodos[0] -> IDENTIFICADOR  (nombre función)
            nodo.nodos[1] -> PARAMETROS     (hijos = argumentos)
        """
        ident_node = nodo.nodos[0]

        # --- recuperar la ficha de la función ---
        ficha = self.ts.verificar_existencia(ident_node.contenido)
        if ficha["tipo"] != TipoDatos.FUNCION:
            raise Exception(f"'{ident_node.contenido}' no es una función")

        params_esperados = ficha.get("parametros", [])

        # --- recoger argumentos reales ---
        if len(nodo.nodos) >= 2 and nodo.nodos[1].tipo == TipoNodo.PARAMETROS:
            args_nodes = nodo.nodos[1].nodos
        else:
            args_nodes = []          # invocación sin paréntesis/args

        # --- comprobar cantidad ---
        if len(args_nodes) != len(params_esperados):
            raise Exception(
                f"'{ident_node.contenido}' esperaba {len(params_esperados)} argumento(s), "
                f"recibió {len(args_nodes)}"
            )

        # --- verificar cada argumento ---
        for arg in args_nodes:
            self.visitar(arg)        # esto anota su 'tipo'

        # (si necesitaras devolver tipo de retorno, anótalo aquí)
        nodo.atributos["tipo"] = ficha.get("retorno", TipoDatos.CUALQUIERA)
        
    def _visitar_string(self, nodo):
        nodo.atributos['tipo'] = TipoDatos.TEXTO

    def _visitar_entero(self, nodo):
        nodo.atributos['tipo'] = TipoDatos.NÚMERO

    def _visitar_flotante(self, nodo):
        nodo.atributos['tipo'] = TipoDatos.FLOTANTE

    def _visitar_booleano(self, nodo):
        nodo.atributos['tipo'] = TipoDatos.BOOLEANO

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