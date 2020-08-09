@echo off
set PGPASSWORD=postgres45
echo.
echo.
echo Pay attention Database catering is being removed!!!
echo.
echo.
echo Press a key to remove!
echo.
echo.
echo or press Ctrl+C to abort
pause > nul

"C:\ProgramData\postgres\bin\dropdb.exe"  -h localhost -p 5432 -U postgres  -w catering
echo.
echo.
echo.
echo.
echo Database catering is removed.
echo.
echo.
echo.
echo Press a key for ending program .........
pause > nul
