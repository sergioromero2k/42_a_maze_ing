# NORTE = 1  # 0001
# ESTE  = 2  # 0010
# SUR   = 4  # 0100
# OESTE = 8  # 1000

# celda = 13  # 1101

# if celda & NORTE:
#     print("Dibuja línea arriba")
# if celda & ESTE:
#     print("Dibuja línea derecha")
# if celda & SUR:
#     print("Dibuja línea abajo")
# if celda & OESTE:
#     print("Dibuja línea izquierda")

ancho = 3
alto = 3

matriz = [[15 for x in range (ancho)] for y in range(alto)]
print(matriz)