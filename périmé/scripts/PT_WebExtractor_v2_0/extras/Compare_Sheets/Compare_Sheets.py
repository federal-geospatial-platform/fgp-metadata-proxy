import os
import sys
import codecs
import csv
import collections
import argparse
import json
import ast
from Tkinter import *
import tkFileDialog as tkFD
import traceback
import inflect
from openpyxl import *
from openpyxl.styles import *
from openpyxl.worksheet.write_only import WriteOnlyCell
#from methods import xl_methods as xl

home_folder = os.path.abspath(os.path.join(__file__, "..\\..\\.."))
scripts_folder = os.path.join(os.sep, home_folder, 'scripts')
sys.path.append(scripts_folder)

from common import shared
from common import spreadsheet as sh

def run(inputs, output=None):

	first_fn, sec_fn = inputs
	
	# Open the first Excel spreadsheet
	first_xl = sh.PT_XL(fn=first_fn, read_only=True)
	first_xl.set_workbook()
	first_xl.set_worksheet()
	#print first_xl.get_ws_name()
	
	# Open the second Excel spreadsheet
	sec_xl = sh.PT_XL(fn=sec_fn, read_only=True)
	sec_xl.set_workbook()
	sec_xl.set_worksheet()
	#print sec_xl.get_ws_name()
	
	f_rows = first_xl.get_rows()
	s_rows = sec_xl.get_rows()
	for f_idx, f_row in enumerate(f_rows):
		if f_idx == 0: continue
		if len(f_row) > 3:
			f_title = f_row[1].value
			f_desc = f_row[2].value
		
			#print f_title
			#print f_desc
			
			for s_idx, s_row in enumerate(s_rows):
				if s_idx == 0: continue
				if len(s_row) > 3:
					s_title = s_row[1].value
					s_desc = s_row[2].value
					
					if s_title == f_title:
						print s_title
		
		#for s_row in s_rows:
			

def main():
	try:
		root = Tk()
		root.withdraw()
		
		in_files = tkFD.askopenfilenames(initialdir = home_folder, 
						title = "Select File(s)", 
						filetypes = (("XLSX files","*.xlsx"), 
						("all files","*.*")))
		file_lst = list(in_files)
		
		if len(file_lst) < 2:
			sec_file = tkFD.askopenfilename(initialdir = home_folder, 
						title = "Select Second Excel File", 
						filetypes = (("XLSX files","*.xlsx"), 
						("all files","*.*")))
			if not sec_file == '':
				file_lst.append(sec_file)
		
		#print len(file_lst)
		if len(file_lst) < 2:
			print "ERROR: 2 files are required to compare sheets."
			return None
		
		run(file_lst[:2])
		
	except Exception, err:
		print 'ERROR: %s\n' % str(err)
		print traceback.format_exc()
		
		
	# try:
		# parser = argparse.ArgumentParser()
		# parser.add_argument("-i", "--inputs", help=.",
							# metavar="Province or Territory")
		# args = parser.parse_args()

		# juris = args.jurisdiction
		
		# if juris is None:
			# answer = raw_input("\nPlease enter a province or territory for extraction (full name or 2-letter "
							   # "abbreviation): ")
			# if not answer == "":
				# juris = answer.lower()
			# else:
				# print "\nERROR: Please specify a province or territory."
				# print "Exiting process."
				# sys.exit(1)
				
		# if juris.lower() == 'alberta' or juris.lower() == 'ab':
			# juris = 'Alberta'
		# elif juris.lower() == 'british columbia' or juris.lower() == 'bc':
			# juris = 'BC'
		# elif juris.lower() == 'manitoba' or juris.lower() == 'mb':
			# juris = 'Manitoba'
		# elif juris.lower() == 'new brunswick' or juris.lower() == 'nb':
			# juris = 'New Brunswick'
		# elif juris.lower().find('newfoundland') > -1 or juris.lower().find('labrador') > -1 or juris.lower() == 'nl':
			# juris = 'NL'
		# elif juris.lower() == 'nova scotia' or juris.lower() == 'ns':
			# juris = 'Nova Scotia'
		# elif juris.lower() == 'nunavut' or juris.lower() == 'nu':
			# juris = 'Nunavut'
		# elif juris.lower().find('northwest') > -1 or juris.lower() == 'nt':
			# juris = 'NWT'
		# elif juris.lower() == 'ontario' or juris.lower() == 'on':
			# juris = 'Ontario'
		# elif juris.lower().find('edward') > -1 or juris.lower() == 'pe':
			# juris = 'PEI'
		# elif juris.lower() == 'quebec' or juris.lower() == 'qc':
			# juris = 'Quebec'
		# elif juris.lower() == 'saskatchewan' or juris.lower() == 'sk':
			# juris = 'Saskatchewan'
		# elif juris.lower() == 'yukon' or juris.lower() == 'yt' or juris.lower() == 'yk':
			# juris = 'Yukon'
		# elif juris.lower() == 'all':
			# juris = 'all'
		# elif answer.lower() == 'help' or answer.lower().find('h') > -1:
			# parser.print_help()
			# sys.exit(1)
		# else:
			# print "\nERROR: '%s' is not a valid province or territory."
			# print "Exiting process."
			# sys.exit(1)

		# res_folder = shared.get_results_folder()
		# if juris == 'all':
			# pt_folders = shared.get_pt_folders()
			# for pt in pt_folders:
				# juris = os.path.basename(pt.strip('\\'))
				# if not juris == "Canada":
					# print "\nRunning Analysis for %s" % juris
					# csv_fn = os.path.join(os.sep, pt, "_%s_merged.csv" % juris)
					# run(juris, csv_fn)
		# else:
			# juris = juris.replace(' ', '_')
			# csv_fn = os.path.join(os.sep, res_folder, juris, "_%s_merged.csv" % juris)
			# run(juris, csv_fn)
		
		# print "\nFilter completed successfully."

if __name__ == '__main__':
	sys.exit(main())