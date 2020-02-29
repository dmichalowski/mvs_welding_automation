import cv2
import numpy as np
from math import copysign, log10

class HuDescriptor():
    def __init__(self, distance = 10):
        self.distance = distance

    def describe(self,cnt):
        return self._huMoments(cnt)

        

    def _huMoments(self,cnt):
        moments = cv2.moments(cnt)
        huMoments = cv2.HuMoments(moments)
        # Log scale hu moments
        for i in range(0,7):
            try:
                huMoments[i] = -1* copysign(1.0, huMoments[i]) * log10(abs(huMoments[i]))
            except ValueError:
                return None

        return huMoments.flatten()
