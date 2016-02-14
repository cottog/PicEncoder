from PIL import Image
import random
import bitarray
import math
import copy
import os.path

class PicEncoder:
	def __init__(self):
		pass

	def encode(self, inputfile):
		
		(filepath, file_ext) = os.path.splitext(inputfile)
		
		if (file_ext != ".png"):
			print "Please input a .png file."
			return None
			
		filepath_encoded = filepath + "_encoded.png"
		filepath_scrambled = filepath + "_scrambled.png"
		
		user_input = raw_input("What do you want to encode? ")
		
		
		ba = bitarray.bitarray()
		ba.frombytes(user_input)
		
		ba = self.pad_input_string(user_input, ba)
		
		#ensure that ba is a multiple of eight
		ba.fill()
		
		im = Image.open(inputfile,"r")
		(width, height) = im.size
		
		#if there are more bytes than R, G, and B entries, print a warning and return
		if ((ba.length() / 8) + 2) > (width*height*3):
			print("Please find a larger image to encode this much data.")
			return None
		
		#get the pixelaccess object for the image
		im_pixels = im.load()
		
		for i in range(0, ba.length() / 8):
			index = i*8
			curr_int = self.bits_to_int(ba[index:index+8])
			
			curr_pixel = i / 3
			curr_pixel_x = curr_pixel / width
			curr_pixel_y = curr_pixel % width
			
			#XOR the current R, G, or B value with the current byte of data to encode
			rgb_list = list(im_pixels[curr_pixel_x, curr_pixel_y])
			rgb_list[i % 3] = im_pixels[curr_pixel_x, curr_pixel_y][i % 3] ^ curr_int
			im_pixels[curr_pixel_x, curr_pixel_y] = tuple(rgb_list)
		
		im.save(filepath_encoded)
		
		password = raw_input("What password would you like to use? ")
		self.encrypt(im, width, height, password)
		
		
		im.save(filepath_scrambled)
		
		x_range = range(0, width - 1)
		y_range = range(0, height - 1)


	def scramble_columns(self, im,columns,rows):
		pixels =list(im.getdata())

		newOrder=range(columns)     
		random.shuffle(newOrder)            #shuffle

		newpixels=[]
		for i in xrange(rows):
			for j in xrange(columns):
				newpixels+=[pixels[i*columns+newOrder[j]]]

		im.putdata(newpixels)

	def unscramble_columns(self, im,columns,rows):
		pixels =list(im.getdata())

		newOrder=range(columns)     
		random.shuffle(newOrder)            #shuffle

		newpixels=copy.deepcopy(pixels)
		for i in xrange(rows):
			for j in xrange(columns):
				newpixels[i*columns+newOrder[j]]=pixels[i*columns+j]

		im.putdata(newpixels)

	def scramble_rows(self, im,columns,rows):
		pixels =list(im.getdata())

		newOrder=range(rows)        
		random.shuffle(newOrder)            #shuffle the order of pixels

		newpixels=copy.deepcopy(pixels)
		for j in xrange(columns):
			for i in xrange(rows):
				newpixels[i*columns+j]=pixels[columns*newOrder[i]+j]

		im.putdata(newpixels)

	def unscramble_rows(self, im,columns,rows):
		pixels =list(im.getdata())

		newOrder=range(rows)        
		random.shuffle(newOrder)            #shuffle the order of pixels

		newpixels=copy.deepcopy(pixels)
		for j in xrange(columns):
			for i in xrange(rows):
				newpixels[columns*newOrder[i]+j]=pixels[i*columns+j]

		im.putdata(newpixels)


	#set random seed based on the given password
	def set_seed(self, password):
		passValue=0
		for ch in password:                 
			passValue=passValue+ord(ch)
		random.seed(passValue)

	def encrypt(self, im,columns,rows,password):
		self.set_seed(password)
		# scramble(im,columns,rows)
		self.scramble_columns(im,columns,rows)
		self.scramble_rows(im,columns,rows)

	def decrypt(self, im,columns,rows,password):
		self.set_seed(password)
		# unscramble(im,columns,rows)
		self.unscramble_columns(im,columns,rows)
		self.unscramble_rows(im,columns,rows)	
					
	def pad_input_string(self, input_string, input_bits):
		length = len(input_string)
		
		length_string = str(length)

		temp_ba = bitarray.bitarray()
		temp_ba.frombytes(length_string)

		#add eight zeroes to the end of the temp_ba
		temp_ba.append(0)
		temp_ba.fill()
		
		input_bits = temp_ba + input_bits

		return input_bits
		
		
		
	def bits_to_int(self, bits):
		int = 0
		for elem in bits:
			int = (int << 1) | elem
		
		return int

	def decode(self, filepath_encoded, filepath_original):		
		ba = bitarray.bitarray()
		temp_ba = bitarray.bitarray()
		
		encoded_image = Image.open(filepath_encoded)
		orig_image = Image.open(filepath_original)
			
		(width, height) = orig_image.size
		
		password = raw_input("What's the password? ")
		self.decrypt(encoded_image, width, height, password)
		
		encoded_pix = encoded_image.load()  
		orig_pix = orig_image.load()
		
		ba = self.find_length_to_decode(orig_pix, encoded_pix, width, height)
		
		encoded_string_length = ba.tobytes()
		encoded_length = int(encoded_string_length)
		
		encoded_length = encoded_length + len(encoded_string_length) + 1
		
		ba = bitarray.bitarray()
		
		for x in range(0, width):
			for y in range(0, height):
				for r in range(0,3):
					
					if encoded_length == 0:
						return temp
					
					curr_int = encoded_pix[x,y][r] ^ orig_pix[x,y][r]
					
					temp_ba = self.int_to_bits(curr_int)

					ba = ba + temp_ba

					temp = ba.tobytes()

					encoded_length = encoded_length - 1
			

	def find_length_to_decode(self, orig_pix, encoded_pix, width, height):
		
		ba = bitarray.bitarray()
		
		for x in range(0,width):
			for y in range(0, height):
				for r in range(0,3):
					
					curr_int = encoded_pix[x,y][r] ^ orig_pix[x,y][r]
					
					if curr_int == 0:
						return ba
					
					temp_ba = self.int_to_bits(curr_int)

					for i in range(0, 8 - temp_ba.length()):
						ba.append(0)

					ba = ba + temp_ba
					
		return ba
		

	def int_to_bits(self, int):
		ba_temp = bitarray.bitarray()
		
		while int:
			if int & 1 == 1:
				ba_temp.append(1)
			else:
				ba_temp.append(0)
			
			int /= 2

		for i in range(0, 8 - ba_temp.length()):
			ba_temp.append(0)

		ba_temp.bytereverse()
		
		return ba_temp
	
	
#encode()	
#print "Decode"
#stoop = decode()	
#print stoop