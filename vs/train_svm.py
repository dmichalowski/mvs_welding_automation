# USAGE
# python classify.py

# import the necessary packages
from __future__ import print_function
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from joblib import load, dump

import numpy as np
import sklearn
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
	help = "Path to the directory that contains the features and labels")

args = vars(ap.parse_args())

# handle older versions of sklearn
if int((sklearn.__version__).split(".")[1]) < 18:
	from sklearn.cross_validation import train_test_split

# otherwise we're using at lease version 0.18
else:
	from sklearn.model_selection import train_test_split

source = np.loadtxt("/home/pi/rvs-git/rvs/resources/" + args["dataset"], delimiter = ',')
X = source[:,:-1]
print(X.shape)

y = source[:,-1].astype(int)
# print(features)
# print("features", type(features))
# print("labels", type(labels))


# generate the XOR data
# tl = np.random.uniform(size=(100, 2)) + np.array([-2.0, 2.0])
# tr = np.random.uniform(size=(100, 2)) + np.array([2.0, 2.0])
# br = np.random.uniform(size=(100, 2)) + np.array([2.0, -2.0])
# bl = np.random.uniform(size=(100, 2)) + np.array([-2.0, -2.0])
# X = np.vstack([tl, tr, br, bl])
# y = np.hstack([[1] * len(tl), [-1] * len(tr), [1] * len(br), [-1] * len(bl)])

# print("X", type(X))
# print("y",type(y))

# construct the training and testing split by taking 75% of the data for training
# and 25% for testing
(trainData, testData, trainLabels, testLabels) = train_test_split(X, y, test_size=0.25,
	random_state=42)

#train the linear SVM model, evaluate it, and show the results
print("[RESULTS] SVM w/ Linear Kernel")
model = SVC(kernel="linear")
model.fit(trainData, trainLabels)
print(classification_report(testLabels, model.predict(testData)))
print("")

#dump(model, '/home/pi/rvs-git/rvs/resources/zernike9_linear.joblib') 

# train the SVM + poly. kernel model, evaluate it, and show the 
# ‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘precomputed’
print("[RESULTS] SVM w/ Polynomial Kernel")
model = SVC(kernel="poly", degree=2, coef0=1)
model.fit(trainData, trainLabels)
print(classification_report(testLabels, model.predict(testData)))
print(model.kernel)
print("")

print("[RESULTS] SVM w/ RBF Kernel")
model = SVC(kernel="rbf")
model.fit(trainData, trainLabels)
print(classification_report(testLabels, model.predict(testData)))
print("")

print("[RESULTS] SVM w/ Sigmoid Kernel")
model = SVC(kernel="sigmoid")
model.fit(trainData, trainLabels)
print(classification_report(testLabels, model.predict(testData)))
print("")