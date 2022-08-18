import sys
import os

#--------------------------------------------------------------------------------------
# input is of the form:
#version: 1
#n_points: 20
#{
#159.128 108.541  -- right pupil
#230.854 109.176  -- left pupil
#164.841 179.633
#223.237 178.998
#132.469 93.9421
#183.883 94.5768
#211.177 95.2116
#254.974 91.4031
#129.295 109.176
#144.529 109.811  -- right eye outside corner
#176.901 107.272  -- right eye inside corner
#216.89 107.272  -- left eye inside corner
#246.088 110.445  -- left eye outside corner
#261.957 109.811
#196.578 139.009  -- nose tip
#184.518 147.261
#207.369 145.991
#195.943 175.189
#193.404 193.597
#192.769 229.143
#}

# eye region centres are determined by averaging the corner points

import glob
import os
import math

def unpack_bioid_dataset (pathname):
	eyecorners_file = open(os.path.join(pathname,'eyecorners_bioid.txt'),'w')
	eyedata_file = open(os.path.join(pathname,'eyedata_bioid.txt'),'w')
	nosedata_file = open(os.path.join(pathname,'nosedata_bioid.txt'),'w')
	landmark_file = open(os.path.join(pathname,'landmark_bioid.txt'),'w')
	pupildata_file = open(os.path.join(pathname,'pupildata_bioid.txt'),'w')
	altmark_file = open(os.path.join(pathname,'altmark_bioid.txt'),'w')

	long_pathname = os.path.join(pathname,'BioID-FaceDatabase-V1.2')
	data_pathname = os.path.join(pathname,'points_20')

	for id in range(0,1521):
		textfile = open(os.path.join(data_pathname,f'bioid_{id:04}.pts'),'r')
		textlines = textfile.readlines()

		rightpupil = textlines[3].split()
		rightpupil_x = float(rightpupil[0])
		rightpupil_y = float(rightpupil[1])

		leftpupil = textlines[4].split()
		leftpupil_x = float(leftpupil[0])
		leftpupil_y = float(leftpupil[1])

		rightoc = textlines[12].split()
		rightoc_x = float(rightoc[0])
		rightoc_y = float(rightoc[1])

		rightic = textlines[13].split()
		rightic_x = float(rightic[0])
		rightic_y = float(rightic[1])

		leftic = textlines[14].split()
		leftic_x = float(leftic[0])
		leftic_y = float(leftic[1])

		leftoc = textlines[15].split()
		leftoc_x = float(leftoc[0])
		leftoc_y = float(leftoc[1])

		lefteye_x = (leftic_x+leftoc_x)/2
		lefteye_y = (leftic_y+leftoc_y)/2
		righteye_x = (rightic_x+rightoc_x)/2
		righteye_y = (rightic_y+rightoc_y)/2

		nosetip = textlines[17].split()
		nosetip_x = float(nosetip[0])
		nosetip_y = float(nosetip[1])

		bridge_x = (lefteye_x+righteye_x+nosetip_x)/3
		bridge_y = (lefteye_y+righteye_y)/2

		image_name = f'bioid_{id:04}.pgm'
		eyecorners_file.write(f'{long_pathname} {image_name} {leftoc_x} {leftoc_y} {leftic_x} {leftic_y} {rightoc_x} {rightoc_y} {rightic_x} {rightic_y}\n')
		eyedata_file.write(f"{long_pathname} {image_name} {righteye_x} {righteye_y} 0 0 {lefteye_x} {lefteye_y} 0 0\n")
		nosedata_file.write(f"{long_pathname} {image_name} {nosetip_x} {nosetip_y}\n")
		landmark_file.write(f"{long_pathname} {image_name} {righteye_x} {righteye_y} 0 0 {lefteye_x} {lefteye_y} 0 0 {nosetip_x} {nosetip_y}\n")
		pupildata_file.write(f"{long_pathname} {image_name} {rightpupil_x} {rightpupil_y} {leftpupil_x} {leftpupil_y} 0 0\n")
		altmark_file.write(f"{long_pathname} {image_name} {rightpupil_x} {rightpupil_y} 0 0 {leftpupil_x} {leftpupil_y} 0 0 {bridge_x} {bridge_y}\n")

	eyecorners_file.close()
	eyedata_file.close()
	nosedata_file.close()
	landmark_file.close()
	pupildata_file.close()
	altmark_file.close()

#--------------------------------------------------------------------------------------

if __name__ == "__main__":
	unpack_bioid_dataset(sys.argv[1])

#--------------------------------------------------------------------------------------
