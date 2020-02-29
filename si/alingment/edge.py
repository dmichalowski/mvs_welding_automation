import numpy as np
import cv2
import math
from .line import Line, calculateDistance
from rvs.robot.tool import Tool

class AlingmentPoint():
    def __init__(self):
        self.weldingPoints = []
        self.coordinates = None
        self.alingmentPoint = None
        self.alingmentVector = (0,0)

class Vertex(AlingmentPoint):
    def __init__(self, point):
        self.vertex = point
        self.weldingPoints = []
        self.alingmentPoint = None
        self.alingmentVector = (0,0)

    def drawVertex(self, image):
        color = tuple(map(int, np.random.randint(25, high=255, size=(3,))))
        image = cv2.circle(image, self.vertex, 5, color, -1)
        for p in self.weldingPoints: image = cv2.circle(image, p, 5, color, -1)

        return image

class Edge(AlingmentPoint,Line):
    def __init__(self):
        self.p1 = (0,0)
        self.p2 = (0,0)
        #self.weldingPoints = []
        self.alingmentPoint = None
        self.alingmentVector = None

    def drawEdge(self, image):
        #random color
        color = tuple(map(int, np.random.randint(25, high=255, size=(3,))))
        #draw edge line
        image = self.drawLine(image,color)
        #draw weld points of that edge
        if self.weldingPoints:
            for p in self.weldingPoints: image = cv2.circle(image, p, 5, color, -1)

        return image


    @classmethod
    def fromPoints(cls,p1,p2):
        edge = Edge()
        edge.m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        edge.b = p1[1] - edge.m*p1[0]
        edge.p1 = p1
        edge.p2 = p2
        #line.vector = 
        return edge

    def distanceCheck(self,point):
        perpendicular = Line.perpendicularLine(self,point)
        cross = Line.findIntersetion(self, perpendicular)

        ys = [self.p1[1], self.p2[1]]
        ys.sort()
        #test if cross point is in range of line segment
        if ys[0] <= cross[1] <= ys[1]:
            return calculateDistance(cross,point)
        else:
            return np.inf

    # def findAlingment(self, point, dist):
    #     mean = np.mean(self.weldingPoints, axis = 0)
    #     perpendicular = Line.perpendicularLine(self.line,mean)
    #     cross = Line.findIntersetion(self.line, perpendicular)
    #     vector = [(cross[0] - mean[0]),(cross[1] - mean[1])]
    #     vector  = (vector / np.linalg.norm(vector))*dist
    #     self.alingmentPoint = (cross[0] + vector[0], cross[1] + vector[1])





        #if m > 1 sort by Y
            #if last point was lower sort rising

            #if last point was lower sort revere
        #if m < 1 sort by X

            #if last point was to the left sort rising

            #if last point was to the right sort falling
        



    # @staticmethod
    # def minDistance(edges, point):
    #     closestedge = edges[0]
    #     mindist = closestedge.line.distanceCheck(point)
    #     for edge in edges:
    #         dist = edge.line.distanceCheck(point)
    #         if dist < mindist:
    #             closestedge = edge
    #             mindist = dist
    #     return closestedge


def getEdgesFromPoints(points):
    edges = []
    for i,_ in enumerate(points):
        #linking last point to first
        index = i+1 if i < (len(points) -1 ) else 0 

        edges.append(Edge.fromPoints(points[i],points[index]))
        
    return edges