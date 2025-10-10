# NOMBRE: IVÁN VALOR VERDU => GRUPO 40 I2ADE 
# DNI: 20525805F

#########################################################################  
# REPRESENTA EL ALGORITMO DE BACKTRACKING +
#########################################################################

# Variables globales para estadísticas
variables_exploradas = 0  # Cuenta cuántas veces se llama recursivamente al algoritmo
valores_probados = 0      # Cuenta cuántos valores del dominio se prueban en total

# Reinicia las estadísticas antes de cada ejecución
# Resetea los contadores globales a 0.
# Se debe llamar desde main.py ANTES de ejecutar el algoritmo.
def reset_stats_bk():
   
    global variables_exploradas, valores_probados
    variables_exploradas = 0
    valores_probados = 0

# Devuelve los contadores actuales
def get_stats_bk():
   
    return variables_exploradas, valores_probados


#########################################################################
# VALIDACIÓN DE RESTRICCIONES DEL SUDOKU
#########################################################################
# Comprueba si asignar un valor a una variable ('valor' a 'var') es válido según las reglas del Sudoku.
# Devuelve True si la asignación es válida, False si viola alguna restricción.
# Args:
#   variables: Lista de todas las variables del Sudoku
#   var: Variable a la que queremos asignar el valor
#   valor: Valor que queremos asignar (1-9)
# Returns:
#   True si la asignación es válida, False si viola alguna restricción  

def es_valido(variables, var, valor):
  
    fila, col = var.fila, var.col

    # Comprobar si esta en la misma fila
    for v in variables:
        if v.fila == fila and v.valor == valor:
            return False
    
    # Comprobar si esta en la columna
    for v in variables:
        if v.col == col and v.valor == valor:
            return False
    
    # Comprobar si esta en la misma subcuadrícula 3x3
    inicio_f = (fila // 3) * 3  # Fila de inicio del bloque (0, 3 o 6)
    inicio_c = (col // 3) * 3   # Columna de inicio del bloque (0, 3 o 6)
    
    for v in variables:
        # Comprobar si v está en el mismo bloque 3x3 y tiene el mismo valor
        if (inicio_f <= v.fila < inicio_f+3 and 
            inicio_c <= v.col < inicio_c+3 and 
            v.valor == valor):
            return False
    
    return True  # Si pasa todas las comprobaciones, la asignación es válida


#########################################################################
# HEURÍSTICA MRV (Minimum Remaining Values)
#########################################################################
# Selecciona la variable NO instanciada con MENOR dominio (menos valores posibles).
# Esto hace que que se reduzca el espacio de búsqueda porque si tiene menos dominio, es
# mejor probarla antes, porque es más probable que falle pronto.

def seleccionar_variable_mrv(variables):

    mejor_var = None
    min_dominio = 10  # Mayor que el máximo posible (9)
    
    for var in variables:
        # Solo considerar variables SIN valor asignado (celdas vacías)
        if not var.esta_instanciada():
            tam_dominio = len(var.dominio)
            
            # DETECCIÓN TEMPRANA DE FALLO: Dominio vacío = imposible continuar
            if tam_dominio == 0:
                return None
            
            # OPTIMIZACIÓN: Si encontramos dominio de 1, es la mejor opción posible
            # (solo tiene una opción, así que la asignamos directamente)
            if tam_dominio == 1:
                return var
            
            # Actualizar la mejor variable si tiene menos opciones
            if tam_dominio < min_dominio:
                min_dominio = tam_dominio
                mejor_var = var
    
    return mejor_var  # Retorna la variable con menor dominio


#########################################################################
# ALGORITMO BACKTRACKING RECURSIVO CON MRV
#########################################################################

#Algoritmo de Backtracking con heurística MRV para resolver Sudokus.
    
#    FUNCIONAMIENTO:
#    1. Selecciona la variable con menor dominio (MRV)
#    2. Prueba cada valor de su dominio
#    3. Si un valor es válido:
#       - Lo asigna
#       - Llama recursivamente para resolver el resto
#       - Si falla, BACKTRACK: deshace la asignación
#    4. Si ningún valor funciona → Retorna False (backtrack al nivel anterior)
    
#    CASO BASE:
#    - Si no hay más variables sin instanciar → Solución encontrada (True)
#    - Si hay una variable sin opciones válidas → Fallo (False)
    
#    Args:
#        variables: Lista de todas las variables del Sudoku
    
#    Returns:
#        True si encuentra solución, False si no hay solución posible
#    """
def resolver_backtracking(variables):
   
    global variables_exploradas, valores_probados

    # PASO 1: Seleccionar la mejor variable, es decir, que tenga menor domino
    var = seleccionar_variable_mrv(variables)
    
    # CASO BASE: Verificar si hemos terminado
    if var is None:
        # Si todas las variables están instanciadas, he terminado
        # Si hay alguna sin instanciar con dominio vacío, algo falla
        return all(v.esta_instanciada() for v in variables)
    
    # Incrementar contador de variables exploradas
    variables_exploradas += 1

    # PASO 2: Probar cada valor del dominio de la variable seleccionada
    for valor in var.dominio:
        # Incrementar contador de valores probados 
        valores_probados += 1

        # Comprobar si el valor es válido 
        if es_valido(variables, var, valor):
            # ASIGNAR: Probar con este valor
            var.asignar(valor)

            # RECURSIÓN: Intentar resolver el resto del Sudoku
            if resolver_backtracking(variables):
                return True  # Solucion encontrada, paso la solución hacia arriba

            # BACKTRACKING: Si la recursión falló, deshacer la asignación
            var.desasignar()

    # Si ninguno va, no hay solución 
    return False