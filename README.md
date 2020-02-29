# mvs_welding_automation
Creation of a fully autonomous system enabling robot positioning in order to perform spot welds on metal sheets, using image analysis to obtain information about the welded object and the location of markers. Project carried out as part of the diploma thesis.
- design and construction of camera and control system mount,
- image acquisition, processing and analysis using machine learning methods,
- generating a robot motion path,
- creating a module enabling communication with the robot (based on BLE technology)

![raspi mount](/images/mount_rasp.png)

## Computer Vision

Image enchancment was done using morphological operators, canny edge detecion algorithm and contour localization. Contours are filtered using simple contour properties (area, centroid).

Marker detection was developed using zernike/hu moments descriptors and classiffied by Support Vector Machine algorithm.

![communication schematic](/images/image_analysys_example.png)

In order to aquire best accuarcy few descrpitors and svm kernels were tested.

| svm kernel  | hu moments| zernike moments |
| ------------- | ------------- |-------------|
| linear  | 0.77  | 0.95 |
| polynomial (2 deg.)  | 0.84  | 0.28|
| sigmoid  | 0.54  | 0.28|
| rbf  | 0.79  | 0.28|

## Path generation

The problem of the distribution of welding points is decided by assignment their to the nearest edges(no further than the tools can be extended for this). The greatest range of welding electrodes occurs with perpendicular orientation of vector tools to the edges. In this way, the capture of each edge in turn by welding points.

regular edge             |  exception
:-------------------------:|:-------------------------:
![](/images/pathing_1.png)  |  ![](/images/pathing_2.png)

Projection of a point on an edge will only be possible if it is crossed by a straight line in the interval between the points forming it.

To prevent this situation, after assigning points to edges, if some of them have not been assigned, the closest vertices are searched. Points are assigned to them.


## Communication
The generated path must be sent to the robot controller. I decided to use bluetooth communication for this task.

Information sent to controller:
- location of tool point on the X-Y plane,
- tool vector orientation,
- information flag whether a weld should be done at a given point

### Information flow:
Raspberry Pi -> HC-05 -> Arduino -> Robot controller


## Requirements

### Hardware
- Raspberry Pi with BLE
- webcamera
- Arduino or other MCU with UART
- HC-06 bluetooth module
- Power supplies

### Software
- Python 3.4 or later
- [pybluez](https://github.com/pybluez/pybluez)
- OpenCV 3.4 or later
- scikit-learn
- [imutils](https://github.com/jrosebr1/imutils)
