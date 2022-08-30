import sys
import numpy as np
import scipy.io
import os
import math

#--------------------------------------------------------------------------------------

def distance_calculation(x,y,z):
	return math.sqrt(x*x+y*y+z*z)

def distance_calculation_2eye(rx,ry,rz,lx,ly,lz):
	return (distance_calculation(rx,ry,rz)+distance_calculation(lx,ly,lz))/2

#--------------------------------------------------------------------------------------
# with thanks to ufoym/simgan
# https://github.com/ufoym/simgan/blob/master/utils/mpii_gaze_dataset_organize.py
#
# The items in each line of "annotation.txt" are:
# 0,  1: right eye outside corner
# 2,  3: right upper eyelid centre
# 4,  5: right eye inside corner (? not exact)
# 6,  7: right eye inside corner
# 8,  9: right eye on lower eyelid
#10, 11: right eye where iris meets lower eyelid
#12. 13: left eye inside corner
#14. 15: left upper eyelid centre
#16, 17: left upper eyelid (another point)
#18, 19: left eye outside corner
#20, 21: left eye on lower eyelid
#22, 23: left lower eyelid centre
#24, 25: on-screen gaze target position in screen coordinates
#26, 27, 28: 3D gaze target position related to camera
#29, 30, 31, 32, 33, 34: estimated 3D head pose based on 6 points-based 3D face model, rotation and translation
#35, 36, 37: estimated 3D right eye centre in the camera coordinate system
#38, 39, 40: estimated 3D left eye centre in the camera coordinate system

def unpack_mpiigaze_metadata (pathname):
	landmark_file = open(os.path.join(pathname,'landmark_mpiigaze.txt'),'w')
	metadata_file = open(os.path.join(pathname,'metadata_mpiigaze.txt'),'w')
	list_file = open(os.path.join(pathname,'list_mpiigaze.txt'),'w')

	textlines = None

	for person in range(0,15):
		for day in range(0,100):
			person_day_path = os.path.join(pathname,'Data','Original',f'p{person:02d}',f'day{day:02d}')
			filename = os.path.join(person_day_path,'annotation.txt')
			if os.path.exists(filename):
				textfile = open(filename,'r')
				textlines = textfile.readlines()

			mat_name = os.path.join(pathname,'Data','Normalized',f'p{person:02d}',f'day{day:02d}.mat')
			if os.path.exists(mat_name):
				matlab_file = scipy.io.loadmat(mat_name)

				matlab_data = matlab_file['data']
				matlab_data = matlab_data[0][0]
				#print(type(matlab_data),matlab_data.shape)
				#print(matlab_data)
				python_data = np.asarray(matlab_data[0],np.dtype([('gaze', 'O'), ('image', 'O'), ('pose', 'O')]))
				gaze_data = python_data['gaze']
				gaze_data = gaze_data[0][0]
				images,three = gaze_data.shape

				for image in range(0,images):
					pitch = math.asin(-gaze_data[image][1])
					yaw = math.atan2(-gaze_data[image][0], -gaze_data[image][2])
					print(f'{person:02d} {day:02d} {image:04d} {yaw} {pitch}')

					textline = textlines[image]
					items = textline.split()
					#print(items)

					rex = float(items[35])
					rey = float(items[36])

					distance = distance_calculation_2eye(rex,rey,float(items[37]),float(items[38]),float(items[39]),float(items[40]))/100.0

					metadata_file.write(f'{person:02d} {day:02d} {image:04d} {yaw} {pitch} {distance}\n')
					image_filename = os.path.join(person_day_path,f'{image:04d}.jpg')
					list_file.write(f'{image_filename} {yaw} {pitch}\n')

					rox = float(items[0])
					roy = float(items[1])
					rix = float(items[6])
					riy = float(items[7])

					lox = float(items[18])
					loy = float(items[19])
					lix = float(items[12])
					liy = float(items[13])

					landmark_file.write(f'{person_day_path} {image:04d}.jpg {lix} {min(liy,loy)} {lox-lix+1} {abs(loy-liy)+1} {rox} {min(riy,roy)} {rix-rox+1} {abs(roy-riy)+1}\n')


	landmark_file.close()
	metadata_file.close()
	list_file.close()

#--------------------------------------------------------------------------------------

if __name__ == "__main__":
	unpack_mpiigaze_metadata(sys.argv[1])

#--------------------------------------------------------------------------------------
