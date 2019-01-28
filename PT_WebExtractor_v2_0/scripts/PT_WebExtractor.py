__author__ = "Kevin Ballantyne"
__credits__ = ["Kevin Ballantyne"]
__version__ = "2.0.0"
__maintainer__ = "Kevin Ballantyne"
__email__ = "kevin.ballantyne@canada.ca"

import os
import sys
import traceback
import argparse
import inspect
import collections

# Import all provincial extractors
# from Alberta_extractor import Extractor as AB
# from Manitoba_extractor import Extractor as MB
# from NB_extractor import Extractor as NB
# from NL_extractor import Extractor as NL
# from NovaScotia_extractor import Extractor as NS
# from Nunavut_extractor import Extractor as NU
# from NWT_extractor import Extractor as NT
# from Ontario_extractor import Extractor as ON
# from PEI_extractor import Extractor as PE
# from Quebec_extractor import Extractor as QC
# from SK_extractor import Extractor as SK
# from Yukon_extractor import Extractor as YT

import Main_Extractor as main_ext
import Canada_extractor as CA
import Alberta_extractor as AB
import BC_extractor as BC
import Manitoba_extractor as MB
import NB_extractor as NB
import NL_extractor as NL
import NovaScotia_extractor as NS
import Nunavut_extractor as NU
import NWT_extractor as NT
import Ontario_extractor as ON
import PEI_extractor as PE
import Quebec_extractor as QC
import SK_extractor as SK
import Yukon_extractor as YT

from common import shared

class Cmd:
	''' Object contains methods used to store information for the command prompt, such as the Extractor and a list of Page Groups,
		and also methods to facilitate command prompt entry.
	'''

	def __init__(self, extractor, page_groups):
		self.extractor = extractor
		self.page_groups = page_groups
		self.province = self.extractor.get_province()
		
		os.system("title P/T Web Extractor - %s" % self.province)

	def get_arg_names(self):
		''' Gets a list of argument names from the pages
		:return: A list of argument names
		'''

		# Get unique list of argument names
		arg_names = [pg.get_id() for pg in self.page_groups]
		
		return arg_names

	def set_shortcuts(self):
		''' Sets the shortcut keys for easier command-line entry
		:return: None
		'''

		self.shortcuts = collections.OrderedDict()
		
		#arg_names = self.get_arg_names()
		#if 'all' in arg_names: arg_names.remove('all')

		for pg in self.page_groups:
			pg_id = pg.get_id()
			pg_title = pg.get_title()
			if pg_id == 'all': continue
			sc_index = 0
			shortcut = pg_id[sc_index]
			prev_chrs = [s[1][1] for s in self.shortcuts.items()]
			#print prev_chrs
			while shortcut in prev_chrs or shortcut == 'h' or shortcut == 'a' \
				and sc_index < len(pg_id):
				sc_index += 1
				shortcut = pg_id[sc_index]

			self.shortcuts[pg_id] = (sc_index, shortcut)

	def get_pg_grp_question(self):
		''' Gets the question for asking the user which page to extract with the proper shortcuts
		:return: The question with the proper shortcuts (capital letters in the options list).
		'''

		# Set the parameters for the question
		opts = []
		for k, v in self.shortcuts.items():
			# Get the title of current page_group shortcut
			for pg in self.page_groups:
				if pg.get_id() == k:
					pg_title = pg.get_title()
					pg_title = pg_title.replace("%s's" % self.province, '')
					pg_title = pg_title.replace(self.province, '')
					pg_title = pg_title.strip()
		
			# Get the index of the shortcut character
			chr_idx = v[0]
			opt_chrs = list(k)
			opt_chrs[chr_idx] = k[chr_idx].upper()
			opt = "%s: %s" % (pg_title, ''.join(opt_chrs))
			opts.append(opt)

		print "\nAvailable Page Groups:"
		for opt in opts:
			print " - %s" % opt
		print " - All"
		#question = "Please enter the page group you would like to extract (%s or All) [all]: " % ', '.join(opts)
		question = "Please enter the page group from above you would like " \
					"to extract [all]: "

		return question

	def determine_pg_grp(self, answer):
		''' Determines which page to extract based on the user's answer.
		:param answer: The answer given by the user
		:return: A list of the proper page objects.
		'''

		chosen_groups = []
		
		# Get a list of the page group names
		pg_grp_names = [pg.get_id() for pg in self.page_groups]
		
		if answer == '' or answer.lower() == 'all' or answer.lower() == 'a':
			#chosen_groups.append('all')
			if self.extractor.get_province() == 'Canada':
				chosen_groups = ['all']
			else:
				chosen_groups = pg_grp_names
		elif answer.lower() == 'help' or answer.lower() == 'h':
			chosen_groups.append('help')
		else:
			answers = answer.split(',')
			for answer in answers:
				answer = answer.strip()
				if answer.lower() in pg_grp_names:
					chosen_groups.append(answer)
				else:
					for k, v in self.shortcuts.items():
						sc_chr = v[1]
						if answer.lower() == sc_chr:
							chosen_groups.append(k)

		return chosen_groups

