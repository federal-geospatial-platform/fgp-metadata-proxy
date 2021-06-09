import os
import sys

home_folder = os.path.abspath(os.path.join(__file__, "..\\.."))
scripts_folder = os.path.join(os.sep, home_folder, 'scripts')
sys.path.append(scripts_folder)

print scripts_folder

import Main_Extractor as main_ext
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

extractor_list = []

extractor_list.append(AB.PT_Extractor())
extractor_list.append(BC.PT_Extractor())
extractor_list.append(MB.PT_Extractor())
extractor_list.append(NB.PT_Extractor())
extractor_list.append(NL.PT_Extractor())
extractor_list.append(NS.PT_Extractor())
extractor_list.append(NU.PT_Extractor())
extractor_list.append(NT.PT_Extractor())
extractor_list.append(ON.PT_Extractor())
extractor_list.append(PE.PT_Extractor())
extractor_list.append(QC.PT_Extractor())
extractor_list.append(SK.PT_Extractor())
extractor_list.append(YT.PT_Extractor())

out_f = open('PT_Bookmarks.html', 'w')

out_f.write('''<!DOCTYPE html>
<html>

	<head>
		<style>
			.main-txt {
				font-family: verdana;
			}
			.bold-txt {
				
			}
		</style>
	</head>

	<body>
''')

for ext in extractor_list:
	pt = shared.get_pt_name(ext.get_province())
	pt = pt.replace('_', ' ')
	
	out_f.write('''		<h1 class='main-txt'>%s</h1>\n''' % pt)
	
	pg_grps = ext.get_pg_grps()
	
	for k, pg in pg_grps.items():
		page_title = pg.get_title()
		urls = pg.get_url_list()
		
		print urls
		
		out_f.write('''		<p class='main-txt'><strong>%s</strong>: ''' % page_title)
		
		for url in urls:
			if isinstance(url, tuple) or isinstance(url, list):
				for sub_url in url:
					out_f.write('''<br>\n			<a href='%s'>%s</a>''' % (sub_url, sub_url))
			else:
				out_f.write('''<br>\n			<a href='%s'>%s</a>''' % (url, url))
		
		#out_f.write("%s: '%s' %s\n" % (k, urls, urls))
		
	#answer = raw_input("Press enter...")
		
out_f.write('''\t</body>
</html>''')
		
out_f.close()