# NOMBRE: IVÁN VALOR VERDU => GRUPO 40 I2ADE 
# DNI: 20525805F

#########################################################################
# REPRESENTA EL ALGORITMO DE FORWARD CHECKING CON HEURÍSTICAS MRV + LCV
# 
# Forward Checking (FC): Técnica de poda que, tras asignar un valor a una variable,
# ELIMINA ese valor del dominio de los vecinos (variables relacionadas).
# Esto detecta fallos ANTES que el Backtracking simple.
#
# Heurísticas usadas:
# - MRV (Minimum Remaining Values): Selecciona variables con menor dominio
# - LCV (Least Constraining Value): Ordena valores para probar primero los que menos restringen
#########################################################################

# Variables globales para estadísticas
variables_exploradas = 0  # Cuenta cuántas veces se llama recursivamente al algoritmo
valores_probados = 0      # Cuenta cuántos valores del dominio se prueban en total

#Reinicia los contadores antes de cada ejecución
def reset_stats_fc():
    global variables_exploradas, valores_probados
    variables_exploradas = 0
    valores_probados = 0
# Devuelve los contadores actuales
def get_stats_fc():
    return variables_exploradas, valores_probados


#########################################################################
# VALIDACIÓN DE RESTRICCIONES DEL SUDOKU
#########################################################################
#Comprueba las restricciónes como en BT
def es_valido_fc(variables, var, val):
    
    fila, col = var.fila, var.col
    inicio_f = (fila // 3) * 3  # Calcular inicio de la subcuadrícula (fila)
    inicio_c = (col // 3) * 3   # Calcular inicio de la subcuadrícula (columna)
    
    for v in variables:
        # Ignorar la variable actual y las no instanciadas
        if v is var or not v.esta_instanciada():
            continue
        
        # Si otra variable ya tiene este valor
        if v.valor == val:
            # Comprobar FILA
            if v.fila == fila:
                return False
            # Comprobar COLUMNA
            if v.col == col:
                return False
            # Comprobar SUBCUADRÍCULA 3x3
            if (inicio_f <= v.fila < inicio_f + 3 and 
                inicio_c <= v.col < inicio_c + 3):
                return False
                
    return True  # Si pasa todas las comprobaciones, es válido


#########################################################################
# INICIALIZACIÓN DE DOMINIOS CON LAS PISTAS FIJAS
#########################################################################
# Recorta los dominios iniciales según las celdas fijas del Sudoku que cargamos
# Esta poda inicial acelera el algoritmo porque reduce el espacio de búsqueda ANTES de empezar
def inicializar_dominios_fc(variables):
    # Separar variables en PISTAS (con valor) y VACÍAS (sin valor)
    pistas = [v for v in variables if v.esta_instanciada()]
    vacias = [v for v in variables if not v.esta_instanciada()]
    
    # Para cada pista fija del Sudoku
    for pista in pistas:
        val = pista.valor
        fila_actual, col_actual = pista.fila, pista.col
        box_f, box_c = (fila_actual // 3) * 3, (col_actual // 3) * 3  # Inicio del bloque 3x3
        
        # Eliminar este valor del dominio de todas las celdas vecinas
        for var_vacia in vacias:
            # Comprobar si var_vacia es vecina (misma fila, columna o bloque)
            es_vecina = (var_vacia.fila == fila_actual or 
                         var_vacia.col == col_actual or 
                         ((box_f <= var_vacia.fila < box_f + 3) and 
                          (box_c <= var_vacia.col < box_c + 3)))

            # Si es vecina y tiene este valor en su dominio, ELIMINARLO
            if es_vecina and val in var_vacia.dominio:
                var_vacia.quitar_valor(val, pista)  # Usa el método de la clase Variable
                
                # Si el dominio queda vacío, no hay solución posible
                if not var_vacia.dominio:
                    return False 
    
    return True  # Inicialización exitosa


#########################################################################
# OBTENER VECINOS DE UNA VARIABLE
#########################################################################
#Retornar todas las variables NO instanciadas que son VECINAS de 'var',
#es decir, que comparten fila, columna o subcuadrícula 3x3.
def obtener_vecinos_fc(variables, var):
   
    vecinos = []
    fila, col = var.fila, var.col
    box_f, box_c = (fila // 3) * 3, (col // 3) * 3  # Inicio de la subcuadrícula
    
    for v in variables:
        # Ignorar la variable actual y las que ya tienen valor
        if v is var or v.esta_instanciada():
            continue
        
        # Comprobar si comparten fila, columna o subcuadrícula
        if (v.fila == fila or 
            v.col == col or 
            ((box_f <= v.fila < box_f + 3) and 
             (box_c <= v.col < box_c + 3))):
            vecinos.append(v)
    
    return vecinos


#########################################################################
# HEURÍSTICA LCV (Least Constraining Value)
#########################################################################
#Cuenta cuántos vecinos de 'var' tienen 'valor' en su dominio
#Se usa para la heurística LCV: queremos probar primero los valores que
#MENOS opciones eliminan de los vecinos (menos restrictivos).
#EJEMPLO
#Si quitas opciones a 3 vecinos → 3 celdas tienen MENOS posibilidades de resolverse
#Si quitas opciones a 1 vecino → Solo 1 celda tiene menos posibilidades
#Menos restricciones = Menos backtracking = Más rápido
def contar_conflictos_lcv(variables, var, valor):

    vecinos = obtener_vecinos_fc(variables, var)
    conflictos = 0
    
    for vecino in vecinos:
        # Si el vecino tiene este valor como opción, cuenta como conflicto
        if valor in vecino.dominio:
            conflictos += 1
    
    return conflictos

#Ordena los valores del dominio de 'var' según la heurística LCV
#Probar primero los valores que MENOS vecinos afectan porque
#esto reduce el backtracking porque deja más opciones abiertas para otras variables
#EJEMPLO
#Valor 5 afecta a 2 vecinos
#Valor 7 afecta a 6 vecinos
#→ Orden LCV: [5, 7] (probar 5 primero)
def ordenar_valores_lcv(variables, var):
    valores_conflictos = []
    
    # Para cada valor del dominio, contar cuántos vecinos afecta
    for valor in var.dominio:
        conflictos = contar_conflictos_lcv(variables, var, valor)
        valores_conflictos.append((valor, conflictos))
    
    # Ordenar por conflictos ascendente (menos conflictos primero)
    valores_conflictos.sort(key=lambda x: x[1])
    
    # Retornar solo los valores (sin los conflictos)
    return [valor for valor, _ in valores_conflictos]


#########################################################################
# RESTAURACIÓN SELECTIVA DE DOMINIOS
#########################################################################
 #Restaura el dominio de la variable al estado anterior que tenía antes
#  de hacer la poda, para eso usa la información de la lista de tuplas que se llama PODA.
# Cuando hacemos backtrack, debemos restaurar los dominios de las variables
# que fueron podados por var_causante.
#Cada variable tiene una lista 'poda' que guarda:
#- Qué valores fueron eliminados
#- Qué variable causó la eliminación (coordenadas)
#Esta función restaura SOLO los valores podados por 'var_causante',
#manteniendo los podados por otras variables.
#Esto es importante para que FC funcione correctamente: no queremos restaurar
#valores que fueron podados por otras asignaciones que siguen activas.
def restaurar_selectivo(var_vecino, var_causante):

    coord_causante = (var_causante.fila, var_causante.col)
    valores_a_restaurar = []
    poda_restante = []
    
    # Separar la poda: qué fue por var_causante y qué fue por otras variables
    for val, coord in var_vecino.poda:
        if coord == coord_causante:
            # Este valor fue podado por var_causante → RESTAURAR
            valores_a_restaurar.append(val)
        else:
            # Fue podado por otra variable → MANTENER
            poda_restante.append((val, coord))
    
    # Añadir de vuelta al dominio los valores restaurados
    for val in valores_a_restaurar:
        if val not in var_vecino.dominio:
            var_vecino.dominio.append(val)
    
    # Actualizar la lista de poda (quitar los de var_causante)
    var_vecino.poda = poda_restante
    var_vecino.dominio.sort()  # Mantener el dominio ordenado


#########################################################################
# PROPAGACIÓN DE RESTRICCIONES (FORWARD CHECKING)
#########################################################################
#Tras asignar 'val' a 'var_actual', eliminar 'val' del dominio de todos los vecinos
#Si algún dominio queda vacío → FALLO (detectado tempranamente)
#Esto es el CORAZÓN del Forward Checking
#1. Obtener vecinos de var_actual
#2. Eliminar 'val' del dominio de cada vecino
#3. Si algún dominio queda VACÍO → FALLO (detectado tempranamente)
#4. Guardar qué variables fueron afectadas (para restaurar después)
#Devuelve True si la propagación fue exitosa, False si algún dominio quedó vacío
#También devuelve la lista de variables cuyo dominio fue modificado (para backtrack)
def propagar_fc(var_actual, val, variables):
    vecinos = obtener_vecinos_fc(variables, var_actual)
    variables_afectadas = []
    
    for v in vecinos:
        # Si el vecino tiene 'val' en su dominio, ELIMINARLO
        if val in v.dominio:
            v.quitar_valor(val, var_actual)  # Usa el método de la clase Variable
            variables_afectadas.append(v)
            
            # DETECCIÓN TEMPRANA DE FALLO: Si el dominio queda vacío, no hay solución
            if not v.dominio:
                # Restaurar inmediatamente lo que acabamos de podar
                for var_rest in variables_afectadas:
                    restaurar_selectivo(var_rest, var_actual)
                return False, []  # Fallo: retornar lista vacía
    
    return True, variables_afectadas  # Éxito: retornar variables afectadas para backtrack


#########################################################################
# HEURÍSTICA MRV 
#########################################################################
#Como en BT, selecciona la variable NO instanciada con MENOR dominio (MRV)
#  Esto reduce el árbol de búsqueda porque variables con pocas opciones es 
# mejor explorarlas antes (fallan pronto)
def seleccionar_variable_mrv(variables): 

    mejor_var = None
    min_dominio = 10  # Mayor que el máximo posible, y si después es menor actualizo...
    
    for v in variables:
        if not v.esta_instanciada():
            tam = len(v.dominio)
            
            # DETECCIÓN DE FALLO: Dominio vacío
            if tam == 0:
                return None
            
            # OPTIMIZACIÓN: Dominio de 1 es la mejor opción posible
            if tam == 1:
                return v
            
            # Actualizar mejor variable
            if tam < min_dominio:
                min_dominio = tam
                mejor_var = v
    
    return mejor_var


#########################################################################
# ALGORITMO FC RECURSIVO CON MRV + LCV
#########################################################################
# Implementa el algoritmo de Forward Checking con las heurísticas MRV y LCV
# 1.Selecciona variables con menor dominio (MRV)
# 2.Ordena valores para probar primero los que menos restringen a los vecinos (LCV)
# 3.Para cada valor:
    # a. Lo asigna
    # b. Propaga (Forward Checking): elimina el valor de dominios vecinos
    # c. Si la propagación falla → Backtrack
    # d. Si tiene éxito → Llama recursivamente
    # e. Si la recursión falla → Restaura dominios y backtrack
# CASO BASE:
# - Si no hay más variables sin instanciar → Solución encontrada (True)
# - Si hay una variable sin opciones → Fallo (False)

def _resolver_fc_recursivo(variables):
    
    global variables_exploradas, valores_probados

    # PASO 1: Seleccionar variable con MRV
    var_actual = seleccionar_variable_mrv(variables)
    
    # CASO BASE: Verificar si hemos terminado
    if var_actual is None:
        # Si todas están instanciadas, hemos terminado, si no, hay fallo
        return all(v.esta_instanciada() for v in variables)

    # Incrementar contador de variables exploradas
    variables_exploradas += 1
    
    # PASO 2: Ordenar valores con LCV (menos restrictivos primero)
    valores_ordenados = ordenar_valores_lcv(variables, var_actual)
    
    # PASO 3: Probar cada valor en el orden LCV
    for val in valores_ordenados:
        # Incrementar contador de valores probados
        valores_probados += 1
        
        # Comprobar si el valor es válido
        if es_valido_fc(variables, var_actual, val):
            # ASIGNAR el valor
            var_actual.asignar(val)
            
            # PROPAGACIÓN (FORWARD CHECKING): Podar dominios de vecinos
            exitoso, vars_afectadas = propagar_fc(var_actual, val, variables)
            
            # Si la propagación tuvo éxito (ningún dominio quedó vacío)
            if exitoso:
                # RECURSIÓN: Intentar resolver el resto
                if _resolver_fc_recursivo(variables):
                    return True  # Tiene solución
                
                # BACKTRACK: Si la recursión falló, restaurar dominios
                for var_rest in vars_afectadas:
                    restaurar_selectivo(var_rest, var_actual)
            
            # desaginar el valor (backtrack):
            var_actual.desasignar()
        
    return False


#########################################################################
# FUNCIÓN PRINCIPAL
#########################################################################
def resolver_forward_checking(variables):
    # PASO 1: Inicializar dominios recortando con las celdas fijas
    inicializacion_exitosa = inicializar_dominios_fc(variables)
    
    # Si algún dominio quedó vacío en la inicialización, no hay solución
    if not inicializacion_exitosa:
        return False
    
    # PASO 2: Ejecutar el algoritmo recursivo
    solucion_encontrada = _resolver_fc_recursivo(variables)
    
    return solucion_encontrada