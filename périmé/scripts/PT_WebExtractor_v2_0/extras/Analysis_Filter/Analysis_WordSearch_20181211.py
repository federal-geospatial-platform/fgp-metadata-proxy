import os
import sys
import codecs
import csv
import re
import collections
import argparse
import json
import ast
import shlex
import traceback
import inflect
import operator
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

def get_groups(in_csv):
	''' Gets a list of available groups from the input CSV file
	'''

	# Open the CSV and get its lines
	srch_csv = open(in_csv, mode='rb')
	srch_lines = srch_csv.readlines()
	
	groups = []
	
	for line in srch_lines[1:]:
		
		# Ignore any lines without double-quotes
		if line.find('|') == -1: continue
		
		# Split the line by comma
		line_parse = line.split(',')
		# Get the first item in the split line
		group = line_parse[0]
		group = group.strip()
		if not group == '':
			# Add the group to the list of available groups
			groups.append(group)
	
	# Remove any duplicate entries from the list
	groups = list(set(groups))
	
	# Sort the list alphabetically
	#print groups
	groups = sorted(groups)
	#print groups
	
	return groups

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
	
def get_search_words(juris, group='gb3', kword_fn=None):
	''' Gets a list of search words from a CSV file
	:param juris: The province/territory.
	:param group: The group abbreviation containing the keywords.
	:param kword_fn: The CSV filename containing a list of keywords.
	'''

	if kword_fn is not None:
		# If the CSV file is specified, open it
		srch_csv = codecs.open(kword_fn, encoding='utf-8', mode='rb')
	else:
		# If no CSV file specified, open default
		srch_csv = open('files\\filter_lists.csv', mode='rb')
		
	# Get the lines of the CSV file
	srch_lines = srch_csv.readlines()
	
	srch_words = collections.OrderedDict()
	
	for line in srch_lines[1:]:
		# Each line in the filter list CSV file contains
		#	either 2 or 3 columns:
		#
		#	If 2 columns:
		#	Column 1 - the group and theme name
		#	Column 2 - a list of keywords contained in double-quotes
		# 	Ex: Adaptation,"shorelines data,permafrost,agriculture"
		#
		#	If 3 columns:
		#	Column 1 - the group name
		#	Column 2 - the theme name
		#	Column 3 - a list of keywords contained in double-quotes
		#	Ex: Land,Topography,"topography, dem, dsm, dtm, ntdb, elevation, base map"
		
		# Remove whitespace from line
		line = line.strip()
		
		# If line is empty, proceed to next line
		if line == '': continue
		
		# Extract the text contained within the double-quotes
		quotes = []
		start_pos = line.find('"')
		while start_pos > -1:
			end_pos = line.find('"', start_pos+1)
			quote = line[start_pos+1:end_pos]
			quotes.append(quote)
			start_pos = line.find('"', end_pos+1)
		
		if len(quotes) == 0: continue
			
		# Split and strip quoted text
		keywords = []
		for k in quotes:
			out_k = k.split(',')
			out_k = [k.strip() for k in out_k]
			keywords.append(out_k)
		
		# Get all text before the first quote and split it by commas
		first_quote = line.find('"')
		vals = line[:first_quote].split(',')
		
		if len(vals) > 2:
			# If the text contains 2 columns
			#	set the group and theme accordingly
			group_val = vals[0]
			theme = vals[1]
		else:
			# If the text contains 1 column
			group_val = vals[0]
			theme = group_val
		
		if not group == 'all':
			# If the group to be extracted is specified,
			#	add the list of only that group
			if group_val.lower().find(group.lower()) > -1:
				srch_words[theme] = keywords
		else:
			srch_words[theme] = keywords
			
	#print srch_words
	
	#answer = raw_input("Press enter...")
		
	return srch_words
	
def search_dataset(row, idx, in_word, place=None):
	''' Searches in the Keywords, Title and Description fields, 
		in that order, for a list words
		:param row: The current row (dataset) with entries.
		:param idx: The index of the current row.
		:param words: The list of keywords used in the search.
		:param place: The place name to narrow the results (places
						are only checked for in Description).
	'''

	#out_lines = []
	found_idx = []
	
	# Get the title and description of the current row
	title_str = row['Title'].lower().replace('_', ' ')
	desc_str = row['Description'].lower()
	
	# Get a list of keywords
	keywords = row['Keywords']
	keywords = keywords.lower()
	
	# If place name provided, check in description
	if place is not None and not place == '':
		if desc_str.lower().find(place.lower()) == -1:
			return None
	
	# Create the inflect engine to get plurals
	p = inflect.engine()
	srch_word = [in_word, p.plural(in_word)]

	# Search for words in the Keywords field
	found = False
	key_srch = search_text(keywords, srch_word)
	if key_srch is None:
		# If none of the words were found in the Keywords field
		
		# Search for words in Title field
		title_srch = search_text(title_str, srch_word)
		if title_srch is None:
			# If none of the words were found in the Title field
			
			# Search for words in the description
			desc_srch = search_text(desc_str, srch_word)
			if desc_srch is not None:
				# If any word was found in Description,
				#	specify the word that was found and
				#	where it was found
				found_word = desc_srch
				found_in = 'desc'
				found = True
		else:
			# If any word was found in Title,
			#	specify the word that was found and
			#	where it was found
			found_word = title_srch
			found_in = 'title'
			found = True
	else:
		# If any word was found in Keywords,
		#	specify the word that was found and
		#	where it was found
		found_word = key_srch
		found_in = 'keywords'
		found = True
	
	if found:
		# If the word was found in the current row
		
		# Return the index, the keyword, 
		#	the column where the keyword was found and the dataset row
		return (idx, found_word, found_in, row)
		
	
