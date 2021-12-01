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
SET NomApp=NB_ATTRIBUTE_MANAGER
SET metrique=metrique_NB_ATTRIBUTE_MANAGER
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

REM Définition des source 
REM Source 1
REM Une feature témoin sans erreur
REM Source 2
REM Deux features : 1.La feature témoin 2.Une feature avec id = ksan-r62m qui doit être discatée.
REM Source 3
REM Une feature sans liste de tags{}
REM Source 4
REM Une feature sans l'attribut "category"
REM Source 5
REM Une feature sans l'attribut "metadata.custom_fields.Department / Ministère.Department / Ministère"
REM Source 6
REM Une feature avec l'attribut "metadata.custom_fields.Department / Ministère.Department / Ministère", mais sans séparation (slash) en/fr
REM Source 7
REM Une feature sans les attributs "attribution" et "metadata.custom_fields.Department / Ministère.Department / Ministère"
REM Source 8
REM Une feature avec un champ de date non comforme

REM ============================================================================
REM ========================== TEST  #1   ======================================
REM ============================================================================
REM On test une feature témoin incluant tous les champs requis.
REM ============================================================================
SET test_number=1
SET source=met\source_%test_number%.ffs
SET etalon=met\etalon_1_2.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\%metrique%.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #2   ======================================
REM ============================================================================
REM On test une feature comportant un id à discarter.
REM ============================================================================
SET test_number=2
SET source=met\source_%test_number%.ffs
SET etalon=met\etalon_1_2.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\%metrique%.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%

FIND "dataset_to_discard_name dataset with id value ksan-r62m has been succesfully discarded." %log%
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #3   ======================================
REM ============================================================================
REM On test une feature sans list de "tags{}". Une nouvelle liste doit être créée avec la valeur default_domain_tag_value.
REM ============================================================================
SET test_number=3
SET source=met\source_%test_number%.ffs
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\%metrique%.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #4   ======================================
REM ============================================================================
REM On test une feature sans attribut "category". 
REM Un nouvel attribut "category" doit être créé avec la valeur default_category.
REM ============================================================================
SET test_number=4
SET source=met\source_%test_number%.ffs
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\%metrique%.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #5   ======================================
REM ============================================================================
REM On test une feature sans attribut "metadata.custom_fields.Department / Ministère.Department / Ministère".
REM De nouveaux attributs "sector" et "sector_fr" doivent être créés avec les valeurs en/fr de l'attribut "attribution".
REM ============================================================================
SET test_number=5
SET source=met\source_%test_number%.ffs
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\%metrique%.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #6   ======================================
REM ============================================================================
REM On test une feature avec l'attribut "metadata.custom_fields.Department / Ministère.Department / Ministère" dont la valeur est sans séparation en/fr.
REM De nouveaux attributs sector et sector_fr doivent être créés avec la valeur unique de l'attribut "metadata.custom_fields.Department / Ministère.Department / Ministère"
REM ============================================================================
SET test_number=6
SET source=met\source_%test_number%.ffs
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\%metrique%.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #7   ======================================
REM ============================================================================
REM On test une feature sans les attributs "attribution" et "metadata.custom_fields.Department / Ministère.Department / Ministère".
REM De nouveaux attributs "sector" et "sector_fr" doivent être créés avec la valeur de l'attribut "attribution".
REM ============================================================================
SET test_number=7
SET source=met\source_%test_number%.ffs
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\%metrique%.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%


REM ============================================================================
REM ========================== TEST  #8   ======================================
REM ============================================================================
REM On test une feature avec un champ de date non conforme.
REM ============================================================================
SET test_number=8
SET source=met\source_%test_number%.ffs
SET etalon=met\etalon_%test_number%.ffs
SET resultat=met\resultat_%test_number%.ffs
SET log=met\log_%test_number%.log
SET log_comp=met\log_comp_%test_number%.log

IF EXIST %log% del %log%
IF EXIST %resultat% DEL %resultat%
%fme% met\%metrique%.fmw ^
--IN_FFS_FILE %source% ^
--OUT_FFS_FILE %resultat% ^
--LOG_FILE %log% 
SET Statut=%Statut%%ERRORLEVEL%

REM Comparaison avec l'étalon
IF EXIST %log_comp% del %log_comp%
%fme% met\Comparateur.fmw ^
--IN_FFS_ETALON_FILE %etalon% ^
--IN_FFS_RESULTAT_FILE %resultat% ^
--LOG_FILE %log_comp% 
SET Statut=%Statut%%ERRORLEVEL%



@IF [%Statut%] EQU [0000000000000000000] (
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