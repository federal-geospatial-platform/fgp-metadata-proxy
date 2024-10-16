import os
import sys
import argparse
import glob
import traceback
import codecs
import fileinput
import datetime
import time
import dateutil.parser as parser
import csv
import collections
import re
from StringIO import StringIO

home_folder = os.path.abspath(os.path.join(__file__, "..\\..\\.."))
scripts_folder = os.path.join(os.sep, home_folder, 'scripts')
sys.path.append(scripts_folder)

from common import shared
from common import spreadsheet as sh

# def remove_duplicates(in_fn, out_fn):
	
	# # Open input and output CSV
	# in_f = codecs.open(in_fn, encoding='utf-8', mode='r')
	# out_f = codecs.open(out_fn, encoding='utf-8', mode='w')
	
	# lines = in_f.readlines()
	# print "Number of lines: %s" % len(lines)
	# out_lines = set()
	# for l in lines:
		
		# if l not in out_lines:
			# out_lines.add(l)
			
	# for l in out_lines:
		# out_f.write(l)
		
	# in_f.close()
	# out_f.close()
			
def clean_updates(csv_fn):

	# Remove items that are in Ontario's updated data catalogue CSV
	update_lines = []
	csv_f = codecs.open(csv_fn, encoding='utf-8', mode='rb')
	lines = csv_f.readlines()
	for l in lines:
		split_line = l.split(',')
		if split_line[0].find('Ontario_Discovering_Update') > -1 or split_line[0].find('DataDistributionCatalogue') > -1:
			update_lines.append((split_line, l))
			
	csv_f.close()
	
	#for ul in update_lines:
	#	print ul
	
	for idx, line in enumerate(fileinput.FileInput(csv_fn, inplace=1)):
	
		msg = "Replacing Ontario Discovery with updates: %s of %s lines" % (idx + 1, len(lines))
		shared.print_oneliner(msg)
	
		#print "line %s" % idx
	
		# Split the line by ','
		split_line = line.split(',')
		
		found = False
		
		if split_line[0].find('Ontario_Discovering_Update') == -1 or \
			split_line[0].find('DataDistributionCatalogue') > -1:
		
			# Remove first column from the line for duplicate check
			check_line = ','.join(split_line[1:2])
			
			for ul, orig_line in update_lines:
				ul_str = ','.join(ul[1:2])
				
				ul_str = shared.filter_unicode(ul_str, 'str')
				#ul_str = str(ul_str)
				
				#sys.stderr.write("%s\n" % type(check_line))
				#sys.stderr.write("%s\n" % type(ul_str))
				
				#answer = raw_input("Press enter...")
				
				#ul_str = shared.filter_unicode(ul_str)
				#check_line = shared.filter_unicode(check_line)
				
				if check_line.find('Dispositions') > -1:
					sys.stderr.write("%s|%s\n" % (check_line, ul_str))
					sys.stderr.write(str(check_line == ul_str) + "\n")
				
				if not check_line == ul_str:
					out_line = line
				else:
					out_line = orig_line
					break
				
			print out_line,
					
	print
					
def copy_csv(csv_f, outcsv_file):

	row_lst = []

	# Grab each line in the CSV file
	csv_lines = csv_f.readlines()
	
	total_lines = len(csv_lines)
	
	for idx, line in enumerate(csv_lines[1:]):
		msg = "Copying %s of %s lines" % (idx + 1, len(csv_lines[1:]))
		shared.print_oneliner(msg)
	
		#print line.encode(sys.stdout.encoding, errors='replace')
		items = line.split(',')
		
		csv_bname = os.path.basename(csv_f.name).replace("_results.csv", "")
		out_items = ['"%s"' % csv_bname] + items
		
		out_line = ','.join(out_items)
		
		out_line = shared.filter_unicode(out_line)
		
		outcsv_file.write(out_line)
		
		# Store the title and description in a list
		row_lst.append()
		
	print
	
