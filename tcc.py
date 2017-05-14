import numpy
import cv2

minArea = 10000

#Carregar as imagens do estacionamento
imgOriginal = cv2.imread('Imagens/parking2-occupied3.jpg')
background = cv2.imread('Imagens/parking2-empty.jpg', 0)
img = cv2.imread('Imagens/parking2-occupied3.jpg', 0)

cv2.imshow('Estacionamento Vazio', background)
cv2.waitKey(0)
cv2.imshow('Estacionamento Ocupado', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Aplicar o efeito Blur nas imagens
background = cv2.GaussianBlur(background, (21, 21), 0)
img = cv2.GaussianBlur(img, (21, 21), 0)

cv2.imshow('Aplicando Blur [1]', background)
cv2.waitKey(0)
cv2.imshow('Aplicando Blur [2]', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Calcular a diferenca entre as imagens
imgSemBackground = cv2.absdiff(background, img)

cv2.imshow('Diferenca entre as imagens', imgSemBackground)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Aplicar a tecnica de Threshold
ret, imgThreshold = cv2.threshold(imgSemBackground, 25, 255, cv2.THRESH_OTSU)

#Dilatar imagem
imgThreshold = cv2.dilate(imgThreshold, None, iterations=10)

cv2.imshow('Excluindo o Background', imgThreshold)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Detectar contornos
im2, contours, hierarchy = cv2.findContours(imgThreshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(imgThreshold, contours, -1, (100, 100, 100), 3)

cv2.imshow('Detectando Contornos', imgThreshold)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Identificar veiculos nas vagas
for contorno in contours:
    if cv2.contourArea(contorno) < minArea:
        continue

    (x, y, w, h) = cv2.boundingRect(contorno)
    cv2.rectangle(imgOriginal, (x, y), (x + 150, y + 200), (0, 255, 0), 3)

cv2.imshow('Vagas Livres', imgOriginal)
cv2.waitKey(0)
cv2.destroyAllWindows()
