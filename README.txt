This is a collection of unpackers which take metadata from whichever format a particular dataset happens to use
and converts it into an easy-to-read and easy-to-use plain text format.

--------------------------------------------------------------------------

Unpack AFLW2000

One parameter, the pathname of the directory into which AFLW2000 was downloaded, e.g.

python unpack_aflw.py AFLW2000

Produces lists of:
eye centres
nose tips
fixed landmarks (eye centres and nose tips)
eye corners

--------------------------------------------------------------------------

Unpack BioID V1.2

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

One parameter, the pathname of the directory into which CelebA was downloaded, e.g.

python unpack_celeba.py CelebA

Produces lists of:
eye centres
nose tips
fixed landmarks (eye centres and nose tips)

--------------------------------------------------------------------------

Unpack Dlib5

One parameter, the pathname of the directory which contains dlib_faces_5points.train_cleaned.xml, e.g.

python unpack_dlib5.py Dlib/dlib_faces_5points

Produces lists of:
eye centres
noses (BEWARE: this is not the nose tip, it is the base of the septum)
fixed landmarks (eye centres and noses (BEWARE as above))
eye corners

--------------------------------------------------------------------------
