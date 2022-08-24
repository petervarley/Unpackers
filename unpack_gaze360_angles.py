import sys
import os
import numpy as np
import scipy.io

#--------------------------------------------------------------------------------------

import math

def distance_calculation(e,t):
	dx = float(e[0])-float(t[0])
	dy = e[1]-t[1]
	dz = e[2]-t[2]
	return math.sqrt(dx*dx+dy*dy+dz*dz)

#--------------------------------------------------------------------------------------
# Create two text files, in which the data looks like:
# Metadata:
# 000 000015 000001 -0.32729897748259296 -0.12690680766267312 4.284811938335886
# List:
# Gaze360/gaze360_dataset/imgs/rec_000/head/000015/000001.jpg -0.32729897748259296 -0.12690680766267312
#
# It is the responsibility of the unpacker to ensure that yaw is +ve to the subject's right, and pitch is +ve upwards
# Sign checks for Gaze360:
# 000 000015 000001: the subject is definitely looking to his left and down, so yaw should be -ve and pitch should be -ve

def unpack_gaze360_metadata (pathname):
	# https://docs.scipy.org/doc/scipy/reference/tutorial/io.html
	metadata_file = open(os.path.join(pathname,'metadata_gaze360.txt'),'w')
	list_file = open(os.path.join(pathname,'list_gaze360.txt'),'w')

	matlab_file = scipy.io.loadmat(os.path.join(pathname,'gaze360_dataset','metadata.mat'))

	recording = matlab_file['recording']
	frame = matlab_file['frame']
	person_id = matlab_file['person_identity']
	gaze_dir = matlab_file['gaze_dir']
	eyes3D = matlab_file['person_eyes3d']
	target3D = matlab_file['target_pos3d']

	for r in range(0,len(recording)):
		this_recording = recording[r]
		this_frame = frame[r]
		this_person = person_id[r]
		for n in range(0,len(this_recording)):
			# according to the documentation, the eye and target positions are in metres and measured from the camera
			distance = distance_calculation(eyes3D[n],target3D[n])

			this_gaze = gaze_dir[n]
			pitch = np.arcsin(this_gaze[1])
			yaw = np.arctan2(-this_gaze[0],-this_gaze[2])
			print(f'{this_recording[n]:03d} {this_person[n]:06d} {this_frame[n]:06d} {yaw} {pitch} {distance}')
			metadata_file.write(f'{this_recording[n]:03d} {this_person[n]:06d} {this_frame[n]:06d} {yaw} {pitch} {distance}\n')
			rec_person_frame = os.path.join(pathname,'gaze360_dataset','imgs',f'rec_{this_recording[n]:03d}','head',f'{this_person[n]:06d}',f'{this_frame[n]:06d}.jpg')
			list_file.write(f'{rec_person_frame} {yaw} {pitch}\n')

	metadata_file.close()
	list_file.close()

#--------------------------------------------------------------------------------------

if __name__ == "__main__":
	unpack_gaze360_metadata(sys.argv[1])

#--------------------------------------------------------------------------------------
