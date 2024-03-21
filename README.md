Dnamro's Battlefield 2 Navmesh Generator

This is a navmesh generator for Battlefield 2 and BF2142(Battlefield 2142 may need extra modifications)

Creator: Dnamro

Purpose:  To rewrite the DICE Navmesh generator completely in a menu driven Python version 3 script automating as much as possible, adding helpful tips during the process.  This is based on a verion of Python 2.7 that I have been working on for a while.  I have more to add, but wanted to released the current version which does everthing that the DICE version did and more.

Current Improvements over DICE Navmesh scripts:   
- Menu Driven (as apposed to command line)
- All in one Python script (as opposed to different command line scripts that had to be run seperately)
- Creates backups automatically.
- Adds a lot of error checking for missing files.  
- Automatically copies the largest navmesh islands.
- Has an option to run the Fixnavmesh step automatic or manual
   Automatic option: Uses the largest navmesh islands for both infantry and vehicle obj files.
   Manual Option:  This is for when the infantry/vehicle obj files are manually edited.
- Does not automatically launch the Editor (which does not seem to work correctly with Win 10/11), 
   instead tells you when you need launch it and provides reminder tips for the next steps. 
- Allows for the use of the DICE navmesh.exe or the new NavMeshBang.exe

Planned enhancements:
- Check for missing AI files and fix common AI issues.  
- Add more failure suport detertion and provide helpful tips to resolve them.
- Add a step by step PDF tutorial.

Required:

Python version 3.x (Freely available)
Battlefield 2 Editor 

Optional:  
3d modeling tool.  Blender (Open source) could be used..
Advanced Navmeshtool (This also replaced the DICE Navmesh python script tools, but does not work with Win 11.  
  It does include an updated navmeshBang.exe that can replace the existing navmesh.exe to reduce the problem of over of over optimization of large maps that should help reduce in game crashes.)
https://www.moddb.com/games/battlefield-2/downloads/advance-navmesh-tool

Setup:
There are two files included: 

_CreateNavmesh3.bat  - this opens a command windows to catch any errors and runs _CreateNavmesh3.bat 
CreateNavmesh3.py - this is the python script that does all the work.

In the Bf2editor folder, copy the two files to the navmesh folder.

If your Python was not installed with the path variable, then edit the _CreateNavmesh3.bat file in notepad 
	and edit this line:

python.exe CreateNavmesh3.py 

Add your location to python.exe for your system.

Example:  c:\program files\python\python3.exe CreateNavmesh3.py 

Note:  This is also how you would use the tool if you have both python 2.7 and Python 3.x installed.

You will edit the CreateNavmesh3.py file with notepad or another text editor like Notepad++
Look for this line:
_ModName = "Edit_BF2"

You will need to change it to your Bf2 editor folder that is after the \mods\ folder that you used to edit maps with the editor.

On my system, my folder looks this:
 \Battlefield_2_Editor\mods\Edit_Bf2

the script will look in the Battlefield_2_Editor\mods for the mod listed on the _ModName line.

If you want to try the NavMeshBang.exe 

Change:
_NavmeshGenerator = "NavMesh.exe";
to:
#_NavmeshGenerator = "NavMeshBang.exe"; 

To run:   Just double click on  _CreateNavmesh3.bat

Questions or suggestions:
Dnamro16@gmail.com