def main():

	try:
		parser = argparse.ArgumentParser(prog='PT_WebExtractor')
		parser.add_argument("-j", "--juris", help="The province or " \
							"territory to be extracted.", 
							metavar="Province/Territory")
		parser.add_argument("-p", "--page_group", help="The name of the " \
							"page group to extract",
							metavar="Page Group Name")
		# # NOTE: category is for debugging only
		# parser.add_argument("-b", "--subpage", help="The sub-page to " \
							# "extract from within the page group (for " \
							# "debugging only).", metavar="Page Group Sub-Page")
		# parser.add_argument("-w", "--word", help="The key word(s) to " \
							# "search for in a catalogue.",
							# metavar="Catalogue Search Word")
		# parser.add_argument("-f", "--format", help="The format(s) to " \
							# "filter for in a catalogue search.",
							# metavar="Format Catalogue Filter")
		# parser.add_argument("-c", "--category", help="The category to " \
							# "filter for in a catalogue search.",
							# metavar="Category Catalogue Filter")
		# parser.add_argument("-s", "--status", help="The status to filter " \
							# "for in a catalogue search.",
							# metavar="Status Catalogue Filter")
		# parser.add_argument("-t", "--ds_type", help="The type of data " \
							# "filter for a catalogue search.",
							# metavar="Data Type Catalogue Filter")
		# parser.add_argument("-k", "--keyword", help="The keyword for the " \
							# "Canada Government Portal.",
							# metavar="Keyword Catalogue Filter")
		# parser.add_argument("-d", "--downloadable", action='store_true',
							# help="Determines if searching for downloadable " \
							# "datasets.")
		# parser.add_argument("-a", "--start", help="The record on which to " \
							# "start extraction (for debugging only).", 
							# metavar="Data Type Catalogue Filter")
		# parser.add_argument("-x", "--xl", action='store_true',
							# help="If used, the output will be an Excel " \
							# "spreadsheet (only for Canada).", 
							# default=None)
		# parser.add_argument("-s", "--silent", action='store_true', 
							# help="If used, no extra parameters will be " \
							# "queried.")
		args = parser.parse_args()

		# Switch the args Namespace to a dictionary
		args_dict = vars(args)

		juris = args.juris
		page_group = args.page_group
		#silent = args.silent
		#word = args.word
		#xl = args.xl
		# category = args.category
		# format = args.format
		# status = args.status
		# downloadable = args.downloadable
		# silent = args.silent
		
		debug = False
		answer = ''
		invalid = False
		
		print "\n\n########################################################"\
					"################################"
		print
		print " FGP P/T Web Extractor version 2.0"
		
		while not answer.lower() == 'quit' and \
			not answer.lower() == 'exit':
			
			print
			print "##########################################################"\
					"##############################"
				
			juris = shared.prompt_juris(juris)
			
			if juris is None:
				invalid = False
				continue
			elif juris == 'debug':
				debug = True
				juris = None
				continue
			elif juris == 'help':
				print
				parser.print_help()
				invalid = False
				juris = None
				continue
			elif juris == 'exit':
				print "\nExiting P/T Web Extractor."
				sys.exit(0)
			# elif answer.lower() == 'reset':
				# print "\nResetting P/T Web Extractor."
				# invalid = False
				# juris = None
				# continue
				
			# Get the proper PT_Extractor object
			pt_abbr = shared.get_pt_abbreviation(juris)
			#print '%s.PT_Extractor()' % pt_abbr
			print "\nProvince/Territory: %s" % juris
			pt_ext = eval('%s.PT_Extractor()' % pt_abbr)

			page_groups = pt_ext.get_pg_grps()
			
			pt_ext.set_debug(debug)

			cmd = Cmd(pt_ext, page_groups)

			cmd.set_shortcuts()

			if page_group is None:
				answer = raw_input(cmd.get_pg_grp_question())
				if answer.lower() == 'quit' or answer.lower() == 'exit':
					print "\nExiting P/T Web Extractor."
					sys.exit(0)
				elif answer.lower() == 'reset':
					print "\nResetting P/T Web Extractor."
					invalid = False
					juris = None
					continue
				pg_ans = cmd.determine_pg_grp(answer)
			else:
				print "\nPage Group: %s" % page_group
				pg_ans = cmd.determine_pg_grp(page_group)

			if len(pg_ans) == 0:
				print "\nERROR: No valid page group was chosen."
				#print "Exiting extraction."
				invalid = False
				juris = None
				page_group = None
				continue

			if pg_ans[0] == 'help':
				print
				parser.print_help()
				invalid = False
				juris = None
				page_group = None
				continue
				
			#print "pg_ans: %s" % pg_ans
			#answer = raw_input("Press enter...")

			# Set the list of page groups which will be run
			pg_ans = [page_group.lower() for page_group in pg_ans]
			pt_ext.set_run_pg_grps(pg_ans)
			
			# Keep track of the search word
			srch_wrd = None
			#xl_choice = None
			
			# Keep track of arguments already asked
			used_args = []
			
			for pgrp_name in pg_ans:
				if invalid:
					# If the user entered an invalid value, this is used
					#	to exit the process
					break
					
				# Get the page group
				pg_grp = pt_ext.get_pg_grp(pgrp_name)
			
				# Get a list of the arguments for the specified page group
				pg_args = pg_grp.get_args()
				
				#print "List of arguments for %s: %s" % (pgrp_name, pg_args)
				#answer = raw_input("Press enter...")
				
				# if args_dict['silent']:
					# # If silent mode, don't ask any questions
					# #	but set the values entered in the batch file
					
					# for a in pg_args:
						# arg_name = a.get_name()
						# #a.set_method(page_group)
						# if a.name in args_dict.keys():
							# a.set_value(args_dict[a.name])
					
					# continue
					
				for a in pg_args:
					if invalid:
						break
				
					a_val = a.get_value()
					a_name = a.get_name()
					#a.set_method(page_group)
					
					skip = False
					for used_arg in used_args:
						if a_name == used_arg[0]:
							# If the argument has already been asked, 
							#	use existing value
							a.set_value(used_arg[1])
							skip = True
							break
					
					if not a.is_unique() and skip: continue
					
					if a_val is None:
				
						# For each argument for the current page_group
						question = a.get_question()
						
						if a.is_debug():
							answer = ''
							# If the argument is for debug only,
							#	only prompt user if debug=True
							if debug:
								answer = raw_input("\n%s: " % question)
								if answer.lower() == 'quit' or answer.lower() == 'exit':
									print "\nExiting P/T Web Extractor."
									sys.exit(0)
								elif answer.lower() == 'help':
									print
									parser.print_help()
									invalid = False
									juris = None
									page_group = None
									continue
								elif answer.lower() == 'reset':
									print "\nResetting P/T Web Extractor."
									invalid = True
									juris = None
									page_group = None
									break
								
								# Set the value
								if not a.set_value(answer):
									# The set value returns False 
									#	if the answer is not valid.
									print "No valid option was entered."
									print "Exiting process."
									invalid = True
									break
								
								# Add the argument name and value to the used_args
								used_args.append((a_name, a.get_value()))
							
							continue
						
						# Ask the user for answer to question
						answer = raw_input("\n%s: " % question)
						if answer.lower() == 'quit' or answer.lower() == 'exit':
							print "\nExiting P/T Web Extractor."
							sys.exit(0)
						elif answer.lower() == 'help':
							print
							parser.print_help()
							invalid = False
							juris = None
							page_group = None
							continue
						elif answer.lower() == 'reset':
							print "\nResetting P/T Web Extractor."
							invalid = True
							juris = None
							page_group = None
							break
						
						# Set the value
						if not a.set_value(answer):
							# The set value returns False 
							#	if the answer is not valid.
							print "No valid option was entered."
							print "Exiting process."
							invalid = True
							break
						
						# Add the argument name and value to the used_args
						used_args.append((a_name, a.get_value()))
						
			if invalid:
				# Reset parameters
				invalid = False
				juris = None
				pgrp_name = None
				page_group = None
				continue
						
			# Ask whether the output should be Excel
			#if not args_dict['silent']:
			if juris == 'Canada':
				answer = raw_input("\nWould you like the results in an " \
								"Excel spreadsheet? (yes/no) [no]: ")
				if answer.lower() == 'quit' or answer.lower() == 'exit':
					print "\nExiting P/T Web Extractor."
					sys.exit(0)
				elif answer.lower() == 'help':
					print
					parser.print_help()
					invalid = False
					juris = None
					page_group = None
					continue
				elif answer.lower() == 'reset':
					print "\nResetting P/T Web Extractor."
					invalid = False
					juris = None
					continue
				if answer.lower().find('y') > -1:
					pt_ext.set_xl(True)
			# else:
				# if xl.lower().find('y') > -1 or \
					# xl.lower().find('t') > -1:
					# pt_ext.set_xl(True)

			pt_ext.run()
			
			print "\nExtraction completed successfully."
			
			if len(sys.argv) > 1:
				break
			
			# Reset parameters
			invalid = False
			juris = None
			page_group = None

	except Exception, err:
		#ext.print_log('ERROR: %s\n' % str(err))
		#ext.print_log(traceback.format_exc())
		#ext.close_log()
		print '\nERROR: %s\n' % str(err)
		print traceback.format_exc()
		answer = raw_input("Press enter...")

if __name__ == '__main__':
	sys.exit(main())