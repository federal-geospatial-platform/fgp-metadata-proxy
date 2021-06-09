import os
import sys
import urllib2
from bs4 import BeautifulSoup, Comment
import collections
import math
import csv
import re
import numpy as np
import json
import inspect
import urlparse
import argparse
import traceback
import datetime
import time
import pprint
import codecs
from openpyxl import *
from openpyxl.styles import *

from operator import itemgetter
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options

from common import shared
#from common import access_rest as rest
#from common import page_group
from common import recurse_ftp as rec_ftp

class Ext_Opt:
	""" This class represents an option for an argument (Ext_Arg) in a
		specific Page_Group.
	"""
	
	def __init__(self, name, entry_opts=[], url_tags=[], arg_obj=None, 
					method=None):
		""" The initializer for the Ext_Opt class.
			:param name: The unique option name.
			:param entry_opts: The available options for the user
								to enter in the command-prompt (will also
								include the name as a option).
			:param url_tags: The tags used in the URL query.
			:param arg_obj: The parent Ext_Arg object for the option.
			:param method: The method/page_group of the argument.
		"""
		
		self.name = name
		if entry_opts is None: entry_opts = []
		self.entry_opts = [name] + entry_opts
		self.url_tags = url_tags
		self.arg = arg_obj
		self.method = method
		
	def get_name(self):
		""" Gets the name of the option object.
		"""
		return self.name
		
	def set_name(self, name):
		""" Sets the name of the option object.
		"""
		self.name = name
		
	def get_entryopts(self):
		""" Gets a list of prompting options.
		"""
		return self.entry_opts
		
	def set_entryopts(self, opts):
		""" Sets a list of prompting options.
		"""
		self.entry_opts = opts
		
	def get_urltags(self):
		""" Gets a list of the URL tags.
		"""
		return self.url_tags
		
	def set_urltags(self, tags):
		""" Sets the list of the URL tags.
		"""
		self.url_tags = tags
		
	def get_arg(self):
		""" Gets the argument of the option object.
		"""
		return self.arg
		
	def set_arg(self, arg):
		""" Sets the argument of the option object.
		"""
		self.arg = arg
		
	def get_method(self):
		""" Gets the method/page_group name.
		"""
		return self.method
		
	def set_method(self, method):
		""" Sets the method/page_group name.
		"""
		self.method = method

