import os
import sys
import codecs
import csv
import collections
import argparse
import traceback
import inflect
import openpyxl

home_folder = os.path.abspath(os.path.join(__file__, "..\\..\\.."))
scripts_folder = os.path.join(os.sep, home_folder, 'scripts')
sys.path.append(scripts_folder)

from common import shared

def get_word_list(words, omit=False):

	# Create the inflect engine to get plurals
	p = inflect.engine()
	
	# First, remove any blanks in the list
	words = [word for word in words if not word.strip() == '']

	if omit:
		singular_words = [word.strip()[1:] for word in words if word[0] == '-']
	else:
		singular_words = [word.strip() for word in words if not word[0] == '-']
	plural_words = [p.plural(word) for word in singular_words]
	srch_words = singular_words + plural_words
	
	return srch_words

def run(juris, csv_fn):

	# Open the input (merged) CSV file for reading to 
	#	get the header at the top of the file
	csv_f = codecs.open(csv_fn, mode='rb')
	
	# Get the header list from the top line of the CSV file
	header = csv_f.readline().strip().split(',')
	
	# Put the input (merged) CSV file into a dictionary
	#reader_f = codecs.open(csv_fn, mode='rb')
	reader = csv.DictReader(csv_f)
	
	# Get the list of search words from a CSV file
	srch_csv = open('filter_lists.csv', mode='rb')
	srch_lines = srch_csv.readlines()
	srch_words = collections.OrderedDict()
	for line in srch_lines:
		# Each line in the filter list CSV file contains:
		#	- first column is the theme name
		#	- the rest of the columns are the search words for the key
		# Ex: GB3_imagery,imagery,uav,drone,ortho
		vals = line.split(',')
		srch_words[vals[0]] = vals[1:]
	
	out_lines = collections.OrderedDict()
	
	found_idx = []
	
	# Create the inflect engine to get plurals
	p = inflect.engine()
	
	for k, words in srch_words.items():
		# Go through each list of words
	
		#print "%s: %s" % (k, words)
		
		filtered_lines = []
		
		# Get a list of the search words
		keep_words = get_word_list(words)
		# Get a list of words to omit in search
		omit_words = get_word_list(words, True)
		
		print "%s: %s" % (k, keep_words)
		print "%s omissions: %s" % (k, omit_words)
		
		csv_f.seek(0)
	
		for idx, line in enumerate(reader):
			# Go through each line in the merged CSV
		
			if line['Source'] == 'err_log.csv': continue
			
			title_str = line['Title'].lower()
			desc_str = line['Description'].lower()
			
			# FOR DEBUGGING
			# if title_str.find('house') > -1:
				# print title_str
				# print any(s in title_str for s in keep_words) and \
					# not any(s in title_str for s in omit_words)
			
			if any(s in title_str for s in keep_words) and \
				not any(s in title_str for s in omit_words):
				# If the title matches the word or the plural of the word:
				
				# Join each item in line together, separated by commas
				out_line = '","'.join([line[key] for key in header])
				# Add quotes at the beginning and end of the line
				out_line = '"' + out_line + '"'
				# Add the line to the filtered list
				filtered_lines.append(('title', out_line))
				
				# Add the line index to the found_idx list
				found_idx.append(idx)
				
			elif any(s in desc_str for s in keep_words) and \
				not any(s in desc_str for s in omit_words):
				# If the description matches the word or the plural of the word:
				
				# Join each item in line together, separated by commas
				out_line = '","'.join([line[key] for key in header])
				# Add quotes at the beginning and end of the line
				out_line = '"' + out_line + '"'
				# Add the line to the filtered list
				filtered_lines.append(('desc', out_line))
				
				# Add the line index to the found_idx list
				found_idx.append(idx)
		
			# # Get a list of the titles
			# for word in srch_words:
				# # Strip the word of any newline characters
				# plural = p.plural(word)
				# if not word == '':
					# if line['Title'].lower().find(word) > -1 or \
						# line['Title'].lower().find(p.plural(word)) > -1:
						# # If the title matches the word or the plural of the word:
						
						# # Join each item in line together, separated by commas
						# out_line = '","'.join([line[key] for key in header])
						# # Add quotes at the beginning and end of the line
						# out_line = '"' + out_line + '"'
						# # Add the line to the filtered list
						# filtered_lines.append(out_line)
						
						# # Add the line index to the found_idx list
						# found_idx.append(idx)
						
		# Remove any duplicate entries			
		filtered_lines = list(collections.OrderedDict.fromkeys(filtered_lines))
		
		# Add the filtered lines to the out_lines with the current theme as key
		out_lines[k] = filtered_lines
		
	#print out_lines[k]
	
	#answer = raw_input("Press enter...")
	
	for k, v in out_lines.items():
		# Go through each theme's output lines
	
		# Open the output CSV file for editing
		outcsv_fn = "results\\%s\\%s_%s_searchresults.csv" % (juris.replace(' ', '_'), juris.replace(' ', '_'), k)
		outcsv_file = codecs.open(outcsv_fn, encoding='utf_8', mode='w')
		
		# Write the header
		outcsv_file.write(','.join(header) + "\n")
		
		for v_line in v:
			outcsv_file.write(unicode(v_line, errors='ignore') + "\n")
		
		outcsv_file.close()
	
	####################################################################
	# Create a CSV file with unknown classifications
	unused_csv_fn = "results\\%s\\_%s_other_searchresults.csv" % (juris.replace(' ', '_'), juris.replace(' ', '_'))
	unused_file = codecs.open(unused_csv_fn, encoding='utf_8', mode='w')
	
	csv_f.seek(0)
	
	for idx, line in enumerate(reader):
	
		if line['Source'] == 'err_log.csv' or line['Source'] == 'URL': continue
		
		if idx not in found_idx:
			out_line = '","'.join([line[key] for key in header])
			out_line = '"' + out_line + '"'
			unused_file.write(unicode(out_line, errors='ignore') + "\n")
		
	unused_file.close()	
	csv_f.close()

def main():
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("-j", "--jurisdiction", help="The province or territory to be extracted.",
							metavar="Province or Territory")
		args = parser.parse_args()

		juris = args.jurisdiction
		
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