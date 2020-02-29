import numpy as np
import cv2


from .line import calculateDistance
from rvs.vs.detectanddescribe.contour_operations import getCentroid
from .edge import Edge


def _createRow(weld, point, vector):
    return np.array([[weld,weld],point,vector])

def _createVector(p1,p2,len_ = 0):
    vector = np.asarray([p2[0] - p1[0], p2[1] - p1[1]])

    if len_ > 0:
        return (vector / np.linalg.norm(vector))*len_
    else:
        return vector

def drawRow(image, row):
    pnt = tuple(map(int,row[1]))
    if row[0,0]:
        image = cv2.circle(image, pnt, 5, (255,0,0), -1)

    vectorStart = tuple(map(int,row[1] - row[2]))
    image = cv2.arrowedLine(image, vectorStart, pnt, (0,0,255), 2)
    return image

class Path():
    def __init__(self, edges, vertices, offPnts, cntPnts):
        weldCount = 0
        alignCount = 0
        
        #counting weld points
        for e in edges:
            weldCount += len(e.weldingPoints)
            if e.alingmentPoint is not None: alignCount += 1         

        #initializing numpy matrix
        self.path = np.zeros((len(offPnts)+ alignCount + weldCount + 1,3,2))
        vector = np.array([0,10]) #first vector

        #assign first row
        self.path[0] = _createRow(False,(0,0), vector / np.linalg.norm(vector) * 30)
        
        #go thru edges adding points to path
        index = 1
        for offp,cntp,e in zip(offPnts, cntPnts, edges):
            self.path[index] = _createRow(False,offp,_createVector(offp,cntp,30))
            index +=1
            if e.weldingPoints:
                self.path[index] = _createRow(False,e.alingmentPoint,e.alingmentVector)
                index += 1
                for j,w in enumerate(e.weldingPoints):
                    self.path[index+j] = _createRow(True,w,e.alingmentVector)
                index += j + 1

        #print("PATH1",self.path)

        #go thru vertices inserting points to path
        for v in vertices:
            if v.weldingPoints:
                idx = np.where(v.alingmentPoint == self.path[:,1])[0][0]
                for i,w in enumerate(v.weldingPoints):
                    vector = _createVector(v.alingmentPoint,w,30)
                    row = _createRow(True,w,vector)
                    self.path = np.insert(self.path, idx + 1, row, axis=0)

        # print(self.path)
        # print("align",alignCount)
        # print("weld",weldCount)
        # print("points",len(offPnts))
        # print("sum",(len(offPnts)+ alignCount + weldCount))
        # print("path",len(self.path))

    def transformToRegularAxis(self,ylength):
        for row in self.path:
            row[1][1] = -1*(row[1][1] - ylength)
            row[2][1] *= -1

    def transformPath(self, offset, rotationMatrix):
        for row in self.path:
            endPoint = row[1]
            startPoint = endPoint - row[2]

            #matricie multiplication, appendig 1 to point array to make it possible
            endPoint = np.dot(rotationMatrix,np.append(endPoint,1)) 
            startPoint = np.dot(rotationMatrix,np.append(startPoint,1))

            row[1] = endPoint + offset
            row[2] = _createVector(startPoint,endPoint,30)


    
    def temp(self,offset,rotationMatrix):
        for row in self.path:
            endPoint = row[1]
            startPoint = endPoint - row[2]

            print(endPoint,startPoint)

            #matricie multiplication, appendig 1 to point array to make it possible
            endPoint = np.dot(rotationMatrix,np.append(endPoint,1)) 
            startPoint = np.dot(rotationMatrix,np.append(startPoint,1))

            print(endPoint,startPoint)
            row[1] = endPoint + offset
            row[2] = _createVector(startPoint,endPoint,30)

            break


    def showPath(self,image):
        for row in self.path:
            temp_image = image.copy()
            temp_image = drawRow(temp_image,row)
            cv2.imshow("path", temp_image)
            cv2.waitKey(0)
        return image

        

        #print(self.path)
