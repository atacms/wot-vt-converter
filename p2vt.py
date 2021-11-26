# created by atacms, 13/12/2018
# output vt format as observed in WoT 1.3.0.1
# tested with input primitives created by BW indie 2.1

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
		
parser = argparse.ArgumentParser(description='Extract bsp from BigWorld primitives file and dump to vt.')
parser.add_argument('input', help='primitives file path')
parser.add_argument('-o','--output', dest='vt', help='result vt filename')



def main(filename_primitive):
	filename = os.path.splitext(filename_primitive)[0]
	filename_vt = '%s.vt' %filename
	if args.vt != None:
			filename_vt = args.vt
	if not os.path.exists(filename_primitive):
			print("Failed to find %s" % filename_primitive)
			sys.exit(1)

	with open(filename_primitive, 'rb') as mainFP:
		mainFP.seek(-4, 2)
		table_start = unpack('i', mainFP.read(4))[0]
		mainFP.seek(- 4 - table_start, 2)
		sections = {}

		position = 4
		sub_groups = 0

		#
		#read section table
		#
		while True:		
			data = mainFP.read(4)
			if data == None or len(data) != 4:
				break
			
			section_size = unpack('I', data)[0]
			
			#Skip dummy bytes
			data = mainFP.read(16)
			
			data = mainFP.read(4)
			if data == None or len(data) != 4:
				break
			
			section_name_length = unpack('I', data)[0]
			section_name = mainFP.read(section_name_length).decode('UTF-8')
		
			print("Section [ %s ]" % section_name)

			if 'vertices' in section_name:
				sub_groups += 1
		
			section = {
				'position': position,
				'size': section_size,
				'name': section_name
			}
			position += section_size
			if section_size % 4 > 0:
				position += 4 - section_size % 4	#dword alignment
			
			if section_name_length % 4 > 0:			#dword alignment
				mainFP.read(4 - section_name_length % 4)
			
			sections[section_name] = section
			
		#all section table should be loaded by now
		if 'bsp2' in sections:
			mainFP.seek(sections['bsp2']['position']+4)
			faces_count = unpack("I", mainFP.read(4))[0]
#			version = unpack("I", mainFP.read(4))[0]
#			stride = unpack("I", mainFP.read(4))[0]		#DWORDs per face = 10. 
			mainFP.read(8)	#the next 8 bytes might be padding

			print ('faces_count = %d'%faces_count)
#			if version != 2 or stride != 10:
#				print ('unrecognized bsp version, abort')
#				return
			pindex = 0
			vertices = []
			indicies = []
			minx=0
			miny=0
			minz=0
			maxx=0
			maxy=0
			maxz=0
			for i in range(0, faces_count):
				for j in range(0,3):
					vert = Vertice()
					vert.x = unpack('f', mainFP.read(4))[0] 
					vert.y = unpack('f', mainFP.read(4))[0] 
					vert.z = unpack('f', mainFP.read(4))[0] 
					vertices.append(vert)
					indicies.append(pindex)
					pindex += 1
					minx = vert.x if vert.x < minx else minx
					minY = vert.y if vert.y < miny else miny
					minz = vert.z if vert.z < minz else minz
					maxx = vert.x if vert.x > maxx else maxx
					maxy = vert.y if vert.y > maxy else maxy
					maxz = vert.z if vert.z > maxz else maxz
				mainFP.read(4)
			print ('bsp loaded into memory')
#			print vertices
#			print indicies
			print ('reconstructed boundingbox:')
			print (minx, miny, minz)
			print (maxx, maxy, maxz)
			
			with open(filename_vt, 'wb') as vtFP:
				vtFP.write(b'\x0b\xb0\x0b\xb0\x02\x00\x00\x00')
				vtFP.write(pack('f',minx))
				vtFP.write(pack('f',miny))
				vtFP.write(pack('f',minz))
				vtFP.write(pack('f',maxx))
				vtFP.write(pack('f',maxy))
				vtFP.write(pack('f',maxz))
				v_count = len(vertices)
				print ('v_count = %d' %v_count)
				vtFP.write(pack('I',v_count))
				for v in vertices:
					vtFP.write(pack('f',v.x))
					vtFP.write(pack('f',v.y))
					vtFP.write(pack('f',v.z))
				vtFP.write(pack('I',len(indicies)))
				if len(indicies) <= 65535:
					vtFP.write(b'\x01')
					for ele in indicies:
						vtFP.write(pack('H',ele))
				else:
					print ('FYI: extracted bsp is very large. obj-to-vt conversion recommended')
					vtFP.write(b'\x02')
					for ele in indicies:
						vtFP.write(pack('I',ele))
				vtFP.write(b'\x01\x00\x00\x00\x00\x00\x00\x00')
				vtFP.write(pack('I',v_count))
				vtFP.close()
				print ('Done')
				
						
			
				
		else:
			print ('bsp not found or incompatible bsp version, skip.')


		
args = parser.parse_args()
for fname in glob(args.input):
	print('\nprocessing %s' % fname)
	main(fname)

