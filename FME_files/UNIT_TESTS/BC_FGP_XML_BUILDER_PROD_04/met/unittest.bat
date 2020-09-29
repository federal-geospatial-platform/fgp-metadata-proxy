REM ===========================================================================
REM Enable local variables 
REM ===========================================================================
SETLOCAL ENABLEDELAYEDEXPANSION
 
REM ===========================================================================
REM Allow accented characters
REM ===========================================================================
chcp 1252

REM ===========================================================================
REM Determine the directory where the.bat is located and place it  
REM in the directory above while keeping the original directory
REM ===========================================================================
SET Repertoire=%~dp0
PUSHD %Repertoire%\..

REM Define FME transformer path
SET FME_USER_RESOURCE_DIR=%USERPROFILE%\Documents\FME

REM ===========================================================================
REM Create file name variable in relative mode.
REM ===========================================================================
SET NomApp=BC_FGP_XML_BUILDER_PROD_04
SET fme=%FME2019%

SET UserProfileFmw="%FME_USER_RESOURCE_DIR%\workspaces\%NomApp%.fmw"

REM ===========================================================================
REM Initialization of the variable that contains the result of the execution
REM ===========================================================================
SET Statut=0

REM ===========================================================================
REM Copy FMW to Documents
REM ===========================================================================
COPY/Y fme\%NomApp%.fmw %UserProfileFmw%
SET Statut=%Statut%%ERRORLEVEL%

REM Define sources

REM First FME call, processing FFS file with 305 source data files to output 56 XML files.  Error introduced with missing record in UUID_Spatial lookup table.
set test_number=1
set source=met\source%test_number%.ffs
set lookup=met\P-T_ETL_LOOKUP_TABLES.xlsx
set log=met\log_%test_number%.log
set log_comp_xml=met\log_comp_xml_%test_number%.log
set log_comp_xlsx=met\log_comp_xlsx_%test_number%.log
set No=No
set Yes=Yes
set xml_etalon=met\XML_etalon_%test_number%
set xml_resultat=met\XML_resultat
set process_report_directory_etalon=met\XLSX_etalon_%test_number%
set process_report_directory_resultat=met\XLSX_resultat_%test_number%
set process_report_subdirectory_resultat=\met\XLSX_resultat_%test_number%

set xlsx_etalon=%process_report_directory_etalon%\xlsx_etalon_%test_number%.xlsx
set xlsx_resultat=%process_report_directory_resultat%\xlsx_resultat_%test_number%.xlsx

IF EXIST %log% del %log%
IF EXIST %xml_resultat% del %xml_resultat% /Q
REM Create XLSX directory
MD %process_report_directory_resultat%
%fme% fme\BC_FGP_XML_BUILDER_PROD_04.fmw ^
--ACTIVATE_TRANSLATION %No% ^
--CATALOGUE_READER_SELECT %No% ^
--IN_FFS_TESTING_FILE %source% ^
--IN_XLS_LOOKUP_TABLE_FILE %lookup% ^
--LOCAL_WRITER %Yes% ^
--LOCAL_SOURCE_METADATA_DELTA_FINDER %Yes% ^
--OUT_XML_LOCAL_DIR %xml_resultat% ^
--OUT_XLS_NOTIFICATION_DIR %process_report_directory_resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%
FIND "Data record with unique ID 30aeb5c1-4285-46c8-b60b-15b1a6f4258b missing from UUID_Spatial lookup table in SPATIAL_TYPE_MAPPER transformer and could not be mapped to a value." %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison of XML output directory with the standard XML output directory
IF EXIST %log_comp_xml% del %log_comp_xml%
%fme% met\XML_Comparateur.fmw ^
--ETALON_SOURCE_DIR %xml_etalon% ^
--RESULTAT_SOURCE_DIR %xml_resultat% ^
--LOG_FILE %log_comp_xml% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison of XLSX Process Report with the standard
IF EXIST %log_comp_xlsx% del %log_comp_xlsx%
REM Move XLSX file written to subdirectory by bug to main directory
XCOPY /s/e %process_report_directory_resultat%%process_report_subdirectory_resultat% %process_report_directory_resultat%
REM Rename XLSX file with date in title to generic name for testing
RENAME %process_report_directory_resultat%\"*" "xlsx_resultat_%test_number%.xlsx"
%fme% met\XLSX_Comparateur.fmw ^
--IN_ETALON_FILE %xlsx_etalon% ^
--IN_RESULTAT_FILE %xlsx_resultat% ^
--LOG_FILE %log_comp_xlsx% 
SET Statut=%Statut%%ERRORLEVEL%
REM Remove XLSX directory
RD %process_report_directory_resultat% /S /Q

