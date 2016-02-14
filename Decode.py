from PicEncoder import PicEncoder
import sys, getopt

def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"he:c:",["efile=","cfile="])
	except getopt.GetoptError:
		print 'Decode.py -e <encodedfile> -c <controlfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Decode.py -c <encodedfile> -c <controlfile>'
			sys.exit()
		elif opt in ("-e", "--efile"):
			encoded = arg
		elif opt in ("-c", "--cfile"):
			control = arg
	encoder = PicEncoder()
	
	output_string = encoder.decode(encoded, control)
	
	print output_string[2:]
		
if __name__ == "__main__":
	main(sys.argv[1:])