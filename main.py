# NOMBRE: IVÁN VALOR VERDU => GRUPO 40 I2ADE 
# DNI: 20525805F

#########################################################################
# CURSO 25-25
# PRACTICA 1 DE SISTEMAS INTELIGENTES: RESOLUCION DE SUDOKUS
#########################################################################   


#########################################################################  
#  REPRESENTA EL MAIN  
#########################################################################


import pygame
import copy
from tablero import *
from pygame.locals import *
import sys

#Librerias añadidas por mi
from backtraking import resolver_backtracking, get_stats_bk, reset_stats_bk 
from FC import resolver_forward_checking, get_stats_fc, reset_stats_fc
import time

GREY=(220,220,220)
NEGRO=(10,10,10)
GRIS_ACTIVO=(245,245,245)
GRIS_NORMAL=(169,169,169)
BLANCO=(255, 255, 255)

MARGEN=5 #ancho del borde entre celdas
MARGEN_DERECHO=125 #ancho del margen derecho entre la cuadrícula y la ventana
TAM=60  #tamaño de la celda
N=9 # número de filas del sudoku
VACIA='0'

#########################################################################
# Detecta si se pulsa un botón
#########################################################################   
def pulsaBoton(pos, boton):
    if boton.collidepoint(pos[0], pos[1]):    
        return True
    else:
        return False



#########################################################################
# Pintar un boton
#########################################################################   
def pintarBoton(screen, fuenteBot, boton, mensaje):
    if boton.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, GRIS_ACTIVO, boton, 0)        
    else:
        pygame.draw.rect(screen, GRIS_NORMAL, boton, 0)
        
    texto=fuenteBot.render(mensaje, True, NEGRO)
    screen.blit(texto, (boton.x+(boton.width-texto.get_width())/2, boton.y+(boton.height-texto.get_height())/2))         



#########################################################################
# Pintar el sudoku
#########################################################################         
def pintarTablero(screen, fuenteSud, tablero, copTab):
    pygame.draw.rect(screen, GREY, [0, 0, N*(TAM+MARGEN)+MARGEN, N*(TAM+MARGEN)+MARGEN],0)
    for fil in range(9):
        for col in range(9):
            if tablero is None or tablero.getCelda(fil, col)==VACIA :
                pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)            
            else:
                pygame.draw.rect(screen, BLANCO, [(TAM+MARGEN)*col+MARGEN, (TAM+MARGEN)*fil+MARGEN, TAM, TAM], 0)
                if tablero.getCelda(fil, col)==copTab.getCelda(fil, col):
                    color=NEGRO
                else:
                    color=GRIS_NORMAL                 
                texto= fuenteSud.render(tablero.getCelda(fil, col), True, color)            
                screen.blit(texto, [(TAM+MARGEN)*col+MARGEN+15, (TAM+MARGEN)*fil+MARGEN+5])
    
    #dibujar línea de cuadrícula     
    pygame.draw.line(screen, GRIS_NORMAL, (MARGEN, 3*(TAM+MARGEN)+2), (9*(TAM+MARGEN),3*(TAM+MARGEN)+2), 5)
    pygame.draw.line(screen, GRIS_NORMAL, (MARGEN, 6*(TAM+MARGEN)+2), (9*(TAM+MARGEN),6*(TAM+MARGEN)+2), 5)    
    pygame.draw.line(screen, GRIS_NORMAL, (3*(TAM+MARGEN)+2,MARGEN), (3*(TAM+MARGEN)+2,9*(TAM+MARGEN)), 5)
    pygame.draw.line(screen, GRIS_NORMAL, (6*(TAM+MARGEN)+2, MARGEN), (6*(TAM+MARGEN)+2,9*(TAM+MARGEN)), 5)
    pygame.draw.rect(screen, GRIS_NORMAL, [MARGEN, MARGEN, N*(TAM+MARGEN), N*(TAM+MARGEN)],5)