REM Second FME call, processing FFS file with 153 source data files filtered to 29 data records.  Two are are updated in the local XML repository.  
REM 27 records identified as no longer existant in source data in METADATA_DELTA_FINDER and logged in PROCESS_REPORT_MANUAL_TASKS for manual deletion.  
REM PROCESS_REPORT_MANUAL_TASKS also identifies the following errors:
REM 1 GEOSPATIAL_FORMAT_NOT_MAPPED
REM 2 SPATIAL_TYPE_NOT_MAPPED
REM 1 MAP_SERVICE_URL_ERROR
REM 13 items are logged to the attribute mapping errors FFS file
set test_number=2
set source=met\source%test_number%.ffs
set lookup=met\P-T_ETL_LOOKUP_TABLES.xlsx
set log=met\log_%test_number%.log
set log_comp_ffs=met\log_comp_ffs_%test_number%.log
set log_comp_xml=met\log_comp_xml_%test_number%.log
set log_comp_xlsx=met\log_comp_xlsx_%test_number%.log
set No=No
set Yes=Yes
set xml_etalon=met\XML_etalon_%test_number%
set xml_resultat=met\XML_resultat
set ffs_etalon=met\FFS_etalon_%test_number%\ffs_etalon_%test_number%.ffs
set ffs_resultat=met\FFS_resultat_%test_number%\ffs_resultat_%test_number%.ffs
set process_report_directory_etalon=met\XLSX_etalon_%test_number%
set process_report_directory_resultat=met\XLSX_resultat_%test_number%
set process_report_subdirectory_resultat=\met\XLSX_resultat_%test_number%
set xlsx_etalon=%process_report_directory_etalon%\xlsx_etalon_%test_number%.xlsx
set xlsx_resultat=%process_report_directory_resultat%\xlsx_resultat_%test_number%.xlsx

IF EXIST %log% del %log%
IF EXIST %ffs_resultat% del %ffs_resultat%
REM Create XLSX directory
MD %process_report_directory_resultat%
%fme% fme\BC_FGP_XML_BUILDER_PROD_04.fmw ^
--ACTIVATE_TRANSLATION %No% ^
--CATALOGUE_READER_SELECT %No% ^
--IN_FFS_TESTING_FILE %source% ^
--IN_XLS_LOOKUP_TABLE_FILE %lookup% ^
--LOCAL_WRITER %Yes% ^
--LOCAL_SOURCE_METADATA_DELTA_FINDER %Yes% ^
--OUT_XML_LOCAL_DIR %xml_resultat% ^
--OUT_FFS_MAPPING_ERROR %ffs_resultat% ^
--OUT_XLS_NOTIFICATION_DIR %process_report_directory_resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%
FIND "Client side error.  Status code 400" %log%
SET Statut=%Statut%%ERRORLEVEL%
FIND "Attribute value TOTO missing from Geospatial lookup table in GEOSPATIAL_DATA_VALIDATOR transformer.  See PROCESS_REPORT_MANUAL_TASKS.xls file in XLS directory for details." %log%
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison of FFS attribute mapping error file with the standard
IF EXIST %log_comp_ffs% del %log_comp_ffs%
%fme% met\FFS_Comparateur.fmw ^
--IN_ETALON_FILE %ffs_etalon% ^
--IN_RESULTAT_FILE %ffs_resultat% ^
--LOG_FILE %log_comp_ffs% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison of XML output directory with the standard XML output directory
IF EXIST %log_comp_xml% del %log_comp_xml%
%fme% met\XML_Comparateur.fmw ^
--ETALON_SOURCE_DIR %xml_etalon% ^
--RESULTAT_SOURCE_DIR %xml_resultat% ^
--LOG_FILE %log_comp_xml% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison of XLSX Process Report with the standard
IF EXIST %log_comp_xlsx% del %log_comp_xlsx%
REM Move XLSX file written to subdirectory by bug to main directory
XCOPY /s/e %process_report_directory_resultat%%process_report_subdirectory_resultat% %process_report_directory_resultat%
REM Rename XLSX file with date in title to generic name for testing
RENAME %process_report_directory_resultat%\"*" "xlsx_resultat_%test_number%.xlsx"
%fme% met\XLSX_Comparateur.fmw ^
--IN_ETALON_FILE %xlsx_etalon% ^
--IN_RESULTAT_FILE %xlsx_resultat% ^
--LOG_FILE %log_comp_xlsx% 
SET Statut=%Statut%%ERRORLEVEL%
REM Remove XLSX Directory
RD %process_report_directory_resultat% /S /Q

@IF [%Statut%] EQU [000000000000] (
 @ECHO INFORMATION : Metric test passed
 @COLOR A0
 @SET CodeSortie=999999
) ELSE (
 @ECHO ERROR: Metric test failed
 @COLOR CF
 @SET CodeSortie=-1
)

REM ===========================================================================
REM We return the window to the starting directory
REM ===========================================================================
POPD
 
REM ===========================================================================
REM We pause so that the window does not close 
REM in case we have to double-click on the.bat to execute it.
REM ===========================================================================
PAUSE
COLOR
EXIT /B %CodeSortie%

