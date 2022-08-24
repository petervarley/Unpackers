This is a collection of unpackers which take metadata from whichever format a particular dataset happens to use
and converts it into an easy-to-read and easy-to-use plain text format.

--------------------------------------------------------------------------

Unpack AFLW2000
Find AFLW2000 at: http://www.cbsr.ia.ac.cn/users/xiangyuzhu/projects/3DDFA/main.htm

One parameter, the pathname of the directory into which AFLW2000 was downloaded, e.g.

python unpack_aflw.py AFLW2000

Produces lists of:
eye centres
nose tips
fixed landmarks (eye centres and nose tips)
eye corners

NOTES:

You don't always get 2000 landmarks in each list, as some landmarks are not visible in some images.

--------------------------------------------------------------------------

Unpack BioID V1.2
Find BioID at: https://www.bioid.com/facedb/

One parameter, the pathname of the directory into which BioID was downloaded, e.g.

python unpack_bioid.py BioID

Produces lists of:
eye centres
nose tips
fixed landmarks (eye centres and nose tips)
eye corners
eye pupils
alternative landmarks (eye pupils and nose bridges)

--------------------------------------------------------------------------

Unpack CelebA
Find CelebA at: https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html

One parameter, the pathname of the directory into which CelebA was downloaded, e.g.

python unpack_celeba.py CelebA

Produces lists of:
eye centres
nose tips
fixed landmarks (eye centres and nose tips)

--------------------------------------------------------------------------

Unpack Dlib5
Find Dlib5 at: https://github.com/davisking/dlib-models and follow the link for "dlib 5-point face landmark dataset"

One parameter, the pathname of the directory which contains dlib_faces_5points.train_cleaned.xml, e.g.

python unpack_dlib5.py Dlib/dlib_faces_5points

Produces lists of:
eye centres
noses (BEWARE: this is not the nose tip, it is the base of the septum)
fixed landmarks (eye centres and noses (BEWARE as above))
eye corners

--------------------------------------------------------------------------

Unpack EVE gaze angles
Find EVE at: https://ait.ethz.ch/projects/2020/EVE/ (the dataset is available on request, but you have to fill in a form)

Two parameters:
1. source: the pathname of the top-level directory which contains the downloaded EVE dataset
2. destination: the pathname of the top-level directory which will eventually contain extracted and processed EVE images (the unpacker will create this, and it will have the same tree structure as the source)

e.g.

python unpack_eve_angles.py EVE/eve_dataset EVE/eve_unpacked

Produces lists of gaze angles (left eye yaw and pitch, right eye yaw and pitch)
There will be one such list, "metadata.txt", in each person-level directory of the destination directory tree,
and it will list each frame of each video "webcam_c.mp4" in subdirectories of corresponding location in the source directory tree.

NOTES:

This unpacker does not extract the frames from the video.
There will be separate tools for that, as extracted image data will be application-specific,
whereas extracted metadata is application-agnostic.

This unpacker requires version 2.10.0 of h5py, so may not run in your usual environment.

--------------------------------------------------------------------------

Unpack Gaze360 gaze angles
Find Gaze360 at: http://gaze360.csail.mit.edu/index.php (registration is required)

One parameter, the pathname of the directory into which Gaze360 was downloaded
(which should contain a subfolder named gaze360_dataset), e.g.

python unpack_gaze360_angles.py Gaze360

Produces two output files, which contain essentially the same information in different formats:
[recording number] [person id] [image base filename excluding path] [yaw] [pitch] [distance]
[image full filename including path] [yaw] [pitch]

--------------------------------------------------------------------------
