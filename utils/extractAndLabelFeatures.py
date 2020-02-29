#python3 -m rvs.utils.extractAndLabelFeatures

import cv2
import argparse
import numpy as np
from imutils import paths, resize, grab_contours, auto_canny
from rvs.vs.detectanddescribe.detector import ContourDetecor
from rvs.vs.detectanddescribe.hudescriptor import HuDescriptor
from rvs.vs.detectanddescribe.detectanddescribe import DetectAndDescribe


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-o", "--output",
	help = "Folder name of for output")
ap.add_argument("-f", "--filename",
	help = "Filename for features and labels csv file")

args = vars(ap.parse_args())

imagePaths = list(paths.list_images(args["dataset"]))

detector = ContourDetecor(minArea= 20)
descriptor = HuDescriptor()
dad = DetectAndDescribe(detector,descriptor,labeling=True)

features = np.zeros(shape = (1,7))
labels = np.zeros(shape = (1,1))
for path in imagePaths:
    image = cv2.imread(path)
    image = resize(image, width=800)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    autoCanny = auto_canny(blurred)
    autoCanny = cv2.dilate(autoCanny,None,iterations = 1)
    autoCanny = cv2.erode(autoCanny,None,iterations = 1)

    _,imageFeatures, imageLabels = dad.detect_and_describe(autoCanny, source_image = image)

    features = np.concatenate((features,imageFeatures),axis = 0)
    labels = np.concatenate((labels,imageLabels), axis = 0)
    break


features = np.delete(features, 0, 0)
labels = np.delete(labels, 0, 0)

print(labels.flatten())

stackArray = np.concatenate((features,labels), axis = 1)
stackArray = stackArray[~np.isnan(stackArray).any(axis=1)]

#stackArray = stackArray[np.logicaap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-f", "--filename",
	help = "Filename for features and labels csv file")

args = vars(ap.parse_args())
l_not(np.isnan(stackArray))]


print(stackArray)
if args["filename"]:
    print(args["filename"])
    np.savetxt(args["output"]+args["filename"], stackArray, delimiter=",")

