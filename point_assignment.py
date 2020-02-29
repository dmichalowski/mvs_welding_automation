import numpy as np
import cv2
import math
import os.path
from rvs.si.alingment.line import Line, calculateDistance
from rvs.si.alingment.edge import Edge, Vertex, getEdgesFromPoints
from rvs.vs.tool import Tool

def minDistance(pnts, point):
    closestPoint = pnts[0]
    mindist = calculateDistance(point, closestPoint)
    for p in pnts:
        dist = calculateDistance(point, p)
        if dist < mindist:
            closestPoint = p
            mindist = dist
    return closestPoint

def _nearest_point_sorting(weldingPoints):
    if weldingPoints:
        #define first object
        closest_point = weldingPoints[0]
        sortedWeldPoints = [closest_point]

        #hard copy welding point list
        temp = weldingPoints.copy()

        #start looping thru points and sorting by nearest neighbour
        for w in weldingPoints:
            temp.remove(closest_point)

            if temp:
                closest_point = minDistance(temp,w)
                sortedWeldPoints.append(closest_point)

        return sortedWeldPoints

    else:
        return weldingPoints

def assignPointsToEdges(contour,pnts,dist):
    edges = getEdgesFromPoints(np.asarray(contour[:,0]))
    for e in edges:
        #searching for points near edge
        e.weldingPoints = [p for p in pnts if e.distanceCheck(p) < dist]
        #removing used points
        pnts[:] = [x for x in pnts if x not in e.weldingPoints]

        #sorting by nearest neigbour, starting from p1
        e.weldingPoints = sorted(e.weldingPoints, key = lambda p: calculateDistance(p,e.p1))
        e.weldingPoints = _nearest_point_sorting(e.weldingPoints)


    return edges,pnts

def assignPointsToVertecies(contour,pnts,dist):
    vertices = [Vertex(tuple(x)) for x in contour[:,0]]

    for v in vertices:
        #searching for points near vertex
        v.weldingPoints = [p for p in pnts if calculateDistance(v.vertex,p) < dist]
        #removing used points
        pnts[:] = [x for x in pnts if x not in v.weldingPoints]

        #sorting by nearest neigbour, starting from vertex
        v.weldingPoints = sorted(v.weldingPoints, key = lambda p: calculateDistance(p,v.vertex))
        v.weldingPoints = _nearest_point_sorting(v.weldingPoints)


    return vertices, pnts



if __name__ == '__main__':
    from rvs.vs.contour_operations import loadContour
    white = (255,255,255)
    image = np.zeros((300,300,3),dtype='uint8')
    tool = Tool(30)

    #loading contour
    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "resources/dog_contour.data")
    contour = loadContour(path)

    pnts = [(73,142),(192,174),(115,135),(232,122),(150,150),(240,70)]
    for point in pnts: image = cv2.circle(image, point, 5, white, -1)

    edges = getEdgesFromPoints(np.asarray(contour[:,0]))

    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "resources/dog_contour.data")
    contour = loadContour(path)
    #edges, vertices, pnts = assignPoints(contour,pnts,tool.size)
    edges, pnts = assignPointsToEdges(contour,pnts,tool.size)
    vertices,pnts = assignPointsToVertecies(contour, pnts, tool.size)

    for e in edges:
        if e.weldingPoints:
            image = e.drawEdge(image)

    for v in vertices:
        if v.weldingPoints:
            image = v.drawVertex(image)

    cv2.imshow("image",image)
    cv2.waitKey(0)

    
