import numpy
import cv2


class ImgProcessing(object):
    bg = False
    cameraEnable = False

    def __init__(self, background, frame):
        self.minArea = 10000
        self.background = background
        self.frame = frame

    def set_grayscale(self):
        self.background = cv2.cvtColor(self.background, cv2.COLOR_RGB2GRAY)
        self.grayscale = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        cv2.imwrite('Imagens/grayscale.jpg', self.grayscale)

    def set_blur(self):
        self.background = cv2.GaussianBlur(self.background, (21, 21), 0)
        self.blur = cv2.GaussianBlur(self.grayscale, (21, 21), 0)
        cv2.imwrite('Imagens/blur.jpg', self.blur)

    def set_difference(self):
        self.diff = cv2.absdiff(self.background, self.blur)
        cv2.imwrite('Imagens/diff.jpg', self.diff)

    def set_threshold(self):
        ret, self.threshold = cv2.threshold(self.diff, 25, 255, cv2.THRESH_OTSU)
        cv2.imwrite('Imagens/threshold.jpg', self.threshold)

    def set_dilation(self):
        self.dilate = cv2.dilate(self.threshold, None, iterations=6)
        cv2.imwrite('Imagens/dilate.jpg', self.dilate)

    def set_contours(self):
        im2, self.contours, hierarchy = cv2.findContours(self.dilate.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(self.dilate, self.contours, -1, (100, 100, 100), 3)
        cv2.imwrite('Imagens/contours.jpg', self.dilate)

    def set_result(self):
        for contour in self.contours:
            if cv2.contourArea(contour) < self.minArea:
                continue

            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(self.frame, (x, y), (x + 150, y + 200), (0, 255, 0), 3)

        cv2.imwrite('Imagens/result.jpg', self.frame)
