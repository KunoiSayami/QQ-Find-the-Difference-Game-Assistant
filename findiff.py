import pyautogui
from PIL import Image
import time
import cv2
from skimage.measure import compare_ssim
import imutils

size_x = 286
size_y = 381

x_offset = 45

img2_offset = 76

while True:
	loc = pyautogui.locateOnScreen('side.png')
	if loc is None:
		continue
	scr = pyautogui.screenshot()
	scr.save('tmp.png')
	with Image.open('side.png') as img:
		_, y = img.size
	with Image.open('tmp.png') as img:
		# Reference: https://www.geeksforgeeks.org/python-pil-image-crop-method/
		im1 = img.crop((
			loc.left + x_offset,
			loc.top + y + 1,
			loc.left + x_offset + size_y,
			loc.top + y + size_x
			))
		im2 = img.crop((
			loc.left + x_offset + img2_offset + size_y,
			loc.top + y + 1,
			loc.left + x_offset + size_y + img2_offset + size_y,
			loc.top + y + size_x
			))
	#im1.show()
	#im2.show()
	im1.save('diff1.png', "PNG")
	im2.save('diff2.png', "PNG")
	# Reference: https://www.pyimagesearch.com/2017/06/19/image-difference-with-opencv-and-python/
	imageA = cv2.imread('diff1.png')
	imageB = cv2.imread('diff2.png')
	grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
	grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
	(score, diff) = compare_ssim(grayA, grayB, full=True)
	diff = (diff * 255).astype("uint8")
	#print("SSIM: {}".format(score))
	thresh = cv2.threshold(diff, 0, 255,
		cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	for c in cnts:
		# compute the bounding box of the contour and then draw the
		# bounding box on both input images to represent where the two
		# images differ
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
		cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

	# show the output images
	cv2.imshow("Original", imageA)
	#cv2.imshow("Modified", imageB)
	#cv2.imshow("Diff", diff)
	#cv2.imshow("Thresh", thresh)
	cv2.waitKey(0)
