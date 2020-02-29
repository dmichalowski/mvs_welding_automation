import argparse
import imutils
import cv2
import numpy as np

import math

#[TODO] check if used
import sys
from os import path

def cart2pol(point):
	x,y = point
	theta = np.arctan2(y, x)
	rho = np.hypot(x, y)
	if theta < 0:
		theta += 2*np.pi

	return theta, rho

def pol2cart(theta, rho):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y

def calculateDistance(p1,p2):  
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)  
	
def filterContoursByArea(cnts, minArea, maxArea):
	#find indexes of list outside of defined area
	list_of_indexes = []
	i = 0
	for cnt in cnts:
		
		if minArea <= cv2.contourArea(cnt) <= maxArea:
			pass
		else:
			list_of_indexes.append(i)
		i += 1
	
	#sort list
	list_of_indexes.sort(reverse = True)	
	
	#delete found objects
	for index in list_of_indexes:
		del cnts[index]
	return cnts
	
def filterContoursByMoments(cnts, source, maxDiffrence):
	#find indexes of list with too large diffrence
	#source is contour by which we compute diffrence
	list_of_indexes = []
	i = 0
	for cnt in cnts:
		
		if cv2.matchShapes(source,cnt,cv2.CONTOURS_MATCH_I3,0) <= maxDiffrence:
			pass
		else:
			list_of_indexes.append(i)
		i += 1
	
	#sort list
	list_of_indexes.sort(reverse = True)	
	
	#delete found objects
	for index in list_of_indexes:
		del cnts[index]
		
	return cnts	

def getCentroid(moments):
	#compute center of the contour
	cX = int(moments["m10"] / moments["m00"])
	cY = int(moments["m01"] / moments["m00"])

	return cX, cY
	
	
def drawCenter(cnts, image):
	i = 0
	for cnt in cnts:
		# compute the center of the contour
		moments = cv2.moments(cnt)
		cX, cY = getCentroid(moments)
	 
		# draw the contour and center of the shape on the image
		cv2.drawContours(image, [cnt], -1, (0, 255, 0), 2)
		cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
		cv2.putText(image, "center " + str(i), (cX - 20, cY - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		i += 1
	 
	return image
	
def saveContourToFile(cnt,filename):
	points = np.asarray(cnt[:,0])
	np.savetxt(filename,points)

def loadContour(filename):
	source = np.loadtxt(filename).astype(int)
	source = np.array(source)[:,np.newaxis,:]

	return source

def scaleContour(cnt, scale):
    M = cv2.moments(cnt)
    cx, cy = getCentroid(M)

    cnt_norm = cnt - [cx, cy]
    cnt_scaled = cnt_norm * scale
    cnt_scaled = cnt_scaled + [cx, cy]
    cnt_scaled = cnt_scaled.astype(np.int32)

    return cnt_scaled

def filterContoursByCentroid(cnts, dist):
	new_cnts = []
	kps = []

	cnt = cnts[0]
	cntrd = getCentroid(cv2.moments(cnt))
        
	for c in cnts[1:]:
		temp_cntrd = getCentroid(cv2.moments(c))
		
		if calculateDistance(cntrd, temp_cntrd) > dist:
			new_cnts.append(cnt)
			kps.append(cntrd)
			
			cnt = c
			cntrd = temp_cntrd
			
		elif cv2.contourArea(c) > cv2.contourArea(cnt):
			cnt = c
			cntrd = temp_cntrd
			
	return np.asarray(kps),np.asarray(new_cnts)
 
# def main():
# 	# construct the argument parse and parse the arguments
# 	ap = argparse.ArgumentParser()
# 	ap.add_argument("-i", "--image", required=True,
# 		help="path to the input image")
# 	args = vars(ap.parse_args())
	
# 	image = cv2.imread(args["image"])
# 	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# 	#thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)[1]
# 	thresh = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV, 11, 4)
# 	thresh = cv2.erode(thresh,None,iterations = 1)
# 	thresh = cv2.dilate(thresh,None,iterations = 2)

# 	cv2.imshow("img",image)
# 	cv2.imshow("gray",gray)
# 	cv2.imshow("thresh",thresh)
# 	cv2.waitKey(0)
	
# 	source = loadContour('/home/pi/rvs-git/rvs/resources/contour.dat')

# 	cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
# 		cv2.CHAIN_APPROX_SIMPLE)
# 	cnts = imutils.grab_contours(cnts)
# 	cnts = filterContoursByArea(cnts,100,4000)
# 	cnts = filterContoursByMoments(cnts, source, 0.45)
	
# 	i = 0
# 	#saveContourToFile(cnts[23], "/home/pi/rvs-git/rvs/resources/contour.dat")
# 	# for cnt in cnts:
# 	# 	print(str(i) + " :" + str(cv2.matchShapes(source,cnt,cv2.CONTOURS_MATCH_I3,0)))
# 	# 	i += 1
	
	
# 	#drawing contours and centers
# 	image = drawCenter(cnts, image)
	 
# 	# show the image
# 	cv2.imshow("Image", image)
# 	cv2.waitKey(0)

# if __name__ == '__main__':
# 	main()
