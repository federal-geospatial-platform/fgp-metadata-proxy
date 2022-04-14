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
SET NomApp=XML_PUBLISHER
SET fme=%fme2018%


SET UserProfileFmx="%FME_USER_RESOURCE_DIR%\Transformers\%NomApp%.fmx"

REM ===========================================================================
REM Initialization of the variable that contains the result of the execution
REM ===========================================================================
SET Statut=0

REM ===========================================================================
REM Copy FMX to Documents
REM ===========================================================================
COPY/Y fme\%NomApp%.fmx %UserProfileFmx%
SET Statut=%Statut%%ERRORLEVEL%

REM Define sources


REM First FME call,creating One XML record
REM  1 tag, 1 ref system, 1 transfer option, 1 distribution format, 1 topic
set test_number=1
SET source=met-xml\source%test_number%.ffs
set lookup=met-xml\Config_BC_XML_Publisher.xlsx
set etalon=met-xml\etalon%test_number%.xml
set log=met-xml\log_%test_number%.log
set log_comp=met-xml\log_comp_%test_number%.log


IF EXIST %log% del %log%
IF EXIST met-xml\resultat.xml DEL met-xml\resultat.xml
fme.exe met-xml\metrique_xml_publisher.fmw ^
--IN_FFS_FILE %source% ^
--LOOKUP_TABLE %lookup% ^
--OUT_XML_DIR met-xml ^
--SELECT_METHOD Local ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp% del %log_comp%
fme.exe met-xml\Comparateur.fmw ^
--IN_XML_ETALON %etalon% ^
--IN_XML_RESULTAT met-xml\resultat.xml ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Second FME call,creating One XML record
REM  3 tag, 2 ref system, 7 transfer option, 5 distribution format, 2 topic
set test_number=2
SET source=met-xml\source%test_number%.ffs
set lookup=met-xml\Config_BC_XML_Publisher.xlsx
set etalon=met-xml\etalon%test_number%.xml
set log=met-xml\log_%test_number%.log
set log_comp=met-xml\log_comp_%test_number%.log


IF EXIST %log% del %log%
IF EXIST met-xml\resultat.xml DEL met-xml\resultat.xml
fme.exe met-xml\metrique_xml_publisher.fmw ^
--IN_FFS_FILE %source% ^
--LOOKUP_TABLE %lookup% ^
--OUT_XML_DIR met-xml ^
--SELECT_METHOD Local ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp% del %log_comp%
fme.exe met-xml\Comparateur.fmw ^
--IN_XML_ETALON %etalon% ^
--IN_XML_RESULTAT met-xml\resultat.xml ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Third FME call,Testing for attribute error
set test_number=3
SET Source=met-xml\source1.ffs
set etalon=met-xml\etalon1.xml
set log=met-xml\log_%test_number%.log
set log_comp=met-xml\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met-xml\resultat.xml DEL met-xml\resultat.xml
fme.exe met-xml\metrique_xml_publisher.fmw ^
--IN_FFS_FILE %source% ^
--LOOKUP_TABLE %lookup% ^
--OUT_XML_DIR met-xml ^
--SELECT_METHOD TOTO ^
--LOG_FILE %log% 
FIND "ERROR: Unknown method.  Value must be Local, Insert or Update." %log%
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [0000000] (
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