#########################################################################  
# Principal
#########################################################################
def main():    
    
    pygame.init()
    reloj=pygame.time.Clock()
    
    if len(sys.argv)==1: #si no se indica un mapa coge mapa.txt por defecto
        file='m1.txt'
    else:
        file=sys.argv[-1]
    
    anchoVentana=N*(TAM+MARGEN)+MARGEN_DERECHO
    altoVentana= N*(TAM+MARGEN)+2*MARGEN    
    dimension=[anchoVentana,altoVentana]
    screen=pygame.display.set_mode(dimension) 
    pygame.display.set_caption("Practica 1: Sudoku") 
    
    fuenteBot=pygame.font.Font(None, 30)
    fuenteSud= pygame.font.Font(None, 70)
    
    botLoad=pygame.Rect(anchoVentana-95, 75, 70, 50)    
    botBK=pygame.Rect(anchoVentana-95, 203, 70, 50)
    botFC=pygame.Rect(anchoVentana-95, 333, 70, 50)
    botAC3=pygame.Rect(anchoVentana-95, 463, 70, 50)
    
    game_over=False
    tablero=None
    copTab=None
    
    
    while not game_over:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:               
                game_over=True
            if event.type==pygame.MOUSEBUTTONUP:                
                #obtener posición                               
                pos=pygame.mouse.get_pos()

                #################  
                #   BOTON LOAD  #
                #################
                if pulsaBoton(pos, botLoad):                                      
                    tablero=Tablero(file)
                    copTab=copy.deepcopy(tablero) 
                    # Cuando pulso el boton LOAD, creo todas las 81 variables a partir 
                    # de las celdas del tablero con el metodo getCelda que guardo en una lista
                    variables_aux = []
                    for f in range(9):
                        for c in range(9):
                            variables_aux.append(Variable(f, c, tablero.getCelda(f, c)))
                    variables = list(variables_aux)
                    recortar_dominios_iniciales(variables)
                #################  
                #   BOTON BT  #
                #################              
                if pulsaBoton(pos, botBK):                    
                    if tablero is None:
                        print('Hay que cargar un sudoku')
                    else:
                        #Aqui llamo a algoritmo BT 
                        #Actualizo el tablero si hay solución,en caso contrario mostrar mensaje de SIN SOLUCIÓN
                        print("BK")
                        inicio = time.time()
                        reset_stats_bk()  # Reiniciar estadísticas antes de cada ejecución
                        if resolver_backtracking(variables):
                            fin = time.time()
                            pintar_variables(variables, tablero)

                            print("✅ Solución encontrada")
                            vars_exp, vals_prob = get_stats_bk()
                            print(f"📊 Variables exploradas: {vars_exp}")
                            print(f"📊 Valores probados: {vals_prob}")
                            print(f"⏱ Tiempo de ejecución: {fin - inicio:.4f} segundos") 
                        else:
                            fin = time.time()
                            print("❌ Sin solución, el algoritmo BK no lo resuelve")
                        

                #################  
                #   BOTON FC  #
                #################                                                 
                elif pulsaBoton(pos, botFC):                    
                    if tablero is None:
                        print('Hay que cargar un sudoku')
                    else:
                        #Aqui llamo a algoritmo FC 
                        #Actualizo el tablero si hay solución,en caso contrario mostrar mensaje de SIN SOLUCIÓN
                        print("FC")
                        inicio = time.time()
                        reset_stats_fc()  # Reiniciar estadísticas antes de cada ejecución
                        if resolver_forward_checking(variables):
                            fin = time.time()
                            pintar_variables(variables, tablero)

                            print("✅ Solución encontrada")
                            vars_exp, vals_prob = get_stats_fc()                     
                            print(f"📊 Variables exploradas: {vars_exp}")
                            print(f"📊 Valores probados: {vals_prob}")
                            print(f"⏱ Tiempo de ejecución: {fin - inicio:.4f} segundos") 
                        else:
                            print("❌ Sin solución, el algoritmo FC no lo resuelve")

                #################  
                #   BOTON AC3  #
                #################    
                elif pulsaBoton(pos, botAC3):
                    if tablero is None:
                        print('Hay que cargar un sudoku')
                    else:                        
                        print("AC3")                        
                        #aquí llamar al AC3    
               
        #limpiar pantalla
        screen.fill(GREY)
        #pintar cuadrícula del sudoku  
        pintarTablero(screen, fuenteSud, tablero, copTab)                   
        #pintar botones        
        pintarBoton(screen, fuenteBot, botLoad, "Load")
        pintarBoton(screen, fuenteBot, botBK, "BK")
        pintarBoton(screen, fuenteBot, botFC, "FC")
        pintarBoton(screen, fuenteBot, botAC3, "AC3")        
        #actualizar pantalla
        pygame.display.flip()
        reloj.tick(40)
        if game_over==True: #retardo cuando se cierra la ventana
            pygame.time.delay(500)
    
    pygame.quit()



#########################################################################  
# Pintar las variables (lista de Clase Variable) en el Tablero
#########################################################################
def pintar_variables(variables, tablero):
    for var in variables:
        # Pinta en el objeto Tablero el valor de cada Variable
        # var.fila y var.col son las coordenadas, var.valor es el número que tiene del 1 al 9
        if var.valor:
            tablero.setCelda(var.fila, var.col, var.valor)



