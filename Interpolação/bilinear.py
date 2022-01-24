import numpy as np
from PIL import Image
from abre_img import abre_img
 


def novo_tamanho(path) :
    img_original = Image.open(path)
 
    img1 = np.asarray(img_original)    # Convete imagem em Array
    linhas, colunas, camadas = img1.shape
    novo = np.zeros( (2*linhas - 1, 2*colunas - 1, camadas) )
    
    #Exibe Imagem Original
    abre_img(path, 'Imagem antes de Interpolacao Bilinear')
    # print("Dimensões Originais da Imagem:", img1.shape)
 
    for layer in range(3) :
        novo[:, :, layer] = bilinear(img1[:, :, layer])
 
    # converter os valores em números inteiros de 8 bits
    novo = novo.astype(np.uint8)

    #Exibe Imagem depois de Interpolação
    # abre_img(nova_img, 'Imagem depois de Interpolação Bilinear')
    print("Novas dimensoes da Imagem: ", novo.shape)
 
    img2 = Image.fromarray(novo)  # Converte Array de Volta em Imagem
    img2.save(nova_img)
 
 
def bilinear(img1) :
    linhas, colunas = img1.shape
 
    rnovo = 2*linhas - 1
    cnovo = 2*colunas - 1
    novo = np.zeros((rnovo, cnovo))
 
    # Move pontos da Imagem Original

    novo = np.zeros( (2*linhas - 1, 2*colunas - 1) )
    for r in range(linhas) :
        for c in range(colunas) :
            novo[2*r, 2*c] = img1[r,c]
 
    linhas, colunas = novo.shape
  
    # Gera novos valores Verticais
    for r in range(1, linhas, 2) :
        for c in range(0, colunas, 2) :
            # topo + fundo
            novo[r,c] = ( novo[r-1,c] + novo[r+1,c] ) // 2
 
    # Gera novos valores Horizontais

    for r in range(0, linhas, 2) :
        for c in range(1, colunas, 2) :
            # esquerda + direita
            novo[r,c] = ( novo[r,c-1] + novo[r,c+1] ) // 2
 
    # Gera novos valores de centro, a partir de coordenadas

    for r in range(1, linhas, 2) :
        for c in range(1, colunas, 2) :
            # topo + fundo + esquerda + direita
            novo[r,c] = ( novo[r-1,c] + novo[r+1,c] + novo[r,c-1] + novo[r,c+1] ) // 4

    return novo
 
####################  main  ####################
 
if __name__=="__main__":
    path = 'Imagens/teste.jpg'
    nova_img = 'Bilinear.png'
    novo_tamanho(path)