def get_csv(csv_f):
	
	# Grab each line in the CSV file
	csv_lines = csv_f.readlines()
	
	row_lst = []
	
	header = csv_lines[0].split(',')
	
	for idx, line in enumerate(csv_lines[1:]):
		msg = "Extracting %s of %s lines" % (idx + 1, len(csv_lines[1:]))
		shared.print_oneliner(msg)
		
		# Get the source based on the file
		source = os.path.basename(csv_f.name).replace("_results.csv", "")
		line = '"%s",%s' % (source, line)
		
		# Convert the line to a dictionary
		row_dict = row_to_dict(line, header)
		
		# Store the title and description in a list
		row_lst.append(row_dict)
		
	print
	
	return row_lst
	
def get_recent_date(date1, date2, format='%Y-%m-%d'):
	# Parse and remove anything after the 'T'
	if 'T' in date1:
		date1 = date1.split('T')[0]
	if 'T' in date2:
		date2 = date2.split('T')[0]
	
	try:
		dt_date1 = parser.parse(date1.strip('"'))
	except:
		dt_date1 = datetime.datetime(1900, 1, 1, 0, 0)
		
	#print "dt_date1: %s" % dt_date1
		
	try:
		dt_date2 = parser.parse(date2.strip('"'))
	except:
		dt_date2 = datetime.datetime(1900, 1, 1, 0, 0)
		
	#print "dt_date2: %s" % dt_date2
	
	if int(dt_date1.strftime("%f")) == 0 and int(dt_date2.strftime("%f")) == 0:
		out_date = ''
	
	if int(dt_date1.strftime("%f")) == 0:
		out_date = dt_date2
		
	if int(dt_date2.strftime("%f")) == 0:
		out_date = dt_date1
	
	if dt_date1 > dt_date2:
		out_date = dt_date1.strftime(format)
	else:
		out_date = dt_date2.strftime(format)
		
	#print "out_date: %s" % out_date
	
	return out_date
	
def row_to_dict(row, header):
	# Clean the header if from a file
	header = [h.replace(u'\ufeff', '') for h in header]

	# Convert each row in the row list to a CSV reader object
	try:
		filtered_row = shared.filter_unicode(row, french=True)
		csv_reader = sh.UnicodeReader(StringIO(filtered_row))
		
		entry_lst = [item for item in csv_reader]
	except Exception, e:
		# If an error occurs, filter the row to remove unicode characters
		filtered_row = shared.filter_unicode(row, french=True)
		csv_reader = csv.reader(StringIO(shared.filter_unicode(filtered_row)))
		
		entry_lst = []
		for item in csv_reader:
			print item
			entry_lst.append(item)
			
	entry_lst = entry_lst[0]
	
	# Convert entry to dictionary
	entry_dict = collections.OrderedDict()
	for idx, h in enumerate(header):
		entry_dict[h] = entry_lst[idx]
		
	return entry_dict
	
def find_duplicates(in_rows, header):
	''' Finds the indices of all the duplicate entries
	'''

	dup_indices = []
	
	for idx, row in enumerate(in_rows):
	
		msg = "Find duplicates: %s of %s rows" % (idx + 1, len(in_rows))
		shared.print_oneliner(msg)
		
		#print "row: %s" % row
	
		title = row['Title']
		desc = row['Description']
		
		idx_lst = [idx]
		
		indices = [i for i, x in enumerate(in_rows) if x['Title'] == title \
					and x['Description'][:100] == desc[:100]]
		
		if len(indices) > 1:
			dup_indices.append(indices)
		
	#print dup_indices
	
	print
		
	out_indices = list(set(tuple(i) for i in dup_indices))
	
	return out_indices
	
def remove_duplicates(in_rows, header):
	
	dup_indices = find_duplicates(in_rows, header)
	
	for i in dup_indices:
		if len(i) > 2:
			print i
	
