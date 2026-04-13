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
  if exist "%ALTFINS_SKILLS_PYTHON%" (
    "%ALTFINS_SKILLS_PYTHON%" "%ALTFINS_SKILLS_ROOT%\scripts\skills.py" %*
    exit /b %ERRORLEVEL%
  )
  echo ALTFINS_SKILLS_PYTHON is set but not executable: %ALTFINS_SKILLS_PYTHON% 1>&2
)

where /q py.exe
if not errorlevel 1 (
  py -3.12 "%ALTFINS_SKILLS_ROOT%\scripts\skills.py" %*
  if %ERRORLEVEL% EQU 0 exit /b 0
  py -3 "%ALTFINS_SKILLS_ROOT%\scripts\skills.py" %*
  if %ERRORLEVEL% EQU 0 exit /b 0
)

where /q python3.12.exe
if not errorlevel 1 (
  python3.12 "%ALTFINS_SKILLS_ROOT%\scripts\skills.py" %*
  exit /b %ERRORLEVEL%
)

where /q python3.exe
if not errorlevel 1 (
  python3 "%ALTFINS_SKILLS_ROOT%\scripts\skills.py" %*
  exit /b %ERRORLEVEL%
)

where /q python.exe
if not errorlevel 1 (
  python "%ALTFINS_SKILLS_ROOT%\scripts\skills.py" %*
  exit /b %ERRORLEVEL%
)

echo Could not find a usable Python interpreter. Tried ALTFINS_SKILLS_PYTHON, py -3.12, py -3, python3.12, python3, and python. 1>&2
exit /b 1
