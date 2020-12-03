import numpy as np
import cv2
from matplotlib import pyplot as plt
import math 
import pytesseract


def adjust_gamma(image, gamma=1.0):
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	return cv2.LUT(image, table)

def recognize_text(imag):
	
	img=cv2.imread(imag)
	kernel = (np.ones((3,3),np.uint8))
	imagen = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	img=adjust_gamma(imagen,gamma=.85)

	alto,ancho= img.shape
	t_rec=int(alto*0.25)

	t_rec_ancho=int(ancho*0.05)

	img=img[t_rec:alto-t_rec,t_rec_ancho:ancho-t_rec_ancho]

	ret,th2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
	opening = cv2.morphologyEx(th2, cv2.MORPH_OPEN, kernel)

	text1 =pytesseract.image_to_string(img, config='--psm 11')
	text2 =pytesseract.image_to_string(th2, config='--psm 11')
	text3 =pytesseract.image_to_string(opening, config='--psm 11')
	matricula=[]
	
	if len(text1)==11 and len(text2)==11 and len(text3)==11:
		text1=text1[0:9]
		text2=text2[0:9]
		text3=text3[0:9]
		if text1==text2 and text1==text3:
			matricula=text1
		elif text1==text2:
			matricula=text1
		elif text1==text3:
			matricula=text1
		elif text2==text3:
			matricula=text2
	elif len(text1)==11 and len(text2)==11:
		text1=text1[0:9]
		text2=text2[0:9]
		if text1==text2:
			matricula=text1
	elif len(text1)==11 and len(text3)==11:
		text1=text1[0:9]
		text3=text3[0:9]
		if text1==text3:
			matricula=text1
	elif len(text2)==11 and len(text3)==11:
		text2=text2[0:9]
		text3=text3[0:9]
		if text2==text3:
			matricula=text2
	elif len(text1)==11:
		text1=text1[0:9]
		matricula=text1
	elif len(text2)==11:
		text2=text2[0:9]
		matricula=text2	
	elif len(text3)==11:
		text3=text3[0:9]
		matricula=text3

	return matricula