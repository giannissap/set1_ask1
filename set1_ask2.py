import numpy as np
from scipy.misc import imread, imsave
import sys


def threshold(image, k ):
    return int(np.amin(image) + k*(np.amax(image) -  np.amin(image))/9)

if len(sys.argv)!=2:
    print 'Usage:'+sys.argv[0] +' <filename'
    exit(0)



image = imread(sys.argv[1]).astype(np.float32)

M = image.shape[0]
N = image.shape[1]

for k in range(9):
    thres = threshold(image, k)
    image = imread(sys.argv[1]).astype(np.float32)

    for i in range(M):
        for j in range(N):
            if image[i][j]<=thres:
                image[i][j]=0
            else:
                image[i][j]=255


    imsave(str(thres)+'.png', image)