class Ext_Arg:
	""" This class represents an argument for a specific Page_Group.
	"""

	def __init__(self, arg_name, pg_grp, def_val=None, val=None, \
				debug=False, in_opts=None, title=None, required=False, 
				unique=False):
		""" The initializer for the Ext_Arg class
			:param arg_name: The argument unique ID.
			:param pg_grp: The page_group object of the argument.
			:param def_val: The default value(s) of the argument.
							(The default can be a string or a 
							dictionary with the page groups as keys).
			:param val: The specified value(s) of the argument.
							(It can be a string or a dictionary
							with page groups as keys).
			:param debug: The value used for debug mode.
			:param in_opts: A list of options.
			:param title: The title of the argument.
			:param required: Determines whether the argument is required.
			:param unique: Determines whether the argument is unique.
		"""
				
		self.name = arg_name
		self.default = def_val
		self.value = val
		self.cur_opt = None
		#self.method_list = methlst
		#self.cur_method = None
		self.pg_grp = pg_grp
		self.question = None
		self.debug = debug
		self.title = title
		self.required = required
		self.unique = unique
		
		# Set the default values for each method
		self.default = def_val
		
		# Set the available options for each method
		if in_opts is None: in_opts = []
		self.opts = in_opts
		
		# Set the value for each method
		self.value = val
		
	def add_opt(self, name, entry_opts=[], url_tags=[], arg_obj=None, 
					method=None):
		""" Adds an option to the list of options.
			:param name: The name of the option being added.
			:param entry_opts: The list of options containing the valid
								prompting options.
			:param url_tags: The list URL tags.
			:param arg_obj: The argument object.
			:param method: The method/page_group name.
		"""
		#print entry_opts
		new_opt = Ext_Opt(name, entry_opts, url_tags, arg_obj, method)
		
		self.opts.append(new_opt)
		
		return new_opt
		
	def get_opt(self):
		""" Gets the current option.
		""" 
		return self.cur_opt
		
	def set_opt(self):
		""" Sets the current option.
		"""
		if not self.value == '':
			for opt in self.opts:
				entryopts = opt.get_entryopts()
				#print "entryopts: %s" % entryopts
				if self.value in entryopts:
					self.cur_opt = opt
					
	def get_optname(self):
		""" Gets the current option name.
		"""
		if self.cur_opt is not None:
			return self.cur_opt.get_name()
		
	def get_opts(self): #, method=None):
		""" Gets a list of the options.
		"""
		return self.opts
		
	def set_opts(self, opts):
		""" Sets a list options for the argument.
		"""
		self.opts = opts
		
	def get_default(self):
		""" Gets the default value of the argument.
		"""
		return self.default
		
	def set_default(self, def_val):
		""" Sets the default value of the argument.
		"""
		self.default = def_val
		
	def get_pg_grp(self):
		""" Gets the page_group of the argument.
		"""
		return self.pg_grp
		
	def set_pg_grp(self, pg_grp):
		""" Sets the page_group of the argument.
		"""
		self.pg_grp = pg_grp

	# def get_method_list(self):
		# return self.method_list
		
	# def set_method_list(self, methlst):
		# self.method_list = methlst
				
	def get_name(self):
		""" Gets the name of the argument.
		"""
		return self.name
		
	def set_name(self, arg_name):
		""" Sets the name of the argument.
		"""
		self.name = arg_name

	def get_value(self): #, method=None):
		""" Gets the value of the argument.
		"""
		return self.value
		
	def set_value(self, val): #, method=None):
		""" Determines if the input value is valid and then
			sets the self.value.
			:param val: The value for the argument.
		"""
	
		#if method is None: method = self.cur_method
		
		# Check if value is empty
		#print "val: %s" % val
		if val is None or val == '':
			if self.required:
				# If the value is required, then send error.
				print "\nERROR: The '%s' is a required argument." % self.name
				return False
			else:
				# If the value is not required
				if self.default is not None:
					# If a default value exists, use it
					print "Using the default value of '%s'." % self.default
					self.value = self.default
				else:
					self.value = val
				self.set_opt()
				return True
		
		# If no available options, set the value
		if len(self.opts) == 0:
			self.value = val
			self.set_opt()
			return True
			
		# Check if the value is a valid available option
		entry_lst = [item.get_entryopts() for item in self.opts]
		for entries in entry_lst:
			if val.lower() in [e.lower() for e in entries]:
				self.value = val
				self.set_opt()
				return True
		
		# If the entry is not valid, set to default if applicable
		print "\nWARNING: The specified value of '%s' is not a valid option." % val
		if self.default is not None:
			print "Using the default value of '%s'." % self.default
			self.value = self.default
			self.set_opt()
			return True
			
		# If argument is not required, the value is not a valid available option 
		#	and no default exists, then set the self.value to empty
		if not self.required:
			print "The value for '%s' will be empty." % self.name
			self.value = ''
			self.set_opt()
			return True
			
		return False
		
	def get_urltags(self):
		""" Gets the URL tags of the argument.
		"""
		print "cur_opt: %s" % self.cur_opt
		if self.cur_opt is not None:
			return self.cur_opt.get_urltags()
		else:
			return [self.default]
		
	def is_debug(self):
		""" Determines if the argument is used only for debugging.
		"""
		return self.debug
		
	def is_unique(self):
		""" Determines whether the argument should be asked more than once
			(if the argument is unique, it will be asked even if it has
			already been asked).
		""" 
		return self.unique
		
	def get_question(self, pg_grp=None):
		""" Gets the question for the argument.
			:param pg_grp: The page_group object.
		"""
		if pg_grp is None:
			pg_grp = self.pg_grp
	
		id = pg_grp.get_id()
		title = pg_grp.get_title()
		url = pg_grp.get_urls().values()[0]
	
		if self.name == 'word':
			self.question = "Please enter a search word " \
							"(leave blank to skip this option)"
		elif self.name == 'downloadable':
			self.question = "Would you like to filter for downloadable " \
							"content in the '%s' site?" % title
		# elif self.name == 'ds_type':
			# root_question = "Please enter the dataset type for the '%s' " \
						# "(URL: %s) page" % (title, url)
			
			# def_text = ''
			# if self.default is not None and not self.default == '':
				# def_text = " [%s]" % self.default
				
			# self.question = "%s%s" % (root_question, def_text)
		elif self.name == 'xl':
			self.question = "Would you like to export the results as an " \
							"Excel spreadsheet? [no]"
		else:

			# # Create the question text
			# root_question = "Please enter the %s for the '%s' (URL: %s) " \
							# "page group" % (self.name, title, url)
			
			#print self.default
			if self.default is None or self.default == '':
				def_txt = ''
			else:
				def_txt = ' [%s]' % self.default
			
			# Get a string of available options
			#avail_opts = " - " + '\n - '.join(["%s, %s or %s" % (o[0], o[1], o[2]) \
			#									for o in self.opts])
			
			method_opts = self.get_opts()
			
			if len(method_opts) > 0:
				# if isinstance(self.opts[0], tuple):
					# opts_str = [', '.join(o) for o in self.opts]
				# else:
					# opts_str = self.opts
				opts_str = []
				for opt in method_opts:
					opt_title = opt.get_name()
					entry_lst = opt.get_entryopts()
					if isinstance(entry_lst, list):
						if len(entry_lst) > 1:
							entry_lst.remove(opt_title)
							opts_str.append('%s: %s' % (opt_title, \
											', '.join(entry_lst)))
						else:
							opts_str.append(entry_lst[0])
					else:
						opts_str.append(entry_lst)
				avail_opts = " - " + '\n - '.join(opts_str)
			
				#print opts_str
				#print avail_opts
			
			arg_title = self.title
			if arg_title is None: arg_title = self.name
			
			if len(method_opts) == 0:
				opts_text = ''
				
				question = "Please enter the %s for the '%s' " \
							"page group%s" % (arg_title, title, def_txt)
			else:
				opts_text = "List of '%s' options:\n%s" % (arg_title, avail_opts)
				
				question = "Please enter the %s from the options above " \
							"for the '%s' page group%s" % (arg_title, \
							title, def_txt)
						
			self.question = "%s\n%s" % (opts_text, question)
			

			# if self.default is None or self.default == '':
				# if avail_opts == '':
					# opts_text = "(press enter to skip this option)"
				# else:
					# opts_text = "(available options: %s or press enter " \
								# "to skip this option)" % avail_opts
			# else:
				# if avail_opts == '':
					# opts_text = "[%s]" % self.default
				# else:
					# opts_text = "(available options: %s) [%s]" \
								# % (avail_opts, self.default)

			# self.question = "%s %s" % (root_question, opts_text)
	
		return self.question