def search_text(text, words):
	''' Searches for a list of keywords in a specified text.
		The search will only find the complete keyword:
		Ex: if the keyword is 'house', the search will not locate
			the word 'household'.
		:param text: The text in which to search.
		:param words: The list of keywords.
	'''
	
	print "\nWords: %s" % words
	
	for wrd in words:
		
		if wrd.find(' ') > -1:
		
			sub_words = shlex.split(wrd)
			
			#print sub_words
			#answer = raw_input("Press enter...")
			
			found = []
			for sub_wrd in sub_words:
				res = re.compile(r'\b' + sub_wrd + r'\b').search(text)
				if res is not None:
					found.append(sub_wrd)
			
			if len(found) == len(sub_words):
				return wrd
		else:
			res = re.compile(r'\b' + wrd + r'\b').search(text)
			if res is not None:
				return wrd

def run(juris, xl_fn, keyword, place=None):

	juris = juris.replace(' ', '_')
	
	os.system("title Analysis Filter - %s" % juris)
	
	# Open merged spreadsheet
	merged_xl = sh.PT_XL(fn=xl_fn, read_only=True)
	merged_xl.set_workbook()
	merged_xl.set_worksheet('Merged Datasets')
	
	# Get a list of rows (as dictionaries) from the input spreadsheet
	in_rows = merged_xl.get_dictrows('values')
	# Get the header text
	header_txts = in_rows[0].keys()
	
	# # Get a list of search words from the filter CSV file
	# srch_words = get_search_words(juris, group, keywords)
	
	# if not srch_words:
		# # If no search words exist, close spreadsheet and exit.
		# print "No search words for that group."
		# merged_xl.close_workbook()
		# return None
	
	out_lines = collections.OrderedDict()
	
	found_idx = []
	
	# Create the inflect engine to get plurals
	p = inflect.engine()
	
	try:
		
		if place == '' or place is None:
			outxl_fn = "results\\%s\\%s_wordsearch.xlsx" % (juris, juris)
		else:
			outxl_fn = "results\\%s\\%s_%s_wordsearch.xlsx" % (juris, juris, \
															place)
		
		# Create the Excel file
		out_xl = sh.PT_XL(fn=outxl_fn, replace_ws=True)
		
		# Get the proper header info for analyses
		header_info = sh.get_header_info('analysis')['xl']
		
		# Create the worksheet with the group as the sheet name
		#ws_name = keyword.replace('"', '')
		out_ws = out_xl.add_worksheet(keyword, header_info) #, \
										#'Found in Titles & Keywords')
										
		found_datasets = []
			
		for idx, row in enumerate(in_rows):
			msg = "Filtering %s of %s lines for search words" % \
					(idx + 1, len(in_rows))
			shared.print_oneliner(msg)
			
			# Go through each line in the merged CSV
			
			# Ignore any datasets that had an error
			if row['Source'] == 'err_log.csv': continue
			
			srch_res = search_dataset(row, idx, keyword, place)
			
			if srch_res is not None:
			
				#print "\nSearch results:"
				#print srch_res
				#answer = raw_input("Press enter...")
				
				# Parse the search results
				idx = srch_res[0]
				category = srch_res[2]
				keyword = srch_res[1]
				ds = srch_res[3]
				
				# Add this information to the dataset's row
				ds['Word Found'] = keyword
				ds['Found In'] = category
				ds['Layer'] = 'N/A'
				ds['P/T'] = shared.get_pt_abbreviation(juris)
				
				# Add them to a list to remove duplicates
				found_datasets.append(ds)
			
				# answer = raw_input("Press enter...")
			
				# cur_lines, cur_found = srch_res
			
				# filtered_lines += cur_lines
				# found_idx += cur_found				
		print
			
		unique_lst = shared.remove_duplicates(found_datasets)
		
		unique_lst.sort(key=operator.itemgetter('Title'))
		unique_lst.sort(key=operator.itemgetter('Found In'))
		unique_lst.sort(key=operator.itemgetter('Layer'))
		
		print "\nNumber of results found: %s" % len(unique_lst)
		
		for ds in unique_lst:
		
			for k, v in ds.items():
				out_xl.add_cell(v, k)
		
			out_xl.write_row()
			
		# save the file
		out_xl.save_file()
		
		merged_xl.close_workbook()
			
	except Exception, e:
		print e
		traceback.print_exc(file=sys.stdout)
		#out_f.write(unicode(in_line))
		#out_f.write('\n')
		answer = raw_input("Press enter...")
	
	#out_f.close()
			
			# Add the filtered lines to the out_lines with the current theme as key
			#out_lines[theme] = filtered_lines
		
		# # NOTE: Only needed for error checking
		# #out_f = codecs.open('out_tmp.txt', encoding='utf-8', mode='w')
		
		# # Categorize list of found rows into 'keywords', 'title' and 'desc'
		# sort_dict = collections.OrderedDict()
		# for theme, lines in out_lines.items():
			# for l in lines:
				# # Get the place where the keyword was found (category)
				# category = l[0]
				# # Get the keyword
				# srch_wrd = l[1]
				# # Get the row (dataset)
				# sort_line = l[2]
				# # Add the keyword to the row
				# sort_line['Word Found'] = srch_wrd
				# # Add the place where the keyword was found
				# sort_line['Found In'] = category.title()
				# # Add the theme/layer of the keyword
				# sort_line['Layer'] = theme.title()
				# # Add the province/territory
				# sort_line['P/T'] = shared.get_pt_abbreviation(juris)
				
				# if category in sort_dict:
					# # If the current category is already in the dictionary
					# #	get its list
					# prev_lst = sort_dict[category]
				# else:
					# # If not, create the list
					# prev_lst = []
				# # Add the current row to the category's list
				# prev_lst.append(sort_line)
				# sort_dict[category] = prev_lst
	
	
		
		# # Get the list of 'keywords' and 'title' items and sort it by 'Layer'
		# title_lst = []
		# if 'title' in sort_dict.keys(): 
			# title_lst = sort_dict['title']
		# keywrd_lst = []
		# if 'keywords' in sort_dict.keys():
			# keywrd_lst = sort_dict['keywords']
		# join_lst = title_lst + keywrd_lst
		# join_lst.sort(key=operator.itemgetter('Layer'))
		# unique_titles = shared.remove_duplicates(join_lst)
		
		# # Go through each title line and add it to the Excel sheet
		# for idx, line in enumerate(unique_titles):
			# msg = "Saving %s of %s lines to '%s'" % \
					# (idx + 1, len(unique_titles), outxl_fn)
			# shared.print_oneliner(msg)
			
			# # Convert the current line dictionary to cells
			# for k, v in line.items():
				# out_xl.add_cell(v, k)
			
			# out_xl.write_row()
			
		# print
		
		# # Get the list of 'desc' items and sort it by 'Layer'
		# desc_lst = []
		# if 'desc' in sort_dict.keys():
			# desc_lst = sort_dict['desc']
		# desc_lst.sort(key=operator.itemgetter('Layer'))
		# unique_desc = shared.remove_duplicates(desc_lst)
		
		# # Go through each title line and add it to the Excel sheet
		# for idx, line in enumerate(unique_desc):
			# msg = "Saving %s of %s lines to '%s'" % \
					# (idx + 1, len(unique_desc), outxl_fn)
			# shared.print_oneliner(msg)
			
			# # Convert the current line dictionary to cells
			# for k, v in line.items():
				# out_xl.add_cell(v, k)
			
			# out_xl.write_row()
		
		# print
		
		# # Add a keywords table as well
		# out_xl.write_row()
		# out_xl.add_title('Keywords')
		# for theme, words in srch_words.items():
			# value = '%s: %s' % (theme, ', '.join(words[0]))
			# out_xl.add_cell(value, 0)
			# out_xl.write_row()

