'''
The code is from:
http://www.juddzone.com/ALGORITHMS/least_squares_3D_ellipsoid.html

The link was found in post at:
https://stackoverflow.com/questions/58501545/python-fit-3d-ellipsoid-oblate-prolate-to-3d-points

Some information on same method available in some paper at this link:
https://www.scielo.br/j/bcg/a/QLYFKckKMmxdPvTYD67dzRC/


'''

import numpy as np
from numpy.linalg import eig, inv
import math

def ls_ellipsoid(xx,yy,zz):

   x = xx[:,np.newaxis]
   y = yy[:,np.newaxis]
   z = zz[:,np.newaxis]

   J = np.hstack((x*x,y*y,z*z,x*y,x*z,y*z, x, y, z))
   K = np.ones_like(x)

   JT=J.transpose()
   JTJ = np.dot(JT,J)
   InvJTJ=np.linalg.inv(JTJ)
   ABC= np.dot(InvJTJ, np.dot(JT,K))

   eansa=np.append(ABC,-1)

   return (eansa)


def polyToParams3D(vec):

   Amat=np.array(
   [
   [ vec[0],     vec[3]/2.0, vec[4]/2.0, vec[6]/2.0 ],
   [ vec[3]/2.0, vec[1],     vec[5]/2.0, vec[7]/2.0 ],
   [ vec[4]/2.0, vec[5]/2.0, vec[2],     vec[8]/2.0 ],
   [ vec[6]/2.0, vec[7]/2.0, vec[8]/2.0, vec[9]     ]
   ])

   A3=Amat[0:3,0:3]
   A3inv=inv(A3)
   ofs=vec[6:9]/2.0
   center=-np.dot(A3inv,ofs)
   
   Tofs=np.eye(4)
   Tofs[3,0:3]=center
   R = np.dot(Tofs,np.dot(Amat,Tofs.T))

   R3=R[0:3,0:3]
   R3test=R3/R3[0,0]
   s1=-R[3, 3]
   R3S=R3/s1
   (el,ec)=eig(R3S)

   recip=1.0/np.abs(el)
   axes=np.sqrt(recip)

   inve=inv(ec)
#    print(f"Center at: {center} Axes are {axes} Rotation matrix: {inve}")
   print("\n")
   return (center,axes,inve)

def parsefile(filename):
    with open(filename, "r") as my_file:
        data = my_file.read()
    new_data = data.replace('\n', ' ').replace('\t', ' ')
    list_data = new_data.split(" ")
    max_idx = len(list_data)
    arr_data = np.array(list_data, dtype=np.float32)
    arr1 = arr_data[0:max_idx:3]
    arr2 = arr_data[1:max_idx:3]
    arr3 = arr_data[2:max_idx:3]
    return arr1, arr2, arr3

cfiles = ["calibdata4_circles.txt", "pdata_calib4.txt", "data_lawn.txt", "data_lawn_table3.txt"]
vx, vy, vz = parsefile(cfiles[0])

eansa            = ls_ellipsoid(vx, vy, vz) #get ellipsoid polynomial coefficients
# print("coefficients:"  , eansa)
center,axes,inve = polyToParams3D(eansa)   #get ellipsoid 3D parameters
print("center:"        , center)
print("axes:"          , axes)
# print("rotationMatrix:", inve)

R = inve
yaw=math.atan2(R[1,0],R[0,0])
pitch=math.atan2(-R[2,0],math.sqrt(math.pow(R[2,1],2)+math.pow(R[2,2],2)))
roll=math.atan2(R[2,1],R[2,2])

print("angles:", math.degrees(roll), math.degrees(pitch), math.degrees(yaw))