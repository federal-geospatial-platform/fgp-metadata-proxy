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
	
def get_csv(csv_f, in_header=None):
	
	# Grab each line in the CSV file
	csv_lines = csv_f.readlines()
	
	row_lst = []
	
	#print csv_lines[0].replace(u'\ufeff', '')
	
	#print "\nHeader: %s" % header
	
	if in_header is None:
		in_header = shared.get_header(csv_lines)
		
	#print "\nHeader: %s" % header
	
	for idx, line in enumerate(csv_lines[1:]):
		msg = "Extracting %s of %s lines" % (idx + 1, len(csv_lines[1:]))
		shared.print_oneliner(msg)
		
		#print "header: %s" % header
		
		# Get the source based on the file
		source = os.path.basename(csv_f.name).replace("_results.csv", "")
		dict_header = in_header[:]
		if 'Source' not in in_header:
			line = '"%s",%s' % (source, line)
			#print "line: %s" % line
			# Add the 'Source' to the header
			dict_header.insert(0, 'Source')
				
		#print "header: %s" % header
		
		# Convert the line to a dictionary
		#print "line: %s" % line
		row_dict = row_to_dict(line, dict_header)
		
		if row_dict is None: continue
		
		if row_dict['Source'] == '':
			row_dict = source
		
		# Store the title and description in a list
		row_lst.append(row_dict)
		
	print
	
	return row_lst
	
def row_to_dict(row, header):
	
	#print header
	#answer = raw_input("Press enter...")

	# Convert each row in the row list to a CSV reader object
	try:
		filtered_row = shared.filter_unicode(row, french=True)
		filtered_row = filtered_row.replace('\r', ' ')
		#csv_reader = sh.UnicodeReader(StringIO(filtered_row))
		
		entry_lst = shared.parse_csv_row(filtered_row)
		
		#entry_lst = [item for item in csv_reader]
	except Exception, e:
		# If an error occurs, filter the row to remove unicode characters
		filtered_row = shared.filter_unicode(row, french=True)
		#csv_reader = csv.reader(StringIO(shared.filter_unicode(filtered_row)))
		
		entry_lst = shared.parse_csv_row(filtered_row)
		
	
	if len(entry_lst) == 0:
		print "\n"
		print "\nWARNING: The current row is empty."
		answer = raw_input("Press enter...")
		return None
			
	if not len(entry_lst) == len(header):
		print "\n"
		print
		print "Header: %s" % header
		print
		print "Number of columns: %s" % len(header)
		print
		print "Input Row: %s" % row
		print
		print "Filtered Row: %s" % filtered_row
		print
		print "Entry List: %s" % entry_lst
		print
		print len(entry_lst)
		print "\nWARNING: The current row does not contain the correct " \
				"number of columns."
		answer = raw_input("Press enter...")
	
	# Convert entry to dictionary
	entry_dict = collections.OrderedDict()
	for idx, h in enumerate(header):
		entry_dict[h] = entry_lst[idx]
		
	return entry_dict
	
def run(juris):
	''' Merges all the CSV files in a province/territory to a single CSV file
	:param juris: The province/territory to merge.
	'''
	
	work_folder = shared.get_home_folder() + '\\results\\%s' % juris.replace(" ", "_")
	
	os.system("title Merging PT XLs - %s" % juris)
	
	#csv_header = ['Title', 'Description', 'Type', 'Start Date', 'Recent Date', 
	#			'Update Frequency', 'Publisher',
	#			'Licensing', 'Available Formats', 'Access', 'Download',
	#			'Web Page URL', 'Web Map URL', 'Data URL',
	#			'Spatial Reference', 'Service', 'Service Name', 'Service URL',
	#			'Metadata URL', 'Metadata Type', 'Notes']
	csv_header = sh.get_header_info()['csv']
	
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
	dup_tuples = shared.find_duplicates(row_lst)
	all_dups = [x for t in dup_tuples for x in t]
	
	merged_rows = shared.merge_duplicates(row_lst, dup_tuples)
	merged_indices = [v[0] for v in merged_rows]
	
	# Go through each item in the row_lst, ignore duplicates indices
	final_rows = []
	for idx, row in enumerate(row_lst):
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
		
	xl_header = sh.get_header_info()['xl']
	
	outcsv_fn = "%s\\_%s_merged.xlsx" % (work_folder, juris.replace(" ", "_"))
	pt_xl = sh.PT_XL(fn=outcsv_fn, header=xl_header, write_only=True, 
						replace_ws=True, ws_title='Merged Datasets')
	
	for row in final_rows:
		for k, v in row.items():
			#print "%s: %s" % (k, v)
			pt_xl.add_item(k, v)
	
		pt_xl.write_row()
		
		#answer = raw_input("Press enter...")
	
	pt_xl.save_file()

