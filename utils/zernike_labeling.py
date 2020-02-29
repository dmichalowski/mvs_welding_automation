# USAGE
# #python3 -m rvs.utils.extractAndLabelFeatures

# import the necessary packages
from scipy.spatial import distance as dist
import numpy as np
import mahotas
import cv2
import argparse
from imutils import paths, resize, grab_contours, auto_canny

from rvs.vs.detectanddescribe.detector import ContourDetecor
from rvs.vs.detectanddescribe.zernike_descriptor import ZernikeDescriptor
from rvs.vs.detectanddescribe.detectanddescribe import DetectAndDescribe


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-f", "--filename",
	help = "Filename for features and labels csv file")

args = vars(ap.parse_args())

imagePaths = list(paths.list_images(args["dataset"]))

detector = ContourDetecor(minArea= 20)

descriptors = (ZernikeDescriptor(degree = 7),ZernikeDescriptor(degree = 8),
    ZernikeDescriptor(degree = 9))

featureSizes = (20,25,30)


dad = DetectAndDescribe(detector, labeling = True)

multipleFeatures = []
for fs in featureSizes:
    multipleFeatures.append(np.zeros(shape = (1,fs)))

labels = np.zeros(shape = (1,1))


for path in imagePaths:
    image = cv2.imread(path)
    image = resize(image, width=800)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    autoCanny = auto_canny(blurred)
    autoCanny = cv2.dilate(autoCanny,None,iterations = 1)

    _,imageMultipleFeatures, imageLabels = dad.dad_multiple_zernike(autoCanny,
        image, descriptors, featureSizes)

    for i,_ in enumerate(multipleFeatures):
        multipleFeatures[i] = np.concatenate((multipleFeatures[i]
            ,imageMultipleFeatures[i]),axis = 0)

    labels = np.concatenate((labels,imageLabels), axis = 0)

labels = np.delete(labels, 0, 0)

for i,_ in enumerate(multipleFeatures):
    multipleFeatures[i] = np.delete(multipleFeatures[i],0,0)
    multipleFeatures[i] = np.concatenate((multipleFeatures[i],labels), axis = 1)

if args["filename"]:
    for i,f in enumerate(multipleFeatures):
        np.savetxt("/home/pi/rvs-git/rvs/resources/zernike/"+ str(i+7)
            + "_" + args["filename"], f, delimiter=",")

