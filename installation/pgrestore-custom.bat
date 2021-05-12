@echo off

set PGPASSWORD=postgres45


echo.
echo.
echo.
echo. 
echo Remove first met pgdrop-cashregister.bat database if already exist
echo.
echo.
echo You are going to replace database catering.
echo Press a key to restore ........
echo.
echo or press  CTRL+C to cancel
echo.
pause > nul
echo.
echo.
echo Restoring database catering by  catering.backup
echo.
echo.
echo.
"C:\ProgramData\postgres\bin\createdb.exe" -h  localhost -p 5432 -U postgres -w catering
"C:\ProgramData\postgres\bin\pg_restore.exe" --dbname=catering  --verbose "C:\ProgramData\Catering\installation\full_catering.backup"
echo.
echo Database catering is restored!
echo.
echo Press a key to end program .........
pause > nul
