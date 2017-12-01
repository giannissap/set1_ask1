import numpy as np
from scipy.misc import imread, imsave
import sys




if len(sys.argv)!=12 and len(sys.argv)!=28:
    print 'Wrong usage'
    exit(0)

image = imread(sys.argv[1]).astype(np.float32)
if len(sys.argv) == 12:
    linearFilter = [[0 for i in range(3)] for j in range(3)]

    k=3
    for i in range(3):
        for j in range(3):
            linearFilter[i][j] = float(sys.argv[k])
            k = k+1
    new_image = np.zeros(image.shape)
    image = np.pad(image,1,'constant')

    M = new_image.shape[0]
    N = new_image.shape[1]


    for i in range(M):
        for j in range(N):
            for k in range(-1, 2, 1):
                for l in range(-1,2, 1):
                    new_image[i][j] = new_image[i][j] + image[i+k+1][j+l+1]*linearFilter[k+1][l+1]


elif len(sys.argv) == 28:

    k=3
    for i in range(3):
        for j in range(3):
            linearFilter[i][j] = float(sys.argv[k])
            k = k+1

    new_image = np.zeros(image.shape)
    image = np.pad(image,3,'constant')

    M = new_image.shape[0]
    N = new_image.shape[1]


    for i in range(M):
        for j in range(N):
            for k in range(-3, 4, 1):
                for l in range(-3,4, 1):
                    new_image[i][j] = new_image[i][j] + image[i+k+2][j+l+2]*linearFilter[k+2][l+2]


imsave(sys.argv[2], new_image)
