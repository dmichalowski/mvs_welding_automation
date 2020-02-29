import numpy as np
import cv2
import argparse
from imutils import resize

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", required = True,
	    help = "Filename for image")

    args = vars(ap.parse_args())

    rows = 9
    cols = 6
    dimension = 26

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, dimension, 0.001)
    objp = np.zeros((rows*cols,3), np.float32)
    objp[:,:2] = np.mgrid[0:cols,0:rows].T.reshape(-1,2)

    objpoints = []
    imgpoints = []

    image = cv2.imread(args["filename"])
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (cols,rows),None)

    if ret == True:
        print("Pattern found! Press ESC to askip or ENTER to accept")
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        print(corners2[3,0].astype(int),corners2[50])

        # Draw and display the corners
        cv2.drawChessboardCorners(image, (cols,rows), corners2,ret)

        pnt1 = corners2[2,0].astype(int).astype(int)
        pnt2 = corners2[50,0].astype(int)

        cv2.circle(image, tuple(pnt1), 5, (0,255,0), -1)
        cv2.circle(image, tuple(pnt2), 5, (0,255,0), -1)
        cv2.imshow('img',image)

        print("Image accepted")
        objpoints.append(objp)
        imgpoints.append(corners2)
        imageSize = gray.shape
                

                #print(obj)
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
        cv2.waitKey(0)

if __name__ == '__main__':
    main()

    