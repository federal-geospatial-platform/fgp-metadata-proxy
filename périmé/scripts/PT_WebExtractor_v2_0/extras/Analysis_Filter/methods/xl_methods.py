#import recurse_ftp as rec_ftp
import os
import sys
import os
import sys
import codecs
import csv
import collections
import argparse
import traceback
import inflect
import glob
from openpyxl import *
from openpyxl.styles import *
from openpyxl.worksheet.write_only import WriteOnlyCell

home_folder = os.path.abspath(os.path.join(__file__, "..\\..\\..\\.."))
scripts_folder = os.path.join(os.sep, home_folder, 'scripts')
sys.path.append(scripts_folder)

from common import shared

def add_cell(ws, row_list, cell_val, fill=None, font=None, border=None, 
	alignment=None, number_format=None, protection=None):
	
	new_cell = WriteOnlyCell(ws, value=cell_val)
	if fill is not None: new_cell.fill = fill
	if font is not None: new_cell.font = font
	if border is not None: new_cell.border = border
	if alignment is not None: new_cell.alignment = alignment
	if number_format is not None: new_cell.number_format = number_format
	if protection is not None: new_cell.protection = protection
	row_list.append(new_cell)
	
	return row_list

def add_header(ws, header_txts):
	header = []
	for h in header_txts:
		cell = WriteOnlyCell(ws, value=h)
		cell.fill = PatternFill("solid", fgColor="C6EFCE")
		cell.font = Font(name='Calibri (Body)', size=14, color="006100")
		cell.alignment = Alignment(horizontal='center')
		thin = Side(border_style="thin", color="A6A6A6")
		cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)
		header.append(cell)
	ws.append(header)
	
	return header

def get_abbreviation(pt):
	
	if pt == 'Alberta':
		return 'AB'
	elif pt == 'British Columbia':
		return 'BC'
	elif pt == 'Manitoba':
		return 'MB'
	elif pt == 'New Brunswick':
		return 'NB'
	elif pt == 'Newfoundland & Labrador':
		return 'NL'
	elif pt == 'Nova Scotia':
		return 'NS'
	elif pt == 'Northwest Territories' or pt == 'NWT':
		return 'NT'
	elif pt == 'Nunavut':
		return 'NU'
	elif pt == 'Ontario':
		return 'ON'
	elif pt == 'Prince Edward Island' or pt == 'PEI':
		return 'PE'
	elif pt == 'Quebec':
		return 'QC'
	elif pt == 'Saskatchewan':
		return 'SK'
	elif pt == 'Yukon':
		return 'YT'
	else:
		return pt