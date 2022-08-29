import sys
import os

#--------------------------------------------------------------------------------------
# Create two text files, in which the data looks like:
# Metadata:
# 001 011665 -0.577460921894 -0.417485326846 1.82
# 001 014386 0.385355773193 -0.274458644766 1.82
# List:
# RT-GENE\rtgene_dataset\s001_glasses\inpainted\face\face_011665_rgb.png -0.577460921894 -0.417485326846
# RT-GENE\rtgene_dataset\s001_glasses\inpainted\face\face_014386_rgb.png 0.385355773193 -0.274458644766
#--------------------------------------------------------------------------------------
# Spot-check for spherical coordinates
# Session s001, frame 011665, the subject is looking to the left and down
# Session s001, frame 014386, the subject is looking to the right and level
#--------------------------------------------------------------------------------------

def find_rtgene_eyes(pathname,metadata_file,list_file,index,count):

	textname = os.path.join(pathname,f's{index:03d}_glasses','label_combined.txt')
	textfile = open(textname,'r')

	for num in range(0,count):
		facepath_png = os.path.join(pathname,f's{index:03d}_glasses','inpainted','face',f'face_{num:06d}_rgb.png')

		if os.path.exists(facepath_png):
			textline = textfile.readline()
			textdata = textline.split('[')
			textdata = textdata[1].split()
			yaw = float(textdata[0].split(',')[0])
			pitch = float(textdata[1].split(']')[0])
			distance = 1.82 # mean, the range is 0.5 to 2.9

			list_file.write(f'{facepath_png} {yaw} {pitch}\n')
			metadata_file.write(f'{index:03d} {num:06d} {yaw} {pitch} {distance}\n')
			print(f'{index:03d} {num:06d} {yaw} {pitch} {distance}')

	textfile.close()

#--------------------------------------------------------------------------------------

def read_all_rtgene_eyes (pathname):
	metadata_file = open(os.path.join(pathname,'metadata_rtgene.txt'),'w')
	list_file = open(os.path.join(pathname,'list_rtgene.txt'),'w')

	find_rtgene_eyes(pathname,metadata_file,list_file,0,11552)
	find_rtgene_eyes(pathname,metadata_file,list_file,1,14417)
	find_rtgene_eyes(pathname,metadata_file,list_file,2,9704)
	find_rtgene_eyes(pathname,metadata_file,list_file,3,14417)
	find_rtgene_eyes(pathname,metadata_file,list_file,4,9836)
	find_rtgene_eyes(pathname,metadata_file,list_file,5,6684)
	find_rtgene_eyes(pathname,metadata_file,list_file,6,17721)
	find_rtgene_eyes(pathname,metadata_file,list_file,7,9056)
	find_rtgene_eyes(pathname,metadata_file,list_file,8,11436)
	find_rtgene_eyes(pathname,metadata_file,list_file,9,12909)
	find_rtgene_eyes(pathname,metadata_file,list_file,10,18553)
	find_rtgene_eyes(pathname,metadata_file,list_file,11,15674)
	find_rtgene_eyes(pathname,metadata_file,list_file,12,3199)
	find_rtgene_eyes(pathname,metadata_file,list_file,13,17574)
	find_rtgene_eyes(pathname,metadata_file,list_file,14,8949)
	find_rtgene_eyes(pathname,metadata_file,list_file,15,10056)
	find_rtgene_eyes(pathname,metadata_file,list_file,16,12049)

	metadata_file.close()
	list_file.close()

#--------------------------------------------------------------------------------------

if __name__ == "__main__":
	read_all_rtgene_eyes(sys.argv[1])

#--------------------------------------------------------------------------------------
