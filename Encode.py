from PicEncoder import PicEncoder
import sys, getopt

def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'Encode.py -i <inputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Encode.py -i <inputfile>'
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
	
	encoder = PicEncoder()
	
	encoder.encode(inputfile)
	
		
if __name__ == "__main__":
	main(sys.argv[1:])
