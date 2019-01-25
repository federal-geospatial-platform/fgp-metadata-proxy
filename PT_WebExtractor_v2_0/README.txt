**********************************************************************
PT Web Extractor README
**********************************************************************


****** Folder Structure **********************************************

PT_WebExtractor
    └> batch: Contains the batch files for all the provinces and for 
				setup the PT Web Extractor.
    └> files: Contains files used by the Web Extractor scripts.
        └> epsg: Contains CSV files with EPSG codes.
		└> errors: Contains error JSON files from the BC Extractor.
    └> results: Contains a folder for every province/territory with
				the CSV inventory results.
    └> scripts: Contains the provincial/territorial scripts used 
		by the Web Extractor.
		└> common: Contains the Python scripts shared by the 
					provincial/territorial extractor scripts.
    └> webdrivers: Contains the webdrivers which Selenium uses.
		└> browsermob-proxy-2.1.4: Contains the files for the 
								browsermob-proxy package.
		└> chromedriver_win32: Contains the driver for Chrome.
		└> geckodriver-v0.20.0-win64: Contains the driver for Firefox.
		└> IEDriverServer_x64_2.42.0: Contains the driver for Internet 
								Explorer.


****** Setup *********************************************************

1. Unzip the PT_WebExtractor.zip to the C drive.
2. Run the check_packages.bat to see which Python packages need to be
	installed before using the PT Web Extractor.
3. If a package needs to be installed, run the install_packages.bat.
	- When asked, type in the package for installing (NOTE: make sure
	to type the name of the package as it appears).
4. Once all the packages have been installed, PT Web Extractor should
	be ready to use.

****** Usage *********************************************************