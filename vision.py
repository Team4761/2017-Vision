import cv2
import numpy
import sys

def binarize_otsu(img):
	grayed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	_, thresholded = cv2.threshold(grayed, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	return thresholded

def draw_horizon_lines(img, bb1, bb2):
	def get_center_of_line(x, y, w):
		return (x + (w / 2), y)

	#expand rectangle tuples
	x1, y1, w1, h1 = bb1
	x2, y2, w2, h2 = bb2

	bb1_top_center = get_center_of_line(x1, y1, w1)
	bb2_top_center = get_center_of_line(x2, y2, w2)

	cv2.line(img, bb1_top_center, bb2_top_center, (255, 0, 0), 2)

img = cv2.imread(sys.argv[1])
img = binarize_otsu(img)
img = cv2.Canny(img, 100, 200)
contours, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

img_shape = numpy.shape(img)
img_w = img_shape[0]
img_h = img_shape[1]
out_dimensions = (img_w, img_h, 3)
out_img = numpy.zeros(out_dimensions, numpy.uint8)
cv2.drawContours(out_img, contours, -1, (0, 255, 0), 1)

bounding_rects = []

bounding_rects = [cv2.boundingRect(contour) for contour in contours[::2]]

for rect in bounding_rects:
	x, y, w, h = rect
	cv2.rectangle(out_img, (x, y), (x + w, y + h), (255, 255, 255), 2, 8, 0)

#print bounding_rects
draw_horizon_lines(out_img, bounding_rects[0], bounding_rects[1])

cv2.imshow("frame", out_img)
cv2.waitKey(0)