def main():

	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("-j", "--jurisdiction", help="The province or territory to be extracted.",
							metavar="Province or Territory")
		args = parser.parse_args()

		juris = args.jurisdiction
				
		print "\n\n########################################################"\
				"################################"
		print
		print " FGP P/T Web Extractor Merger version 1.1"
		
		answer = ''
		while not answer.lower() == 'quit' and \
			not answer.lower() == 'exit':
		
			answer = 'debug'
			
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
				print "\nExiting P/T Web Extractor Merger."
				sys.exit(0)

			run(juris)
			
			print "\nMerge completed successfully."
			
			# Reset parameters
			juris = None

	except Exception, err:
		print 'ERROR: %s\n' % str(err)
		print traceback.format_exc()

if __name__ == '__main__':
	sys.exit(main())
	
# def merge_duplicates(row_lst, header):
	
	# # Create the titles and descriptions to keep track of
	# #	what has already been seen
	# # These lists will contain tuples with the current row index as
	# #	the first entry and the value as the second
	# seen_lst = []
	# dup_indices = []
	
	# for idx, row in enumerate(row_lst):
		# msg = "Checking for duplicates: %s of %s lines" % (idx + 1, len(row_lst))
		# shared.print_oneliner(msg)
	
		# row_dict = row_to_dict(row, header)
			
		# #print entry_dict
		
		# #answer = raw_input("Press enter...")
		
		# title = row_dict['Title']
		# desc = row_dict['Description']
		
		# # Check for duplicates based on Title and Description
		# for idx, s in enumerate(seen_lst):
			# if title == s['Title'] and desc[50:] == s['Description'][50:]:
				# #dup_idx = s['Index']
				
				# # Merge the two duplicates together:
				# # - Use the most recent date
				# # - If one cell is blank but the other isn't, use the one
				# #		with the value
				
				# # Determine the date
				# date1 = s['Date']
				# date2 = row_dict['Date']
				
				# new_date = get_recent_date(date1, date2)
				# row_dict['Date'] = '"%s"' % new_date
				
				# # Go through each column and determine is the value is empty
				# for h in header:
					# # Skip the items already checked and updated
					# if h == 'Title' or h == 'Description' or h == 'Date' or \
						# h == 'Source':
						# continue
					
					# val1 = s[h]
					# val2 = row_dict[h]
					
					# #print "\n%s" % h
					# #print "val1: %s" % val1
					# #print "val2: %s" % val2
					
					# # Check to see if the MapServer has a date
					# ms_date = re.search('\d{4}\d{2}\d{2}', val1)
					
					# if ms_date is not None:
						# # Get the most recent MapServer dataset
						# ms_date1 = re.search('\d{4}\d{2}\d{2}', val1)
						# ms_date2 = re.search('\d{4}\d{2}\d{2}', val2)
						
						# #print "ms_date1: %s" % ms_date1
						# #print "ms_date2: %s" % ms_date2
					
						# ms_newdate = get_recent_date(ms_date1.group(0), 
													# ms_date2.group(0), 
													# '%Y%m%d')
						
						# if val1.find(ms_newdate) > -1:
							# ms_newest = val1
						# else:
							# ms_newest = val2
							
						# #print ms_newest
					
						# #answer = raw_input("Press enter...")
					
					# new_val = '"%s"' % val1
					# if val1.strip('"').strip() == '':
						# new_val = val2
					# if val2.strip('"').strip() == '':
						# new_val = val1
						
					# #print "new_val: %s" % new_val
						
					# row_dict[h] = new_val
					
				# dup_indices.append(idx)
				
				# #answer = raw_input("Press enter...")
				
				# break
		
		# # Add the current row dictionary to the seen list
		# #entry_dict['Index'] = idx
		# seen_lst.append(row_dict)
		
	# print
	
	# # FOR DEBUG ONLY:
	# out_f = codecs.open('all_rows.txt', encoding='utf-8', mode='w')
	# for s in seen_lst:
		# row_lst = s.values()
		# out_f.write("%s\n" % '\t'.join(row_lst))
	# out_f.write('%s' % ", ".join([str(d) for d in dup_indices]))
	# out_f.close()
	
	# print dup_indices
	
	# # Remove any duplicates from the seen list
	# out_list = []
	# for idx, row in enumerate(seen_lst):
		# if idx not in dup_indices:
			# out_list.append(row)
		
	# print len(out_list)
	
	# return out_list
	