def main():
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("-j", "--jurisdiction", help="The province or territory to be extracted.",
							metavar="Province or Territory")
		parser.add_argument("-k", "--keyword", help="The keyword(s) to search for.",
							metavar="Keyword")
		parser.add_argument("-p", "--place", help="The place name to narrow the search.",
							metavar="Place Name")
		args = parser.parse_args()

		juris = args.jurisdiction
		keyword = args.keyword
		place = args.place
		
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
			
		if keyword is None:
			answer = raw_input("Please enter keyword(s) to search: ")
			if not answer == "":
				keyword = answer.lower()
			else:
				print "No keyword(s) specified. Please enter keyword(s) next time."
				print "Exiting."
				sys.exit(1)
			
		if place is None:
			answer = raw_input("Please enter a place name to narrow the location of the results: ")
			if not answer == "":
				place = answer.lower()
		
		res_folder = shared.get_results_folder()
		if juris == 'all':
			pt_folders = shared.get_pt_folders()
			for pt in pt_folders:
				juris = os.path.basename(pt.strip('\\'))
				if not juris == "Canada":
					print "\nRunning Analysis for %s" % juris
					xl_fn = os.path.join(os.sep, pt, "_%s_merged.xlsx" % juris)
					run(juris, xl_fn, keyword, place)
		else:
			juris = juris.replace(' ', '_')
			xl_fn = os.path.join(os.sep, res_folder, juris, \
									"_%s_merged.xlsx" % juris)
			run(juris, xl_fn, keyword, place)
		
		print "\nFilter completed successfully."

	except Exception, err:
		print 'ERROR: %s\n' % str(err)
		print traceback.format_exc()

if __name__ == '__main__':
	sys.exit(main())