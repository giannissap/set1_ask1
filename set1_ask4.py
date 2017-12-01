import numpy as np
from scipy.misc import imread, imsave
from math import *
import sys



if len(sys.argv) != 10:
     print "Wrong usage!"
     exit(0)

image = imread(sys.argv[1]).astype(np.float32)
M = image.shape[0]
N = image.shape[1]
transform = [[0,0,0],[0,0,0] ,[0,0,0]]
k = 3
for i in range(2):
    for j in range(3):
        transform[i][j] = float(sys.argv[k])
        k = k+1

transform[2][0] = 0
transform[2][1] = 0
transform[2][2] = 1
transform = [[1/2.0,-2.0/3,0],
     [2.0/3,1/2.0,0],
     [0,0,1]]


new_image = np.zeros(image.shape)
interpolatePoints = np.zeros(image.shape)+1

grid = np.zeros((3,M*N))
k=0
for i in range(-int(M/2),int(M/2)+1,1):
    for j in range(-int(N/2),int(N/2)+1,1):

        grid[0][k]=i
        grid[1][k]=j
        grid[2][k]=1
        k=k+1

newGrid = np.dot(transform, grid)

for i in range(len(newGrid[0])):
    if newGrid[0][i].is_integer() and newGrid[1][i].is_integer():
        if int(newGrid[0][i])+M/2>=0 and int(newGrid[0][i])+M/2<M and int(newGrid[1][i])+M/2<0 and int(newGrid[1][i])+M/2<N:
            new_image[int(newGrid[0][i])+M/2][int(newGrid[1][i])+M/2] =  image[int(grid[0][i])+M/2][int(grid[1][i])+M/2]
            interpolatePoints[int(newGrid[0][i])+M/2][int(newGrid[1][i])+M/2] = 0


if sys.argv[9]=='neighbor':
    print(M)
    for i in range(-int(M/2),int(M/2)+1,1):
        for j in range(-int(N/2),int(M/2)+1,1):
            if interpolatePoints[i+M/2][j+M/2] == 1:

                minD = sqrt(pow(i-newGrid[0][0],2)+pow(j-newGrid[1][0],2));
                minPos = 0

                for k in range(len(newGrid[0])):
                    if sqrt(pow(i-newGrid[0][minPos],2)+pow(j-newGrid[1][minPos],2)) > sqrt(pow(i-newGrid[0][k],2)+pow(j-newGrid[1][k],2)):
                        minPos = k
                new_image[i+M/2][j+M/2] =  image[int(grid[0][minPos])+M/2][int(grid[1][minPos])+M/2]
else:
    for i in range(-int(M/2),int(M/2)+1,1):
        for j in range(-int(N/2),int(M/2)+1,1):
            if interpolatePoints[i+M/2][j+M/2] == 1:
                minPosArray = [0,1,2,3]
                minDistArray = [0,0,0,0]
                for k in minPosArray:
                    minDistArray[k] = sqrt(pow(i-newGrid[0][k],2)+pow(j-newGrid[1][k],2))

                for k in range(len(newGrid[0])):

                    if max(minDistArray) > sqrt(pow(i-newGrid[0][k],2)+pow(j-newGrid[1][k],2)):
                        posMax = minDistArray.index(max(minDistArray))
                        minPosArray[posMax] = k
                        minDistArray[minDistArray.index(max(minDistArray))] = sqrt(pow(i-newGrid[0][k],2)+pow(j-newGrid[1][k],2))

                x0 = int(newGrid[0][minPosArray[0]])+M/2
                y0 = int(newGrid[1][minPosArray[0]])+M/2

                x1 = int(newGrid[0][minPosArray[1]])+M/2
                y1 = int(newGrid[1][minPosArray[1]])+M/2

                x2 = int(newGrid[0][minPosArray[2]])+M/2
                y2 = int(newGrid[1][minPosArray[2]])+M/2

                x3 = int(newGrid[0][minPosArray[3]])+M/2
                y3 = int(newGrid[1][minPosArray[3]])+M/2

                A = [[1, x0, y0, x0*y0],
                    [1, x1, y0, x1*y0],
                    [1, x0, y1, x0*y1],
                    [1, x1, y1, x1*y1]]
                b = [0, 0, 0, 0]

                b[0] = image[x0][y0]
                b[1] = image[x1][y0]
                b[2] = image[x0][y1]
                b[3] = image[x1][y1]
                if abs(np.linalg.det(A))<7:
                    minPos=minPosArray[minDistArray.index(min(minDistArray))]
                    new_image[i+M/2][j+M/2] = image[int(grid[0][minPos])+M/2][int(grid[1][minPos])+M/2]
                else:



                    if abs(np.linalg.det(A))<5:
                        minPos=minPos[minDistArray.index(min(minDistArray))]
                        new_image[i+M/2][j+M/2] = image[int(grid[0][minPos])+M/2][int(grid[1][minPos])+M/2]
                    else:
                        x = np.linalg.solve(A,b)
                        new_image[i+M/2][j+M/2] = x[0] + x[1]*(i+M/2) + x[2]*(j+M/2)+x[3]*(i+M/2)*(j+M/2)
imsave(sys.argv[2], new_image)
