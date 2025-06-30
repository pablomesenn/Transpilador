import re
from enum import Enum, auto as autogen


class TipoComponente(Enum):
    COMENTARIO = autogen()
    PALABRA_CLAVE = autogen()
    FUNCION = autogen()
    CONDICIONAL = autogen()
    REPETICION = autogen()
    ASIGNACION = autogen()
    TIPO = autogen()
    OPERADOR = autogen()
    OPERADOR_LOGICO = autogen()
    COMPARADOR = autogen()
    ENTERO = autogen()
    FLOTANTE = autogen()
    STRING = autogen()
    BOOLEANO = autogen()
    PUNTUACION = autogen()
    BLANCOS = autogen()
    IDENTIFICADOR = autogen()
    NOMBRE_POKEMON = autogen()
    ERROR = autogen()


class ComponenteLexico:
    def __init__(self, tipo, texto, fila, col):
        self.tipo = tipo
        self.texto = texto
        self.linea = fila
        self.columna = col

    def __str__(self):
        return f"{self.tipo.name:<15} <{self.texto}> (línea {self.linea}, col {self.columna})"


class ExploradorPokeScript:

    # Descriptores de componentes (regex por prioridad)
    descriptores = [
        (TipoComponente.COMENTARIO, r'^pika:.*'),
        (TipoComponente.BOOLEANO, r'^(capturado|escapo)\b'),
        (TipoComponente.ERROR, r'^[0-9][a-zA-Z_][a-zA-Z0-9_]*'),
        (TipoComponente.ERROR, r'^[A-Za-z][a-zA-Z0-9_]*[@#$%&*]+[a-zA-Z0-9_]*'),
        (TipoComponente.TIPO, r'^(planta|agua|fuego|hielo)\b'),
        (TipoComponente.PALABRA_CLAVE, r'^(equipo|Batalla|turnos|usar|huir|ResetearStats|retirada|capturar|evolución|chachara|teElijo|teReto)\b'),
        (TipoComponente.PALABRA_CLAVE, r'^(vida_[a-zA-Z0-9_]+|energia_[a-zA-Z0-9_]+)\b'),
        (TipoComponente.FUNCION, r'^(batalla)\b'),
        (TipoComponente.CONDICIONAL, r'^(si|sinnoh)\b'),
        (TipoComponente.REPETICION, r'^(trampa|Arena)\b'),
        (TipoComponente.COMPARADOR, r'^(==|!=|<=|>=|<|>)'),
        (TipoComponente.ASIGNACION, r'^='),
        (TipoComponente.OPERADOR, r'^(ataque|poción|fortalecer|golpecritrico)\b'),
        (TipoComponente.STRING, r'^"[^"\n]*"'),
        (TipoComponente.STRING, r'^"[^"\n]*$'),
        (TipoComponente.FLOTANTE, r'^-?\d+\.\d+'),
        (TipoComponente.ENTERO, r'^-?\d+'),
        (TipoComponente.OPERADOR_LOGICO, r'^(and|or)\b'),
        (TipoComponente.IDENTIFICADOR, r'^[a-zA-Z_][a-zA-Z0-9_]*\b'),
        (TipoComponente.PUNTUACION, r'^[():,{}]'),
        (TipoComponente.BLANCOS, r'^\s+'),
        (TipoComponente.ERROR, r'^.'),
    ]

    def __init__(self, fuente: str):
        self.lineas = fuente.splitlines()
        self.componentes = []
        self.errores = []
        self.linea_actual = 0
        self.col_actual = 0

    def explorar(self):
        for i, contenido_linea in enumerate(self.lineas, start=1):
            self.linea_actual = i
            col = 1
            linea_restante = contenido_linea
            while linea_restante:
                detectado = False
                for tipo, patron in self.descriptores:
                    emparejamiento = re.match(patron, linea_restante)
                    if emparejamiento:
                        token = emparejamiento.group(0)

                        if tipo == TipoComponente.ERROR:
                            msg = self._crear_error(token)
                            self.errores.append(f"Error léxico en línea {i}, columna {col}: {msg}")
                            self.componentes.append(ComponenteLexico(tipo, token, i, col))

                        elif tipo == TipoComponente.STRING and not token.endswith('"'):
                            self.errores.append(f"Error léxico en línea {i}, columna {col}: String sin cerrar '{token}'")
                            self.componentes.append(ComponenteLexico(TipoComponente.ERROR, token, i, col))

                        elif tipo not in [TipoComponente.BLANCOS, TipoComponente.COMENTARIO]:
                            self.componentes.append(ComponenteLexico(tipo, token, i, col))

                        col += len(token)
                        linea_restante = linea_restante[len(token):]
                        detectado = True
                        break

                if not detectado:
                    simbolo = linea_restante[0]
                    self.errores.append(f"Error léxico en línea {i}, columna {col}: '{simbolo}' no es válido")
                    self.componentes.append(ComponenteLexico(TipoComponente.ERROR, simbolo, i, col))
                    col += 1
                    linea_restante = linea_restante[1:]

        return self.componentes

    def _crear_error(self, texto):
        if re.match(r'^[0-9][a-zA-Z]+', texto):
            return f"'{texto}' inicia con número: no válido como identificador"
        elif re.match(r'^[A-Za-z][a-zA-Z0-9_]*[@#$%&*]+[a-zA-Z0-9_]*', texto):
            return f"'{texto}' contiene caracteres inválidos"
        else:
            return f"'{texto}' no reconocido"

    def imprimir_componentes(self):
        print("== Componentes Léxicos ==")
        for c in self.componentes:
            print(c)

    def imprimir_errores(self):
        if self.errores:
            print("\n== Errores Encontrados ==")
            for e in self.errores:
                print(e)
            print(f"\nErrores totales: {len(self.errores)}")
        else:
            print("\nSin errores léxicos.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python scanner_pokescript.py <archivo.poke>")
        sys.exit(1)

    archivo = sys.argv[1]
    with open(archivo, encoding="utf-8") as f:
        datos = f.read()

    scanner = ExploradorPokeScript(datos)
    scanner.explorar()
    scanner.imprimir_componentes()
    scanner.imprimir_errores()
