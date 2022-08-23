import sys
import os
import h5py # Note that this must be version 2.10.0

######################################################################
# Keys

# 'camera_matrix'
# 'camera_transformation'
# 'face_PoG_tobii', 'face_R', 'face_W'
# 'face_g_tobii', 'face_h', 'face_o'
# 'facial_landmarks'
# 'head_rvec', 'head_tvec'
# 'inv_camera_transformation'
# 'left_PoG_tobii'
# 'left_R'
# 'left_W'
# 'left_g_tobii' looks like one that I want
# 'left_h'
# 'left_o', 'left_p'
# 'millimeters_per_pixel', 'pixels_per_millimeter'
# 'right_PoG_tobii', 'right_R'
# 'right_W'
# 'right_g_tobii' looks like one that I want
# 'right_h'
# 'right_o'
# 'right_p'

######################################################################

def unpack_eve_frames(metaname,framepath,listfile):
	metadata = h5py.File(metaname,'r+')
	#print(f'Keys: {metadata.keys()}')
	l = metadata['left_g_tobii']
	ld = l['data']
	r = metadata['right_g_tobii']
	rd = r['data']
	for n in range(0,ld.shape[0]):
		listfile.write(f'{framepath} frame{n:03}.png {ld[n][0]} {ld[n][1]} {rd[n][0]} {rd[n][1]}\n')

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
