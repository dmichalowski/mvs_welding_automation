import cv2
import numpy as np
from imutils import resize
from joblib import load
import yaml

from rvs.vs.image_processor import ImageProcessor
from rvs.vs.detectanddescribe.detector import ContourDetecor
from rvs.vs.detectanddescribe.zernike_descriptor import ZernikeDescriptor
from rvs.vs.detectanddescribe.detectanddescribe import DetectAndDescribe
from rvs.utils.conf import Conf

#prawdopodobnie wypadna
import argparse

def analyze_image(image,conf):
    #loading calibration data
    with open(conf["calibration_file"]) as file:
        calib = yaml.full_load(file)

    #loading svm model
    clf = load(conf["svm_mode_file"]) #classifier

    #defining detectors
    detector = ContourDetecor(minArea = conf["min_contour_area"], maxArea= conf["max_contour_area"])
    descriptor = ZernikeDescriptor(image.shape[:2],degree = 9)
    dad = DetectAndDescribe(detector,descriptor)

    #processing photo
    img_prcs = ImageProcessor(np.asarray(calib['camera_matrix']),np.asarray(calib['dist_coeffs']),
        conf["tophat_coeff"], conf["thresh_coeff"])
    image = img_prcs.undistort_image(image)
    cv2.imshow("result",image)
    cv2.waitKey(0)

    image = resize(image, width=conf["output_width"])

    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, tuple(conf["kernel_size"]))
    processed_workspace, processed_markers = img_prcs.process(image, rectKernel)

    #detect workspace
    convex_pathing = True if conf["pathing_type"] == 'convex' else False

    #[TODO], revert to processed_markers, and change to convex=convex_pathing
    workspace_cnt = detector.detect_workspace(processed_markers, convex=False)

    #[TODO] delete
    cv2.drawContours(image, [workspace_cnt], -1, (0,255,0), 3)
    cv2.imshow("result",image)
    cv2.waitKey(0)

    #detect and describe marker candidates
    kps,features,_ = dad.detect_and_describe(processed_markers, 30)

    #classify contours
    if len(features) > 0:
        predictions = clf.predict(features)
        pnts = [k for p,k in zip(predictions,kps) if p > 0]

    return workspace_cnt,pnts,image


if __name__ == '__main__':
    #taking photo
    conf = Conf('/home/pi/rvs-git/rvs/config/config.json')

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", required = True,
	    help = "Filename for image")
    ap.add_argument("-c", "--calib", required = True,
	    help = "Filename for camera calibration data")
    args = vars(ap.parse_args())

    image = cv2.imread(args["filename"])
    workspace_cnt,pnts,image = analyze_image(image,conf)

    cv2.drawContours(image, [workspace_cnt], -1, (0,255,0), 3)

    cv2.imshow("result",image)
    cv2.waitKey(0)
    
    [cv2.circle(image, tuple(p), 5, (0,255,0), -1) for p in pnts]

    cv2.imshow("result",image)
    cv2.imwrite("workspace_convex.png", image)
    cv2.waitKey(0)


