######################################################################################
# Unpack AFLW2000 metadata into an easy-to-read and easy-to-use plain text format.
#
# One parameter, the pathname of the directory into which AFLW2000 was downloaded, e.g.
# python unpack_aflw.py AFLW2000
#
# I found this web page helpful:
# https://docs.scipy.org/doc/scipy/reference/tutorial/io.html

import sys
import numpy as np
import scipy.io
import cv2
import os

######################################################################################
# The points are:
#  6: right eye outside corner
#  7: right eye centre
#  8: right eye inside corner
#  9: left eye inside corner
# 10: left eye centre
# 11: left eye outside corner
# 14: nose tip
#
# This version uses the eye centres rather than interpolate between the two corners

REc = 7
LEc = 10
Ntip = 14

def unpack_aflw_dataset (pathname):

	aflw_all3list = open(os.path.join(pathname,'landmark_aflw.txt'),'w')
	aflw_eyelist = open(os.path.join(pathname,'eyedata_aflw.txt'),'w')
	aflw_noselist = open(os.path.join(pathname,'nosedata_aflw.txt'),'w')
	aflw_eyecorners = open(os.path.join(pathname,'eyecorners_aflw.txt'),'w')

	for p in range(0,4500):
		matlab_name = f'{pathname}/image{p:05d}.mat'
		image_name = f'image{p:05d}.jpg'
		if os.path.exists(matlab_name):
			matlab_file = scipy.io.loadmat(matlab_name)

			points = matlab_file['pt2d']
			if (points[0][LEc] > 0) and (points[0][REc] > 0):
				aflw_eyelist.write(f'{pathname} {image_name} {points[0][LEc]} {points[1][LEc]} 0 0 {points[0][REc]} {points[1][REc]} 0 0\n')
			elif (points[0][LEc] > 0):
				aflw_eyelist.write(f'{pathname} {image_name} {points[0][LEc]} {points[1][LEc]} 0 0 -1 -1 0 0\n')
			elif (points[0][REc] > 0):
				aflw_eyelist.write(f'{pathname} {image_name} -1 -1 0 0 {points[0][REc]} {points[1][REc]} 0 0\n')

			aflw_eyecorners.write(f'{pathname} {image_name} {points[0][LEc+1]} {points[1][LEc+1]} {points[0][LEc-1]} {points[1][LEc-1]} {points[0][REc-1]} {points[1][REc-1]} {points[0][REc+1]} {points[1][REc+1]}\n')

			if (points[0][Ntip] > 0):
				aflw_noselist.write(f'{pathname} {image_name} {points[0][Ntip]} {points[1][Ntip]}\n')

			if (points[0][LEc] > 0) and (points[0][REc] > 0) and (points[0][Ntip] > 0):
				aflw_all3list.write(f'{pathname} {image_name} {points[0][LEc]} {points[1][LEc]} 0 0 {points[0][REc]} {points[1][REc]} 0 0 {points[0][Ntip]} {points[1][Ntip]}\n')

	aflw_all3list.close()
	aflw_eyelist.close()
	aflw_noselist.close()
	aflw_eyecorners.close()

######################################################################################

if __name__ == "__main__":
	unpack_aflw_dataset(sys.argv[1])

######################################################################################