def merge_duplicates(row_lst, header):
	
	# Create the titles and descriptions to keep track of
	#	what has already been seen
	# These lists will contain tuples with the current row index as
	#	the first entry and the value as the second
	seen_lst = []
	dup_indices = []
	
	for idx, row in enumerate(row_lst):
		msg = "Checking for duplicates: %s of %s lines" % (idx + 1, len(row_lst))
		shared.print_oneliner(msg)
	
		row_dict = row_to_dict(row, header)
			
		#print entry_dict
		
		#answer = raw_input("Press enter...")
		
		title = row_dict['Title']
		desc = row_dict['Description']
		
		# Check for duplicates based on Title and Description
		for idx, s in enumerate(seen_lst):
			if title == s['Title'] and desc[50:] == s['Description'][50:]:
				#dup_idx = s['Index']
				
				# Merge the two duplicates together:
				# - Use the most recent date
				# - If one cell is blank but the other isn't, use the one
				#		with the value
				
				# Determine the date
				date1 = s['Date']
				date2 = row_dict['Date']
				
				new_date = get_recent_date(date1, date2)
				row_dict['Date'] = '"%s"' % new_date
				
				# Go through each column and determine is the value is empty
				for h in header:
					# Skip the items already checked and updated
					if h == 'Title' or h == 'Description' or h == 'Date' or \
						h == 'Source':
						continue
					
					val1 = s[h]
					val2 = row_dict[h]
					
					#print "\n%s" % h
					#print "val1: %s" % val1
					#print "val2: %s" % val2
					
					# Check to see if the MapServer has a date
					ms_date = re.search('\d{4}\d{2}\d{2}', val1)
					
					if ms_date is not None:
						# Get the most recent MapServer dataset
						ms_date1 = re.search('\d{4}\d{2}\d{2}', val1)
						ms_date2 = re.search('\d{4}\d{2}\d{2}', val2)
						
						#print "ms_date1: %s" % ms_date1
						#print "ms_date2: %s" % ms_date2
					
						ms_newdate = get_recent_date(ms_date1.group(0), 
													ms_date2.group(0), 
													'%Y%m%d')
						
						if val1.find(ms_newdate) > -1:
							ms_newest = val1
						else:
							ms_newest = val2
							
						#print ms_newest
					
						#answer = raw_input("Press enter...")
					
					new_val = '"%s"' % val1
					if val1.strip('"').strip() == '':
						new_val = val2
					if val2.strip('"').strip() == '':
						new_val = val1
						
					#print "new_val: %s" % new_val
						
					row_dict[h] = new_val
					
				dup_indices.append(idx)
				
				#answer = raw_input("Press enter...")
				
				break
		
		# Add the current row dictionary to the seen list
		#entry_dict['Index'] = idx
		seen_lst.append(row_dict)
		
	print
	
	# FOR DEBUG ONLY:
	out_f = codecs.open('all_rows.txt', encoding='utf-8', mode='w')
	for s in seen_lst:
		row_lst = s.values()
		out_f.write("%s\n" % '\t'.join(row_lst))
	out_f.write('%s' % ", ".join([str(d) for d in dup_indices]))
	out_f.close()
	
	print dup_indices
	
	# Remove any duplicates from the seen list
	out_list = []
	for idx, row in enumerate(seen_lst):
		if idx not in dup_indices:
			out_list.append(row)
		
	print len(out_list)
	
	return out_list
	
