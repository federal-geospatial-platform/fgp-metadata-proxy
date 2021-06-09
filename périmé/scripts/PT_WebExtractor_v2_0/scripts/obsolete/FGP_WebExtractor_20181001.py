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

class Cmd:
	''' Object contains methods used to store information for the command prompt, such as the Extractor and a list of Page Groups,
		and also methods to facilitate command prompt entry.
	'''

	def __init__(self, extractor, page_groups):
		self.extractor = extractor
		self.page_groups = page_groups
		
		os.system("title FGP Web Extractor - %s" % self.extractor.get_province())

	def get_arg_names(self):
		''' Gets a list of argument names from the pages
		:return: A list of argument names
		'''

		return self.page_groups.keys()

	def set_shortcuts(self):
		''' Sets the shortcut keys for easier command-line entry
		:return: None
		'''

		self.shortcuts = collections.OrderedDict()

		for k in self.page_groups.keys():
			sc_index = 0
			shortcut = k[sc_index]
			prev_chrs = [s[1][1] for s in self.shortcuts.items()]
			#print prev_chrs
			while shortcut in prev_chrs or shortcut == 'h' and sc_index < len(k):
				sc_index += 1
				shortcut = k[sc_index]

			self.shortcuts[k] = (sc_index, shortcut)

	def get_pg_grp_question(self):
		''' Gets the question for asking the user which page to extract with the proper shortcuts
		:return: The question with the proper shortcuts (capital letters in the options list).
		'''

		# Get the argunement names
		arg_names = self.get_arg_names()

		# Set the parameters for the question
		opts = []
		for k, v in self.shortcuts.items():
			# Get the index of the shortcut character
			chr_idx = v[0]
			opt_chrs = list(k)
			opt_chrs[chr_idx] = k[chr_idx].upper()
			opt = ''.join(opt_chrs)
			opts.append(opt)

		question = "Please enter the page group you would like to extract (%s or all) [all]: " % ', '.join(opts)

		return question

	def determine_pg_grp(self, answer):
		''' Determines which page to extract based on the user's answer.
		:param answer: The answer given by the user
		:return: A list of the proper page objects.
		'''

		page_groups = []
		if answer == '' or answer.lower() == 'all':
			page_groups.append('all')
		elif answer.lower() == 'help' or answer.lower().find('h') > -1:
			page_groups.append('help')
		else:
			answers = answer.split(',')
			for answer in answers:
				answer = answer.strip()
				if answer in self.page_groups.keys():
					page_groups.append(answer)
				else:
					for k, v in self.shortcuts.items():
						sc_chr = v[1]
						if answer == sc_chr:
							page_groups.append(k)

		return page_groups