#########################################################################  
# Recortar dominios iniciales (antes de FC y BT)
#########################################################################
# Para cada variable SIN valor, elimina del dominio los valores
# que ya están en su fila, columna o subcuadrícula.
def recortar_dominios_iniciales(variables):
    for var in variables:
        if not var.esta_instanciada():  # Solo celdas vacías
            # Obtener valores prohibidos
            valores_prohibidos = set()
            
            # Recoger valores de la fila
            for v in variables:
                if v.fila == var.fila and v.esta_instanciada():
                    valores_prohibidos.add(v.valor)
            
            # Recoger valores de la columna
            for v in variables:
                if v.col == var.col and v.esta_instanciada():
                    valores_prohibidos.add(v.valor)
            
            # Recoger valores de la subcuadrícula 3x3
            inicio_f = (var.fila // 3) * 3
            inicio_c = (var.col // 3) * 3
            for v in variables:
                if (inicio_f <= v.fila < inicio_f + 3 and 
                    inicio_c <= v.col < inicio_c + 3 and 
                    v.esta_instanciada()):
                    valores_prohibidos.add(v.valor)

            # Recortar el dominio
            var.dominio = [val for val in var.dominio if val not in valores_prohibidos]




#########################################################################  
# CLASE VARIABLE (se pide en la práctica)
#########################################################################
class Variable:
    ##############################  
    # Constructor clase Variable #
    ##############################
    def __init__(self, fila, col, valor):
        self.fila = fila
        self.col = col
        self.valor = valor if valor != '0' else None

        #He añadido esta variable para identificar a las celdas fijas,  si tiene valor 
        # cuando  cargo del fichero, es true (lo q significa que es fija)
        self.es_celda_fija = self.valor is not None

        #Si la celda no tiene valor entonces CELDA VACIA, su dominio es del 1 al 9
        #Si la celda si tiene valor entonces CELDA FIJA, su dominio es el valor (numero) que tenga
        if self.valor is None: 
            self.dominio = [str(i) for i in range(1, 10)]
        else:
            self.dominio = [valor]

        #Atributo para la poda de FC, que es una tupla donde para cada variable
        #guardo el dominio que he quitado y por que variable ha sido quitada con
        #el siguiente FORMATO => [ (dominio_quitado, (Coordenada_causante)) , () , () ...]
        #EJEMPLO     
        #self.poda = [(1,(0,0)),()]
        #Esto quiere decir que he quitado del dominio el 1 por la variable 0,0
        # (se hace para saber quien ha quitado el 1)
        self.poda = [] 


    ##############################  
    #  Métodos  clase Variable   #
    ##############################
    
    # Indica si la variable ya tiene valor
    def esta_instanciada(self):
        return self.valor is not None

    # Asignamos un valor a la variable del 1 al 9
    def asignar(self, val):
        self.valor = val

    # Quitamos el valor que tenga la variable
    def desasignar(self):
        # La desasignación debe ocurrir SIEMPRE que sea una CELDA VACIA,
        #  si es una CELDA FIJA (la que cargo del fichero) NO!!
        if not self.es_celda_fija:
            self.valor = None

    #ESTE LO TENÍA ANTERIORMENTE PERO ME HE DADO CUENTA QUE EN FC no funcionaba
    #def desasignar(self):
    #    if len(self.dominio) > 1:  # <-- ¡ESTA ERA LA REGLA PELIGROSA!
    #        self.valor = None

    #Métodos que uso para el algoritmo FC
    
    #Quita un valor del dominio y lo registra en poda con el formato que he explicado
    #  anteriormente [ (dominio_quitado, (Coordenada_causante)) , () , () ...]
    def quitar_valor(self, val, var_causante):
        if val in self.dominio:
            self.dominio.remove(val)
            # Añadi el valor podado y la variable que causó la poda a la tupla llamada PODA
            self.poda.append((val, (var_causante.fila, var_causante.col))) 
            return True
        return False
   
    #def restaurar(self): NO LO USO, IMPLEMENTO UNO EN FC.py
    #    if self.poda:
    #        for val, _ in self.poda:
    #            # Se añade el valor de vuelta
    #            if val not in self.dominio:
    #                self.dominio.append(val)
    #        
    #        self.poda = [] # Vacio la tupla PODA
    #        self.dominio.sort() # Dominio ordenado








if __name__=="__main__":
    main()



