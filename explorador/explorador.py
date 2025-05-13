import re
from enum import Enum, auto

class TipoComponente(Enum):
    
    COMENTARIO = auto()
    PALABRA_CLAVE = auto()
    FUNCION = auto()
    CONDICIONAL = auto()
    REPETICION = auto()
    ASIGNACION = auto()
    TIPO = auto()
    OPERADOR = auto()
    OPERADOR_LOGICO = auto()
    COMPARADOR = auto()
    ENTERO = auto()
    FLOTANTE = auto()
    STRING = auto()
    BOOLEANO = auto()
    PUNTUACION = auto()
    BLANCOS = auto()
    IDENTIFICADOR = auto()
    NOMBRE_POKEMON = auto()  # Tipo específico para nombres de Pokémon
    ERROR = auto()  # Para tokens no reconocidos

class ComponenteLexico:
    def __init__(self, tipo: TipoComponente, texto: str, linea: int, columna: int):
        self.tipo = tipo
        self.texto = texto
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f'{self.tipo.name:15} <{self.texto}> (línea {self.linea}, col {self.columna})'

class ExploradorPokeScript:
    descriptores_componentes = [
        (TipoComponente.COMENTARIO,    r'^pika:.*'),
        (TipoComponente.BOOLEANO,      r'^(capturado|escapo)\b'),

        # --- ERRORES léxicos específicos ---
        (TipoComponente.ERROR,         r'^[0-9][a-zA-Z_][a-zA-Z0-9_]*'),  # Identificador que empieza con número
        (TipoComponente.ERROR,         r'^[A-Za-z][a-zA-Z0-9_]*[@#$%&*]+[a-zA-Z0-9_]*'),  # Caracteres no permitidos
        (TipoComponente.ERROR,         r'^-?\d+\.\d+'),  # Punto decimal en vez de coma

        # Palabras clave y otros tokens específicos
        (TipoComponente.TIPO,          r'^(planta|agua|fuego|hielo)\b'),
        (TipoComponente.PALABRA_CLAVE, r'^(equipo|Batalla|turnos|usar|huir|ResetearStats|retirada|capturar|evolución|chachara|teElijo)\b'),
        (TipoComponente.PALABRA_CLAVE, r'^(vida_[a-zA-Z0-9_]+|energia_[a-zA-Z0-9_]+)\b'),
        (TipoComponente.FUNCION,       r'^(batalla)\b'),
        (TipoComponente.CONDICIONAL,   r'^(si|sinnoh)\b'),
        (TipoComponente.REPETICION,    r'^(trampa|Arena)\b'),
        (TipoComponente.ASIGNACION,    r'^='),
        (TipoComponente.OPERADOR,      r'^(ataque|poción|fortalecer|golpecritrico)\b'),
        (TipoComponente.COMPARADOR,    r'^(==|!=|<=|>=|<|>)'),
        (TipoComponente.STRING,        r'^"[^"\n]*"'),
        (TipoComponente.STRING,        r'^"[^"\n]*$'),
        (TipoComponente.FLOTANTE,      r'^-?\d+,\d+'),
        (TipoComponente.ENTERO,        r'^-?\d+'),
        (TipoComponente.OPERADOR_LOGICO, r'^(and|or)\b'),

        # Correcto identificador y nombres de Pokémon
        (TipoComponente.NOMBRE_POKEMON, r'^poke[a-zA-Z0-9_]+\b'),
        (TipoComponente.IDENTIFICADOR, r'^[a-zA-Z_][a-zA-Z0-9_]*\b'),
        
        (TipoComponente.PUNTUACION,    r'^[():,{}]'),
        (TipoComponente.BLANCOS,       r'^\s+'),

        # Captura cualquier carácter no reconocido
        (TipoComponente.ERROR,         r'^.'),
    ]

    def __init__(self, contenido: str):
        self.lineas = contenido.splitlines()
        self.componentes = []
        self.errores = []
        self.linea_actual = 0
        self.columna_actual = 0

    def explorar(self):
        for numero_linea, linea in enumerate(self.lineas, start=1):
            self.linea_actual = numero_linea
            columna = 1
            self.columna_actual = columna
            
            while linea:
                matched = False
                for tipo, regex in self.descriptores_componentes:
                    match = re.match(regex, linea)
                    if match:
                        texto = match.group(0)
                        
                        # Procesar el token según su tipo
                        if tipo == TipoComponente.ERROR:
                            mensaje_error = self.generar_mensaje_error(texto, tipo)
                            self.errores.append(
                                f"Error léxico en línea {numero_linea}, columna {columna}: {mensaje_error}"
                            )
                            # Aún así, agregamos el token de error para referencia
                            self.componentes.append(
                                ComponenteLexico(tipo, texto, numero_linea, columna)
                            )
                        elif tipo == TipoComponente.STRING and not texto.endswith('"'):
                            # String sin cerrar
                            self.errores.append(
                                f"Error léxico en línea {numero_linea}, columna {columna}: String sin cerrar '{texto}'"
                            )
                            self.componentes.append(
                                ComponenteLexico(TipoComponente.ERROR, texto, numero_linea, columna)
                            )
                        elif tipo != TipoComponente.BLANCOS and tipo != TipoComponente.COMENTARIO:
                            self.componentes.append(
                                ComponenteLexico(tipo, texto, numero_linea, columna)
                            )
                            
                        avance = len(texto)
                        linea = linea[avance:]
                        columna += avance
                        self.columna_actual = columna
                        matched = True
                        break
                
                if not matched:
                    # Este caso no debería ocurrir con la nueva expresión regular para ERROR
                    simbolo = linea[0]
                    self.errores.append(
                        f"Error léxico en línea {numero_linea}, columna {columna}: '{simbolo}' no es un símbolo válido"
                    )
                    self.componentes.append(
                        ComponenteLexico(TipoComponente.ERROR, simbolo, numero_linea, columna)
                    )
                    linea = linea[1:]
                    columna += 1
                    self.columna_actual = columna
                    
        return self.componentes

    def generar_mensaje_error(self, texto, tipo):
        """Genera mensajes de error específicos según el tipo de error encontrado"""
        if re.match(r'^[0-9][a-zA-Z]+', texto):
            return f"'{texto}' es un identificador inválido, no puede comenzar con un número"
        elif re.match(r'^[A-Za-z][a-zA-Z0-9_]*[@#$%&*]+[a-zA-Z0-9_]*', texto):
            return f"'{texto}' contiene caracteres no permitidos en identificadores"
        elif re.match(r'^-?\d+\.\d+', texto):
            return f"'{texto}' usa punto decimal en lugar de coma para flotantes"
        else:
            return f"'{texto}' no es un token válido"

    def imprimir_componentes(self):
        print("=== Componentes Léxicos ===")
        for comp in self.componentes:
            print(comp)

    def imprimir_errores(self):
        if self.errores:
            print("\n=== Errores Léxicos ===")
            for error in self.errores:
                print(error)
            print(f"\nTotal de errores léxicos: {len(self.errores)}")
        else:
            print("\nNo se encontraron errores léxicos.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python scanner_pokescript.py <archivo.poke>")
        sys.exit(1)

    ruta = sys.argv[1]
    with open(ruta, 'r', encoding='utf-8') as f:
        texto = f.read()

    explorador = ExploradorPokeScript(texto)
    explorador.explorar()
    explorador.imprimir_componentes()
    explorador.imprimir_errores()