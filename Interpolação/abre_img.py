import cv2
import numpy as np


def abre_img(img_path, nome_img):
    img = cv2.imread(img_path, cv2.IMREAD_ANYCOLOR)

    cv2.namedWindow(nome_img) #Nomeia a janela
    cv2.imshow(nome_img, img) #Exibe a imagem

    #Mostra caracteristícas da imagem
    print('Altura (height): %d pixels' % (img.shape[0])) 
    print('Largura (width): %d pixels' % (img.shape[1]))
    print('Canais (channels): %d'      % (img.shape[2]))

    cv2.waitKey(5000) #Função Wait para que a imagem não feche