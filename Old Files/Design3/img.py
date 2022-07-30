import cv2
import numpy as np
import matplotlib.pyplot as plt

img=cv2.imread("icon.png",cv2.IMREAD_COLOR)
dimensions = img.shape
b, g, r = cv2.split(img)
#print(dimensions)
#print(img[55,55])
for i in range(0,dimensions[0]):
	for j in range(0,dimensions[1]):
		if g[i,j]<100:
#(b[i,j]==84 and g[i,j]==76 and r[i,j]==70):
			b[i,j]=204
			g[i,j]=209
			r[i,j]=208
img2 = cv2.merge([b, g, r])
cv2.imwrite('newimg.png', img2)
