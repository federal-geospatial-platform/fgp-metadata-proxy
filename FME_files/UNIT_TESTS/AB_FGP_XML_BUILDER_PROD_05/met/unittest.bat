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
SET Wsfolder=%Repertoire%\..\..\..\FME_Workspaces\
PUSHD %Wsfolder%

REM Define FME workspace path
SET FME_USER_RESOURCE_DIR=%USERPROFILE%\Documents\FME

REM ===========================================================================
REM Create file name variable in relative mode.
REM ===========================================================================
SET NomApp=AB_FGP_XML_BUILDER_PROD_05
SET fme=%FME2019%


SET UserProfileFmw="%FME_USER_RESOURCE_DIR%\Workspaces\%NomApp%.fmw"

REM ===========================================================================
REM Initialization of the variable that contains the result of the execution
REM ===========================================================================
SET Statut=0

REM ===========================================================================
REM Copy FMX to Documents
REM ===========================================================================
COPY/Y %Wsfolder%\%NomApp%.fmw %UserProfileFmw%
SET Statut=%Statut%%ERRORLEVEL%

PUSHD %Repertoire%\..

REM Define sources

REM First FME call, processing FFS file with 2402 source data files to output 169 XML files without error.
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
%fme% %UserProfileFmw% ^
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

REM Comparison of XML output directory with the standard XML output directory
IF EXIST %log_comp_xml% del %log_comp_xml%
%fme% met\XML_Comparateur.fmw ^
--ETALON_SOURCE_DIR %xml_etalon% ^
--RESULTAT_SOURCE_DIR %xml_resultat% ^
--LOG_FILE %log_comp_xml% 
SET Statut=%Statut%%ERRORLEVEL%

REM Second FME call, processing FFS file with 2402 source data records to output to the dataset created in first FME call, and output is two updated records, and one deleted record due to missing map service.  Items have been removed from lookup table to throw errors, writing 403 items to ATTRIBUTE MAPPING ERRORS FFS file and two items to the XLS action items file.

set test_number=2
set source=met\source%test_number%.ffs
set lookup=met\P-T_ETL_LOOKUP_TABLES_2.xlsx
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
%fme% %UserProfileFmw% ^
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

REM Comparison of XML output directory with the standard XML output directory
IF EXIST %log_comp_xml% del %log_comp_xml%
%fme% met\XML_Comparateur.fmw ^
--ETALON_SOURCE_DIR %xml_etalon% ^
--RESULTAT_SOURCE_DIR %xml_resultat% ^
--LOG_FILE %log_comp_xml% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison of FFS attribute mapping error file with the standard
IF EXIST %log_comp_ffs% del %log_comp_ffs%
%fme% met\FFS_Comparateur.fmw ^
--IN_ETALON_FILE %ffs_etalon% ^
--IN_RESULTAT_FILE %ffs_resultat% ^
--LOG_FILE %log_comp_ffs% 
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

@IF [%Statut%] EQU [00000000] (
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

