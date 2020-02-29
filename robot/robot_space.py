import cv2
import numpy as np
from math import cos,sin,pi

def affine_matrix(t = (0,0),theta = 0,s = 1):
    return np.asarray([
        [s*cos(theta),-1*s*sin(theta),s*t[0]],
        [s*sin(theta), s*cos(theta), s*t[1]],
        [0,0,1]
    ])

class RobotSpace:
    def __init__(self, ofstx = 0, ofsty = 0, pixelDimRatio = 1, angle = 0):
        self.angle = angle
        self.pixelDimRatio = pixelDimRatio

    def getRotationMatrix(self,cx,cy):
        return cv2.getRotationMatrix2D((cx,cy),self.angle,self.pixelDimRatio)

class RobotSpaceTemp:
    def __init__(self, tool_offset,camera_offset, image_shape, pixelDimRatio = 1, angle = 0):
        self.tool_offset = tool_offset
        self.camera_offset = camera_offset
        self.angle = angle
        self.pixelDimRatio = pixelDimRatio
        self.image_shape = image_shape

        T1 = affine_matrix(t = -1*(np.asarray(image_shape[::-1])/2).astype(int),s = self.pixelDimRatio)
        T2 = affine_matrix(t = camera_offset, theta =  self.angle)
        T3 = affine_matrix(t = tool_offset)

        self.transformations = (T1,T2,T3)

    def _offset_center(self,pnt,image_shape):
        return (np.asarray(image_shape[::-1])/2).astype(int)

    def _flip_y(self,pnt,image_shape):
        pnt[1] = -1*(pnt[1] - (image_shape[0] - 2))
        return pnt

    def getRotationMatrix(self,cx,cy):
        return cv2.getRotationMatrix2D((cx,cy),self.angle,self.pixelDimRatio)

    def transformaPoint(self,pnt):
        pnt[1] = -1*(pnt[1] - (self.image_shape[0])) #flip y
        pnt = np.append(pnt,1)
        for T in self.transformations:
            pnt = np.dot(T,pnt)
        return pnt[:2]




def test():
    tool_offset = np.array([150,300])
    camera_offset = np.array([50,100])
    robotspace = RobotSpaceTemp(tool_offset,camera_offset, (100,100))
    #robotspace = RobotSpace()
    white = np.array([255,255,255],dtype='uint8')

    T1 = affine_matrix(s = 2)
    POINT = np.array([5,5])
    POINT = np.append(POINT,1)
    print(np.dot(T1,POINT))



    photo = np.zeros((25,51,3),dtype='uint8')
    image = np.zeros((600,800,3),dtype='uint8')
    
    image = cv2.arrowedLine(image, (0,0), (300,150), (0,0,255), 2)
    image = cv2.arrowedLine(image, (300, 150), (50+300,150+100), (0,0,255), 2)
    image = cv2.flip(image, 0)

    pnts = np.array([[0,0],[0,24],[50,0],[25,12],[50,24]])

    for p in pnts:
        p = robotspace._flip_y(p,photo.shape[:2])
        # p = robotspace._centering_image(p,photo.shape[:2])

    #print()
    print(pnts)

    photo[0,0] = white
    photo[24,0] = white
    photo[24,50] = white
    photo[0,50] = white
    photo[12,25] = white

    #photo[]


    
    
    cv2.imshow("PLANE",image)
    cv2.imshow("Photo",photo)
    cv2.waitKey(0)

def tryingToGetToWork():
    tool_offset = np.array([0,0])
    camera_offset = np.array([0,0])
    image_shape = np.array([100,200])
    # pnt = (np.asarray(image_shape[::-1])/2).astype(int)
    pnt = np.array([100,100])
    robotspace = RobotSpaceTemp(tool_offset,camera_offset,image_shape)

    pnt = robotspace.transformaPoint(pnt)
    print(pnt)




    

if __name__ == '__main__':
    tryingToGetToWork()
