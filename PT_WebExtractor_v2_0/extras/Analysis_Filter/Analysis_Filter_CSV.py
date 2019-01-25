import os
import sys
import codecs
import csv
import collections
import argparse
import json
import ast
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

def get_word_list(words, juris, omit=False):

	# Create the inflect engine to get plurals
	p = inflect.engine()
	
	# First, remove any blanks in the list
	words = [word for word in words if not word.strip() == '']

	if omit:
		singular_words = [word.strip()[1:] for word in words if word[0] == '-']
	else:
		singular_words = [word.strip() for word in words if not word[0] == '-']
		
	#print singular_words
	if not juris == 'Quebec':
		plural_words = [p.plural(word) for word in singular_words]
		srch_words = singular_words + plural_words
	else:
		srch_words = singular_words
	
	return srch_words
	
def get_search_words(juris, theme='gb3'):
	# Get the list of search words from a CSV file
	if juris == 'Quebec':
		srch_csv = codecs.open('filter_lists_fr.csv', encoding='utf-8', mode='rb')
	else:
		srch_csv = open('filter_lists.csv', mode='rb')
	srch_lines = srch_csv.readlines()
	srch_words = collections.OrderedDict()
	for line in srch_lines:
		# Each line in the filter list CSV file contains:
		#	- first column is the theme name
		#	- the rest of the columns are the search words for the key
		# Ex: GB3_imagery,imagery,uav,drone,ortho
		vals = line.split(',')
		if vals[0].lower().find(theme) > -1:
			srch_words[vals[0]] = vals[1:]
		
	return srch_words

