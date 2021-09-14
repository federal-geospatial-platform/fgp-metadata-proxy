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
SET Ctfolder=%Repertoire%\..\..\..\FME_Custom_Transformers\
PUSHD %Ctfolder%

REM Define FME transformer path
SET FME_USER_RESOURCE_DIR=%USERPROFILE%\Documents\FME

REM ===========================================================================
REM Create file name variable in relative mode.
REM ===========================================================================
SET NomApp=AB_MISSING_ATTRIBUTE_MANAGER
SET fme=%FME2020%


SET UserProfileFmx="%FME_USER_RESOURCE_DIR%\Transformers\%NomApp%.fmx"

REM ===========================================================================
REM Initialization of the variable that contains the result of the execution
REM ===========================================================================
SET Statut=0

REM ===========================================================================
REM Copy FMX to Documents
REM ===========================================================================
COPY/Y %Ctfolder%\%NomApp%.fmx %UserProfileFmx%
SET Statut=%Statut%%ERRORLEVEL%

PUSHD %Repertoire%\..

REM Define sources

REM First FME call,creating One XML record
REM  1 tag, 1 ref system, 1 transfer option, 1 distribution format, 1 topic
set test_number=1
SET source=met\source%test_number%.ffs
set lookup=met\Config_QC_XML_Publisher.xlsx
set etalon=met\etalon%test_number%.xml
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log


IF EXIST %log% del %log%
IF EXIST met\resultat.xml DEL met\resultat.xml
%fme% met\metrique_xml_publisher.fmw ^
--IN_FFS_FILE %source% ^
--LOCAL_WRITER Yes ^
--LOOKUP_TABLE %lookup% ^
--OUT_XML_DIR met ^
--METHOD_SELECT Insert ^
--TEMPLATE_GMD_CITEDRESPONSIBLEPARTY met\GMD_CITEDRESPONSIBLEPARTY.xml ^
--TEMPLATE_GMD_CONTACT met\GMD_CONTACT.xml ^
--TEMPLATE_GMD_DISTRIBUTIONFORMAT met\GMD_DISTRIBUTIONFORMAT.xml ^
--TEMPLATE_GMD_DISTRIBUTOR met\GMD_DISTRIBUTOR.xml ^
--TEMPLATE_GMD_KEYWORDS met\GMD_KEYWORDS.xml ^
--TEMPLATE_GMD_MDMETADATA met\GMD_MDMETADATA.xml ^
--TEMPLATE_GMD_REFERENCESYSTEMINFO met\GMD_REFERENCESYSTEMINFO.xml ^
--TEMPLATE_GMD_RESOURCEMAINTENANCE met\GMD_RESOURCEMAINTENANCE.xml ^
--TEMPLATE_GMD_TOPICCATEGORY met\GMD_TOPICCATEGORY.xml ^
--TEMPLATE_GMD_TRANSFEROPTIONS met\GMD_TRANSFEROPTIONS.xml ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_XML_ETALON %etalon% ^
--IN_XML_RESULTAT met\resultat.xml ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Second FME call,creating One XML record
REM  3 tag, 3 ref system, 21 transfer option, 11 distribution format, 1 topic
set test_number=2
SET source=met\source%test_number%.ffs
set lookup=met\Config_QC_XML_Publisher.xlsx
set etalon=met\etalon%test_number%.xml
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.xml DEL met\resultat.xml
%fme% met\metrique_xml_publisher.fmw ^
--IN_FFS_FILE %source% ^
--LOCAL_WRITER Yes ^
--LOOKUP_TABLE %lookup% ^
--OUT_XML_DIR met ^
--METHOD_SELECT Insert ^
--TEMPLATE_GMD_CITEDRESPONSIBLEPARTY met\GMD_CITEDRESPONSIBLEPARTY.xml ^
--TEMPLATE_GMD_CONTACT met\GMD_CONTACT.xml ^
--TEMPLATE_GMD_DISTRIBUTIONFORMAT met\GMD_DISTRIBUTIONFORMAT.xml ^
--TEMPLATE_GMD_DISTRIBUTOR met\GMD_DISTRIBUTOR.xml ^
--TEMPLATE_GMD_KEYWORDS met\GMD_KEYWORDS.xml ^
--TEMPLATE_GMD_MDMETADATA met\GMD_MDMETADATA.xml ^
--TEMPLATE_GMD_REFERENCESYSTEMINFO met\GMD_REFERENCESYSTEMINFO.xml ^
--TEMPLATE_GMD_RESOURCEMAINTENANCE met\GMD_RESOURCEMAINTENANCE.xml ^
--TEMPLATE_GMD_TOPICCATEGORY met\GMD_TOPICCATEGORY.xml ^
--TEMPLATE_GMD_TRANSFEROPTIONS met\GMD_TRANSFEROPTIONS.xml ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_XML_ETALON %etalon% ^
--IN_XML_RESULTAT met\resultat.xml ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Third FME call,creating One XML record
REM  9 tag, 6 ref system, 9 transfer option, 6 distribution format, 1 topic, all attribute fields populated
set test_number=3
SET source=met\source%test_number%.ffs
set lookup=met\Config_QC_XML_Publisher.xlsx
set etalon=met\etalon%test_number%.xml
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.xml DEL met\resultat.xml
%fme% met\metrique_xml_publisher.fmw ^
--IN_FFS_FILE %source% ^
--LOCAL_WRITER Yes ^
--LOOKUP_TABLE %lookup% ^
--OUT_XML_DIR met ^
--METHOD_SELECT Insert ^
--TEMPLATE_GMD_CITEDRESPONSIBLEPARTY met\GMD_CITEDRESPONSIBLEPARTY.xml ^
--TEMPLATE_GMD_CONTACT met\GMD_CONTACT.xml ^
--TEMPLATE_GMD_DISTRIBUTIONFORMAT met\GMD_DISTRIBUTIONFORMAT.xml ^
--TEMPLATE_GMD_DISTRIBUTOR met\GMD_DISTRIBUTOR.xml ^
--TEMPLATE_GMD_KEYWORDS met\GMD_KEYWORDS.xml ^
--TEMPLATE_GMD_MDMETADATA met\GMD_MDMETADATA.xml ^
--TEMPLATE_GMD_REFERENCESYSTEMINFO met\GMD_REFERENCESYSTEMINFO.xml ^
--TEMPLATE_GMD_RESOURCEMAINTENANCE met\GMD_RESOURCEMAINTENANCE.xml ^
--TEMPLATE_GMD_TOPICCATEGORY met\GMD_TOPICCATEGORY.xml ^
--TEMPLATE_GMD_TRANSFEROPTIONS met\GMD_TRANSFEROPTIONS.xml ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_XML_ETALON %etalon% ^
--IN_XML_RESULTAT met\resultat.xml ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

