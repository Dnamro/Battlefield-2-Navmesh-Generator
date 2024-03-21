@echo off
:start
cls
echo --------------------------------------
echo Battlefield 2  Navmesh Generation
echo 
echo Create a new NavMesh
echo updated by Dnamro
echo
echo    Purpose:
echo    1. Rewrite the Dice Navmesh ceation tools to Python 3.x
echo    2. Consolidate to one script that is menu based
echo    3. Add funcitonality to automated as much as possible.
echo    4. Add prechecks to make sure the map is set up for AI support.
echo    
echo --------------------------------------

REM make sure work dir exists
rem if not exist work md work

REM   call python script
REM   if you have python 2.x installed or you get an error that python.exe is not found, 
REM   then specify the path to where python.exe for python 3.x is installed
REM   example:  c:\program files\python\python.exe 
python.exe CreateNavmesh3.py 
pause
