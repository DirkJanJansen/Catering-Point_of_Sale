@echo off

set PGPASSWORD=postgres45

echo.
echo.
echo.
echo Press a key to backup database catering.
pause > nul
echo.
"C:\ProgramData\postgres\bin\pg_dump.exe" -U postgres -v --verbose -d  catering -Fc -f  "C:\ProgramData\Catering\installation\catering.backup"
echo.
echo.
echo Backup of database catering is done.
echo.
echo Press a key to exit.
pause > nul
#-Fp Plain
#-Fc Custom
#-Fd directory
#-Ft tar
