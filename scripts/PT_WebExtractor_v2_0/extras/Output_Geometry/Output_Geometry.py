import os
import sys
import codecs
import csv
import re
import collections
import argparse
import json
import ast
import traceback
import inflect
import arcpy
import Tkinter, Tkconstants, tkFileDialog
from openpyxl import *
from openpyxl.styles import *
from openpyxl.worksheet.write_only import WriteOnlyCell
#from methods import xl_methods as xl

home_folder = os.path.abspath(os.path.join(__file__, "..\\..\\.."))
scripts_folder = os.path.join(os.sep, home_folder, 'scripts')
sys.path.append(scripts_folder)

from common import shared
from common import spreadsheet as sh

def parse_wkt(wkt):

	# nums = re.findall(r'\d+(?:\.\d*)?', wkt) #.rpartition(',')[0])
	# print "1: %s" % nums
	# coords = [float(n) for n in nums]
	# print "2: %s" % coords
	# coords = zip(*[iter(nums)] * 2)
	# print "3: %s" % coords
	
	start = wkt.find('(')
	end = wkt.rfind(')')
	#print start
	#print end
	coords_str = wkt[start+1:end]
	
	#print coords_str
	coords = []
	for c in coords_str.split(', '):
		c = c.replace('(', '').replace(')', '')
		c_split = c.split(' ')
		coords.append((c_split[0], c_split[1]))
	
	#print coords
	
	#answer = raw_input("Press enter...")
	
	return coords

def run(juris, input_fn):

	juris = juris.replace(' ', '_')
	
	os.system("title Geometry Extraction - %s" % juris)
	
	# Open file and get the extents info
	datasets = []
	if input_fn.find('.xls') > -1:	
		# Open merged spreadsheet
		in_xl = sh.PT_XL(fn=input_fn, read_only=True)
		in_xl.set_workbook()
		in_xl.set_worksheet(0)
		header = in_xl.get_header()
		datasets = in_xl.get_dictrows('values')
	else:
		in_csv = sh.PT_CSV(input_fn, read_only=True)
		in_csv.open_csv()
		header = in_csv.get_header()
		datasets = in_csv.get_dictrows()
		
	# Parse the input filename
	fn_split = os.path.basename(input_fn).split('_')
	source = fn_split[1]
		
	print "Header: %s" % header
		
	if not 'Extents' in datasets[0].keys():
		print "\nNo 'Extents' column exists in input file."
		print "Exiting process."
		return None
	
	# Create the Feature Class
	out_fc = '%s_%s_AOIs.shp' % (juris, source)
	out_shp = 'results\\' + out_fc
	prj_file = 'files\\4326.prj'
	sp_ref = arcpy.SpatialReference(prj_file)
	
	print "out_fc: %s" % out_fc
	
	if os.path.exists(out_shp):
		arcpy.Delete_management(out_shp)
	
	cur = None
	try:
		# Create the output feature class
		print "\n**** Creating Feature Class ****"
		arcpy.CreateFeatureclass_management('results', out_fc, 
											"POLYGON", spatial_reference=sp_ref)
												
		#cur = arcpy.da.InsertCursor(out_fc, ["SHAPE@"])
		out_header = sh.get_header_info('shp')
		
		print "\n**** Adding Fields to Feature Class ****"
		for h in out_header['xl']:
			#print h
			new_h = h[0].replace(' ', '')[:9]
			length = h[1]
			#print new_h
			arcpy.AddField_management(out_shp, new_h, "TEXT", \
										field_length=length)
		
		print "\n**** Adding Geometry to Feature Class ****"
		for idx, ds in enumerate(datasets):
			msg = "Adding Geometry %s of %s datasets" % (idx + 1, len(datasets))
			shared.print_oneliner(msg)
		
			# Get the attributes
			attrs = []
			for idx, h in enumerate(header):
				 attrs.append(ds[h])
			
			#print attrs
			#answer = raw_input("Press enter...")
			
			wkt_extents = ds['Extents']
			
			if wkt_extents is None or wkt_extents == '':
				print "\nDataset %s does not contain extents." % idx
				continue
			
			#print "WKT Extents: %s" % wkt_extents
			
			coords = parse_wkt(wkt_extents)
			
			#print "Coordinates: %s" % coords
			
			fields = [f.name for f in arcpy.ListFields(out_shp)]
			
			#print "fields: %s" % fields
			
			# Open an insert cursor for the new feature class
			fields = out_header['csv'] + ["SHAPE@"]
			cur = arcpy.da.InsertCursor(out_shp, fields)

			# Create an array object needed to create features
			array = arcpy.Array()

			# Initialize a variable for keeping track of a feature's ID.
			ID = -1
			for coords in coords: 
				array.add(arcpy.Point(coords[0], coords[1]))
			
			polygon = arcpy.Polygon(array, sp_ref)

			cur.insertRow(attrs + [polygon])
	
	except Exception as e:
		traceback.print_exc(file=sys.stdout)
		print(e)
		return e
	finally:
		# Cleanup the cursor if necessary
		if cur:
			del cur
	
	return None

