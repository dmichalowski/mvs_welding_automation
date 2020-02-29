import numpy as np
#from .temp_sheet import Perimeter
#from .contour_operations import loadContour
#import contour_operations
import cv2
import math

class Line():
    # def __init__(self,p1,p2):
    #     self.m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    #     self.b = p1[1] - self.m*p1[0]
    def __init__(self):
        self.m = 0
        self.b = 0
        self.p1 = (0,0)
        self.p2 = (0,0)
        self.vector = np.array([0,0])

    @classmethod
    def fromPoints(cls,p1,p2):
        line = Line()
        line.m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        line.b = p1[1] - line.m*p1[0]
        line.p1 = p1
        line.p2 = p2
        #line.vector = 
        return line

    @classmethod
    def perpendicularLine(cls, line, point):
        perpendicular = Line()
        perpendicular.m = -1*(1/line.m)
        perpendicular.b = point[1] - perpendicular.m*point[0]
        return perpendicular

    @classmethod
    def offsetLine(cls, line, offset, dirvector):
        offsetline = Line()
        offsetline.m = line.m
        offsetline.b = line.b

        #checking offset direction
        if dirvector[1] < 0:
            offsetline.b -= offset * math.sqrt(line.m ** 2 + 1)
        else:
            offsetline.b += offset * math.sqrt(line.m ** 2 + 1)
    
        return offsetline

    # def distanceFromPoint(self, point):
    #     d = abs((-1*self.m * point[0] + 1 * point[1] - self.b)) / (math.sqrt(self.m * self.m + 1 * 1)) 
    #     return d
    #     #print("Perpendicular distance is"),d

    def distanceCheck(self,point):
        perpendicular = Line.perpendicularLine(self,point) #230 80
        cross = Line.findIntersetion(self, perpendicular)

        ys = [self.p1[1], self.p2[1]]
        ys.sort()

        #test if cross point is in range of line segment
        if ys[0] <= cross[1] <= ys[1]:
            return calculateDistance(cross,point)
        else:
            return np.inf


    def drawLine(self,image,color):
        p1 = np.asarray([0,self.b], dtype = 'int')
        p2 = np.asarray([image.shape[0],self.m*image.shape[0]+self.b], dtype = 'int')
        image = cv2.line(image, tuple(p1), tuple(p2), color, 1)
        return image

    @staticmethod
    def findIntersetion(line1, line2):
        if line1.m == line2.b:
            return None
        x = (line2.b - line1.b) / (line1.m - line2.m)
        y = line1.m * x + line1.b
        return x,y

    @staticmethod
    def minDistance(lines, point):
        closestLine = lines[0]
        for line in lines:
            if line.distanceCheck(point) < closestLine.distanceCheck(point):
                closestLine = line
        return closestLine

def calculateDistance(p1,p2):  
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)  



def getLinesFromContour(contour):
    lines = []
    for i,_ in enumerate(contour):
        #linking last point to first
        index = i+1 if i < (len(contour) -1 ) else 0 
        #parsing points
        p1 = np.asarray(contour[i,0])
        p2 = np.asarray(contour[index,0])
        #print(p1, p2)
        lines.append(Line.fromPoints(p1,p2))
    return lines

class MovementLine(Line):
    def __init__(self):
        self.weldingMarkers = (0,0)
        self.crossPoint = (0,0)
        self.positioningMarkers = []

# def main():
#     #def distanceFromPoint:
#     image = np.zeros((300,300),dtype='uint8')
#     perimeter = Perimeter(loadContour("../resources/dog_contour.data"))
#     cv2.drawContours(image, [perimeter.contour], -1, 255, 3)

#     lines = getLinesFromContour(perimeter.contour)
#     #for line in lines: image = line.drawLine(image)
#     line = Line.minDistance(lines, [80,175])
#     perp = MovementLine.perpendicularLine(line,(80,175))
#     image = cv2.circle(image, (80,175), 5, 255, -1)
#     image = line.drawLine(image,255)
#     image = perp.drawLine(image,255)

#     # p1 = np.asarray(perimeter.contour[0,0])
#     # p2 = np.asarray(perimeter.contour[1,0])
#     # line = Line.fromPoints(p1,p2)

#     #print(line.p1, line.p2)
#     #image = line.drawLine(image)
#     #perpendicular = Line.perpendicularLine(line,[230,80])
#     #image = perpendicular.drawLine(image)
#     #print(distanceCheck(line,[230,80]))

#     #image = cv2.circle(image, cross, 5, 255, 2)

#     #closest_line = max()
#     cv2.imshow("image",image)
#     cv2.waitKey(0)

# if __name__ == '__main__':
#     main()