def main():

	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("-j", "--jurisdiction", help="The province or " \
							"territory to be extracted.", 
							metavar="Province or Territory")
		parser.add_argument("-p", "--page_group", help="The name of the " \
							"page group to extract",
							metavar="Page Group Name")
		# NOTE: category is for debugging only
		parser.add_argument("-b", "--subpage", help="The sub-page to " \
							"extract from within the page group (for " \
							"debugging only).", metavar="Page Group Sub-Page")
		parser.add_argument("-w", "--word", help="The key word(s) to " \
							"search for in a catalogue.",
							metavar="Catalogue Search Word")
		parser.add_argument("-f", "--format", help="The format(s) to " \
							"filter for in a catalogue search.",
							metavar="Format Catalogue Filter")
		parser.add_argument("-c", "--category", help="The category to " \
							"filter for in a catalogue search.",
							metavar="Category Catalogue Filter")
		parser.add_argument("-s", "--status", help="The status to filter " \
							"for in a catalogue search.",
							metavar="Status Catalogue Filter")
		parser.add_argument("-t", "--ds_type", help="The type of data " \
							"filter for a catalogue search.",
							metavar="Data Type Catalogue Filter")
		parser.add_argument("-k", "--keyword", help="The keyword for the " \
							"Canada Government Portal.",
							metavar="Keyword Catalogue Filter")
		parser.add_argument("-d", "--downloadable", action='store_true',
							help="Determines if searching for downloadable " \
							"datasets.")
		parser.add_argument("-a", "--start", help="The record on which to " \
							"start extraction (for debugging only).",
							metavar="Data Type Catalogue Filter")
		parser.add_argument("-x", "--xl", action='store_true',
							help="If used, the output will be an Excel " \
							"spreadsheet (only for Canada).", 
							default=None)
		parser.add_argument("-l", "--silent", action='store_true',
							help="If used, no extra parameters will be " \
							"queried.")
		args = parser.parse_args()

		# Switch the args Namespace to a dictionary
		args_dict = vars(args)

		juris = args.jurisdiction
		page_group = args.page_group
		# category = args.category
		# word = args.word
		# format = args.format
		# status = args.status
		# downloadable = args.downloadable
		# silent = args.silent
		
		debug = False
		answer = 'debug'

		while answer == "debug":
			if juris is None:
				answer = raw_input("\nPlease enter a province or territory " \
									"for extraction (full name or 2-letter "
								   "abbreviation): ")
				if answer == "debug":
					print "\nEntering debug mode."
					debug = True
					continue
				if not answer == "":
					juris = answer.lower()
				else:
					print "\nERROR: Please specify a province or territory."
					print "Exiting process."
					sys.exit(1)

		if juris.lower() == 'canada' or juris.lower() == 'ca':
			pt_ext = CA.PT_Extractor()
		elif juris.lower() == 'alberta' or juris.lower() == 'ab':
			pt_ext = AB.PT_Extractor()
		elif juris.lower() == 'british columbia' or juris.lower() == 'bc':
			pt_ext = BC.PT_Extractor()
		elif juris.lower() == 'manitoba' or juris.lower() == 'mb':
			pt_ext = MB.PT_Extractor()
		elif juris.lower() == 'new brunswick' or juris.lower() == 'nb':
			pt_ext = NB.PT_Extractor()
		elif juris.lower().find('newfoundland') > -1 or \
				juris.lower().find('labrador') > -1 or juris.lower() == 'nl':
			pt_ext = NL.PT_Extractor()
		elif juris.lower() == 'nova scotia' or juris.lower() == 'ns':
			pt_ext = NS.PT_Extractor()
		elif juris.lower() == 'nunavut' or juris.lower() == 'nu':
			pt_ext = NU.PT_Extractor()
		elif juris.lower().find('northwest') > -1 or juris.lower() == 'nt':
			pt_ext = NT.PT_Extractor()
		elif juris.lower() == 'ontario' or juris.lower() == 'on':
			pt_ext = ON.PT_Extractor()
		elif juris.lower().find('edward') > -1 or juris.lower() == 'pe':
			pt_ext = PE.PT_Extractor()
		elif juris.lower() == 'quebec' or juris.lower() == 'qc':
			pt_ext = QC.PT_Extractor()
		elif juris.lower() == 'saskatchewan' or juris.lower() == 'sk':
			pt_ext = SK.PT_Extractor()
		elif juris.lower() == 'yukon' or juris.lower() == 'yt' or \
				juris.lower() == 'yk':
			pt_ext = YT.PT_Extractor()
		elif answer.lower() == 'help' or answer.lower().find('h') > -1:
			parser.print_help()
			sys.exit(1)
		else:
			print "\nERROR: '%s' is not a valid province or territory."
			print "Exiting process."
			sys.exit(1)

		page_groups = pt_ext.get_pg_grps()
		
		pt_ext.set_debug(debug)

		cmd = Cmd(pt_ext, page_groups)

		cmd.set_shortcuts()

		if page_group is None:
			answer = raw_input(cmd.get_pg_grp_question())
			pg_ans = cmd.determine_pg_grp(answer)

		if len(pg_ans) == 0:
			print "\nERROR: No valid page group was chosen."
			print "Exiting extraction."
			sys.exit(1)

		if pg_ans[0] == 'help':
			parser.print_help()
			sys.exit(1)

		# Set the list of page groups which will be run
		pg_ans = [page_group.lower() for page_group in pg_ans]
		pt_ext.set_run_pg_grps(pg_ans)
		
		#print pg_ans
		
		# Keep track of the search word
		srch_wrd = None
		xl_choice = None
		
		for page_group in pg_ans:
			# Go through each page_group in the pg_ans list
			if not args_dict['silent']:
				for k, pg in page_groups.items():
					# Go through each page_group in page_groups
					if page_group == 'all' or pg.get_id() == page_group:
						for arg_k, arg_v in pg.get_args().items():

							# Determine the question to ask the user
							questions = pg.get_questions()
							question = "\n%s: " % questions[arg_k]
							if arg_k in args_dict.keys():
								if args_dict[arg_k] is None:
									# Ask the user for a parameter
									if arg_k == 'subpage':
										# Categories are only asked during debugging
										if debug:
											print
											answer = raw_input(question)
											if not answer == "":
												pg.set_arg(arg_k, answer)
											elif answer.lower() == 'help' or \
												answer.lower().find('h') > -1:
												parser.print_help()
												sys.exit(1)
									elif arg_k == 'start':
										if debug:
											print
											answer = raw_input("What dataset " \
														"would you like to " \
														"start the extraction?: ")
											if not answer == "":
												pg.set_arg(arg_k, answer)
											elif answer.lower() == 'help' or \
												answer.lower().find('h') > -1:
												parser.print_help()
												sys.exit(1)
									elif arg_k == 'word':
										if srch_wrd is None:
											# Ask the user for input
											print
											answer = raw_input(question)
											if not answer == "":
												pg.set_arg(arg_k, answer)
											elif answer.lower() == 'help' or \
												answer.lower().find('h') > -1:
												parser.print_help()
												sys.exit(1)
											srch_wrd = answer
										else:
											pg.set_arg(arg_k, srch_wrd)
									elif arg_k == 'xl':
										if xl_choice is None:
											print
											answer = raw_input("Would you " \
													"like the output to be " \
													"an Excel spreadsheet? " \
													"[no]: ")
											if answer.lower().find('y') > -1:
												xl_choice = True
												pg.set_arg(arg_k, xl_choice)
											else:
												xl_choice = False
												pg.set_arg(arg_k, xl_choice)
										else:
											pg.set_arg(arg_k, xl_choice)
									else:
										# Ask the user for input
										print
										answer = raw_input(question)
										if not answer == "":
											pg.set_arg(arg_k, answer)
										elif answer.lower() == 'help' or \
											answer.lower().find('h') > -1:
											parser.print_help()
											sys.exit(1)
								else:
									pg.set_arg(arg_k, args_dict[arg_k])
			else:
				for k, pg in page_groups.items():
					for arg_k, arg_v in pg.get_args().items():
						pg.set_arg(arg_k, args_dict[arg_k])

		pt_ext.run()
		
		print "\nExtraction completed successfully."

	except Exception, err:
		#ext.print_log('ERROR: %s\n' % str(err))
		#ext.print_log(traceback.format_exc())
		#ext.close_log()
		print 'ERROR: %s\n' % str(err)
		print traceback.format_exc()

if __name__ == '__main__':
	sys.exit(main())