def main():
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("-j", "--jurisdiction", help="The province or territory to be extracted.",
							metavar="Province or Territory")
		parser.add_argument("-f", "--input_fn", help="The input spreadsheet file (Excel or CSV) with 'Extents' column.",
							metavar="Spreadsheet File")
		args = parser.parse_args()

		juris = args.jurisdiction
		input_fn = args.input_fn
		
		if juris is None:
			answer = raw_input("\nPlease enter a province or territory for geometry extraction (full name or 2-letter "
							   "abbreviation): ")
			if not answer == "":
				juris = answer.lower()
			else:
				print "\nERROR: Please specify a province or territory."
				print "Exiting process."
				sys.exit(1)
				
		if juris.lower() == 'alberta' or juris.lower() == 'ab':
			juris = 'Alberta'
		elif juris.lower() == 'british columbia' or juris.lower() == 'bc':
			juris = 'BC'
		elif juris.lower() == 'manitoba' or juris.lower() == 'mb':
			juris = 'Manitoba'
		elif juris.lower() == 'new brunswick' or juris.lower() == 'nb':
			juris = 'New Brunswick'
		elif juris.lower().find('newfoundland') > -1 or juris.lower().find('labrador') > -1 or juris.lower() == 'nl':
			juris = 'NL'
		elif juris.lower() == 'nova scotia' or juris.lower() == 'ns':
			juris = 'Nova Scotia'
		elif juris.lower() == 'nunavut' or juris.lower() == 'nu':
			juris = 'Nunavut'
		elif juris.lower().find('northwest') > -1 or juris.lower() == 'nt':
			juris = 'NWT'
		elif juris.lower() == 'ontario' or juris.lower() == 'on':
			juris = 'Ontario'
		elif juris.lower().find('edward') > -1 or juris.lower() == 'pe':
			juris = 'PEI'
		elif juris.lower() == 'quebec' or juris.lower() == 'qc':
			juris = 'Quebec'
		elif juris.lower() == 'saskatchewan' or juris.lower() == 'sk':
			juris = 'Saskatchewan'
		elif juris.lower() == 'yukon' or juris.lower() == 'yt' or juris.lower() == 'yk':
			juris = 'Yukon'
		elif juris.lower() == 'all':
			juris = 'all'
		elif answer.lower() == 'help' or answer.lower().find('h') > -1:
			parser.print_help()
			sys.exit(1)
		else:
			print "\nERROR: '%s' is not a valid province or territory."
			print "Exiting process."
			sys.exit(1)
			
		# Get the initialdir
		init_dir = shared.get_results_folder(juris)
			
		if input_fn is None:
			root = Tkinter.Tk()
			root.withdraw()
			input_fn = tkFileDialog.askopenfilename(initialdir=init_dir, \
								title="Select Excel File", \
								filetypes=(("CSV files", "*.csv"), 
											("Excel files", "*.xlsx"), 
											("97/2003 Excel files", "*.xls"), 
											("All files", "*.*")))
		
		if input_fn == '':
			print "\nNo input file selected."
			print "Exiting process."
			sys.exit(1)
		
		print input_fn
		
		err_chk = run(juris, input_fn)
		
		if err_chk is None:
			print "\nFilter completed successfully."
		else:
			print "\nFilter did not complete."

	except Exception, err:
		print 'ERROR: %s\n' % str(err)
		print traceback.format_exc()

if __name__ == '__main__':
	sys.exit(main())