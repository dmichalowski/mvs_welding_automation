import cv2
import argparse
import numpy as np
from imutils import paths, resize, grab_contours, auto_canny
import yaml

class ImageProcessor:
    def __init__(self,camera_matrix,dist_coeffs,tophat_coeff = 12,
        thresh_coeff = 8):
        self.mtx = camera_matrix
        self.dist = dist_coeffs
        self.tophat_coeff = tophat_coeff
        self.thresh_coeff = thresh_coeff

    def undistort_image(self,image):
        h,w = image.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(self.mtx,self.dist,(w,h),1,(w,h))

        # undistort
        undstrd_img = cv2.undistort(image, self.mtx, self.dist, None, newcameramtx)

        #crop image
        x,y,w,h = roi
        undstrd_img = undstrd_img[y:y+h, x:x+w]

        return undstrd_img

    def process(self, image, kernel):
        verbose = True
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        if verbose:
            cv2.imshow("gray",blurred)

        #exposing robot workspace
        tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)

        thresh = cv2.adaptiveThreshold(blurred + self.tophat_coeff*tophat, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 15)
        
        if verbose:
            cv2.imshow("thresh_workspace",thresh)

        canny = auto_canny(blurred + 2*self.thresh_coeff*thresh)
       
        output_workspace = cv2.dilate(canny,None,iterations = 5)
        output_workspace = cv2.erode(output_workspace,None,iterations = 1)

        if verbose:
            cv2.imshow("output_workspace",output_workspace)

        #exposing markers
        thresh = cv2.adaptiveThreshold(blurred, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 15)


        canny = auto_canny(blurred  + 6*thresh)


        output_markers = cv2.dilate(canny,None,iterations = 1)
        output_markers = cv2.erode(output_markers,None,iterations = 1)

        if verbose:
            cv2.imshow("output_markers",thresh)

        cv2.waitKey(0)

        return output_workspace,output_markers

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", required = True,
	    help = "Filename for image")
    ap.add_argument("-c", "--calib", required = True,
	    help = "Filename for camera calibration data")

    args = vars(ap.parse_args())

    image = cv2.imread(args["filename"])
    image = resize(image,width = 800)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    with open(args["calib"]) as file:
        documents = yaml.full_load(file)

    img_prcs = ImageProcessor(np.asarray(documents['camera_matrix']),np.asarray(documents['dist_coeffs']))
    image = img_prcs.undistort_image(image)

    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
    processed_image,processed_image_2 = img_prcs.process(image,rectKernel)
    
    cv2.imshow("workspace", resize(processed_image,width = 800))
    cv2.imshow("markers", resize(processed_image_2,width = 800))
    cv2.imshow("Original", resize(image,width = 800))
    cv2.waitKey(0)

if __name__ == '__main__':
    main()

