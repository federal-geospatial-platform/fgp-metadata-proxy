#!/usr/bin/env python

from ftplib import FTP
from time import sleep
import os
import traceback
import shared
import collections

#my_dirs = []  # global
#my_files = [] # global
#curdir = ''   # global

class RecFTP:
	def __init__(self, domain, ftp_dir, header, debug=False):

		self.my_dirs = []
		self.my_files = []
		self.curdir = ''
		self.domain = domain
		self.ftp_dir = ftp_dir
		self.header = header
		self.debug = debug
		
		# FOR DEBUG ONLY
		self.end_val = 150
		self.counter = 0

	def get_dirs(self, ln):
		''' Gets a list of directories under a given line from the FTP page.
		:param ln: FTP line text.
		:return: None
		'''

		# Clean the path
		ln_clean = shared.clean_text(ln)
		
		if self.debug: print "\nClean line: %s" % ln_clean

		# Get a list of columns
		cols = ln_clean.split(' ')

		if self.debug: print "cols: %s" % cols

		line_dict = collections.OrderedDict((k, "") for k in self.header)
		for index, key in enumerate(line_dict.keys()):
			line_dict[key] = cols[index]

		# print line_dict

		# answer = raw_input("Press enter...")

		objname = cols[len(cols) - 1]  # file or directory name

		# print "objname: %s" % objname

		if 'permissions' in line_dict.keys():
			permissions = line_dict['permissions']
			if permissions.startswith('d'):
				self.my_dirs.append(objname)
		elif 'type' in line_dict.keys():
			if line_dict['type'] == '<DIR>':
				self.my_dirs.append(objname)

		if 'filename' in line_dict.keys():
			fn = line_dict['filename']
			if fn.endswith('.zip') or fn.endswith('.gdb') or fn.endswith('.shp') and not fn.endswith('info.zip'):
				self.my_files.append('%s%s/%s' % (self.domain, self.curdir, objname))

		# merge = cols[8:]
		# objname = ' '.join(merge)

		# if ln.startswith('d'):
		#     self.my_dirs.append(objname)
		# else:
		#     if objname.endswith('.zip'):
		#         #my_files.append(os.path.join(curdir, objname)) # full path
		#         if self.curdir.find('Ecosystem_Units_') > -1:
		#             print "Domain: " + str(self.domain)
		#             print "CurDir: " + str(self.curdir)
		#             print "LN: " + str(ln)
		#             print "ObjName: " + str(objname)
		#             answer = raw_input("Press enter...")
		#         self.my_files.append(('ftp://%s%s' % (self.domain, self.curdir), objname))

	def check_dir(self, adir):
		''' Checks for a list of folders in a FTP folder
		:param adir: An FTP folder.
		:return: None
		'''
		
		print "Checking folder '%s'" % adir
		#shared.print_oneliner(msg)
		
		if self.counter == self.end_val:
			return None

		self.my_dirs = []

		# Get the current pathname of the FTP
		self.curdir = self.ftp.pwd()

		if self.debug: print("Going to change to directory '%s' from '%s'" % (adir, self.curdir))

		# Change the folder to the specified adir
		try:
			self.ftp.cwd(adir)
		except Exception, e:
			#print('oh dear.')
			print traceback.format_exc()
			#ftp.quit()
			#err_resp = e
			err_dict = collections.OrderedDict()
			err_dict['err'] = e
			err_dict['url'] = "%s/%s" % (self.domain, adir)
			print err_dict
			#return err_dict
			self.my_files.append(err_dict)
			return None

		# Change the self.curdir to the current FTP folder
		self.curdir = self.ftp.pwd()

		if self.debug: print("Now in directory: %s" % self.curdir)

		self.ftp.retrlines('LIST', self.get_dirs)

		gotdirs = self.my_dirs

		if self.debug: print("Found in '%s' directories:" % adir)
		if self.debug: print(gotdirs)
		if self.debug: print("Total files found so far: %s." % len(self.my_files))

		sleep(1)
		
		self.counter += 1
		#print self.counter

		for subdir in gotdirs:
			self.my_dirs = []
			self.check_dir(subdir) # recurse

		self.ftp.cwd('..') # back up a directory when done here

	def get_file_list(self):
		''' Gets a list of all the files at an FTP location.
		:return: A list of the FTP files.
		'''

		if self.debug: print "domain: %s" % self.domain

		try:
			self.ftp = FTP(self.domain)
			self.ftp.login()
			self.check_dir(self.ftp_dir) # directory to start in
			self.ftp.cwd('/.') # change to root directory for downloading
			#for f in my_files:
			#    print('getting ' + f)
			#    file_name = f.replace('/', '_') # use path as filename prefix, with underscores
			#    ftp.retrbinary('RETR ' + f, open(file_name, 'wb').write)
			#    sleep(1)
		except Exception, e:
			#print('oh dear.')
			print traceback.format_exc()
			#ftp.quit()
			#err_resp = e
			err_dict = collections.OrderedDict()
			err_dict['err'] = e
			err_dict['url'] = "%s%s" % (self.domain, self.ftp_dir)
			return err_dict

		self.ftp.quit()
		if self.debug: print('all done!')

		return self.my_files
		#return my_dirs