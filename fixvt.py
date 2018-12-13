# created by atacms, 13/12/2018
# output vt format as observed in WoT 1.3.0.1
# used to fix vt created before 1.3.0

import pdb
#import subprocess
import sys
import argparse
import os
from ctypes import c_long
from struct import unpack
from struct import pack
from glob import glob

class Vertice:
	def __init__(self):
		self.x = None
		self.y = None
		self.z = None
		
parser = argparse.ArgumentParser(description='upgrade vt from pre-1.3.0 format to be used in WoT V1.3.0+')
parser.add_argument('input', help='old vt file path')
parser.add_argument('-o','--output', dest='vt', help='result vt filename')



def main(filename_oldvt):
	filename = os.path.splitext(filename_oldvt)[0]
	filename_vt = '%s.vt.fixed' %filename
	if args.vt != None:
			filename_vt = args.vt
	if not os.path.exists(filename_oldvt):
			print("Failed to find %s" % filename_oldvt)
			sys.exit(1)

	with open(filename_oldvt, 'rb') as mainFP:
		mainFP.seek(4)
		version = unpack('B',mainFP.read(1))[0]
		if version != 1:
			print 'incompatible source vt version: %d' %version
			return
		mainFP.seek(32)
		vcRaw = mainFP.read(4)
			
		with open(filename_vt, 'wb') as vtFP:
				vtFP.write('\x0b\xb0\x0b\xb0\x02\x00\x00\x00')
				mainFP.seek(8)
				vtFP.write(mainFP.read())
				vtFP.write('\x01\x00\x00\x00\x00\x00\x00\x00')
				vtFP.write(vcRaw)
				vtFP.close()
				print 'Done'

		
args = parser.parse_args()
for fname in glob(args.input):
	print('\nprocessing %s' % fname)
	main(fname)

