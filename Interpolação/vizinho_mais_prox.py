'''
Interpolação de Vizinho mais próximo
Refaz imagem em escala de Ciza
'''
#%%
import numpy as np
from abre_img import abre_img
import matplotlib.image as img
import matplotlib.pyplot as plt
from statistics import mean


#%%
def vizinho_mprox(path, img_cinza):
    m = img.imread(path)
    print("Começando Interpolação - Tempo de processamento médio")
    # Determinando Tamano da imagem Original
    largura, altura = m.shape[:2]

    # Nova dimensão de imagem com 4 atributos por pixel

    nova_img = np.zeros([largura, altura, 4])

    for i in range(largura):
        for j in range(altura):
            lst = [float(m[i][j][0]), float(m[i][j][1]), float(m[i][j][2])]
            avg = float(mean(lst))
            nova_img[i][j][0] = avg
            nova_img[i][j][1] = avg
            nova_img[i][j][2] = avg
            nova_img[i][j][3] = 1 # Valor Alpha se torna 1


    # Salva imagem Cinza
    img.imsave(img_cinza, nova_img)
    print('Interpolação por Vizinho mais próximo finalizada')

#%%
#Main
if __name__=="__main__":
    
    path = 'Imagens/teste_png.png'
    abre_img(path, 'imagem antes do processamento')
    img_cinza = 'vizinho_mais_prox_cinza.png'
    
    vizinho_mprox(path, img_cinza)
    abre_img(img_cinza, 'imagem depois do processamento')
