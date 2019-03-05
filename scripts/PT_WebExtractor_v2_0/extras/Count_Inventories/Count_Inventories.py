import os
import sys
import argparse
import glob
import traceback
import codecs
import fileinput
import glob
import pandas as pd

home_folder = os.path.abspath(os.path.join(__file__, "..\\..\\.."))
scripts_folder = os.path.join(os.sep, home_folder, 'scripts')
sys.path.append(scripts_folder)

from common import shared

def run():
	''' Counts all the items in the CSV files.
	'''
	
	pt_folders = shared.get_pt_folders()
	
	output_folder = os.path.dirname(os.path.join(__file__))
	results_folder = "%s\\results" % output_folder
	
	#print pt_folders
	out_xlsx = '%s\\PT_Inventory_Totals.xlsx' % results_folder
	print out_xlsx
	writer = pd.ExcelWriter(out_xlsx, engine='xlsxwriter')
	
	for pt_folder in pt_folders:
		# Get the province name or abbreviation
		pt_name = os.path.basename(pt_folder.strip('\\'))
		
		# Create the output CSV file for the province
		out_fn = "%s\\%s_Totals.csv" % (results_folder, pt_name)
		print out_fn
		#answer = raw_input("Press enter...")
		outcsv = open(out_fn, 'w')
		
		# Write the header
		outcsv.write("Inventory CSV,Number of Results\n")
		
		# Get all the CSV files
		csv_files = glob.glob(pt_folder + "\\*.csv")
		
		prov_total = 0
		for csv_fn in csv_files:
			if csv_fn.find('err_log') == -1 and \
				csv_fn.find('merge') == -1 and \
				csv_fn.find('duplicate') == -1 and \
				csv_fn.find('DataDistributionCatalogue') == -1:
				# Open the CSV file
				csv_f = codecs.open(csv_fn, encoding='utf-8', mode='r')
				
				# Get the number of lines
				count = len(csv_f.readlines()) #len([line for line in csv_f.readlines()])
				
				# Write the count to the output CSV file
				outcsv.write("%s,%s\n" % (os.path.basename(csv_fn), count))
				
				prov_total += count
				
				csv_f.close()
				
		# Write province total to CSV file
		outcsv.write("Province Total,%s\n" % prov_total)
				
		outcsv.close()
		
		# Add the CSV into the Excel file 
		df = pd.read_csv(out_fn)
		df.to_excel(writer, sheet_name=pt_name)
	
	writer.save()

def main():

	try:
		run()
		
		print "\nInventory Count completed successfully."

	except Exception, err:
		print 'ERROR: %s\n' % str(err)
		print traceback.format_exc()

if __name__ == '__main__':
	sys.exit(main())