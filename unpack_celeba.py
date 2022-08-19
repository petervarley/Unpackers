import sys
import os

#--------------------------------------------------------------------------------------
# input is of the form:
# filename lefteye_x lefteye_y righteye_x righteye_y nose_x nose_y leftmouth_x leftmouth_y rightmouth_x rightmouth_y
# but the left eye is the right eye, and vice versa

import glob
import os
import math

def unpack_celeba_dataset (pathname):
	landmark_file = open(os.path.join(pathname,'landmark_celeba.txt'),'w')
	eyedata_file = open(os.path.join(pathname,'eyedata_celeba.txt'),'w')
	nosedata_file = open(os.path.join(pathname,'nosedata_celeba.txt'),'w')

	long_pathname = os.path.join(pathname,'img_align_celeba')

	textfile = open(os.path.join(pathname,'list_landmarks_align_celeba.txt'),'r')
	textlines = textfile.readlines()

	for textline in textlines:
		items = textline.split()
		image_name = items[0]
		if image_name.endswith('.jpg'):
			lefteye_x = int(items[1])
			lefteye_y = int(items[2])
			righteye_x = int(items[3])
			righteye_y = int(items[4])
			nose_x = int(items[5])
			nose_y = int(items[6])

			landmark_file.write(f"{long_pathname} {image_name} {righteye_x} {righteye_y} 0 0 {lefteye_x} {lefteye_y} 0 0 {nose_x} {nose_y}\n")
			eyedata_file.write(f"{long_pathname} {image_name} {righteye_x} {righteye_y} 0 0 {lefteye_x} {lefteye_y} 0 0\n")
			nosedata_file.write(f"{long_pathname} {image_name} {nose_x} {nose_y}\n")

	landmark_file.close()
	eyedata_file.close()
	nosedata_file.close()

#--------------------------------------------------------------------------------------

if __name__ == "__main__":
	unpack_celeba_dataset(sys.argv[1])

#--------------------------------------------------------------------------------------
