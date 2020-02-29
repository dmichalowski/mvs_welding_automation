import numpy as np
import cv2
import math


from .line import Line, calculateDistance
from .edge import Edge, Vertex, getEdgesFromPoints

def minDistance(pnts, point):
    closestPoint = pnts[0]
    mindist = calculateDistance(point, closestPoint)
    for p in pnts:
        dist = calculateDistance(point, p)
        if dist < mindist:
            closestPoint = p
            mindist = dist
    return closestPoint

def arrangeIdxs(idx, array_length):
    idxs = np.zeros(array_length, dtype = int)
    for i in range(array_length):
        idxs[i] = idx
        idx = (idx + 1) % array_length

    return idxs
        


    

def directionVector(edge, contour):
    #perpendicular line in the middle of edge
    alpha = 1
    edgecenter = ((edge.p1[0] + edge.p2[0])/2, (edge.p1[1] + edge.p2[1])/2)
    perpendicular = Line.perpendicularLine(edge,edgecenter)

    #creating test point
    testp = (edgecenter[0] + alpha, perpendicular.m * (edgecenter[0] + alpha) + perpendicular.b)

    #creting direction vector
    vector = np.asarray([(edgecenter[0] - testp[0]),(edgecenter[1] - testp[1])])
    vector  = (vector / np.linalg.norm(vector))*30
        
    if cv2.pointPolygonTest(contour,testp,False) < 0:
        vector *= -1

    return tuple(map(int,edgecenter)), vector

def offsetLines(contour,edges,dist):
    lines = []
    for e in edges:
        _, vector = directionVector(e, contour)
        #endpoint = (int(edgecenter[0]+vector[0]),int(edgecenter[1]+vector[1]))
        lines.append(Line.offsetLine(e, dist, vector))

    return lines


def linesIntersectionContour(lines):
    #offsetContour = np.array
    offsetContour = []
    for i,_ in enumerate(lines):
        #linking last line to first
        index = i+1 if i < (len(lines) - 1) else 0
        cross = Line.findIntersetion(lines[i],lines[index])
        np.append(offsetContour, [cross])
        offsetContour.append(np.array([cross[0],cross[1]]).astype(int))
    offsetContour.insert(0,offsetContour.pop())
    return np.asarray(offsetContour)

def offsetPointCloud(contour, lines, dist):
    return linesIntersectionContour(offsetLines(contour,lines,dist))

def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a

def test():
    from rvs.vs.contour_operations import loadContour, cart2pol, getCentroid

    white = (255,255,255)
    image = np.zeros((300,300,3),dtype='uint8')

    contour = loadContour("/home/pi/rvs-git/rvs/resources/dog_contour.data")

    #rearanging contour !!!!!!!!
    idx = np.where(contour == minDistance(contour[:,0],(0,0)))[0][0]
    idxs = arrangeIdxs(idx, len(contour))

    contour = contour[idxs]

    cv2.drawContours(image, [contour], -1, white, 3)

    edges = getEdgesFromPoints(np.asarray(contour[:,0]))

    offsetContour = offsetPointCloud(contour, edges, 10)
    #lines = offsetLines(contour, edges, 10)
    #offsetContour = linesIntersectionContour(lines)

    #offsetContour = np.array(offsetContour)[:,np.newaxis,:]
    #cv2.drawContours(image, [offsetContour], -1, (255,0,0), 3)

    #sorting by angle
    M = cv2.moments(contour)
    cx, cy = getCentroid(M)

    #offsetContour_norm = offsetContour - [cx,cy]
    #print(offsetContour_norm)

    #offsetContour_norm = sorted(offsetContour_norm, key=cart2pol, reverse= True)

    #offsetContour = np.asarray(offsetContour_norm) + [cx,cy]

    for i,point in enumerate(offsetContour):
        image = cv2.circle(image, tuple(point), 5, white, -1)
        cv2.putText(image, str(i), (point[0] - 20, point[1] - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)




    cv2.imshow("image",image)
    cv2.waitKey(0)




    

if __name__ == ("__main__"):
    test()