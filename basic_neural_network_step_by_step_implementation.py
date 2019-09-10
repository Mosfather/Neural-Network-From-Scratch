# -*- coding: utf-8 -*-
"""Basic Neural Network Step By Step Implementation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ao3-_4GTguxckFYAVoNHQ9xuwtC28RR7
"""

#importations
from matplotlib import pyplot as plt
import numpy as np
import cv2
import glob

# model functions

def relu(x):
    return np.maximum(0,x)
    
def sigmoid(x):
    return 1/(1+np.exp(-x))

def relu_derivative(x):
    x[x<=0] = 0
    x[x>0] = 1
    return x

def sigmoid_derivative(x):
    return np.multiply(x,1-x)
    
def initialize_variables(n, NUMBER_OF_LAYERS, LAYERS_DIM):
    
    parameters = {}
    
    for i in range(1, NUMBER_OF_LAYERS):
        W = np.random.randn(LAYERS_DIM[i],LAYERS_DIM[i-1]) * 0.01
        b = np.zeros((LAYERS_DIM[i],1))
        parameters["W"+str(i)] = W
        parameters["b"+str(i)] = b
        
    return parameters

def forward_one_layer(W, b, X, activation = "relu"):
    
    Z = np.dot(W,X) + b
    
    if activation == "relu":
        A = relu(Z)
    elif activation == "sigmoid":
        A = sigmoid(Z)
        
    cache = (W,b,X,Z,A)
        
    return cache
    
def forward_all_layers(X, parameters):
    
    caches = []
    NUMBER_OF_LAYERS = (len(parameters) // 2) + 1
    #print(NUMBER_OF_LAYERS)
    caches.append((None,None,None,None,X))
    
    for i in range(1, NUMBER_OF_LAYERS-1):
        cache = forward_one_layer(parameters["W"+str(i)], parameters["b"+str(i)], caches[i-1][4], "relu")
        caches.append(cache)
        
    cache = forward_one_layer(parameters["W"+str(NUMBER_OF_LAYERS-1)], parameters["b"+str(NUMBER_OF_LAYERS-1)], caches[NUMBER_OF_LAYERS-2][4], "sigmoid")
    caches.append(cache)
    
    return caches
    
        
def calculate_cost(A, Y):
    
    m = A.shape[1]
    
    cost = (-1/m)*(np.sum(np.multiply(Y,np.log(A)) + np.multiply(1-Y,np.log(1-A))))
    return cost

def backward_one_layer(dA, cache, activation = "relu"):
    
    W = cache[0]
    A_prev = cache[2]
    A = cache[4]
    m = A.shape[1]
    
    if activation == "relu": 
        dZ = np.multiply(dA, relu_derivative(A))
    elif activation == "sigmoid":
        dZ = np.multiply(dA, sigmoid_derivative(A))
        
    dW = (1/m)*np.dot(dZ,A_prev.T)
    db = (1/m)*np.sum(dZ,axis=1,keepdims=True)
    dA_prev = np.dot(W.T,dZ)
    
    dcache = (dW, db, dZ, dA_prev)
    
    return dcache
    
def backward_all_layers(Y, caches):
    
    dcaches = []
    dcaches.append((None, None, None, None))
    NUMBER_OF_LAYERS = len(caches)
    A = caches[NUMBER_OF_LAYERS-1][4]
    
    dA = np.divide(1-Y,1-A) - np.divide(Y,A)
    dcache = backward_one_layer(dA, caches[NUMBER_OF_LAYERS-1], activation = "sigmoid")
    dcaches.append(dcache)
    
    for i in range(1, NUMBER_OF_LAYERS-1):
        dA = dcaches[i][3]
        dcache = backward_one_layer(dA, caches[NUMBER_OF_LAYERS - 1 - i], activation = "relu")
        dcaches.append(dcache)
    
    return dcaches
    
def update_parameters(parameters, dcaches, learning_rate = 0.001):
    
    NUMBER_OF_LAYERS = (len(parameters) // 2) + 1
    
    for i in range(1, NUMBER_OF_LAYERS):
        parameters["W"+str(i)] = parameters["W"+str(i)] - learning_rate * dcaches[NUMBER_OF_LAYERS-i][0]
        parameters["b"+str(i)] = parameters["b"+str(i)] - learning_rate * dcaches[NUMBER_OF_LAYERS-i][1]
    
    return parameters

def model(X, Y, m, NUMBER_OF_LAYERS, LAYERS_DIM, num_iterations = 2, learning_rate = 0.001):
    
    parameters = initialize_variables(X.shape[0], NUMBER_OF_LAYERS, LAYERS_DIM)
    costs = []
    iterations = []
    
    for i in range(num_iterations):
        caches = forward_all_layers(X, parameters)
        cost = calculate_cost(caches[NUMBER_OF_LAYERS-1][4], Y)
        if i%1 == 0:
            print("Iteration number : "+ str(i) +"cost is : " + str(cost))
            costs.append(cost)
            iterations.append(i)
        dcaches = backward_all_layers(Y, caches)
        parameters = update_parameters(parameters, dcaches, learning_rate = 0.001)
        
    plt.plot(iterations, costs)
    plt.show()
    return parameters
    
def predict(X, parameters):
    caches = forward_all_layers(X, parameters)
    Y = caches[len(caches)-1][4]
    Y[Y<=0.5] = 0
    Y[Y>0.5] = 1
    return Y

pathA = "sample/A/*"
pathB = "sample/B/*"
images_orig_A = np.array([cv2.imread(file) for file in glob.glob(pathA)])
images_orig_B = np.array([cv2.imread(file) for file in glob.glob(pathB)])
images_orig = np.concatenate((images_orig_A, images_orig_B))
images_flatten = images_orig/255
print(images_flatten.shape)
images = images_flatten.reshape(images_flatten.shape[0],images_flatten.shape[1]*images_flatten.shape[2]*images_flatten.shape[3]).T
print(images.shape)
Y_A = np.ones((1,images_orig_A.shape[0]))
Y_B = np.zeros((1,images_orig_B.shape[0]))
Y = np.concatenate((Y_A, Y_B), axis=1)
print(Y.shape)

parameters = None
parameters = model(images, Y, images.shape[1], 4, [images.shape[0], 5, 2, 1], 20000, 1.2)

pathTest = "sample/Test/*"
test_set_orig = np.array([cv2.imread(file) for file in glob.glob(pathTest)])
test_set_flatten = test_set_orig/255
test_set = test_set_flatten.reshape(test_set_flatten.shape[0],test_set_flatten.shape[1]*test_set_flatten.shape[2]*test_set_flatten.shape[3]).T
print(test_set.shape)

results = predict(test_set, parameters)
print(results)

