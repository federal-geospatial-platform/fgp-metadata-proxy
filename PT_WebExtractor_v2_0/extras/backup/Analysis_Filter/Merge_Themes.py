import os
import sys
import codecs
import csv
import collections
import argparse
import traceback
import inflect
import glob
from openpyxl import *
from openpyxl.styles import *
from openpyxl.worksheet.write_only import WriteOnlyCell
#from methods import xl_methods as xl

home_folder = os.path.abspath(os.path.join(__file__, "..\\..\\.."))
scripts_folder = os.path.join(os.sep, home_folder, 'scripts')
sys.path.append(scripts_folder)

from common import shared
from common import spreadsheet as sh

def run():
	
	script_path = os.path.abspath(os.path.join(__file__))
	script_folder = os.path.dirname(script_path)
	results_folder = os.path.join(os.sep, script_folder, 'results')
	
	sub_folders = glob.glob(os.path.join(os.sep, results_folder, '*/'))
	
	#print sub_folders
	
	# Get a list of themes from the file names in the Alberta folder
	themes = []
	
	xl_files = glob.glob(results_folder + "\\Alberta\\*.xlsx")
	
	for xl_f in xl_files:
		if xl_f.find('_other') == -1:
			theme = os.path.basename(xl_f).replace('Alberta_', '')
			theme = theme.replace('_searchresults.xlsx', '')
			themes.append(theme)
			
	print themes
		
	for th in themes:
		
		merged_xl_fn = "%s\\%s_merged.xlsx" % (results_folder, th)
		
		header_txts = [('Layer', 24), ('P/T', 6), ('Source', 50), 
						('Title', 100), ('Description', 100), 
						('Type', 20), ('Date', 20), ('Publisher', 60), 
						('Licensing', 50), ('Available Formats', 50), 
						('Access', 32), ('Download', 25), ('Web Page URL', 70), 
						('Web Map URL', 70), ('Data URL', 70), 
						('Spatial Reference', 50), ('Service', 25), 
						('Service Name', 100), ('Service URL', 70), 
						('Metadata URL', 70), ('Metadata Type', 65), 
						('Notes', 100)]
			   
		out_xl = sh.PT_XL(fn=merged_xl_fn, header=header_txts, 
							write_only=True, setup=False, replace=True, 
							replace_ws=True, ws_title=th)
							
		out_xl.create_workbook()
		
		# Create the worksheet in the output file
		title_ws = "Title Results"
		out_xl.add_worksheet(title_ws)
		out_xl.add_header()
		
		# Create the worksheet in the output file
		desc_ws = "Description Results"
		out_xl.add_worksheet(desc_ws)
		out_xl.add_header()
		
		for idx, pt_folder in enumerate(sub_folders):
		
			pt_name = os.path.basename(pt_folder.strip('\\'))
			pt_abbrev = out_xl.get_abbreviation(pt_name.replace('_', ' '))
			
			msg = "Copying %s of %s provinces/territories for theme %s" \
					% (idx + 1, len(sub_folders), th)
			shared.print_oneliner(msg)
			
			pt_fn = glob.glob('%s\\*%s*.xlsx' % (pt_folder, th))
			
			# Open the P/T spreadsheet for reading
			pt_xl = sh.PT_XL(fn=pt_fn[0], read_only=True)
			pt_xl.set_workbook()
			pt_xl.set_worksheet('Found in Titles')
			
			out_xl.set_worksheet(title_ws)
			
			for idx, row in enumerate(pt_xl.get_rows()):
				# Skip the first row
				if idx == 0: continue
				
				out_vals = []
				# Get the style of the first cell
				fill_val = row[0].fill
				out_xl.add_cell(th.upper(), fill_val)
				out_xl.add_cell(pt_abbrev, fill_val)
				for cell in row:
					out_xl.add_cell(cell.value, cell.fill)
					
				out_xl.write_row()
				
			pt_xl.set_worksheet('Found in Descriptions')
			
			out_xl.set_worksheet(desc_ws)
			
			for idx, row in enumerate(pt_xl.get_rows()):
				# Skip the first row
				if idx == 0: continue
				
				out_vals = []
				# Get the style of the first cell
				fill_val = row[0].fill
				out_xl.add_cell(th.upper(), fill_val)
				out_xl.add_cell(pt_abbrev, fill_val)
				for cell in row:
					out_xl.add_cell(cell.value, cell.fill)
					
				out_xl.write_row()
				
		print
		
		out_xl.save_file()
	
		# # Create the merged CSV file for the theme
		# merged_csv_fn = "%s\\%s_merged.csv" % (results_folder, th)
		# merged_csv = codecs.open(merged_csv_fn, encoding='utf-8', mode='w')

		# header = ['Layer', 'P/T', 'Source', 'Title', 'Description', 'Type', 'Date', 'Publisher',
			   # 'Licensing', 'Available Formats', 'Access', 'Download',
			   # 'Web Page URL', 'Web Map URL', 'Data URL',
			   # 'Spatial Reference', 'Service', 'Service Name', 'Service URL',
			   # 'Metadata URL', 'Metadata Type', 'Notes']
			   
		# # Write the header
		# merged_csv.write(','.join(header) + "\n")
	
		# for pt_folder in sub_folders:
			# # Get the province name or abbreviation
			# pt_name = os.path.basename(pt_folder.strip('\\'))
			# pt_abbrev = get_abbreviation(pt_name.replace('_', ' '))
			
			# theme_fn = glob.glob('%s\\*%s*.csv' % (pt_folder, th))
			
			# if len(theme_fn) == 0: continue
			
			# print th
			# print theme_fn
			
			# # Open the theme's file
			# theme_csv = codecs.open(theme_fn[0], encoding='utf-8', mode='rb')
			
			# for line in theme_csv.readlines()[1:]:
				# new_line = '"%s","%s",%s' % (th.upper(), pt_abbrev, line)
				# merged_csv.write(new_line)
				
			# theme_csv.close()
				
		# merged_csv.close()

def main():
	try:
		run()
		
		print "\nThemes merged successfully."

	except Exception, err:
		print 'ERROR: %s\n' % str(err)
		print traceback.format_exc()

if __name__ == '__main__':
	sys.exit(main())