class PageGroup:
	""" This class is used to group a set of web pages used my a
		specific method in the PT_Extractor.
	"""

	def __init__(self, id, title): #, method=None):
		""" The initializer for the PageGroup object.
			:param id: The unique ID for the page group.
			:param title: The name/title of the page group.
		"""
		self.id = id
		self.title = title
		self.urls = collections.OrderedDict()
		self.arg_lst = [] #arg_lst
		
	def add_arg(self, arg_name, default=None, value=None, debug=False, 
				in_opts=None, title=None, required=False):
		""" Adds a new argument to the list of arguments for the page group.
			:param arg_name: The unique name of the argument being added to 
								the page group.
			:param default: The default value for the argument.
			:param value: The value of the argument.
			:param debug: Determines if the argument is only for debugging.
			:param in_opts: The available options for the argument.
			:param title: The title of the argument.
			:param required: Determines if the argument is required or not.
		"""
		new_arg = Ext_Arg(arg_name, self, default, value, debug, \
								in_opts, title, required)
		self.arg_lst.append(new_arg)
		
		return new_arg
		
	def get_args(self):
		""" Gets the list of argument objects.
		"""
	
		return self.arg_lst
		
	def get_arg(self, arg_name):
		""" Gets the argument object with specified name.
		"""
		
		for a in self.arg_lst:
			if a.get_name() == arg_name:
				return a

	def set_title(self, title):
		""" Sets the title of the page group.
		:param title: The title string for the page group.
		:return: None
		"""
		self.title = title

	def get_title(self):
		""" Gets the title of the page group.
		:return: The title of the page group.
		"""
		return self.title

	def get_arcgis_urls(self, other_word=None):
		""" Gets all the ArcGIS Online URLs
			:param other_word: Provides another search option 
								besides "arcgis".
			:return: A list of ArcGIS URLs.
		"""
		url_list = []
		for key, value in self.urls.items():
			if key.find('url') > -1:
				if isinstance(value, list):
					for url in value:
						if other_word is None:
							if url.find('arcgis') > -1:
								url_list.append(url)
						else:
							if url.find('arcgis') > -1 or url.find(other_word) > -1:
								url_list.append(url)
				else:
					if other_word is None:
						if value.find('arcgis') > -1:
							url_list.append(value)
					else:
						if value.find('arcgis') > -1 or value.find(other_word) > -1:
							url_list.append(value)

		return url_list

	def add_url(self, title, url):
		""" Adds a web page to the list of URLs.
		:param title: The variable title of the web page.
		:param url: The URL of the web page.
		:return: None
		"""
		self.urls[title] = url

	def get_id(self):
		""" Gets the ID of the current page group.
		:return: The ID of the current page group.
		"""
		return self.id
		
	def get_page_count(self):
		""" Gets the number of pages in this page group.
		:return: None
		"""
		
		self.page_count = len(self.urls)
		
		return self.page_count

	def get_url(self, param):
		""" Gets a URL from the list of URLs.
		:param param: The URL name.
		:return: The URL containing param.
		"""
		if param in self.urls:
			return self.urls[param]
		else:
			print "\nPage WARNING: The given URL type is not available."

	def get_url_list(self):
		""" Gets the URL list.
		:return: The URL list.
		"""

		url_list = []
		for key, value in self.urls.items():
			if key.find('url') > -1:
				if isinstance(value, list):
					for url in value:
						url_list.append(url)
				else:
					url_list.append(value)

		return url_list

	def get_urls(self):
		""" Gets a list of the URLs of the page group.
		:return: A list of URLs.
		"""
		return self.urls

	# def get_arg(self, arg_name):
		# """ Gets a specific argument from the method_args dictionary.
		# :param arg_name: The argument name.
		# :return: The argument value
		# """
		# return self.method_args[arg_name]

	# def set_arg(self, arg_name, arg_val):
		# """ Sets a specific argument from the method_args dictionary.
		# :param arg_name: The argument name.
		# :param arg_val: The argument value to set.
		# :return: The argument value
		# """
		# self.method_args[arg_name] = arg_val

	# def get_args_list(self):
		# """ Gets a list of method arguments.
		# :return: The list of method arguments.
		# """
		# return self.method_args.keys()

	# def get_args(self):
		# """ Gets a dictionary of method arguments.
		# :return: A dictionary of method arguments.
		# """
		# return self.method_args

	# def set_args(self, arg_list):
		# """ Sets the keys in the method argument dictionary with emtpy values.
		# :param arg_list: A list of arguments to add to the dictionary
		# :return: None
		# """
		# arg_list.remove('self')
		# for m_arg in arg_list:
			# # Set the value of the argument
			# if m_arg in self.defaults.keys():
				# self.method_args[m_arg] = self.defaults[m_arg]
			# else:
				# self.method_args[m_arg] = None

			# if m_arg == 'word':
				# self.questions[m_arg] = "Please enter a search word"
			# elif m_arg == 'downloadable':
				# self.questions[m_arg] = "Would you like to filter for downloadable content in the '%s' site?" \
										# % self.title
			# elif m_arg == 'ds_type':
				# root_question = "Please enter the dataset type for the '%s' (URL: %s) page" % (self.title, self.urls.values()[0])

				# def_val = ''
				# if m_arg in self.defaults.keys():
					# def_val = self.defaults[m_arg]
				
				# opts_text = ''
				# if not def_val == '':
					# opts_text = " [%s]" % def_val
					
				# self.questions[m_arg] = "%s%s" % (root_question, opts_text)
			# else:
			
				# # Get default value
				# def_val = ''
				# if m_arg in self.defaults.keys():
					# def_val = self.defaults[m_arg]
				
				# if def_val == '':
					# def_text = ''
				# else:
					# def_text = ' [%s]' % def_val

				# # Get the available options
				# avail_opts = ''
				# if self.opts is not None and m_arg in self.opts.keys():
					# opts = self.opts[m_arg]
					# # If the default is not in the list of options, add it
					# if not def_val == '' and def_val not in opts:
						# opts.append(def_val)
						
					# if len(opts) > 0:
						# avail_opts = " - " + '\n - '.join(opts_str)

				# if len(self.opts) == 0:
					# opts_text = ''
					# root_question = "Please enter the %s for the '%s' page" % \
									# (m_arg, self.title)
				# else:
					# opts_text = 'Available %s Options:\n%s' % (m_arg.title(), avail_opts)
					# root_question = "Please enter the %s for the '%s' page " \
									# "group from the above options" % \
									# (m_arg, self.title)

				# self.questions[m_arg] = "%s\n%s" % (opts_text, root_question)

	# def add_default(self, arg_name, arg_val):
		# """ Adds a default value for a specified argument.
		# :param arg_name: The argument name
		# :param arg_val: The argument default value
		# :return: None
		# """

		# self.defaults[arg_name] = arg_val

	# def get_questions(self):
		# """ Gets the dictionary of questions for the page group.
		# :return: A dictionary of the page group's questions.
		# """
		# return self.questions

	# def get_opts(self):
		# """ Gets the options for the method arguments
		# :return: A dictionary of the method arguments and available values
		# """

		# return self.opts

	# def set_opts(self, opts):
		# """ Sets the available options for a method argument.
		# :param opts: A dictionary like
					# {arg_name: [arg_val, arg_val, arg_val, ...],
					 # arg_name: [arg_val, arg_val, arg_val, ...],
					 # ...
					# }
		# :return: None
		# """

		# self.opts = opts

