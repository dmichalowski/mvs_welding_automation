import numpy as np
import cv2
import rvs.point_assignment
from imutils import resize

from rvs.si.alingment.edge import Edge, Vertex, getEdgesFromPoints
from rvs.robot.tool import Tool
from rvs.robot.robot_space import RobotSpace
from rvs.analyze_image import analyze_image
from rvs.si.alingment.line import calculateDistance
from rvs.utils.conf import Conf
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

def drawRow(image, row):
    image = cv2.circle(image, tuple(map(int,row[1])), 5, (0,0,255), -1)
    return image

#[TODO] contour functions to contour operations module

def rearangeContour(contour, point = None, reverse = False):
    #reversing contour (making it cw)
    if reverse:
        contour = contour[::-1]

    #rearanging by given point
    if point is not None:
        idx = np.where(contour == minDistance(contour[:,0],point))[0][0]
        idxs = arrangeIdxs(idx, len(contour))
        contour = contour[idxs]

    return contour

def cutContour(contour):

    indices = [i for (i,v) in enumerate(contour[:,0]) if v[0] > 150]
    contour = np.delete(contour, indices,0)

    return contour
    #a = np.delete(a, indices, 1)

def main():
    verbose_processing = True
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", required = True,
	    help = "Filename for image")
    ap.add_argument("-c", "--config", required = True,
	    help = "Filename for camera calibration data")
    # ap.add_argument("-c", "--calib", required = True,
	#     help = "Filename for camera calibration data")
    args = vars(ap.parse_args())

    image = cv2.imread(args["filename"])
    conf = Conf(args["config"])
    # image = resize(image,width = 800)
    contour,pnts,image = analyze_image(image,conf)

    pnts = [tuple(p) for p in pnts]
    pnts = [p for p in pnts if cv2.pointPolygonTest(contour, p, False) > 0]

    tool = Tool(200)
    robotspace = RobotSpace()
    # #take picture
    white = (255,255,255)
    # image = np.zeros((300,300,3),dtype='uint8')
    # #prepare picture

    # #find Xs
    # pnts = [(73,142),(192,174),(115,135),(232,122),(150,150),(240,70)]

    # #find contour
    # from rvs.vs.detectanddescribe.contour_operations import loadContour
    # import os
    # my_path = os.path.abspath(os.path.dirname(__file__))
    # path = os.path.join(my_path, "resources/dog_contour.data")
    # contour = loadContour(path)

    

    # rearange contour to start closest to (0,0) and in ccw direction
    contour = rearangeContour(contour, (0,0), reverse=False)
    # contour = cutContour(contour)

    cv2.drawContours(image, [contour], -1, white, 3)

    #draw pnts
    for p in pnts:
        image = cv2.circle(image, p, 5, (0,255,0), -1)

    #assign points
    edges, pnts = rvs.point_assignment.assignPointsToEdges(contour,pnts,tool.size)
    vertices, pnts = rvs.point_assignment.assignPointsToVertecies(contour, pnts, tool.size)

    #create offset contour
    from rvs.si.alingment.offset_contour import offsetPointCloud
    offPnts = offsetPointCloud(contour,edges,10)

    #[TODO] zrobic funkcje/klase
    #find alignment points and vectors
        #find alingment for edges
    from rvs.si.alingment.line import Line
    offEdges = getEdgesFromPoints(offPnts)
    for e, offe in zip(edges,offEdges):
        #temp_image = image.copy()
        if(e.weldingPoints):
            perpendicular = Line.perpendicularLine(e,e.weldingPoints[0])
            cross = Line.findIntersetion(offe,perpendicular)
            e.alingmentPoint = np.asarray(cross, dtype = "int")
            vector = np.asarray([e.weldingPoints[0][0] - cross[0],e.weldingPoints[0][1] - cross[1]])
            vector  = (vector / np.linalg.norm(vector))*30
            e.alingmentVector = vector

        #find alingment for vertecies
    for v in vertices:
        if v.weldingPoints:
            v.alingmentPoint = minDistance(offPnts, v.vertex)
            vector = np.asarray([v.weldingPoints[0][0] - v.vertex[0],
                v.weldingPoints[0][1] - v.vertex[1]])
            v.alingmentVector  = (vector / np.linalg.norm(vector))*tool.size
            

    #create path
    from rvs.si.alingment.path import Path,drawRow
    from rvs.vs.detectanddescribe.contour_operations import getCentroid

    #image = cv2.flip(image, 0)
    vertices[:] = [v for v in vertices if v.weldingPoints]
    path = Path(edges,vertices,offPnts,contour[:,0])
    #path.transformToRegularAxis(image.shape[0])
    #path.transformPath(robotspace.offset,robotspace.getRotationMatrix(image.shape[1]/2, image.shape[0]/2))

    #print(path.path)
    #path.showPath(image)

    #print(path.path)
    # for row in path.path:
    #     temp_image = image.copy()
    #     temp_image = drawRow(temp_image,row)
    #     cv2.imshow("path", temp_image)
    #     cv2.waitKey(0)
    #path.displayElements()
    
    
    


    # #show result
    # offEdges = getEdgesFromPoints(offPnts)
    # for e, offe in zip(edges,offEdges):
    #     temp_image = image.copy()
    #     temp_image = e.drawLine(temp_image,white)
    #     temp_image = offe.drawLine(temp_image,white)
    #     cv2.imshow("wut",temp_image)
    #     cv2.waitKey(0)


    #cv2.drawContours(image, [contour], -1, white, 3)

    for i,point in enumerate(offPnts):
        image = cv2.circle(image, tuple(point), 5, white, -1)
        cv2.putText(image, str(i), (point[0] - 20, point[1] - 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    for e in edges:
        #if e.weldingPoints:
        image = e.drawEdge(image)

    for v in vertices:
        if v.weldingPoints:
            image = v.drawVertex(image)

    cv2.imshow("image",image)
    cv2.waitKey(0)


    #send path
    np.savetxt("path.txt",path.path.reshape(path.path.shape[0],6))
    #print(path.path)
    #print(path.path.reshape(path.path.shape[0],6))
    #print(path.path.reshape(path.path.shape[0],6).reshape(path.path.shape[0],3,2))
    #print(path.path.reshape())

if __name__ == '__main__':
    main()