import cv2
import numpy as np

class DetectAndDescribe():
    def __init__(self, detector, descriptor = None, labeling = False,verbose = True):
        self.detector = detector
        self.descriptor = descriptor
        self.verbose = verbose
        self.labeling = labeling

    def detect_and_describe(self,image,feature_size,source_image = None):
        kps,cnts = self.detector.detect(image)

        features = np.zeros(shape = (len(cnts),feature_size))
        #only for manually labeling data
        if self.labeling:
            labels = np.zeros(shape = (len(cnts),1))

        for i,c in enumerate(cnts):
            features[i] = self.descriptor.describe(c)

            #only for manually labeling data
            if self.labeling:
                temp_image = source_image.copy()
                cv2.drawContours(temp_image, [c], -1, (0,255,0), 3)
                cv2.imshow("last", temp_image)

                key = cv2.waitKey(0) & 0xFF
                labels[i] = -1 if key == ord('q') else 1

        if self.labeling:
            return kps,features,labels
        else:
            return kps,features,cnts

    def dad_multiple_zernike(self,image,source_image,descriptors,feature_sizes):
        kps,cnts = self.detector.detect(image)
        multipleFeatures = []

        for _,s in zip(descriptors,feature_sizes):
            multipleFeatures.append(np.zeros(shape = (len(cnts),s)))

        if self.labeling:
            labels = np.zeros(shape = (len(cnts),1))

        for i,c in enumerate(cnts):

            for f,descriptor in zip(multipleFeatures,descriptors):
                f[i] = descriptor.describe(c)

            #only for manually labeling data
            if self.labeling:
                temp_image = source_image.copy()
                cv2.drawContours(temp_image, [c], -1, (0,255,0), 3)
                cv2.imshow("last", temp_image)

                key = cv2.waitKey(0) & 0xFF
                labels[i] = -1 if key == ord('q') else 1


        if self.labeling:
            return kps,multipleFeatures,labels

        else:
            return kps, multipleFeatures
                

                

            
        


            