class Extractor:
	""" This class contains common methods used by all PT_Extractor classes.
	"""

	def __init__(self):
		""" Initializer for the Extractor class. """

		# Set up the initial parameters
		#self.pt_ext = pt_ext
		self.province = self.get_province()
		self.work_folder = shared.get_home_folder() + '\\results\\%s' % self.province
		self.debug = False

		# # Set the arguments for each page
		# for k, v in self.page_groups.items():
			# self.set_args(v)

		# Open the log file
		self.log_fn = '%s\\files\\Extraction_Log.txt' % shared.get_home_folder()
		self.log_f = open(self.log_fn, 'w')
		
		# Open errors log file
		self.errs_fn = "%s\\err_log.csv" % self.work_folder
		self.err_log = open(self.errs_fn, 'a')
		# Write the header if not already there
		if os.path.getsize(self.errs_fn) == 0:
			self.err_log.write('Title,URL,Date Accessed,Error Info\n')
			
		# Create the notes string for any errors
		self.notes = ''
		
		self.argmt = collections.OrderedDict()
		
		self.errs = []
		
		self.xl = False

	def call_method(self):
		""" Calls the proper extract method based on the current page group
		:return: None
		"""
		
		# Gather the list of parameters
		params_list = []
		self.method_params = self.pg_grp.get_args()
		if self.pg_grp.get_id() == 'update':
			method = 'self.update_discover'
		else:
			method = 'self.extract_%s' % self.pg_grp.get_id()
		#print "method: %s" % method
		#for k, v in self.method_params.items():
		for pg_arg in self.method_params:
			arg_name = pg_arg.get_name()
			arg_val = pg_arg.get_value()
			# Get a list of arguments which are in the extract method
			method_args = inspect.getargspec(eval(method)).args
			# If the key is not in the method's arguments list, skip it
			if not arg_name in method_args: continue
			# Create the list of arguments and values for the method
			if arg_val is not None:
				if isinstance(arg_val, str):
					params_list.append('%s="%s"' % (arg_name, arg_val))
				else:
					params_list.append('%s=%s' % (arg_name, arg_val))
		
		params_str = ', '.join(params_list)
		# Run the appropriate method (extract_<page_id> with parameters for arguments)
		method_str = '%s(%s)' % (method, params_str)
		print "\nRunning method: %s" % method_str
		eval(method_str)
		
	def check_result(self, in_res, url='', title='', txt='', output=True):
		"""Verifies if the soup is None or contains an error.
		:param in_res: The input result (soup or other) to check.
		:param url: The URL of the result object.
		:param title: The title for the dataset for the err_log file.
		:param txt: The error text.
		:return: True if the input is valid and has no errors; False if not.
		"""
		
		if isinstance(in_res, urllib2.addinfourl): return True
			
		if isinstance(in_res, (list, tuple)): return True
		
		if isinstance(in_res, dict):
			if 'error' in in_res.keys():
				page_msg = 'JSON data'
			else:
				page_msg = 'Page'
			if 'err' in in_res.keys() or 'error' in in_res.keys():
				# Write the results to the screen
				print "\nWARNING: '%s' (%s): %s could not be opened." \
						% (shared.filter_unicode(title), url, page_msg)
				if output: print "Please check the 'err_log.csv' file " \
							"in the province/territory results folder.\n"
				
				if txt == '':
					if 'err' in in_res.keys():
						err_msg = in_res['err']
					else:
						err_msg = in_res['error']
					txt = '%s could not be loaded: %s.' % (page_msg, err_msg)
				
				if output:
					# Place the error in the err_log CSV
					now = datetime.datetime.now()
					err_line = [title, url, now.isoformat(), txt]
					err_list = ['' if l is None else l for l in err_line]
					self.errs.append(err_list)
					#print "err_list: %s" % err_list
					err_str = shared.filter_unicode(','.join(err_list))
					self.err_log.write('%s\n' % err_str)
					
				self.notes = txt
				
				return False
			else:
				return True
				
		if txt == '':
			txt = 'Page could not be loaded.'
		
		if in_res is None:
			# Write the results to the screen
			print "\nWARNING: %s page '%s' could not be opened." % (title, url)
			if output: print "Please check the 'err_log.csv' file in the " \
						"province/territory results folder."
			
			if output:
				# Place the error in the err_log CSV
				now = datetime.datetime.now()
				err_line = [title, url, now.isoformat(), txt]
				self.errs.append(err_line)
				self.err_log.write('%s\n' % ','.join(err_line))
				
			self.notes = txt
			
			return False
		elif in_res.find('|') > -1:
			# Check to see if the error has a message
			soup_split = in_res.split('|')
			if soup_split[0] == 'ERROR':
			
				err_msg = soup_split[1]
			
				# Write the results to the screen
				print "\nWARNING: Issue loading page '%s': %s." % (url, err_msg)
				if output: print "Please check the 'err_log.csv' file in the province/territory results folder."
				
				if output:
					# Place the error in the err_log CSV
					now = datetime.datetime.now()
					err_line = [title, url, now.isoformat(), txt, err_msg]
					self.errs.append(err_line)
					self.err_log.write('%s\n' % ','.join(err_line))
					
				self.notes = txt
				
				return False
			else:
				return True
		else:
			return True
			
	def get_args(self):
		""" Gets a list of arguments for the current page group.
		"""
		arguments = [pg_arg for pg_arg in self.pg_grp.get_args()]
		
		return arguments

	def set_args(self, pg_grp):
		""" Sets the arguments for the specified page group.
		:param pg_grp: The current page group object.
		:return: None
		"""
		if pg_grp.get_id() == 'update':
			method = 'self.update_discover'
		else:
			method = 'self.extract_%s' % pg_grp.get_id()
		#print "method: %s" % method
		pg_grp.set_args(inspect.getargspec(eval(method)).args)
		
	def get_arg(self, arg_name):
		""" Gets the specified Ext_Arg object from the list of arguments.
		"""
		arg_lst = self.get_args()
		
		for a in arg_lst:
			if a.get_name() == arg_name:
				return a
				
	def get_arg_opts(self, arg_name):
		""" Gets a list of options for a specified argument.
		"""
		arg_lst = self.get_args()
		
		for a in arg_lst:
			if a.get_name() == arg_name:
				return a.get_opts()
		
	def get_arg_val(self, arg_name):
		""" Gets the value of a given argument name.
		"""
		arg_lst = self.get_args()
		
		for a in arg_lst:
			if a.get_name() == arg_name:
				return a.get_value()
		
	def set_debug(self, debug):
		""" Sets the debug value, True if in debug mode.
		:param debug: A boolean determining whether the extractor is in debug mode.
		:return: None
		"""
	
		self.debug = debug
		
	def set_notes(self, notes):
		""" Sets the notes variable to a specified string.
		:param notes: A string for the notes.
		:return: None
		"""
	
		self.notes = notes

	def get_param(self, param):
		""" Gets a parameter from the current page group.
		:param param: The parameter name to extract
		:return: The parameter value
		"""
		pg_grp = self.page_groups[self.pg_grp]
		param_val = pg_grp.get_param(param)
		return param_val
		
	def get_province(self):
		""" Gets the province name of the extractor.
		:return: The province name of the extractor.
		"""
		
		return self.province

	def get_pg_grps(self):
		""" Gets a list of available page group types (ex: cigg, maps, etc.).
		:return: A list of page group types.
		"""
		return self.page_groups
		
	def get_pg_grp(self, pg_name=None):
		""" Gets the current page group of the Extractor.
		"""
		
		if pg_name is None:
			return self.pg_grp
		else:
			for pg in self.page_groups:
				if pg.get_id() == pg_name:
					return pg

	def set_pg_grp(self, pg_grp_name):
		""" Sets the ID for the Extractor based on the given page group type.
		:param pg_grp_name: The page group type to set the ID.
		:return: None
		"""
		self.id = pg_grp_name
		
	def get_pggrp_ids(self):
		""" Gets a list of the page group IDs
		"""
		
		out_ids = [pg.get_id() for pg in self.page_groups]
		
		return out_ids

	def set_run_pg_grps(self, pg_grps):
		""" Sets the list of page group IDs for the Extractor based on the list of pg_grps.
		:param pg_grps: A list of page groups which will be run.
		:return: None
		"""
		self.run_pg_grps = pg_grps

	def set_params(self, params):
		""" Sets the parameters for the extract_opendata method
		:param params: A dictionary of parameters (keys are the method's argument names)
		:return: None
		"""
		self.method_params = params
		
	def set_xl(self, xl):
		""" Sets the self.xl with boolean value
		"""
		self.xl = xl

	def print_log(self, txt):
		""" Writes a text to the log file.
		:param txt: The string which will be written to the log file.
		:return: None
		"""
		# type: (object) -> object
		print txt
		self.log_f.write(txt + "\n")
		
	def print_title(self, title):
		""" Prints the specified title to the command-prompt with a border.
		:param title: The text with the title.
		:return: None
		"""
		
		print "\n****************************************************************************"
		print " %s:" % title
		print "****************************************************************************\n"

	def close_log(self):
		""" Closes the log file."""
		self.log_f.close()

	def run(self):
		""" Runs the extraction methods based on the user's input
		:return: None
		"""
		
		if 'all' in self.run_pg_grps and not self.province == 'Canada':
			# Extract all available pages
			# for key, pg_grp in self.page_groups.items():
				# self.pg_grp = self.page_groups[key]
				# self.call_method()
			for pg in self.page_groups:
				self.pg_grp = pg
				self.call_method()
		else:
			for pg_name in self.run_pg_grps:
				# Extract specified page
				if pg_name in self.get_pggrp_ids():
					self.pg_grp = self.get_pg_grp(pg_name)
					self.call_method()
				else:
					print "\nERROR: Invalid page '%s'. Please enter one of the following: %s" % (
						pg_name, ', '.join(self.get_pggrp_ids()))
					print "Exiting process."
					sys.exit(1)
					
	def write_error(self, url, title='', txt=''):
		""" Writes an error line to the error log file.
		:param url: The URL causing the error.
		:param title: The title of the page.
		:param txt: The text to place in the CSV file.
		:return: None
		"""
		
		now = datetime.datetime.now()
		self.err_log.write("%s,%s,%s,%s\n" % (title, url, now.isoformat(), txt))
		
	def write_err_xl(self, pt_xl, ws_name=None):
		""" Writes the errors to the Excel spreadsheet.
		:param pt_xl: The PT_XL object.
		:param ws_name: The worksheet name in which the errors will be added.
		"""
		
		if ws_name is None: ws_name = pt_xl.get_ws_name()
	
		if len(self.errs) > 0:
			# Add the worksheet if it doesn't exist
			if not pt_xl.ws_exists(ws_name):
				pt_xl.add_worksheet(ws_name)
			
			# Write an empty row to the Excel file
			pt_xl.write_list()
			
			# Add a title just before the header
			pt_xl.add_header(['Errors'])
			
			# Write the header to the Excel file
			header = ['Title', 'URL', 'Date Accessed', 'Error Message']
			pt_xl.add_header(header)
			
			# Add each error to the Excel file
			for e_row in self.errs:
				for e_cell in e_row:
					#print "e: %s" % e
					pt_xl.add_cell(e_cell)
				
				pt_xl.write_row()
		
			# Empty the list of errors
			self.errs = []
