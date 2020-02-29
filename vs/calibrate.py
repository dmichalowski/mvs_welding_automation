import numpy as np
import cv2
import glob
import argparse
import yaml
from imutils import paths, resize

class Calibrate:
    def __init__(self,rows,cols,dimension):
        # rows = 9
        # cols = 6
        # dimension = 26

        imagePaths = sorted(list(paths.list_images("images/chessboard")))

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, dimension, 0.001)

        self.filename = "calibrate.yaml"

        self.objp = np.zeros((rows*cols,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:cols,0:rows].T.reshape(-1,2)

        self.corners = []
        self.imageSize = []

        self.start(imagePaths,rows,cols,criteria)
            
    def start(self,imagePaths,rows,cols,criteria):
        objpoints = []
        imgpoints = []
        for imagePath in imagePaths:
            #-- Read the file and convert in greyscale
            image = cv2.imread(imagePath)

            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (cols,rows),None)

            # If found, add object points, image points (after refining them)
            if ret == True:
                print("Pattern found! Press ESC to askip or ENTER to accept")
                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                print(corners2)

                # Draw and display the corners
                cv2.drawChessboardCorners(image, (cols,rows), corners2,ret)
                cv2.imshow('img',resize(image.copy(),width=500))
                
                k = cv2.waitKey(0) & 0xFF
                if k == 27: #-- ESC Button
                    print("Image Skipped")
                    continue

                print("Image accepted")
                objpoints.append(self.objp)
                imgpoints.append(corners2)
                self.imageSize = gray.shape
                

                #print(obj)
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
        self.saveCameraParams(mtx,dist,ret)

    def saveCameraParams(self, mtx, dist, ret):
        print("Reprojection Error:", ret)
        print(mtx)
        print("")
        print(dist)

        calib_data = dict(
            image_width=self.imageSize[0],
            image_height=self.imageSize[1],
            camera_matrix=mtx.tolist(),
            dist_coeffs=dist.tolist(),
            avg_reprojection_error=ret,
        )

        with open(self.filename, 'w') as outfile:
            print("Saving calibration data")
            try:
                yaml.dump(calib_data, outfile)
                print("Saved.")
            except BaseException as e:
                print(e)

def main():
        calibration = Calibrate(9,6,26)
        #calibration.findingImgsWithChessboard()
        #calibration.loadImgs()
        
if __name__ == "__main__":
    main()
    