def remove_duplicates_old(csv_fn):
	# seen = set() # set for fast O(1) amortized lookup
	
	# for line in fileinput.FileInput(csv_fn, inplace=1):
	
		# # Split the line by ','
		# split_line = line.split(',')
		# # Remove first column from the line for duplicate check
		# check_line = ','.join(split_line[1:])
	
		# if check_line not in seen:
			
			# seen.add(check_line)
			# print line,
			
	print csv_fn
			
	# Open the CSV and add all lines to a list
	csv_f = codecs.open(csv_fn, encoding='utf-8', mode='rb')
	
	# Read the lines from the merged file
	lines = csv_f.readlines()
	
	# Get the header from the first line in the file
	header = lines[0].strip().split(',')
	
	# The output lines converted to dictionaries
	out_lines = []
	# Any lines that don't contain the same number 
	#	of columns as the header
	extra_lines = []
	
	# For Debugging:
	#tmp_lines = []
	indices = []
	
	# Go through each line to convert it to a dictionary
	f = codecs.open('err.txt', encoding='utf-8', mode='w')
	for idx, row in enumerate(lines[1:]):
		msg = "Checking for duplicates: %s of %s lines" % (idx + 1, len(lines[1:]))
		shared.print_oneliner(msg)
		
		try:
			row = shared.filter_unicode(row, french=True)
			csv_reader = sh.UnicodeReader(StringIO(row))
			
			row_lst = [item for item in csv_reader]
		except Exception, e:
			# If an error occurs, filter the row to remove unicode characters
			csv_reader = csv.reader(StringIO(shared.filter_unicode(row)))
			#row_lst = [item for item in csv_reader]
			row_lst = []
			for item in csv_reader:
				print item
				row_lst.append(item)
				
		#print "row_lst: %s" % row_lst
		
		#answer = raw_input("Press enter...")
		
		# Grab the first item which contains the CSV row
		row_csv = row_lst[0]
			
		if len(row_csv) == 0:
			continue
		elif len(row_csv) == len(header):
			line_dict = collections.OrderedDict()
			
			# Convert the current row to a dictionary
			#	with the header as keys
			for idx, h in enumerate(header):
				line_dict[h] = row_csv[idx]
				
			# Get the title and description of the current row
			title_str = line_dict['Title']
			desc_str = line_dict['Description']
			
			#out_dict = line_dict
			
			# Get the index of any titles and descriptions
			#	which are the same as the current line
			title_found = [i for i, r in enumerate(out_lines) \
							if r[1] == title_str]
			#desc_found = [i for i, r in enumerate(out_lines) \
			#				if r['Description'][:100] == desc_str[:100]]
			
			title_idx = -2
			# desc_idx = -1
			if len(title_found) > 0: title_idx = int(title_found[0])
			# if len(desc_found) > 0: desc_idx = desc_found[0]
			
			out_dict = collections.OrderedDict()
			if title_idx > -1 and title_idx < len(out_lines):
				if desc_str[:100] == out_lines[title_idx]['Description'][:100]:
					#print "Title Index: %s" % title_idx
					#print "Desc Index: %s" % desc_idx
					
					for h in header:
						val1 = line_dict[h]
						val2 = out_lines[title_idx][h]
							
						if h == 'Date':
							#print val1
							#print val2
							
							if 'T' in val1:
								val1 = val1.split('T')[0]
							if 'T' in val2:
								val2 = val2.split('T')[0]
								
							#print "First date: %s" % val1
							#print "Second date: %s" % val2
							
							try:
								date1 = parser.parse(val1.strip('"'))
							except:
								date1 = datetime.datetime(1900, 1, 1, 0, 0)
								
							try:
								date2 = parser.parse(val2.strip('"'))
							except:
								date2 = datetime.datetime(1900, 1, 1, 0, 0)
							
							if int(date1.strftime("%f")) == 0 and int(date2.strftime("%f")) == 0:
								out_dict[h] = ''
								continue
							
							if int(date1.strftime("%f")) == 0:
								out_dict[h] = date2
								continue
								
							if int(date2.strftime("%f")) == 0:
								out_dict[h] = date1
							
							if date1 > date2:
								out_dict[h] = date1.strftime('%Y-%m-%d')
							else:
								out_dict[h] = date2.strftime('%Y-%m-%d')
							#except Exception, e:
							#	out_dict[h] = val1
								
						else:
							out_dict[h] = val1
							
							#print "val1: %s" % val1
							#print "val2: %s" % val2
							
							if val1.strip('"').strip() == '':
								out_dict[h] = val2
							if val2.strip('"').strip() == '':
								out_dict[h] = val1
								
							#print "final val: %s" % out_dict[h]
						
					
					# For Debug:
					prev_dict = out_lines[title_idx]
					
					#print "Popping entry: %s" % title_idx
					out_lines.pop(title_idx)
					
					# For debug only
					#tmp_lines.append((title_idx, prev_dict))
					#tmp_lines.append((len(out_lines), line_dict))
					indices.append((title_idx, len(out_lines)))
					
					#answer = raw_input("Press enter...")
				else:
					out_row = ','.join(['"%s"' % v.replace('"', '""') for v in line_dict.values()])
			else:
				out_row = ','.join(['"%s"' % v.replace('"', '""') for v in line_dict.values()])
			
			#if out_row.find('Health Indicator - BMI') > -1:
			#	print "\n%s" % shared.filter_unicode(out_row)
			#	answer = raw_input("Press enter...")
			
			out_lines.append(out_row)
		else:
			extra_lines.append(row_csv)
	
	print
	
	f.close()
	
	all_lines = out_lines + extra_lines
	
	out_csv = csv_fn.replace('.csv', '_filtered.csv')
	out_f = codecs.open(out_csv, encoding='utf-8', mode='w')
	
	out_f.write('%s\n' % ','.join(header))
	
	for idx, line in enumerate(all_lines):
		try:
			#if isinstance(line, dict):
			#	out_f.write('%s\n' % ','.join(line.values()))
			#else:
			out_f.write('%s\n' % line)
		except Exception, e:
			print e
			print "Index: %s" % idx
			print line
			answer = raw_input("Press enter...")
			
	out_f.close()
	csv_f.close()
	
	# Replace the merged file with the filtered one
	os.remove(csv_fn)
	os.rename(out_csv, csv_fn)
	