REM Fourth FME call,Testing for attribute error
set test_number=4
SET Source=met\source1.ffs
set etalon=met\etalon1.xml
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST met\resultat.xml DEL met\resultat.xml
%fme% met\metrique_xml_publisher.fmw ^
--IN_FFS_FILE %source% ^
--LOCAL_WRITER No ^
--LOOKUP_TABLE %lookup% ^
--OUT_XML_DIR met ^
--METHOD_SELECT TOTO ^
--TEMPLATE_GMD_CITEDRESPONSIBLEPARTY met\GMD_CITEDRESPONSIBLEPARTY.xml ^
--TEMPLATE_GMD_CONTACT met\GMD_CONTACT.xml ^
--TEMPLATE_GMD_DISTRIBUTIONFORMAT met\GMD_DISTRIBUTIONFORMAT.xml ^
--TEMPLATE_GMD_DISTRIBUTOR met\GMD_DISTRIBUTOR.xml ^
--TEMPLATE_GMD_KEYWORDS met\GMD_KEYWORDS.xml ^
--TEMPLATE_GMD_MDMETADATA met\GMD_MDMETADATA.xml ^
--TEMPLATE_GMD_REFERENCESYSTEMINFO met\GMD_REFERENCESYSTEMINFO.xml ^
--TEMPLATE_GMD_RESOURCEMAINTENANCE met\GMD_RESOURCEMAINTENANCE.xml ^
--TEMPLATE_GMD_TOPICCATEGORY met\GMD_TOPICCATEGORY.xml ^
--TEMPLATE_GMD_TRANSFEROPTIONS met\GMD_TRANSFEROPTIONS.xml ^
--LOG_FILE %log% 
FIND "ERROR: Unknown method.  Value must be Local, Insert or Update." %log%
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [000000000] (
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

