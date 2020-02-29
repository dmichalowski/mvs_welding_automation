import numpy as np
import cv2
import math
from .line import Line, MovementLine, getLinesFromContour, calculateDistance
from robot.tool import Tool

class AlingmentPoint():
    def __init__(self):
        self.weldingPoints = []
        self.coordinates = None

class Vertex(AlingmentPoint):
    def __init__(self, point):
        self.vertex = point
        self.weldingPoints = []
        self.alingmentPoint = None

class Edge(AlingmentPoint):
    def __init__(self, line):
        self.line = line
        #self.weldingPoints = []
        #self.alingmentPoint = None

    def distanceCheck(self,point):
        perpendicular = Line.perpendicularLine(self.line,point)
        cross = Line.findIntersetion(self.line, perpendicular)

        ys = [self.line.p1[1], self.line.p2[1]]
        ys.sort()
        #test if cross point is in range of line segment
        if ys[0] <= cross[1] <= ys[1]:
            return calculateDistance(cross,point)
        else:
            return np.inf

    def findAlingment(self, point, dist):
        mean = np.mean(self.weldingPoints, axis = 0)
        perpendicular = Line.perpendicularLine(self.line,mean)
        cross = Line.findIntersetion(self.line, perpendicular)
        vector = [(cross[0] - mean[0]),(cross[1] - mean[1])]
        vector  = (vector / np.linalg.norm(vector))*dist
        self.alingmentPoint = (cross[0] + vector[0], cross[1] + vector[1])





        #if m > 1 sort by Y
            #if last point was lower sort rising

            #if last point was lower sort revere
        #if m < 1 sort by X

            #if last point was to the left sort rising

            #if last point was to the right sort falling
        



    @staticmethod
    def minDistance(edges, point):
        closestedge = edges[0]
        mindist = closestedge.line.distanceCheck(point)
        for edge in edges:
            dist = edge.line.distanceCheck(point)
            if dist < mindist:
                closestedge = edge
                mindist = dist
        return closestedge



def findEdges(contour):
    edges = []
    for line in getLinesFromContour(contour): 
        edges.append(Edge(line))
    return edges

#def sortKey(object):



        
# def main():
#     from contour_operations import loadContour

#     white = (255,255,255)
#     image = np.zeros((300,300,3),dtype='uint8')
#     perimeter = Perimeter(loadContour("../resources/dog_contour.data"))

#     vertices = [Vertex(tuple(x)) for x in perimeter.contour[:,0]] 
#     #print([v.vertex for v in vertecies])


#     tool = Tool(30)
#     cv2.drawContours(image, [perimeter.contour], -1, white, 3)
#     pnts = [(73,142),(192,174),(115,135),(232,122),(150,150),(240,70)]
#     for point in pnts: image = cv2.circle(image, point, 5, white, -1)
#     #print("Aquired points: ",pnts)
#     edges = findEdges(perimeter.contour)

#     #drawing edges & points
#     for e in edges:
#         #searching for points near edge
#         e.weldingPoints = [p for p in pnts if e.line.distanceCheck(p) < tool.size]
#         #print("Welding points: ",edge.weldingPoints)

#         #removing used points
#         pnts[:] = [x for x in pnts if x not in e.weldingPoints]
#         #print("Points after assigning",pnts)

#         #random color
#         color = tuple(map(int, np.random.randint(25, high=255, size=(3,))))

#         #draw edge line
#         image = e.line.drawLine(image,color)

#         #draw weld points of that edge
#         for p in e.weldingPoints: image = cv2.circle(image, p, 5, color, -1)

#     # for p in pnts:
#     #     #finding closest vertex
#     #     closestv = vertices[0]
#     #     mindist = calculateDistance(p,closestv.vertex)
#     #     for v in vertices:
#     #         dist = calculateDistance(p,v.vertex)
#     #         if dist < mindist:
#     #             closestv = v
#     #             mindist = dist

#     #     if mindist < tool.size:
#     #         closestv.weldingPoints.append(p)

#     #pnts[:] = [x for x in pnts if x not in vertices.weldingPoints]

#     # print("VERTS")
#     # print([v.weldingPoints for v in vertices])
    

#     cv2.imshow("image",image)
#     cv2.waitKey(0)

# if __name__ == '__main__':
#     main()
