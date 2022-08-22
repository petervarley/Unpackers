import sys
import os
import xml.etree.ElementTree as ET

######################################################################

def trim (item):
	return item[1:len(item)-1]

def widval (a,b):
	return (abs(a-b))+1

######################################################################

def unpack_metadata_file (pathname,out_all3,out_eyes,out_nose,out_corner,metadata_filename):
	tree = ET.parse(metadata_filename)
	root = tree.getroot()
	for child in root:
		#print(child.tag, child.attrib)

		if child.tag == 'images':
			#print("Images")
			images_items = ET.tostringlist(child)

			filename = 'no filename'
			got_filename = False
			eyecoords = [0,0,0,0,0,0,0,0]
			nosecoords = [0,0]
			gotnose = neednose = isnose = False
			goteye = needeye = False
			whicheye = 0

			for images_item in images_items:
				#print('*****',images_item)
				items = images_item.split()
				for item in items:
					bits = item.decode('utf-8')

					bit = bits.split('=')
					#print('Item:', bits, got_filename, isnose, neednose, gotnose, needeye, goteye)

					if bit[0] == 'file':
						filename = trim(bit[1])
						#print('File name is ',filename)
						got_filename = True
						neednose = needeye = True
						gotnose = goteye = False
					elif got_filename and (bit[0] == 'name'):
						#print(filename, " name ",bit[1])
						if bit[1] == '"Leye1"':
							whicheye = 0
						elif bit[1] == '"Leye2"':
							whicheye = 1
						elif bit[1] == '"Reye1"':
							whicheye = 2
						elif bit[1] == '"Reye2"':
							whicheye = 3
						elif bit[1] == '"un"':
							isnose = True
						#print('Eye #',whicheye)
					elif got_filename and (bit[0] == 'x'):
						#print(filename, " x ",bit[1])
						if isnose:
							nosecoords[0] = int(trim(bit[1]))
						else:
							eyecoords[whicheye*2] = int(trim(bit[1]))
					elif got_filename and (bit[0] == 'y'):
						#print(filename, " y ",bit[1], got_filename, isnose, neednose, needeye)

						if isnose:
							filebits = filename.split('/')
							nosecoords[1] = int(trim(bit[1]))
							isnose = False
							gotnose = True
						else:
							eyecoords[whicheye*2+1] = int(trim(bit[1]))
							if whicheye == 3:
								filebits = filename.split('/')
								goteye = True

						if gotnose and goteye:
							out_all3.write(f'{pathname}/{filebits[0]} {filebits[1]} {min(eyecoords[0],eyecoords[2])} {min(eyecoords[1],eyecoords[3])} {widval(eyecoords[0],eyecoords[2])} {widval(eyecoords[1],eyecoords[3])} {min(eyecoords[4],eyecoords[6])} {min(eyecoords[5],eyecoords[7])} {widval(eyecoords[4],eyecoords[6])} {widval(eyecoords[5],eyecoords[7])} {nosecoords[0]} {nosecoords[1]}\n')
							out_nose.write(f'{pathname}/{filebits[0]} {filebits[1]} {nosecoords[0]} {nosecoords[1]}\n')
							out_eyes.write(f'{pathname}/{filebits[0]} {filebits[1]} {min(eyecoords[0],eyecoords[2])} {min(eyecoords[1],eyecoords[3])} {widval(eyecoords[0],eyecoords[2])} {widval(eyecoords[1],eyecoords[3])} {min(eyecoords[4],eyecoords[6])} {min(eyecoords[5],eyecoords[7])} {widval(eyecoords[4],eyecoords[6])} {widval(eyecoords[5],eyecoords[7])}\n')
							out_corner.write(f'{pathname}/{filebits[0]} {filebits[1]} {eyecoords[0]} {eyecoords[1]} {eyecoords[2]} {eyecoords[3]} {eyecoords[4]} {eyecoords[5]} {eyecoords[6]} {eyecoords[7]}\n')
							neednose = False
							needeye = False

						if (not neednose) and (not needeye):
							got_filename = False

					else:
						pass

######################################################################
# As well as unpacking eye corner bounding boxes (for use in determing eye centres)
# and nose coordinates (which will require some processing before they can be used as nose tips),
# this file also unpacks eye corners, in case I find a use for them later.

def unpack_dlib5_dataset(pathname):
	out_all3 = open(os.path.join(pathname,'landmark_dlib5.txt'),'w')
	out_eyes = open(os.path.join(pathname,'eyedata_dlib5.txt'),'w')
	out_nose = open(os.path.join(pathname,'nosedata_dlib5.txt'),'w')
	out_corner = open(os.path.join(pathname,'eyecorners_dlib5.txt'),'w')
	unpack_metadata_file(pathname,out_all3,out_eyes,out_nose,out_corner,os.path.join(pathname,'test_cleaned.xml'))
	unpack_metadata_file(pathname,out_all3,out_eyes,out_nose,out_corner,os.path.join(pathname,'train_cleaned.xml'))
	out_all3.close()
	out_eyes.close()
	out_nose.close()
	out_corner.close()

######################################################################

if __name__ == "__main__":
	unpack_dlib5_dataset(sys.argv[1])

######################################################################################
