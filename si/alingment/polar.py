
import numpy as np

def cart2pol(point):
    x = point[0]
    y = point[1]
    theta = np.arctan2(y, x)
    rho = np.hypot(x, y)

    if theta < 0:
        theta += 2*np.pi

    return theta, rho


def pol2cart(theta, rho):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y