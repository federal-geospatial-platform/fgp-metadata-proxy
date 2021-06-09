__author__ = "Kevin Ballantyne"
__credits__ = ["Kevin Ballantyne"]
__version__ = "1.3.0"
__maintainer__ = "Kevin Ballantyne"
__email__ = "kevin.ballantyne@canada.ca"

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
import shlex
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

class Analysis_Filter:

	def __init__(self, juris, keywrd_fn=None, xl_fn=None, group=None, place=''):
		self.juris = juris
		self.xl_fn = xl_fn
		self.group = group
		self.place = place
		self.keywrd_fn = keywrd_fn
		self.stats_f = None
		self.stats = collections.OrderedDict()
		self.final_res = collections.OrderedDict()
		self.all_stats = collections.OrderedDict()
		
	def set_keywrd_fn(self, keywrd_fn):
		self.keywrd_fn = keywrd_fn
		
	def set_xl_fn(self, xl_fn):
		self.xl_fn = xl_fn
		
	def set_group(self, group):
		self.group = group
		
	def set_place(self, place):
		self.place = place
		
	def build_stats(self, datasets=None):
		out_stats = collections.OrderedDict()
		
		if datasets is None:
			datasets = self.final_res[self.group]
		
		# Get unique list of themes
		themes = [ds['Layer'] for ds in datasets]
		themes = list(set(themes))
		
		print self.keywords
		
		for theme, words in self.keywords.items():
			totals = collections.OrderedDict()
			for wrd in words:
				#chk_wrd = wrd.replace('"', '')
				#print chk_wrd
				count = len([ds['Word Found'] for ds in datasets \
							if ds['Word Found'] == wrd])
				totals[wrd] = count
			out_stats[theme] = totals
			
		return out_stats

	def get_groups(self):
		''' Gets a list of available groups from the input CSV file
		'''

		# Open the CSV and get its lines
		srch_csv = open(self.keywrd_fn, mode='rb')
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
		
		self.groups = groups
		
		return groups

	def get_word_list(self, words, juris, omit=False):
		# Redundant

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
		
	def get_search_words(self):
		''' Gets a list of search words from a CSV file
		:param group: The group abbreviation containing the keywords.
		:param kword_fn: The CSV filename containing a list of keywords.
		'''

		if self.keywrd_fn is not None:
			# If the CSV file is specified, open it
			srch_csv = codecs.open(self.keywrd_fn, encoding='utf-8', mode='rb')
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
			
			# # Extract the text contained within the double-quotes
			# quotes = []
			# start_pos = line.find('"')
			# while start_pos > -1:
				# end_pos = line.find('"', start_pos+1)
				# quote = line[start_pos+1:end_pos]
				# quotes.append(quote)
				# start_pos = line.find('"', end_pos+1)
			
			# if len(quotes) == 0: continue
				
			# # Split and strip quoted text
			# keywords = []
			# for k in quotes:
				# out_k = k.split(',')
				# out_k = [k.strip() for k in out_k]
				# keywords.append(out_k)
			
			# # Get all text before the first quote and split it by commas
			# first_quote = line.find('"')
			# vals = line[:first_quote].split(',')
			
			# if len(vals) > 2:
				# # If the text contains 2 columns
				# #	set the group and theme accordingly
				# group_val = vals[0]
				# theme = vals[1]
			# else:
				# # If the text contains 1 column
				# group_val = vals[0]
				# theme = group_val
				
			# Split by comma
			cols = line.split(',')
			
			if len(cols) > 2:
				group_val = cols[0]
				theme = cols[1]
				keywords = cols[2].split('|')
			else:
				group_val = cols[0]
				theme = group_val
				keywords = cols[1].split('|')
			
			if not self.group == 'all':
				# If the group to be extracted is specified,
				#	add the list of only that group
				if group_val.lower().find(self.group.lower()) > -1:
					srch_words[theme] = keywords
			else:
				srch_words[theme] = keywords
				
		#print srch_words
		
		#answer = raw_input("Press enter...")
			
		return srch_words
		
	def close_stats(self):
		self.stats_f.close()
		
	def open_stats(self):
		self.stats_fn = self.xl_fn.replace('results.xlsx', 'stats.txt')
		self.stats_f = open(self.stats_fn, 'w')
		
	def search_dataset(self, row, idx):
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
		ds_keywrds = row['Keywords']
		ds_keywrds = ds_keywrds.lower()
		
		# If place name provided, check in description
		if self.place is not None and not self.place == '':
			if desc_str.lower().find(self.place.lower()) == -1:
				return None
				
		# If words contain more than 1 entry (contains a second set of keywords)
		# NOTE: currently not used but left in for future use.
		# if len(words) > 1:
			# filter2 = words[1]
			# if search_text(keywords, filter2) is None and \
				# search_text(title_str, filter2) is None and \
				# search_text(desc_str, filter2) is None:
				# # If the second set of keywords is not found in the
				# #	Keywords, Title and Description, return nothing
				# #	for this row
				# return None

		#words = words[0]
		found = False
		# Search for words in the Keywords field
		key_srch = self.search_text(ds_keywrds)
		if key_srch is None:
			# If none of the words were found in the Keywords field
			
			# Search for words in Title field
			title_srch = self.search_text(title_str)
			if title_srch is None:
				# If none of the words were found in the Title field
				
				# Search for words in the description
				desc_srch = self.search_text(desc_str)
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
			
		
	def search_text(self, text):
		''' Searches for a list of keywords in a specified text.
			The search will only find the complete keyword:
			Ex: if the keyword is 'house', the search will not locate
				the word 'household'.
			:param text: The text in which to search.
			:param words: The list of keywords.
		'''
		
		for wrd in self.keywords[self.theme]:
		
			if wrd == '': continue
			
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
				
	def write_stats(self):

		ws_name = 'Stats'
		
		# Move the Stats sheet to the end
		self.out_xl.move_sheet('Stats')
		
		# Get the total for the current group
		grp_total = 0
		theme_totals = collections.OrderedDict()
		#print "stats: %s" % self.stats
		for theme, keywords in self.stats.items():
			theme_total = 0
			for word, val in keywords.items():
				theme_total += val
				grp_total += val
			theme_totals[theme] = theme_total
		#print grp_total
		#answer = raw_input("Press enter...")
		
		# Add Group cell to sheet
		fill = PatternFill("solid", fgColor="CCCCCC")
		font = Font(bold=True)
		alignment = Alignment(horizontal='center', vertical='top')
		grp_val = "%s: %s" % (self.group, grp_total)
		self.out_xl.add_cell(grp_val, ws_name=ws_name, fill=fill, \
							font=font, alignment=alignment)
		self.out_xl.write_row(ws_name)
		
		for theme, th_stats in self.stats.items():
			# Add empty row
			self.out_xl.write_row(ws_name)
			# Add Theme cell to sheet
			theme_val = "%s: %s" % (theme, theme_totals[theme])
			self.out_xl.add_cell(theme_val, ws_name=ws_name, font=font)
			# Add empty row
			self.out_xl.write_row(ws_name)
			for k, v in th_stats.items():
				cell_val = "%s: %s" % (k, v)
				# Add result count to sheet
				self.out_xl.add_cell(cell_val, ws_name=ws_name)
				# Add empty row
				self.out_xl.write_row(ws_name)
				
		# Add 2 empty rows
		self.out_xl.write_row(ws_name)
		self.out_xl.write_row(ws_name)
	
	def process_group(self):
		
		self.juris = self.juris.replace(' ', '_')
		
		os.system("title Analysis Filter - %s" % self.juris)
		
		# Get a list of search words from the filter CSV file
		self.keywords = self.get_search_words()
		
		if not self.keywords:
			# If no search words exist, close spreadsheet and exit.
			print "No search words for that group."
			merged_xl.close_workbook()
			return None
		
		out_lines = collections.OrderedDict()
		
		found_idx = []
		
		# Create the inflect engine to get plurals
		p = inflect.engine()
		
		try:
			
			# Get the proper header info for analyses
			header_info = sh.get_header_info('analysis')['xl']
			
			# Create the worksheet with the group as the sheet name
			group_wsname = '%s' % self.group.title()
			group_ws = self.out_xl.add_worksheet(group_wsname, header_info) #, \
											#'Found in Titles & Keywords')
											
			found_datasets = []
			
			# Create the group_stats
			self.stats = collections.OrderedDict()
		
			for theme, words in self.keywords.items():
				# Go through each list of words
				
				print words
				
				filtered_lines = []
				
				self.theme = theme
				
				# Create the theme's stats
				#theme_stats = collections.OrderedDict()
				
				for idx, row in enumerate(self.merged_rows):
					msg = "Filtering %s of %s lines for search words" % \
							(idx + 1, len(self.merged_rows))
					shared.print_oneliner(msg)
					
					# Go through each line in the merged CSV
					
					# Ignore any datasets that had an error
					if row['Source'] == 'err_log.csv': continue
					
					srch_res = self.search_dataset(row, idx)
					
					if srch_res is not None:
					
						#print "\nSearch results:"
						#print srch_res
						#answer = raw_input("Press enter...")
						
						# Parse the search results
						idx = srch_res[0]
						category = srch_res[2]
						keyword = srch_res[1]
						ds = srch_res[3]
						
						# print
						# print "Category: '%s'" % category
						# print "Keyword: '%s'" % keyword
						# answer = raw_input("Press enter...")
						
						# Add this information to the dataset's row
						ds['Word Found'] = keyword
						ds['Found In'] = category
						ds['Layer'] = theme.title()
						ds['P/T'] = shared.get_pt_abbreviation(self.juris)
						
						# Add them to a list to remove duplicates
						found_datasets.append(ds)
					
						# answer = raw_input("Press enter...")
					
						# cur_lines, cur_found = srch_res
					
						# filtered_lines += cur_lines
						# found_idx += cur_found		

				#self.write_stats(found_datasets, theme)
				# Build stats
				#self.stats[theme] = self.build_stats(found_datasets)
						
				print
				
			unique_lst = shared.remove_duplicates(found_datasets)
			
			unique_lst.sort(key=operator.itemgetter('Title'))
			unique_lst.sort(key=operator.itemgetter('Found In'))
			unique_lst.sort(key=operator.itemgetter('Word Found'))
			unique_lst.sort(key=operator.itemgetter('Layer'))
			
			self.final_res[self.group] = unique_lst
			
			self.stats = self.build_stats()
			
			for ds in unique_lst:
			
				for k, v in ds.items():
					self.out_xl.add_cell(v, k)
			
				self.out_xl.write_row()
				
			self.write_stats()
				
			# save the file
			self.out_xl.save_file()
				
		except Exception, e:
			print e
			traceback.print_exc(file=sys.stdout)
			#out_f.write(unicode(in_line))
			#out_f.write('\n')
			answer = raw_input("Press enter...")
			
	def run(self):
	
		res_folder = shared.get_results_folder()
		if self.group == 'all':
			groups = self.groups
		else:
			groups = [self.group]
			
		# Get the file abbreviation from the CSV filename
		ky_word_fn = os.path.basename(self.keywrd_fn)
		if ky_word_fn.find('CE') > -1:
			out_abbr = 'CE_'
		elif ky_word_fn.find('GB') > -1:
			out_abbr = 'GB3_'
		else:
			out_abbr = ''
			
		if self.place == '' or self.place is None:
			self.outxl_fn = "results\\%s\\%s_%sresults.xlsx" % \
						(self.juris, self.juris, out_abbr)
		else:
			self.outxl_fn = "results\\%s\\%s_%s%sresults.xlsx" % \
						(self.juris, self.juris, self.place, out_abbr)
			
		# Create the Excel file
		self.out_xl = sh.PT_XL(fn=self.outxl_fn, replace_ws=True)
		stats_wsname = 'Stats'
		stats_ws = self.out_xl.add_worksheet('Stats')
		
		# Get a list of all the provinces/territories the user has requested
		pt_folders = []
		if self.juris == 'all':
			pt_folders = shared.get_pt_folders()
		else:
			self.juris = self.juris.replace(' ', '_')
			pt_folder = os.path.join(os.sep, res_folder, self.juris)
			pt_folders.append(pt_folder)
	
		for pt in pt_folders:
			self.juris = self.juris.replace(' ', '_')
			self.xl_fn = os.path.join(os.sep, res_folder, self.juris, \
									"_%s_merged.xlsx" % self.juris)
			# Open merged spreadsheet
			self.merged_xl = sh.PT_XL(fn=self.xl_fn, read_only=True)
			self.merged_xl.set_workbook()
			self.merged_xl.set_worksheet('Merged Datasets')
			
			# Get a list of rows (as dictionaries) from the input spreadsheet
			self.merged_rows = self.merged_xl.get_dictrows('values')
			# Get the header text
			self.header_txts = self.merged_rows[0].keys()
			for grp in groups:
				self.set_group(grp)
				self.process_group()
				self.all_stats[grp] = self.stats
				
			self.merged_xl.close_workbook()
		
			# Add total statistics
			self.total_found = 0
			for group, grp_dict in self.all_stats.items():
				grp_total = 0
				for theme, keywords in grp_dict.items():
					for word, val in keywords.items():
						grp_total += val
				self.total_found += grp_total
			print "\nTotal Records Found: %s of %s" % \
					(self.total_found, len(self.merged_rows))
			self.out_xl.write_row(stats_wsname)
			cell_val = "Total Records Found: %s" % self.total_found
			self.out_xl.add_cell(cell_val, ws_name=stats_wsname)
			self.out_xl.write_row(stats_wsname)
			self.out_xl.save_file()
	
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
		parser.add_argument("-g", "--group", help="The group name (ex: GB3) for the output.",
							metavar="Layer")
		parser.add_argument("-p", "--place", help="The place name used to narrow the results.",
							metavar="Place Name")
		parser.add_argument("-k", "--keywords", help="The file containing the keywords.",
							metavar="Keywords File")
		args = parser.parse_args()

		juris = args.jurisdiction
		keywords = args.keywords
		group = args.group
		place = args.place
		
		print "\n\n########################################################"\
						"################################"
		print
		print " FGP P/T Analysis Filter version 1.1"
		
		answer = ''
		while not answer.lower() == 'quit' and \
			not answer.lower() == 'exit':
		
			print
			print "##########################################################"\
					"##############################"
			
			juris = shared.prompt_juris(juris)
			
			if juris is None: continue
			elif juris == 'help':
				parser.print_help()
				juris = None
				continue
			elif juris == 'exit':
				print "\nExiting P/T Analysis Filter."
				sys.exit(0)
				
			# Get the file with keywords from the user
			script_path = os.path.abspath(__file__)
			init_dir = os.path.dirname(script_path) + "\\files"
			
			if keywords is None:
				root = Tkinter.Tk()
				root.withdraw()
				keywords = tkFileDialog.askopenfilename(initialdir=init_dir, \
									title="Select Keywords File", \
									filetypes=(("CSV files", "*.csv"), 
												("All files", "*.*")))
												
			# If the file does not exist or the user did not enter it,
			#	use the default
			if keywords is None or not os.path.exists(keywords):
				keywords = 'files\\filter_lists.csv'
				# ****** NOTE: add French file for Quebec later **********
				
			# Create Analysis_Filter object
			af = Analysis_Filter(juris, keywords)
			
			# Get a list of available groups from the file
			group_lst = af.get_groups()
			
			avail_grps = '\n - '.join(group_lst)
			
			print group_lst
			
			if group is None:
				# Let the user decide which theme(s) to run
				print '''
Available Group Options:
 - %s
 - all''' % avail_grps
				answer = raw_input("Please enter a group for extraction from the above options [all]: ")
				if answer.lower() == 'quit' or answer.lower() == 'exit':
					print "\nExiting P/T Analysis Filter."
					sys.exit(0)
				if not answer == "":
					group = answer.lower().replace(' ', '_')
				else:
					group = 'all'
			
			avail_grps_lower = [g.lower() for g in group_lst]
			
			if not group.lower() == 'all' and not group.lower() in avail_grps_lower:
				print "Please specify a group from the available options."
				print "Exiting process."
				juris = None
				group = None
				keywords = None
				continue
				
			af.set_group(group)
				
			if place is None:
				answer = raw_input("Please enter a place name to narrow the location of the results: ")
				if answer.lower() == 'quit' or answer.lower() == 'exit':
					print "\nExiting P/T Analysis Filter."
					sys.exit(0)
				if not answer == "":
					place = answer.lower()
				else:
					place = ''
					
			af.set_place(place)
			
			af.run()
			
			print "\nFilter completed successfully."
			
			# Reset parameters
			juris = None
			keywords = None
			group = None
			place = None

	except Exception, err:
		print 'ERROR: %s\n' % str(err)
		print traceback.format_exc()

if __name__ == '__main__':
	sys.exit(main())