# def remove_duplicates_old(csv_fn):
	# # seen = set() # set for fast O(1) amortized lookup
	
	# # for line in fileinput.FileInput(csv_fn, inplace=1):
	
		# # # Split the line by ','
		# # split_line = line.split(',')
		# # # Remove first column from the line for duplicate check
		# # check_line = ','.join(split_line[1:])
	
		# # if check_line not in seen:
			
			# # seen.add(check_line)
			# # print line,
			
	# print csv_fn
			
	# # Open the CSV and add all lines to a list
	# csv_f = codecs.open(csv_fn, encoding='utf-8', mode='rb')
	
	# # Read the lines from the merged file
	# lines = csv_f.readlines()
	
	# # Get the header from the first line in the file
	# header = lines[0].strip().split(',')
	
	# # The output lines converted to dictionaries
	# out_lines = []
	# # Any lines that don't contain the same number 
	# #	of columns as the header
	# extra_lines = []
	
	# # For Debugging:
	# #tmp_lines = []
	# indices = []
	
	# # Go through each line to convert it to a dictionary
	# f = codecs.open('err.txt', encoding='utf-8', mode='w')
	# for idx, row in enumerate(lines[1:]):
		# msg = "Checking for duplicates: %s of %s lines" % (idx + 1, len(lines[1:]))
		# shared.print_oneliner(msg)
		
		# try:
			# row = shared.filter_unicode(row, french=True)
			# csv_reader = sh.UnicodeReader(StringIO(row))
			
			# row_lst = [item for item in csv_reader]
		# except Exception, e:
			# # If an error occurs, filter the row to remove unicode characters
			# csv_reader = csv.reader(StringIO(shared.filter_unicode(row)))
			# #row_lst = [item for item in csv_reader]
			# row_lst = []
			# for item in csv_reader:
				# print item
				# row_lst.append(item)
				
		# #print "row_lst: %s" % row_lst
		
		# #answer = raw_input("Press enter...")
		
		# # Grab the first item which contains the CSV row
		# row_csv = row_lst[0]
			
		# if len(row_csv) == 0:
			# continue
		# elif len(row_csv) == len(header):
			# line_dict = collections.OrderedDict()
			
			# # Convert the current row to a dictionary
			# #	with the header as keys
			# for idx, h in enumerate(header):
				# line_dict[h] = row_csv[idx]
				
			# # Get the title and description of the current row
			# title_str = line_dict['Title']
			# desc_str = line_dict['Description']
			
			# #out_dict = line_dict
			
			# # Get the index of any titles and descriptions
			# #	which are the same as the current line
			# title_found = [i for i, r in enumerate(out_lines) \
							# if r[1] == title_str]
			# #desc_found = [i for i, r in enumerate(out_lines) \
			# #				if r['Description'][:100] == desc_str[:100]]
			
			# title_idx = -2
			# # desc_idx = -1
			# if len(title_found) > 0: title_idx = int(title_found[0])
			# # if len(desc_found) > 0: desc_idx = desc_found[0]
			
			# out_dict = collections.OrderedDict()
			# if title_idx > -1 and title_idx < len(out_lines):
				# if desc_str[:100] == out_lines[title_idx]['Description'][:100]:
					# #print "Title Index: %s" % title_idx
					# #print "Desc Index: %s" % desc_idx
					
					# for h in header:
						# val1 = line_dict[h]
						# val2 = out_lines[title_idx][h]
							
						# if h == 'Date':
							# #print val1
							# #print val2
							
							# if 'T' in val1:
								# val1 = val1.split('T')[0]
							# if 'T' in val2:
								# val2 = val2.split('T')[0]
								
							# #print "First date: %s" % val1
							# #print "Second date: %s" % val2
							
							# try:
								# date1 = parser.parse(val1.strip('"'))
							# except:
								# date1 = datetime.datetime(1900, 1, 1, 0, 0)
								
							# try:
								# date2 = parser.parse(val2.strip('"'))
							# except:
								# date2 = datetime.datetime(1900, 1, 1, 0, 0)
							
							# if int(date1.strftime("%f")) == 0 and int(date2.strftime("%f")) == 0:
								# out_dict[h] = ''
								# continue
							
							# if int(date1.strftime("%f")) == 0:
								# out_dict[h] = date2
								# continue
								
							# if int(date2.strftime("%f")) == 0:
								# out_dict[h] = date1
							
							# if date1 > date2:
								# out_dict[h] = date1.strftime('%Y-%m-%d')
							# else:
								# out_dict[h] = date2.strftime('%Y-%m-%d')
							# #except Exception, e:
							# #	out_dict[h] = val1
								
						# else:
							# out_dict[h] = val1
							
							# #print "val1: %s" % val1
							# #print "val2: %s" % val2
							
							# if val1.strip('"').strip() == '':
								# out_dict[h] = val2
							# if val2.strip('"').strip() == '':
								# out_dict[h] = val1
								
							# #print "final val: %s" % out_dict[h]
						
					
					# # For Debug:
					# prev_dict = out_lines[title_idx]
					
					# #print "Popping entry: %s" % title_idx
					# out_lines.pop(title_idx)
					
					# # For debug only
					# #tmp_lines.append((title_idx, prev_dict))
					# #tmp_lines.append((len(out_lines), line_dict))
					# indices.append((title_idx, len(out_lines)))
					
					# #answer = raw_input("Press enter...")
				# else:
					# out_row = ','.join(['"%s"' % v.replace('"', '""') for v in line_dict.values()])
			# else:
				# out_row = ','.join(['"%s"' % v.replace('"', '""') for v in line_dict.values()])
			
			# #if out_row.find('Health Indicator - BMI') > -1:
			# #	print "\n%s" % shared.filter_unicode(out_row)
			# #	answer = raw_input("Press enter...")
			
			# out_lines.append(out_row)
		# else:
			# extra_lines.append(row_csv)
	
	# print
	
	# f.close()
	
	# all_lines = out_lines + extra_lines
	
	# out_csv = csv_fn.replace('.csv', '_filtered.csv')
	# out_f = codecs.open(out_csv, encoding='utf-8', mode='w')
	
	# out_f.write('%s\n' % ','.join(header))
	
	# for idx, line in enumerate(all_lines):
		# try:
			# #if isinstance(line, dict):
			# #	out_f.write('%s\n' % ','.join(line.values()))
			# #else:
			# out_f.write('%s\n' % line)
		# except Exception, e:
			# print e
			# print "Index: %s" % idx
			# print line
			# answer = raw_input("Press enter...")
			
	# out_f.close()
	# csv_f.close()
	
	# # Replace the merged file with the filtered one
	# os.remove(csv_fn)
	# os.rename(out_csv, csv_fn)