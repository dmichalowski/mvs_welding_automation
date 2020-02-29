import cv2
from .contour_operations import filterContoursByArea, filterContoursByCentroid ,getCentroid
from rvs.si.alingment.line import calculateDistance
import imutils
import numpy as np

class ContourDetecor():
    def __init__(self, minArea = 100, maxArea = 4000, dist = 10):
        self.minArea = minArea
        self.maxArea = maxArea
        self.dist = dist

    def _getContours(self,image):
        cnts = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
        cnts = imutils.grab_contours(cnts)
        cnts = filterContoursByArea(cnts,self.minArea,self.maxArea)
        kps,cnts = filterContoursByCentroid(cnts, self.dist)
        return kps,cnts


    def detect(self,image):
        return self._getContours(image)

    def detect_workspace(self,image,convex = False):
        cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        approx = []

        for c in cnts:
            if convex:
                c = cv2.convexHull(c)

            #approximating contour to have less points
            peri = cv2.arcLength(c, True)
            approx.append(cv2.approxPolyDP(c, 0.01 * peri, True))

        #returning max area contour, presumed to be
        return max(approx,key=cv2.contourArea)