def run(juris):
	''' Merges all the CSV files in a province/territory to a single CSV file
	:param juris: The province/territory to merge.
	'''
	
	work_folder = shared.get_home_folder() + '\\results\\%s' % juris.replace(" ", "_")
	
	header = ['Source', 'Title', 'Description', 'Type', 'Date', 'Publisher',
			   'Licensing', 'Available Formats', 'Access', 'Download',
			   'Web Page URL', 'Web Map URL', 'Data URL',
			   'Spatial Reference', 'Service', 'Service Name', 'Service URL',
			   'Metadata URL', 'Metadata Type', 'Notes']
			   
	# Open the CSV file
	outcsv_fn = "%s\\_%s_merged.csv" % (work_folder, juris.replace(" ", "_"))
	outcsv_file = codecs.open(outcsv_fn, encoding='utf_8', mode='w')
	
	# Write the header
	outcsv_file.write(','.join(header) + "\n")
	
	# Get a list of the CSV files
	csv_files = glob.glob(work_folder + "\\*.csv")
	
	# Find the location of the 'err_log.csv' file and move it to the end of the file list
	err_log = [(idx, fn) for idx, fn in enumerate(csv_files) if fn.find('err_log') > -1]
	if len(err_log) > 0:
		csv_files.append(csv_files.pop(err_log[0][0]))
	
	csv_count = len(csv_files)
	
	items_lst = []
	
	# Go through each CSV file
	row_lst = []
	for idx, csv_fn in enumerate(csv_files[:csv_count - 2]):
	
		print "\nCopying '%s':" % os.path.basename(csv_fn)
	
		# Avoid a merged file if it exists
		if csv_fn.find('merged') > -1: continue
		
		if csv_fn.find('duplicate') > -1: continue
		
		csv_f = codecs.open(csv_fn, encoding='utf-8', mode='r')
	
		# Store the rows in a list
		row_lst += get_csv(csv_f)
		
		csv_f.close()
		
	# Merge any duplicate records
	dup_tuples = find_duplicates(row_lst, header)
	all_dups = [x for t in dup_tuples for x in t]
	
	merged_rows = merge_duplicates(new_list, dup_tuples)
	merged_indices = [v[0] for v in merged_rows]
	
	# Go through each item in the new_list, ignore duplicates indices
	final_rows = []
	for idx, row in enumerate(new_list):
		if idx in merged_indices:
			# If the current index is contained in the merged_rows,
			#	make the output row the merged row
			new_row = [v[1] for v in merged_rows if v[0] == idx][0]
			final_rows.append(new_row)
		else:
			if idx not in all_dups:
				# If the current index is not part of a duplicate,
				#	make the output row the original row
				new_row = row
				final_rows.append(new_row)
				
	wr = csv.writer(outcsv_f, dialect='excel')
	for row in final_rows:
		# Change the order of the new row before adding item
		ordered_row = [row[h] for h in header]
		
		wr.writerow(ordered_row)
		
	outcsv_f.close()
	
	if juris == 'Ontario':
		#print "yo"
		clean_updates(outcsv_fn)

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
				
		if juris.lower() == 'canada' or juris.lower() == 'ca':
			juris = 'Canada'
		elif juris.lower() == 'alberta' or juris.lower() == 'ab':
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
		elif answer.lower() == 'help' or answer.lower().find('h') > -1:
			parser.print_help()
			sys.exit(1)
		else:
			print "\nERROR: '%s' is not a valid province or territory."
			print "Exiting process."
			sys.exit(1)

		run(juris)
		
		print "\nMerge completed successfully."

	except Exception, err:
		print 'ERROR: %s\n' % str(err)
		print traceback.format_exc()

if __name__ == '__main__':
	sys.exit(main())