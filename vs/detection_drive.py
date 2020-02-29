import cv2
import argparse
import numpy as np
from imutils import paths, resize, grab_contours, auto_canny
from joblib import load

from .detectanddescribe.detector import ContourDetecor
from .detectanddescribe.zernike_descriptor import ZernikeDescriptor
from .detectanddescribe.detectanddescribe import DetectAndDescribe

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-f", "--filename",
	help = "Filename for features and labels csv file")

args = vars(ap.parse_args())

#initializng descriptor dector and dac classes

clf = load('/home/pi/rvs-git/rvs/resources/zernike9_linear.joblib') #classifier

imagePaths = list(paths.list_images("/home/pi/rvs-git/rvs/resources/" + args["dataset"]))

temp_image = cv2.imread(imagePaths[0])
temp_image = resize(temp_image, width=800)

detector = ContourDetecor(minArea = 40)
descriptor = ZernikeDescriptor(temp_image.shape[:2],degree = 9)
dad = DetectAndDescribe(detector,descriptor)

for path in imagePaths:
	image = cv2.imread(path)
	image = resize(image, width=800)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)

	autoCanny = auto_canny(blurred)
	autoCanny = cv2.dilate(autoCanny,None,iterations = 1)
	autoCanny = cv2.erode(autoCanny,None,iterations = 1)

	#feature size for deg 9 zernike is 30
	kps,features,cnts = dad.detect_and_describe(autoCanny, 30)

	predictions = clf.predict(features)

	for p,c in zip(predictions,cnts):
		#temp_image = image.copy()
		if p > 0:
			cv2.drawContours(image, [c], -1, (0,255,0), 1)
		else:
			cv2.drawContours(image, [c], -1, (0,0,255), 1)
		#cv2.writemask[y:y + h, x:x + w]
		
	cv2.imshow("wutwut",image)
	cv2.waitKey(0)

# print(predictions)



