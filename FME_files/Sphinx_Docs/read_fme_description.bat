REM ===========================================================================
REM Enable local variables 
REM ===========================================================================
SETLOCAL ENABLEDELAYEDEXPANSION

REM ===========================================================================
REM Allow accented characters
REM ===========================================================================
chcp 1252

REM ===========================================================================
REM Choice of running workspaces, customs or both
REM ===========================================================================
echo off
:begin
echo Select a task:
echo =============
echo -
echo 1) Read only FME Customs transformers descriptions.
echo 2) Read only FME Workspaces descriptions.
echo 3) Read both (Customs and Workspaces).
echo -
set /p op=Type option:
if "%op%"=="1" goto op1
if "%op%"=="2" goto op2
if "%op%"=="3" goto op3

echo Please Pick an option:
goto begin

REM Setting the right variable according to the choice
REM ===========================================================================
:op1
echo Read only FME Customs transformers descriptions.
set choice=customs
goto debutworkspace

:op2
echo Read only FME Workspaces descriptions.
set choice=workspaces
goto debutworkspace

:op3
echo Read both (Customs and Workspaces).
set choice=both
goto debutworkspace


REM Once choice has been made, we ship the others options
REM ===========================================================================
:debutworkspace

REM ===========================================================================
REM Determine the directory where the.bat is located and place it  
REM in the directory above while keeping the original directory
REM ===========================================================================
SET Repertoire=%~dp0
SET FMWfolder=%Repertoire%\..\FME_Workspaces\tools\
PUSHD %FMWfolder%

REM Define FME transformer path
SET FME_USER_RESOURCE_DIR=%USERPROFILE%\Documents\FME

REM ===========================================================================
REM Create file name variable in relative mode.
REM ===========================================================================
SET NomApp=reading_FME_description
SET fme=%FME2020%

REM ===========================================================================
REM Initialization of the variable that contains the result of the execution
REM ===========================================================================
SET Statut=0


REM First FME call
REM ===========================================================================
set IN_FMW_DIR=..\*.fmw
set OUT_XML_Workspace_DIR=..\..\Sphinx_Docs\source\html_FME_Doc
set IN_FMX_DIR=..\..\FME_Custom_Transformers\*.fmx
set OUT_XML_Customs_DIR=..\..\Sphinx_Docs\source\html_FME_Doc
set log=reading_FME_description.log


IF EXIST %log% del %log%
%fme% reading_FME_description.fmw ^
--IN_FMW_DIR %IN_FMW_DIR% ^
--OUT_XML_Workspace_DIR %OUT_XML_Workspace_DIR% ^
--IN_FMX_DIR %IN_FMX_DIR% ^
--OUT_XML_Customs_DIR %OUT_XML_Customs_DIR% ^
--ACTIVATE_READING %choice% ^
--LOG_FILE %log%
SET Statut=%Statut%%ERRORLEVEL%


@IF [%Statut%] EQU [00] (
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

