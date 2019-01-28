# FGP P/T Web Extractor README

## Overview

The FGP P/T Web Extractor is an application which inventories geospatial datasets from provincial and territorial web pages, services and catalogues.

## Setup

### Download
1. Navigate to the repository 'fgp-metadata-proxy' and download a zip file of the entire repository.
2. Unzip the file and copy the PT_WebExtractor folder to the C drive.

### Python Setup
1. Verify that Python 2.7 is installed by typing 'ftype Python.File' in a Command Prompt. Python 2.7 is installed if 'Python.File="C:\Python27\ArcGIS10.4\python.exe" "%1" %*' is returned.
2. Run the 'check_packages.bat' to determine which Python packages have been installed and which ones are still needed before running the FGP P/T Web Extractor.
3. If any Python packages are missing, run the 'install_packages.bat'.

The following Python packages are required for the Extractor:
- [Beautifulsoup](https://www.crummy.com/software/BeautifulSoup/)
- [Selenium](https://selenium-python.readthedocs.io/)
- [lxml](https://lxml.de/)
- [Browsermob-proxy](https://browsermob-proxy-py.readthedocs.io/en/stable/)
- [Requests](http://docs.python-requests.org/en/master/)
- [PyPDF](http://pybrary.net/pyPdf/)
- [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/)
- [XMLtoDict](https://github.com/martinblech/xmltodict)

## Folder Structure

| Folder           | Description   |
| ---------------- | ------------- |
| PT_WebExtractor  | Home folder |
| PT_WebExtractor/batch | Contains the batch files for all the provinces and for setup the P/T Web Extractor. |
| PT_WebExtractor/docs | Contains the documentation for the P/T Web Extractor. |
| PT_WebExtractor/extras | Contains extra applications used for analysing the P/T geospatial data. |
| PT_WebExtractor/files | Contains files used by the Web Extractor scripts. |
| PT_WebExtractor/files/epsg | Contains CSV files with EPSG codes. |
| PT_WebExtractor/files/errors | Contains error JSON files from the BC Extractor. |
| PT_WebExtractor/results | Contains a folder for every province/territory with the CSV inventory results. |
| PT_WebExtractor/scripts | Contains the provincial/territorial scripts used by the Web Extractor. |
| PT_WebExtractor/scripts/common | Contains the Python scripts shared by the provincial/territorial extractor scripts. |
| PT_WebExtractor/webdrivers | Contains the webdrivers which Selenium uses. |
