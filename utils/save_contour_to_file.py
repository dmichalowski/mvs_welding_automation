# USAGE
# python approx_realworld.py

# import the necessary images
import cv2
import imutils
import numpy as np
from vs.contour_operations import saveContourToFile
# load the receipt image and convert, it to grayscale, and detect
# edges
image = cv2.imread("resources/images/dog_contour.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 75, 200)

# show the original image and edged map
cv2.imshow("Original", image)
cv2.imshow("Edge Map", edged)

# find contours in the image and sort them from largest to smallest,
# keeping only the largest ones
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:7]

# loop over the contours
#image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
print(image.shape[:2])
hullImage = np.zeros(image.shape[:2], dtype="uint8")
for c in cnts:
	# approximate the contour and initialize the contour color
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	# show the difference in number of vertices between the original
	# and approximated contours
	print("original: {}, approx: {}".format(len(c), len(approx)))

	# if the approximated contour has 4 vertices, then we have found
	# our rectangle
	if len(approx):
		# draw the outline on the image
		cv2.drawContours(hullImage, [approx], -1, 255, 2)

# show the output image
cv2.imshow("Output", hullImage)
saveContourToFile(approx,"resources/dog_contour.data")
cv2.waitKey(0)
