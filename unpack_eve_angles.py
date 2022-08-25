import sys
import os
import h5py # Note that this must be version 2.10.0

######################################################################
# Keys

# 'camera_matrix'
# 'camera_transformation'
# 'face_PoG_tobii'
# 'face_R'
# 'face_W'
# 'face_g_tobii'
# 'face_h'
# 'face_o'
# 'facial_landmarks'
# 'head_rvec'
# 'head_tvec'
# 'inv_camera_transformation'
# 'left_PoG_tobii'
# 'left_R'
# 'left_W'
# 'left_g_tobii' looks like one that I want
# 'left_h'
# 'left_o'
# 'left_p'
# 'millimeters_per_pixel'
# 'pixels_per_millimeter'
# 'right_PoG_tobii'
# 'right_R'
# 'right_W'
# 'right_g_tobii' looks like one that I want
# 'right_h'
# 'right_o'
# 'right_p'

######################################################################
# Spot-check for spherical coordinates
# Person 1, video 29, frame 1000, the subject is looking to his left and level; the numbers in the file are (L) -0.20082005858421326 -0.44287097454071045 (R) -0.19676651060581207 -0.42068275809288025
# Person 1, video 29, frame 1094, the subject is looking to his right and down; the numbers in the file are (L) -0.40265062451362610  0.39033263921737670 (R) -0.42259392142295840  0.39250752329826355
#
# I want coordinates yaw +ve to the subject's right, and pitch +ve upwards, in that order
#
# It appears from the code that coordinates are ordered:
# pitch first, theta = -arcsin(y)
# yaw second, phi = arctan2(x,z)
#
# By comparison with the spot check:
# pitch is +ve upwards, which is what I want
# yaw is +ve to the subject's right, which is also what I want
# but the order has to be reversed.

######################################################################

def unpack_eve_frames(metaname,framepath,listfile):
	metadata = h5py.File(metaname,'r+')
	#print(f'Keys: {metadata.keys()}')
	l = metadata['left_g_tobii']
	ld = l['data']
	r = metadata['right_g_tobii']
	rd = r['data']
	for n in range(0,ld.shape[0]):
		listfile.write(f'{framepath} frame{n:03}.png {ld[n][1]} {ld[n][0]} {rd[n][1]} {rd[n][0]}\n')

######################################################################

def unpack_eve_directory(rootpath,copypath,directory,listfile):
	os.makedirs(copypath,exist_ok=True)

	for pathname in os.listdir(os.path.join(rootpath,directory)):
		fullname = os.path.join(rootpath,directory,pathname)

		if os.path.isdir(fullname):
			os.makedirs(os.path.join(copypath,directory),exist_ok=True)
			metaname = os.path.join(rootpath,directory,pathname,'webcam_c.h5')
			framepath = os.path.join(copypath,directory,pathname)
			print('Unpacking: ',framepath)
			unpack_eve_frames(metaname,framepath,listfile)

######################################################################

def unpack_eve_person(rootpath,copypath,which,index):
	midpath = f'{which}{index:02}'
	os.makedirs(os.path.join(copypath,midpath),exist_ok=True)
	listfile = open(os.path.join(copypath,midpath,'metadata.txt'),'w')
	unpack_eve_directory(rootpath,copypath,midpath,listfile)
	listfile.close()

######################################################################

def unpack_eve_angles(frompath,topath):
	for index in range(1,40):
		unpack_eve_person(frompath,topath,'train',index)

	# the test sets don't have ground truths :-O
	#for index in range(1,11):
	#	unpack_eve_person(sys.argv[1],sys.argv[2],'test',index)

	for index in range(1,6):
		unpack_eve_person(frompath,topath,'val',index)

######################################################################

######################################################################################

if __name__ == "__main__":
	unpack_eve_angles(sys.argv[1],sys.argv[2])

######################################################################################
