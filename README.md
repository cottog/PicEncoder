Picture Encoder
==============

This repo is for what I am calling a picture-encoder. It does not encode images, but instead encodes data inside an image.

The picture-encoder hides bytes inside the RGB values of a png image, and then scrambles that image using a password to seed a pseudo-random number generator. This same password can then be used to unscramble the image. Then, the original image can be used to retrieve the originally-encoded string from the RGB values of the newly-unscrambled image.

The goal of this toy project is to explore a form of pseudo-TFA using images. The recipient of an encoded, scrambled image needs both the password (something they know) and the original, non-encoded, non-scrambled image (something they have, in a sense) in order to retrieve the data.

Of course, one of the many weaknesses of this toy example is that all of the data in encoded in adjacent pixels. I am assuming that in most images, large blocks of adjacent pixels are all next to each other. Thus, someone who has an unscrambled, encoded image (they know the password) can obviate the need for the original image by using pixels in proximity to those that have been encoded with data, which are likely the same color. Of course, more RNG, the use of specific image files, or probably many other means could be used to extend this project and protect against this weakness.

#How do I use it?
This is a command-line tool. These instructions assume the current working directory is that which contains the three files in this repo.

##To encode some data in an image
Use the following command:

python Encode.py -i "path/to/inputfile"

This should generate, in the directory which contains the inputfile, two more files, one named "inputfile_encoded.png" and one named "inputfile_scrambled.png". The first file, of course, contains an unscrambled version of the input file, with the data you enter encoded in it. The second contains an encoded and scrambled version of the input file.

##To decode some data from an image
Use the following command:

python Decode.py -c "path/to/encodedfile" -c "path/to/controlfile"

Where the encoded file is the "_scrambled" image from the Encode.py file, and the controlfile is the inputfile used to generate the encodedfile.

Decode.py will print the data you encoded in the image to the console.

In this toy example, the data encoded in the file is an input string entered into the commandline.