#import recurse_ftp as rec_ftp
import os
import sys

class RecFTP:
    def __init__(self, domain, ftp_dir):

        self.my_dirs = []
        self.my_files = []
        self.curdir = ''
        self.domain = domain
        self.ftp_dir = ftp_dir

    def get_dirs(self, ln):
        ''' Gets a list of directories under a given line from the FTP page.
        :param ln: FTP line text.
        :return: None
        '''

        # Clean the path
        ln_clean = shared.clean_text(ln)

        print "\nClean line: %s" % ln_clean

        # Get a list of columns
        cols = ln_clean.split(' ')

        print "cols: %s" % cols

        objname = cols[len(cols) - 1]  # file or directory name

        print "objname: %s" % objname

        if ln.startswith('d'):
            self.my_dirs.append(objname)
        else:
            if objname.endswith('.zip'):
                self.my_files.append(os.path.join(self.curdir, objname))  # full path

        answer = raw_input("Press enter...")

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

        self.my_dirs = []

        # Get the current pathname of the FTP
        self.curdir = self.ftp.pwd()

        print("Going to change to directory '%s' from '%s'" % (adir, self.curdir))

        # Change the folder to the specified adir
        self.ftp.cwd(adir)

        # Change the self.curdir to the current FTP folder
        self.curdir = self.ftp.pwd()

        print("Now in directory: %s" % self.curdir)

        self.ftp.retrlines('LIST', self.get_dirs)

        gotdirs = self.my_dirs

        print("Found in '%s' directories:" % adir)
        print(gotdirs)
        print("Total files found so far: %s." % len(self.my_files))

        sleep(1)

        for subdir in gotdirs:
            self.my_dirs = []
            self.check_dir(subdir) # recurse

        self.ftp.cwd('..') # back up a directory when done here

    def get_file_list(self):

        print "domain: %s" % self.domain

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
        except:
            print('oh dear.')
            print traceback.format_exc()
            #ftp.quit()

        self.ftp.quit()
        print('all done!')

        return self.my_files
        #return my_dirs

# Get a list of directories
dir_list = []
dir_list.append('/Elevation/')
dir_list.append('/GeoYukon/')
dir_list.append('/Imagery/')

# Get a list of files on the FTP site
ftp_files = []
#header = [']
for dir in dir_list:
	# Get the FTP object for the current folder
	ftp = RecFTP('ftp.geomaticsyukon.ca', dir)

	# Get a list of files under the current folder
	ftp_list = ftp.get_file_list()

	# Add the files to the overall ftp_files list
	ftp_files += ftp_list