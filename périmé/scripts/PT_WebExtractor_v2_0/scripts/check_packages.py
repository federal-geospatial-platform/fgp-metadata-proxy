import os
import sys

# Try importing BeautifulSoup
try:
	import bs4
	print "\nBeautifulSoup is installed!"
except:
	print "\nBeautifulSoup needs to be installed."
	print "Please run the install_packages.bat before using FGP Web Extractor."
	
# Try importing Selenium
try:
	import selenium
	print "\nSelenium is installed!"
except:
	print "\nSelenium needs to be installed."
	print "Please run the install_packages.bat before using FGP Web Extractor."
	
# Try importing browsermobproxy
try:
	import browsermobproxy
	print "\nBrowsermobproxy is installed!"
except:
	print "\nBrowsermobproxy needs to be installed."
	print "Please run the install_packages.bat before using FGP Web Extractor."
	
# Try importing Requests
try:
	import requests
	print "\nRequests is installed!"
except:
	print "\nRequests needs to be installed."
	print "Please run the install_packages.bat before using FGP Web Extractor."
	
# Try importing PyPDF
try:
	import pyPdf
	print "\nPyPDF is installed!"
except:
	print "\nPyPDF needs to be installed."
	print "Please run the install_packages.bat before using FGP Web Extractor."
	
print ""