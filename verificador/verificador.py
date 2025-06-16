# Verificador para PokeScript

from utils.arbol import ArbolSintaxisAbstracta, NodoArbol, TipoNodo
from utils.tipo_datos import TipoDatos

TIPOS_POKEMON_VALIDOS = {"agua", "fuego", "planta","hielo"}

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
        tipo_extra = nodo.atributos.get('tipo') if hasattr(nodo, 'atributos') else None
        entrada = {
            'nombre': nodo.contenido,
            'profundidad': self.profundidad,
            'referencia': nodo,
            'tipo': tipo_extra
        }
        if 'parametros' in nodo.atributos:
            entrada['parametros'] = nodo.atributos['parametros']
        self.simbolos.append(entrada)

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
        else:
            for hijo in nodo.nodos:
                self.visitar(hijo)
        print(f"[VISITANDO] Nodo tipo: {nodo.tipo}, contenido: {getattr(nodo, 'contenido', '')}")


    def _visitar_asignacion(self, nodo):
        if len(nodo.nodos) == 3:
            ident, tipo, valor = nodo.nodos

            # Visitar primero el valor
            self.visitar(valor)
            tipo_valor = valor.atributos.get('tipo', TipoDatos.CUALQUIERA)

            # Determinar tipo semántico
            if tipo.contenido in TIPOS_POKEMON_VALIDOS:
                tipo_semantico = TipoDatos.NÚMERO if tipo_valor != TipoDatos.TEXTO else TipoDatos.TEXTO
            elif tipo.contenido in [e.name for e in TipoDatos]:
                tipo_semantico = TipoDatos[tipo.contenido]
            else:
                raise Exception(f"Tipo no reconocido: '{tipo.contenido}'")

            ident.atributos['tipo'] = tipo_semantico
            self.ts.nuevo_registro(ident)

            if tipo_valor != TipoDatos.CUALQUIERA and tipo_valor != tipo_semantico:
                raise Exception(f"Tipo incompatible: se esperaba '{tipo_semantico.name}' pero se obtuvo '{tipo_valor.name}' en la asignación a '{ident.contenido}'")

            nodo.atributos['tipo'] = tipo_semantico

        elif len(nodo.nodos) == 2:
            ident, valor = nodo.nodos

            self.visitar(valor)
            tipo_valor = valor.atributos.get('tipo', TipoDatos.CUALQUIERA)

            # Registrar si no existe
            try:
                reg = self.ts.verificar_existencia(ident.contenido)
                tipo_semantico = reg.get('tipo', TipoDatos.CUALQUIERA)
            except Exception:
                tipo_semantico = tipo_valor
                ident.atributos['tipo'] = tipo_semantico
                self.ts.nuevo_registro(ident)

            if tipo_valor != TipoDatos.CUALQUIERA and tipo_valor != tipo_semantico:
                raise Exception(f"Tipo incompatible: se esperaba '{tipo_semantico.name}' pero se obtuvo '{tipo_valor.name}' en la asignación a '{ident.contenido}'")

            nodo.atributos['tipo'] = tipo_semantico

        else:
            raise Exception("Asignación mal formada")
    

    def _visitar_identificador(self, nodo):
        reg = self.ts.verificar_existencia(nodo.contenido)
        nodo.atributos['tipo'] = reg.get('tipo_dato', TipoDatos.CUALQUIERA)

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

    def _visitar_expresion(self, nodo):
        for n in nodo.nodos:
            self.visitar(n)
        tipos = [n.atributos.get('tipo') for n in nodo.nodos if 'tipo' in n.atributos]
        tipos_sin_cualquiera = [t for t in tipos if t != TipoDatos.CUALQUIERA]

        if not tipos_sin_cualquiera:
            nodo.atributos['tipo'] = TipoDatos.CUALQUIERA
        elif all(t == tipos_sin_cualquiera[0] for t in tipos_sin_cualquiera):
            nodo.atributos['tipo'] = tipos_sin_cualquiera[0]
        else:
            raise Exception("Tipos incompatibles en expresión")

        # Validación adicional para operadores no compatibles con texto o booleanos
        for t in tipos_sin_cualquiera:
            if t in (TipoDatos.TEXTO, TipoDatos.BOOLEANO):
                raise Exception("Operaciones no permitidas con tipo TEXTO o BOOLEANO")



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

    def _visitar_invocacion(self, nodo):
        ident        = nodo.nodos[0]

        # --- NUEVO ---
        if len(nodo.nodos) > 1 and nodo.nodos[1].tipo == TipoNodo.PARAMETROS:
            params_node = nodo.nodos[1]
            args_nodes  = params_node.nodos            # ← los argumentos reales
        else:                                          # (por si la gramática cambiara)
            args_nodes  = nodo.nodos[1:]
        # --------------

        # registro de la función
        reg = self.ts.verificar_existencia(ident.contenido)
        if reg['tipo'] != TipoDatos.FUNCION:
            raise Exception(f"'{ident.contenido}' no es una función")

        param_esperados = reg.get('parametros', [])
        if len(args_nodes) != len(param_esperados):
            raise Exception(
                f"'{ident.contenido}' esperaba {len(param_esperados)} argumento(s), "
                f"pero se dieron {len(args_nodes)}"
            )

        # verificar cada argumento
        for arg in args_nodes:
            self.visitar(arg)
        
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