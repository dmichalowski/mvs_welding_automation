import numpy as np
from time import sleep

from bt.bt import BT
from utils.conf import Conf

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--config", required = True, help = "Filename for camera calibration data")
args = vars(ap.parse_args())

conf = Conf(args["config"])

#bt_connection = BT(conf["address"],conf["port"])
path = np.loadtxt("resources/path_files/"+conf["path_file"])

for row in path:
    print("x :", row[2])
    print("y :", row[3])
    print("rot :", row[2])
    
    print("weld :",row[0])