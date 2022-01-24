#%%
from importlib.resources import path
import cv2
import numpy as np
import math
import sys
import time
from abre_img import abre_img

#%%

# Núcleo de interpolação
def u(s, a):
	if (abs(s) >= 0) & (abs(s) <= 1):
		return (a+2)*(abs(s)**3)-(a+3)*(abs(s)**2)+1
	elif (abs(s) > 1) & (abs(s) <= 2):
		return a*(abs(s)**3)-(5*a)*(abs(s)**2)+(8*a)*abs(s)-4*a
	return 0

#%%
# Preenchimento de Valores de Imagem H, W, C
# H: Altura
# W: Largura
# C: Número de Canais da imagem

def preenchimento(img, H, W, C):
	zimg = np.zeros((H+4, W+4, C))
	zimg[2:H+2, 2:W+2, :C] = img
	
	# Preenchimento as primeiras/últimas duas colunas e fileiras
	zimg[2:H+2, 0:2, :C] = img[:, 0:1, :C]
	zimg[H+2:H+4, 2:W+2, :] = img[H-1:H, :, :]
	zimg[2:H+2, W+2:W+4, :] = img[:, W-1:W, :]
	zimg[0:2, 2:W+2, :C] = img[0:1, :, :C]
	
	# Preenchimento dos 8 pontos restantes
	zimg[0:2, 0:2, :C] = img[0, 0, :C]
	zimg[H+2:H+4, 0:2, :C] = img[H-1, 0, :C]
	zimg[H+2:H+4, W+2:W+4, :C] = img[H-1, W-1, :C]
	zimg[0:2, W+2:W+4, :C] = img[0, W-1, :C]
	return zimg

#%%
# Lógica Bicúbica
def bicubica(img, escala, a):
	
	# Captura tamanho da imagem
	H, W, C = img.shape
	
	img = preenchimento(img, H, W, C)
	
	# Cria imagem nova
	dH = math.floor(H*escala)
	dW = math.floor(W*escala)

	# converte imagem em Matriz
	dst = np.zeros((dH, dW, 3))

	h = 1/escala

	print('Execução de Busca Bicúbica\nTempo de espera Longo')
    

	inc = 0
	
	for c in range(C):
		for j in range(dH):
			for i in range(dW):
				
				# Obtendo as coordenadas dos valores próximos
				# X: Horizontal
				# Y: Vertical
				# Z: Profundidade

				x, y = i * h + 2, j * h + 2

				x1 = 1 + x - math.floor(x)
				x2 = x - math.floor(x)
				x3 = math.floor(x) + 1 - x
				x4 = math.floor(x) + 2 - x

				y1 = 1 + y - math.floor(y)
				y2 = y - math.floor(y)
				y3 = math.floor(y) + 1 - y
				y4 = math.floor(y) + 2 - y
				
				# Considerando todos os 16 valores próximos
				mat_l = np.matrix([[u(x1, a), u(x2, a), u(x3, a), u(x4, a)]])
				mat_m = np.matrix([[img[int(y-y1), int(x-x1), c],
									img[int(y-y2), int(x-x1), c],
									img[int(y+y3), int(x-x1), c],
									img[int(y+y4), int(x-x1), c]],
								[img[int(y-y1), int(x-x2), c],
									img[int(y-y2), int(x-x2), c],
									img[int(y+y3), int(x-x2), c],
									img[int(y+y4), int(x-x2), c]],
								[img[int(y-y1), int(x+x3), c],
									img[int(y-y2), int(x+x3), c],
									img[int(y+y3), int(x+x3), c],
									img[int(y+y4), int(x+x3), c]],
								[img[int(y-y1), int(x+x4), c],
									img[int(y-y2), int(x+x4), c],
									img[int(y+y3), int(x+x4), c],
									img[int(y+y4), int(x+x4), c]]])
				mat_r = np.matrix([[u(y1, a)], [u(y2, a)], [u(y3, a)], [u(y4, a)]])
				
				# Função dst usada para obter o produto escalar de 2 matrizes
				dst[j, i, c] = np.dot(np.dot(mat_l, mat_m), mat_r)

	# Se houver uma mensagem de erro, ela vai diretamente para stderr
	sys.stderr.write('\n')
	
	# Limpa o buffer
	# sys.stderr.flush()
	return dst

#%%
# main

if __name__=="__main__":

	local = 'Imagens/teste_png.png'
	destino = 'bicubica.png'
	img = cv2.imread('Imagens/teste_png.png')

	#Exibe imagem antes de Interpolação
	abre_img(local, 'Imagem antes do Processamento')
	print('Tamanho Original:', img.shape)

	# Fator de escala 
	escala = 2
	# Coeficiente
	a = -1/2

	# Execução de função
	dst = bicubica(img, escala, a)
	print('Busca Finalizada')

	# Salvando a imagem
	cv2.imwrite(destino, dst)
	Img_bicubica = cv2.imread(destino)

	#Exibe imagem depois de Interpolação
	abre_img(destino, 'imagem depois do processamento')
	print('Tamanho de imagem pós Interpolação Bicúbica:', Img_bicubica.shape)
