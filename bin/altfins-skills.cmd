@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "ROOT_CANDIDATE="

if exist "%SCRIPT_DIR%repo\scripts\skills.py" set "ROOT_CANDIDATE=%SCRIPT_DIR%repo"
if not defined ROOT_CANDIDATE if exist "%SCRIPT_DIR%..\repo\scripts\skills.py" set "ROOT_CANDIDATE=%SCRIPT_DIR%..\repo"
if not defined ROOT_CANDIDATE if exist "%SCRIPT_DIR%..\scripts\skills.py" set "ROOT_CANDIDATE=%SCRIPT_DIR%.."

if not defined ROOT_CANDIDATE (
  echo Could not locate the altfins-ai-skills repository data. Set ALTFINS_SKILLS_ROOT explicitly if needed. 1>&2
  exit /b 1
)

set "ALTFINS_SKILLS_ROOT=%ROOT_CANDIDATE%"
if defined ALTFINS_SKILLS_PYTHON (
  "%ALTFINS_SKILLS_PYTHON%" "%ALTFINS_SKILLS_ROOT%\scripts\skills.py" %*
  exit /b %ERRORLEVEL%
)

py -3 "%ALTFINS_SKILLS_ROOT%\scripts\skills.py" %*
if %ERRORLEVEL% EQU 9009 python "%ALTFINS_SKILLS_ROOT%\scripts\skills.py" %*
exit /b %ERRORLEVEL%
