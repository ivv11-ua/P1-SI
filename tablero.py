# NOMBRE: IVÁN VALOR VERDU => GRUPO 40 I2ADE 
# DNI: 20525805F

#########################################################################  
# REPRESENTA EL SUDOKU
#########################################################################

class Tablero:   
    def __init__(self, archivo):
        self.tam=9           
        self.tablero=leer(archivo)        
         
    def __str__(self):
        salida=""
        for f in range(self.tam):            
            for c in range(self.tam):
                salida += self.tablero[f][c]                
            salida += "\n"
        return salida
       
    def reset(self):
        for f in range(self.tam):
            for c in range(self.tam):
                self.tablero[f][c]='0'      
       
   
    
    def getCelda(self, fila, col):
        return self.tablero[fila][col]
    
    def setCelda(self, fila, col, val):
        self.tablero[fila][col]=val
        
    def getTablero(self):
        return self.tablero
    
        
def leer(archivo):
    tablero=[]
    
    try:  
        fich=open(archivo, "r")
        
        fila=-1
        for cadena in fich:            
            fila=fila+1            
            tablero.append([])            
            valores=cadena.split() 
            for i in range(9):                
                if valores[i] == '0':                    
                    tablero[fila].append('0')
                else:
                    tablero[fila].append(valores[i])
                
    except:
        print ("Error de fichero")
        fich.close()
    
    fich.close()
   
    return (tablero)




'''
ESTE CODIGO FUE CUANDO LO HICE TRABAJANDO DIRECTAMENTE SOBRE
TABLERO, SIN USAR LA CLASE VARIABLE!!

def es_valido(tablero, fila, col, val):
    # comprobar fila
    for j in range(9):
        if tablero.getCelda(fila, j) == val:
            return False
    # comprobar columna
    for i in range(9):
        if tablero.getCelda(i, col) == val:
            return False
    # comprobar subcuadro 3x3
    inicio_f = (fila // 3) * 3
    inicio_c = (col // 3) * 3
    for i in range(inicio_f, inicio_f + 3):
        for j in range(inicio_c, inicio_c + 3):
            if tablero.getCelda(i, j) == val:
                return False
    return True


def resolver_backtracking(tablero):
    for fila in range(9):
        for col in range(9):
            if tablero.getCelda(fila, col) == '0':
                for val in [str(i) for i in range(1, 10)]:
                    if es_valido(tablero, fila, col, val):
                        tablero.setCelda(fila, col, val)
                        if resolver_backtracking(tablero):
                            return True
                        tablero.setCelda(fila, col, '0')
                return False
    return True
'''