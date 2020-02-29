import cv2
import numpy as np
import mahotas

class ZernikeDescriptor():
    def __init__(self, imageShape, degree = 8):
        
        self.imageShape = imageShape
        self.degree = degree

    def describe(self,cnt):
        roi = self._getRoi(cnt)
        return self._describeZernike(roi,cnt)

    def _getRoi(self,cnt): 
        mask = np.zeros(self.imageShape, dtype="uint8")
        cv2.drawContours(mask, [cnt], -1, 255, -1)

        # extract the bounding box ROI from the mask
        (x, y, w, h) = cv2.boundingRect(cnt)
        return mask[y:y + h, x:x + w]

    def _describeZernike(self,roi,cnt):
        return mahotas.features.zernike_moments(roi, cv2.minEnclosingCircle(cnt)[1], degree=self.degree)