import sys
import os
import scipy.io
import cv2

#--------------------------------------------------------------------------------------
# Create two text files, in which the data looks like:
# Metadata:
# 01 A 1 0000 0.12391766303967348 -0.15204414389979226 0.9
# List:
# /Pathname/GEDDnet/NISLGaze/p01/A1_0000.png 0.12391766303967348 -0.15204414389979226
#
# Unusually, the images themselves also have to be unpacked from the MATLAB file
#
# It is the responsibility of the unpacker to ensure that yaw is +ve to the subject's right, and pitch is +ve upwards
# Sign checks for NISLGaze:
# A1_0008: the subject is definitely looking to her left and down, so yaw should be +ve and pitch should be -ve
# A1_0027: the subject is definitely looking to her left and down, so yaw should be +ve and pitch should be -ve
#
# To avoid FAT32 problems with large directories and long filenames,
# crunch the filename down so that (for example) p01_loc1 becomes A1, and p21_loc9 becomes U9.
#--------------------------------------------------------------------------------------
# Spot-check for spherical coordinates
# Person 2, session 3, frame 0727, the subject is looking to his right and down
# Person 2, session 3, frame 1199, the subject is looking to his left and up
# Person 2, session 3, frame 2275, the subject is looking to his left and down
#
# It appears that yaw and pitch, although both signed correctly, are the wrong way round
#--------------------------------------------------------------------------------------

alphabet = "-ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def unpack_nislgaze_dataset (pathname):
	# https://docs.scipy.org/doc/scipy/reference/tutorial/io.html
	distance = 0.9 # according to the paper, distance was held constant at 90 cm, although the web site says 95 cm

	metadata_file = open(os.path.join(pathname,'metadata_nislgaze.txt'),'w')
	list_file = open(os.path.join(pathname,'list_nislgaze.txt'),'w')

	for p in range(1,22):
		for loc in range(1,10):
			print(p,loc)
			image_path = os.path.join(pathname,f'p{p:02d}')

			matlab_name = os.path.join(image_path,f'p{p:02d}_loc{loc:01d}.mat')
			matlab_file = scipy.io.loadmat(matlab_name)
			#print(matlab_file.keys())

			frame = matlab_file['face_img']
			gaze_dir = matlab_file['gaze_dirs']

			print(matlab_name,len(frame),len(gaze_dir))

			for r in range(0,len(frame)):
				this_frame = frame[r]

				image_filename = os.path.join(image_path,f'{alphabet[p]}{loc:01d}_{r:04d}.png')
				cv2.imwrite(image_filename,cv2.cvtColor(this_frame, cv2.COLOR_RGB2BGR))

				this_gaze = gaze_dir[r]
				yaw = gaze_dir[r][1]
				pitch = gaze_dir[r][0]
				metadata_file.write(f'{p:02d} {alphabet[p]} {loc:01d} {r:04d} {yaw} {pitch} {distance}\n')
				list_file.write(f'{image_filename} {yaw} {pitch}\n')

	metadata_file.close()
	list_file.close()

#--------------------------------------------------------------------------------------

if __name__ == "__main__":
	unpack_nislgaze_dataset(sys.argv[1])

#--------------------------------------------------------------------------------------
