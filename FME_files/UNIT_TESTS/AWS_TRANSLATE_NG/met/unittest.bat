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
SET NomApp=AWS_TRANSLATE_NG
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


REM ===========================================================================
REM Test#1: Everything is fine
REM ===========================================================================
set test_number=1
set etalon=met\etalon%test_number%.ffs
set resultat=met\resultat%test_number%.ffs
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log
set activate_translation=No
set mode="English-->French"
set attr_2_translate=notes,title,sector,dummy
set attr_list_2_translate=tags{}.display_name,resources{}.name,dummy{}.name

IF EXIST %log% del %log%
IF EXIST met\resultat%test_number%.ffs DEL met\resultat%test_number%.ffs
%fme% met\metrique_aws_translate_ng.fmw ^
--ACTIVATE_TRANSLATION %activate_translation% ^
--MODE %mode% ^
--ATTR_2_TRANSLATE %attr_2_translate% ^
--ATTR_LIST_2_TRANSLATE %attr_list_2_translate% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparison with the standard
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_ETALON_FILE %etalon% ^
--IN_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%


REM ===========================================================================
REM Test#2: AWS is active but not acessible
REM ===========================================================================
set test_number=2
set resultat=met\resultat%test_number%.ffs
set log=met\log_%test_number%.log
set log_comp=met\log_comp_%test_number%.log
set activate_translation=Yes
set mode="English-->French"
set attr_2_translate=notes,title,sector,dummy
set attr_list_2_translate=tags{}.display_name,resources{}.name,dummy{}.name

IF EXIST %log% del %log%
IF EXIST met\resultat%test_number%.ffs DEL met\resultat%test_number%.ffs
%fme% met\metrique_aws_translate_ng.fmw ^
--ACTIVATE_TRANSLATION %activate_translation% ^
--MODE %mode% ^
--ATTR_2_TRANSLATE %attr_2_translate% ^
--ATTR_LIST_2_TRANSLATE %attr_list_2_translate% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "Unable to fully translate all the attributes" %log%
SET Statut=%Statut%%ERRORLEVEL%

@IF [%Statut%] EQU [000000] (
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