def run(juris, csv_fn):

	juris = juris.replace(' ', '_')

	# Open the input (merged) CSV file for reading to 
	#	get the header at the top of the file
	csv_f = codecs.open(csv_fn, mode='rb')
	
	#print csv_f
	
	# Get the header list from the top line of the CSV file
	header_txts = csv_f.readline().strip().split(',')
	
	# Put the input (merged) CSV file into a dictionary
	reader = csv.DictReader(csv_f)
	
	# Get a list of search words from the filter CSV file
	srch_words = get_search_words(juris)
	
	out_lines = collections.OrderedDict()
	
	found_idx = []
	
	# Create the inflect engine to get plurals
	p = inflect.engine()
	
	#print srch_words
	
	#answer = raw_input("Press enter...")
	
	for k, words in srch_words.items():
		# Go through each list of words
		
		filtered_lines = []
		
		# Get a list of the search words
		keep_words = get_word_list(words, juris)
		#print "keep_words: %s" % keep_words
		if 'base' in keep_words:
			desc_words = keep_words[:]
			base_idx = desc_words.index('base')
			del desc_words[base_idx]
			if not juris == 'Quebec':
				base_idx = desc_words.index('bases')
				del desc_words[base_idx]
		else:
			desc_words = keep_words
		
		# Get a list of words to omit in search
		omit_words = get_word_list(words, juris, True)
		
		csv_f.seek(0)
		
		f = open(csv_fn)
		numlines = len(f.readlines())
		
		print csv_fn
	
		for idx, line in enumerate(reader):
			msg = "Filtering %s of %s lines for search words" % (idx + 1, numlines)
			#print msg
			shared.print_oneliner(msg)
		
			# Go through each line in the merged CSV
			if line['Source'] == 'err_log.csv': continue
			
			title_str = line['Title'].lower()
			desc_str = line['Description'].lower()

			if any(s in title_str for s in keep_words) and \
				not any(s in title_str for s in omit_words):
				# If the title matches the word or the plural of the word:
				
				# Join each item in line together, separated by commas
				out_line = '","'.join([line[key] for key in header_txts])
				# Add quotes at the beginning and end of the line
				out_line = '"' + out_line + '"'
				# Add the line to the filtered list
				filtered_lines.append(('title', out_line))
				
				# Add the line index to the found_idx list
				found_idx.append(idx)
				
			elif any(s in desc_str for s in desc_words) and \
				not any(s in desc_str for s in omit_words):
				# If the description matches the word or the plural of the word:
				# Join each item in line together, separated by commas
				out_line = '","'.join([line[key] for key in header_txts])
				# Add quotes at the beginning and end of the line
				out_line = '"' + out_line + '"'
				# Add the line to the filtered list
				filtered_lines.append(('desc', out_line))
				
				# Add the line index to the found_idx list
				found_idx.append(idx)
						
		print
		
		# Remove any duplicate entries			
		filtered_lines = list(collections.OrderedDict.fromkeys(filtered_lines))
		
		# Add the filtered lines to the out_lines with the current theme as key
		out_lines[k] = filtered_lines
		
	#print out_lines[k]
	
	#answer = raw_input("Press enter...")
	
	out_f = codecs.open('out_tmp.txt', encoding='utf-8', mode='w')
	
	# Set the widths of each column in the output
	header_info = []
	widths = [('Layer', 24), ('P/T', 6), ('Source', 50), 
				('Title', 100), ('Description', 100), 
				('Type', 20), ('Date', 20), ('Publisher', 60), 
				('Licensing', 50), ('Available Formats', 50), 
				('Access', 32), ('Download', 25), ('Spatial Reference', 50), 
				('Data URL', 70), ('Web Page URL', 70), 
				('Web Map URL', 70), ('Service', 25), 
				('Service Name', 100), ('Service URL', 70), 
				('Metadata URL', 70), ('Metadata Type', 65), 
				('Notes', 100)]
	
	# Set the header and column widths
	for h in header_txts:
		width_lst = [w[1] for w in widths if h == w[0]]
		
		if len(width_lst) == 0:
			width = 50
		else:
			width = width_lst[0]
			
		header_info.append((h, width))
	
	try:
		for k, value in out_lines.items():
		
			# Go through each theme's output lines
		
			# Open the output CSV file for editing
			outcsv_fn = "results\\%s\\%s_%s_searchresults.xlsx" % (juris, juris, k)
			
			# Create the Excel file
			out_xl = sh.PT_XL(fn=outcsv_fn, write_only=True, 
								replace=True, replace_ws=True)
			
			title_wsname = 'Found in Titles'
			desc_wsname = 'Found in Descriptions'
			title_ws = out_xl.add_worksheet(title_wsname, header_info)
			desc_ws = out_xl.add_worksheet(desc_wsname, header_info)
			
			for idx, line in enumerate(value):
				msg = "Saving %s of %s lines to '%s'" % (idx + 1, len(value), outcsv_fn)
				shared.print_oneliner(msg)
			
				line_type = line[0]
				
				# Remove any next lines from the line
				in_line = line[1].replace('\n', '  ')
				in_line = in_line.replace('\r', '  ')
				in_line = in_line[1:-1]
				
				# Split the line
				line_vals = in_line.split('","')
				
				if line_type == 'desc':
					out_xl.write_list(line_vals, desc_wsname)
				else:
					out_xl.write_list(line_vals, title_wsname)
			
			print
			# save the file
			out_xl.save_file()
			
	except Exception, e:
		print e
		traceback.print_exc(file=sys.stdout)
		out_f.write(unicode(in_line))
		out_f.write('\n')
		answer = raw_input("Press enter...")
	
	####################################################################
	# Create an XLSX file with unknown classifications
	
	other_csv_fn = "results\\%s\\_%s_other_searchresults.xlsx" % (juris, juris)
	
	# Create the other Excel file
	other_xl = sh.PT_XL(fn=other_csv_fn, write_only=True, 
						replace=True, replace_ws=True)
	
	wsname = 'Other Datasets'
	title_ws = other_xl.add_worksheet(wsname, header_info)
	
	csv_f.seek(0)
	
	for idx, line in enumerate(reader):
	
		msg = "Saving %s of %s other lines" % (idx + 1, numlines)
		#print msg
		shared.print_oneliner(msg)
	
		if idx == 0:
			#print "idx is zero!"
			continue
	
		if line['Source'] == 'err_log.csv' or line['Source'] == 'URL':
			#print "Source is invalid!"
			continue
		
		if idx not in found_idx:
			vals = [line[key] for key in header_txts]
			other_xl.write_list(vals, wsname)
			
	print
			
	# save the file
	other_xl.save_file()
	
	out_f.close()
	csv_f.close()

def main():
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("-j", "--jurisdiction", help="The province or territory to be extracted.",
							metavar="Province or Territory")
		#parser.add_argument("-k", "--keywords", help="The CSV file with keywords.",
		#					metavar="Keywords File")
		args = parser.parse_args()

		juris = args.jurisdiction
		#keywords = args.keywords
		
		if juris is None:
			answer = raw_input("\nPlease enter a province or territory for extraction (full name or 2-letter "
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

		res_folder = shared.get_results_folder()
		if juris == 'all':
			pt_folders = shared.get_pt_folders()
			for pt in pt_folders:
				juris = os.path.basename(pt.strip('\\'))
				if not juris == "Canada":
					print "\nRunning Analysis for %s" % juris
					csv_fn = os.path.join(os.sep, pt, "_%s_merged.csv" % juris)
					run(juris, csv_fn)
		else:
			juris = juris.replace(' ', '_')
			csv_fn = os.path.join(os.sep, res_folder, juris, "_%s_merged.csv" % juris)
			run(juris, csv_fn)
		
		print "\nFilter completed successfully."

	except Exception, err:
		print 'ERROR: %s\n' % str(err)
		print traceback.format_exc()

if __name__ == '__main__':
	sys.exit(main())