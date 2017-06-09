#from picamera import PiCamera
from PIL import ImageTk
import PIL.Image
from Tkinter import *
from imgProcessing import ImgProcessing
import cv2
from time import sleep


def set_realtime_img(path):
    resize = (PIL.Image.open(path)).resize((422, 302))
    image = ImageTk.PhotoImage(resize)

    lbl = Label(window, width=60, height=25, image=image, borderwidth=1, relief="flat")
    lbl.image = image
    lbl.grid(row=1, column=1, padx=10, sticky=N + S + W + E)


def do_processing(imgProc, path):

    #camera.capture('Imagens/frame.jpg')

    if not ImgProcessing.bg or not ImgProcessing.cameraEnable:
        return

    if path == 'Imagens/grayscale.jpg':

        imgProc.set_grayscale()
        set_realtime_img(path)
        window.after(20000, do_processing, imgProc, 'Imagens/blur.jpg')

    if path == 'Imagens/blur.jpg':
        imgProc.set_blur()
        set_realtime_img(path)
        window.after(20000, do_processing, imgProc, 'Imagens/diff.jpg')

    if path == 'Imagens/diff.jpg':
        imgProc.set_difference()
        set_realtime_img(path)
        window.after(20000, do_processing, imgProc, 'Imagens/threshold.jpg')

    if path == 'Imagens/threshold.jpg':
        imgProc.set_threshold()
        set_realtime_img(path)
        window.after(20000, do_processing, imgProc, 'Imagens/dilate.jpg')

    if path == 'Imagens/dilate.jpg':
        imgProc.set_dilation()
        set_realtime_img(path)
        window.after(20000, do_processing, imgProc, 'Imagens/contours.jpg')

    if path == 'Imagens/contours.jpg':
        imgProc.set_contours()
        set_realtime_img(path)
        window.after(20000, do_processing, imgProc, 'Imagens/result.jpg')

    if path == 'Imagens/result.jpg':
        imgProc.set_result()
        set_realtime_img(path)

        bg = cv2.imread('Imagens/background.jpg')
        frm = cv2.imread('Imagens/frame.jpg')
        imgProc = ImgProcessing(bg, frm)
        window.after(3000, do_processing, imgProc, 'Imagens/grayscale.jpg')


def btnSetImg_Click():
    #camera = PiCamera()
    #camera.capture('Imagens/background.jpg')

    ImgProcessing.bg = True

    imgResize = (PIL.Image.open('Imagens/background.jpg')).resize((422, 302))
    img = ImageTk.PhotoImage(imgResize)

    lblImg = Label(window, width=60, height=25, image=img, borderwidth=1, relief="flat")
    lblImg.image = img
    lblImg.grid(row=1, column=0, padx=10, sticky=N + S + W + E)


def btnPlayCamera_Click():

    ImgProcessing.cameraEnable = True

    if not ImgProcessing.bg:
        return

    # camera.start_preview(fullscreen=False, window = (100, 20, 640, 480))
    background = cv2.imread('Imagens/background.jpg')
    frame = cv2.imread('Imagens/frame.jpg')

    do_processing(ImgProcessing(background, frame), 'Imagens/grayscale.jpg')


def btnStopCamera_Click():
    # camera.stop_preview()
    ImgProcessing.cameraEnable = False

    lblImgRealTime = Label(window, width=60, height=20, bg="grey88", borderwidth=1, relief="flat")
    lblImgRealTime.grid(row=1, column=1, padx=10, sticky=N + S + W + E)


# Configura janela principal
window = Tk()
window.title("TCC")
window["bg"] = "grey99"

#camera = PiCamera()

lblGetBG = Label(window, text="Estacionamento vazio", font="Arial 10 bold", bg="grey99")
lblGetBG.grid(row=0, column=0, padx=10, pady=5, sticky=W)

# Label para mostrar imagem capturada
lblImgBG = Label(window, width=60, height=20, bg="grey88", borderwidth=1, relief="flat")
lblImgBG.grid(row=1, column=0, padx=10)

# Botao "Capturar imagem" para capturar imagem de background
btnSetImg = Button(window, width=20, text="Capturar imagem", font="Arial 10 bold", bg="SkyBlue2", borderwidth=1, relief="flat", command=btnSetImg_Click)
btnSetImg.grid(row=2, column=0, padx=10, pady=5, sticky=E)

lblRealTime = Label(window, text="Tempo real", font="Arial 10 bold", bg="grey99")
lblRealTime.grid(row=0, column=1, padx=10, pady=5, sticky=W)

# Label para mostrar imagens em tempo real do processamento da imagem
lblImgRealTime = Label(window, width=60, height=20, bg="grey88", borderwidth=1, relief="flat")
lblImgRealTime.grid(row=1, column=1, padx=10)

# Widget pai dos botoes
frmButtons = Frame(window, bg="grey99")
frmButtons.grid(row=2, column=1, padx=10, sticky=E)

# Botao "Parar camera"
btnStopCamera = Button(frmButtons, width=15, text="Parar camera", font="Arial 10 bold", bg="tomato", borderwidth=1, relief="flat", command=btnStopCamera_Click)
btnStopCamera.pack(side=RIGHT)

# Botao "Ligar camera"
btnPlayCamera = Button(frmButtons, width=15, text="Ligar camera", font="Arial 10 bold", bg="spring green", borderwidth=1, relief="flat", command=btnPlayCamera_Click)
btnPlayCamera.pack(side=RIGHT, padx=5)

# Width x Height + Left + Top
window.geometry("890x380+400+200")

window.mainloop()
