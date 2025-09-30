@if "%SCM_TRACE_LEVEL%" NEQ "4" @echo off

:: ----------------------
:: KUDU Deployment Script for Azure App Service
:: FitFriendsClub Flask Application with PostgreSQL Binary Enforcement
:: ----------------------

setlocal enabledelayedexpansion

SET ARTIFACTS=%~dp0%..\artifacts

IF NOT DEFINED DEPLOYMENT_SOURCE (
  SET DEPLOYMENT_SOURCE=%~dp0%.
)

IF NOT DEFINED DEPLOYMENT_TARGET (
  SET DEPLOYMENT_TARGET=%ARTIFACTS%\wwwroot
)

IF NOT DEFINED NEXT_MANIFEST_PATH (
  SET NEXT_MANIFEST_PATH=%ARTIFACTS%\manifest

  IF NOT DEFINED PREVIOUS_MANIFEST_PATH (
    SET PREVIOUS_MANIFEST_PATH=%ARTIFACTS%\manifest
  )
)

IF NOT DEFINED KUDU_SYNC_CMD (
  :: Install kudu sync
  echo Installing Kudu Sync
  call npm install kudusync -g --silent
  IF !ERRORLEVEL! NEQ 0 goto error
  
  :: Locally just running "kuduSync" would also work
  SET KUDU_SYNC_CMD=%appdata%\npm\kuduSync.cmd
)

goto Deployment

:: Utility Functions
:: -----------------

:SelectPythonVersion

IF DEFINED KUDU_SELECT_PYTHON_VERSION_CMD (
  call %KUDU_SELECT_PYTHON_VERSION_CMD% "%DEPLOYMENT_SOURCE%" "%DEPLOYMENT_TARGET%" "%DEPLOYMENT_TEMP%"
  IF !ERRORLEVEL! NEQ 0 goto error

  SET /P PYTHON_RUNTIME=<"%DEPLOYMENT_TEMP%\__PYTHON_RUNTIME.tmp"
  IF !ERRORLEVEL! NEQ 0 goto error

  SET PYTHON_VER=%PYTHON_RUNTIME:~-2%
  SET PYTHON_EXE=%SYSTEMDRIVE%\home\python%PYTHON_VER%\python.exe
)

goto :EOF

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Deployment
:: ----------

:Deployment
echo Handling python deployment.

:: 1. KuduSync
IF /I "%IN_PLACE_DEPLOYMENT%" NEQ "1" (
  call :ExecuteCmd "%KUDU_SYNC_CMD%" -v 50 -f "%DEPLOYMENT_SOURCE%" -t "%DEPLOYMENT_TARGET%" -n "%NEXT_MANIFEST_PATH%" -p "%PREVIOUS_MANIFEST_PATH%" -i ".git;.hg;.deployment;deploy.cmd"
  IF !ERRORLEVEL! NEQ 0 goto error
)

:: 2. Select Python Version
call :SelectPythonVersion

pushd "%DEPLOYMENT_TARGET%"

:: 3. Set environment variables for binary installation
echo Setting environment variables for PostgreSQL binary enforcement...
set PIP_NO_CACHE_DIR=1
set PIP_PREFER_BINARY=1
set PIP_ONLY_BINARY=psycopg2,psycopg2-binary
set PYTHONDONTWRITEBYTECODE=1

:: 4. Install Python packages
IF EXIST backend\requirements-flexible.txt (
  echo Installing packages from requirements-flexible.txt...
  %PYTHON_EXE% -m pip install --upgrade pip
  %PYTHON_EXE% -m pip install --no-cache-dir --prefer-binary --only-binary=:all: -r backend\requirements-flexible.txt
  IF !ERRORLEVEL! NEQ 0 goto error
) ELSE (
  IF EXIST backend\requirements.txt (
    echo Installing packages from requirements.txt...
    %PYTHON_EXE% -m pip install --upgrade pip  
    %PYTHON_EXE% -m pip install --no-cache-dir --prefer-binary --only-binary=:all: -r backend\requirements.txt
    IF !ERRORLEVEL! NEQ 0 goto error
  )
)

:: 5. Verify PostgreSQL installation
echo Verifying PostgreSQL installation...
%PYTHON_EXE% -c "import psycopg2; print('PostgreSQL support verified:', psycopg2.__version__)"
IF !ERRORLEVEL! NEQ 0 (
  echo WARNING: PostgreSQL verification failed, but continuing...
)

popd

goto end

:: Execute command routine that will echo out when error
:ExecuteCmd
setlocal
set _CMD_=%*
call %_CMD_%
if "%ERRORLEVEL%" NEQ "0" echo Failed exitCode=%ERRORLEVEL%, command=%_CMD_%
exit /b %ERRORLEVEL%

:error
endlocal
echo An error has occurred during web site deployment.
call :exitSetErrorLevel
call :exitFromFunction 2>nul

:exitSetErrorLevel
exit /b 1

:exitFromFunction
()

:end
endlocal
echo Finished successfully.