import shutil
import os
import sys
import string
from os import listdir
from os.path import isfile, join
import time;
#from optparse import OptionParser;
from shutil import copyfile;
from datetime import datetime

#NavMeshBang.exe is the new version that should reduce over optimazation for larger maps 
#_NavmeshGenerator = "NavMeshBang.exe";  
_NavmeshGenerator = "NavMesh.exe"; 
# Change the line below to the mod you are working on
_ModName = "Edit_BF2"
_skipEditor = True
_cleanOldData = True
_restart = True
_LogFile = ""
_NavmeshMode = 0;  # 0 = both infantry and vehicle
_NavmeshModes = ["Infantry and Vehicle", "Infantry", "Vehicle" ];



def cls():
	os.system('cls');
	return;

################################################################################
#def findNocaseString(strings, toFind):
#    index = 0
#    lowerToFind = string.lowercase(toFind)
#    for entry in strings:
#        if (string.lower(entry) == lowerToFind):
#            return index
#        index = index + 1#
#
#    return -1

def secsToTimeString(secs):
    seconds = secs % 60;
    minutes = (secs / 60) % 60;
    hours = secs / (60 * 60);

    if (hours >= 1.0):
        return "%02d hours %02d minutes and %02d seconds" % (hours, minutes, seconds);
    elif (minutes >= 1.0):
        return "%02d minutes and %02d seconds" % (minutes, seconds);
    else:
        return "%02d seconds" % (seconds);




def executeCommand(commandLine):
    print ("Executing: " + commandLine)
    result = os.system(commandLine)
    print ("")
    return result


def copyDirectory(source, destination):
    executeCommand( "robocopy " + source + " " + destination + " /MIR")


def moveDirectory(source, destination):
    executeCommand("robocopy " + source + " " + destination + " /MOVE /MIR")


def removeDirectory(directory):
    executeCommand("rd /Q /S " + directory)

def removeFolderFiles(srcFolder):
#removes all files in a folder - Not intended for foldes with subfolders
    for file_Name in os.listdir(srcFolder): 
            if file_Name != "":
                srcfile = os.path.join(srcFolder, file_Name);
                os.remove(srcfile)
    return;
                
    
################################################################################
# Creates a backup folder by adding the timestamp to the srcFolder
# Copies files to SrcFolder
# deletes files from SrcFolder
################################################################################
def MoveToBackupFolder (srcFolder):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S");
    print("********************")
    print("Backup up files:")
    print ("From: " + srcFolder)

    backupFolder = srcFolder + timestamp   
    #os.makedirs (backupFolder)
    print ("backupFolder: " + backupFolder)
    print("********************")
    print ("!!! This may take a few seconds")
    print("********************")

    for file_Name in os.listdir(srcFolder): 
        if file_Name != "":
            srcfile = os.path.join(srcFolder, file_Name);
            dstfile = os.path.join(backupFolder, file_Name);
            #print(   "Source files:");
            print("Backup: ", srcfile);
            #os.chmod(file_Name, 0o777);
            #backup obj file 
            copyfile(srcfile, dstfile);	
            os.remove(srcfile)
            print("Deleted: ", srcfile);
    return
	#os.chdir(owd);    
    
    #destination = shutil.copytree (srcFolder, backupFolder)  
    #shutil.rmtree(srcFolder)
    #for fn in os.listdir(srcFolder):
    #    if not os.path.isdir(os.path.join(srcFolder, fn)):
    #        continue # Not a directory    
    #os.rename (GTSdataDir, GTSdataDirBackup)
    #copyFolderFiles(srcFolder, destWorkDir);

################################################################################
# Creates a backup folder by adding the timestamp to the srcFolder
# Copies files to SrcFolder with subfolders 
# deletes files from SrcFolder and subfolders
################################################################################
def MoveToBackupFolderSubs (srcFolder):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S");
    print("********************")
    print("Backup up files:")
    print ("From: " + srcFolder)

    backupFolder = srcFolder + timestamp   
    #os.makedirs (backupFolder)
    print ("backupFolder: " + backupFolder)
    #print ("... This may take a minute")

    destination = shutil.copytree (srcFolder, backupFolder) 
    print("Backup Completed")
    shutil.rmtree(srcFolder)
    print ("Removed SourceFolder")

    return
	#os.chdir(owd);    
    
    #destination = shutil.copytree (srcFolder, backupFolder)  
    #shutil.rmtree(srcFolder)
    #for fn in os.listdir(srcFolder):
    #    if not os.path.isdir(os.path.join(srcFolder, fn)):
    #        continue # Not a directory    
    #os.rename (GTSdataDir, GTSdataDirBackup)
    #copyFolderFiles(srcFolder, destWorkDir);

################################################################################
# Creates a backup folder by adding the timestamp to the srcFolder
# Copies files to SrcFolder with subfolders 
################################################################################
def CopyToBackupFolderSubs (srcFolder):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S");
    print("********************")
    print("Backup up files:")
    print ("From: " + srcFolder)

    backupFolder = srcFolder + timestamp   
    #os.makedirs (backupFolder)
    print ("backupFolder: " + backupFolder)
    #print ("... This may take a minute")

    destination = shutil.copytree (srcFolder, backupFolder) 
    print("Backup Completed")

    return

################################################################################
# Creates a backup folder by adding the timestamp to the srcFolder
# Copies files to SrcFolder
################################################################################
def CopyToBackupFolder (srcFolder):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S");
    print("********************")
    print("Backup up files:")
    print ("From: " + srcFolder)

    backupFolder = srcFolder + timestamp   
    #os.makedirs (backupFolder)
    print ("backupFolder: " + backupFolder)
    #print ("... This may take a minute")

    for file_Name in os.listdir(srcFolder): 
        if file_Name != "":
            srcfile = os.path.join(srcFolder, file_Name);
            dstfile = os.path.join(backupFolder, file_Name);
            #print(   "Source files:");
            print("Copy: ", srcfile);
            #os.chmod(file_Name, 0o777);
            #backup obj file 
            copyfile(srcfile, dstfile);	
    print ("All files copied")
    return

def runEditor(level, conScript):
    global _skipEditor
    if _skipEditor: return
    os.chdir("..")
    executeCommand("bf2editor +loadMod " + mod + " +loadLevel " + level + " +runConFileAndClose \"" + conScript + "\" +enableAsserts 0 +forceLoadPlugin SinglePlayerEditor")
    os.chdir("NavMesh")

def FixNavMenuHelp():
    print ("********************************************************")
    print ("Fix Navmesh Menu Help: Manual/Automatic");  
    print ("********************************************************")    
    print ("By default the Infantry and vehicle obj files have");
    print ("  to be edited manually to remove the islands.");
    print (">>> Automatic mode will use the largest Navmesh islands");
    print ("   so that manual editing is not required");
    print (">>> Manual Mode is when the obj files are to be hand edited");
    print ("---------------------------------------------------------")
    print ("Press any key when ready to continue");
    choice = input();    
    return;

def generateGTSDataHelp():
    print ("********************************************************")
    print ("GtsData Not Found - Can not continue until it is created");  
    print ("********************************************************")    
    print ("Load up the BF2Editor");
    print ("Change to Singleplayer Mode");
    print ("Under Stategic Area");
    print ("   Select Place on All");
    print ("   Select Generate Pathfinding");
    print (".....Save and close Editor..........");
    print ("Restart this Navmesh tool");
    print ("------------------------------------------------------")     
    print ("Press any key when ready to continue");
    choice = input();
    return;

    
def preCreateNavmeshHelp():
    print ("------------------------------------------------------")
    print ("Before Creating the navmesh In the BF2Editor:");
    print ("Copy the GPO into the map editor folder");    
    print ("Make sure a combat area is created counter clockwise");
    print ("... and usedByPathFinding option is checked");
    print ("Change to Singleplayer Mode");
    print ("Under Stategic Area");
    print ("   Select Place on All");
    print ("   Select Generate Pathfinding");
    print (".....Save and close Editor..........");
    print ("This part takes the longest time  ");
    print ("small maps might take 1-2 hours");
    print ("large maps might take 8 or more hours"); 
    print ("------------------------------------------------------")     
    print ("Press any key when ready to continue");
    choice = input();
    return;

def postCreateNavmeshHelp():
    print ("------------------------------------------------------")
    print ("Next step is to run Fix Navmesh ")
    print (">>> Automatic or Manual:")
    print (">>> Automatic - the lagest islands")
    print (">>> Manual - use this if you are editing the navmesh obj")
    print ("Both Options will clean the navmesh obj files")
    print ("and create a material file")
    print ("------------------------------------------------------")  
    print ("Press any key when ready to continue")
    choice = input();
    return;  
    
def preFixNavMeshAutoHelp():
    print ("------------------------------------------------------")
    print ("Running Automatic Fix Navmesh ")
    print ("The lagest Navmesh islands will be used")
    print ("------------------------------------------------------")    
    print ("Press any key when ready to continue")
    choice = input();
    return;  

def preFixNavMeshManualHelp():
    print ("------------------------------------------------------")
    print ("Running Manual Fix Navmesh ")
    print ("This should be run after making any manual edits")
    print (" to the infantry.obj or the vehicle.obj files ")
    print (" The files will be cleaned and a material file created")
    print ("------------------------------------------------------")
    print ("Press any key when ready to continue")
    choice = input();
    return;

def postFixNavMeshHelp():
    print ("------------------------------------------------------")
    print ("Last Step is in the BF2 Editor")
    print ("Editor Commands are In the lower right corner: ")
    print (" select Aipathfinding and then loadgtsdata")
    print (" select Aipathfinding and then savequadrees")
    print (" select Ai and then Aerialheightmap")
    print ("Then you can check out your work") 
    print ("select Render Menu - AI and select Toggle Draw Infantry navmesh") 
    print (" Then toggle the vehicle navmesh") 
    print ("------------------------------------------------------")
    print ("Press any key when ready to continue")
    choice = input();
    return;     

################################################################################
def runNavMeshControl(level, workingFolder):
    global _LogFile
    global _NavmeshGenerator
    #return executeCommand("NavMeshControl3.py " + workingFolder + "\\" + level + "\\GTSData")

    #parser = createCmdLineParser();
    #(options, args) = parser.parse_args();	
        


    meshDir = workingFolder + "\\" + level + "\\GTSData";
    print ("Meshdir: ", meshDir)
    if not(os.path.isdir(meshDir)):
        print("Folder not found -- Can NOT continue")
        return False;
    logDir = meshDir + "\\logfiles";
    logFilename = logDir + "\\navmeshcontrol.log";
    logFile = None;
    if (not os.path.isdir(logDir)):
        os.makedirs(logDir);

    _LogFile = logFilename
        

    print( "Generating navmesh for data in " + meshDir);

    # Make sure the config-file exist.
    # If it doesn't the level has probably not been exported correctly from the editor.
    #configFile = meshDir + "\\meshes\\config.dat";
    #if (not os.path.isfile(configFile)):
    #    print ("Error: Failed to find " + configFile);
    #    return False;
        
    totalStartTime = time.time();

    # Perform manifold step
    print( "Starting manifold-step");
    commandLine = _NavmeshGenerator + " -dir " + meshDir +  " -cmd manifold";
    startTime = time.time();
    result = os.system(commandLine);
    elapsedTime = secsToTimeString(time.time() - startTime)
    if (result == 0):
        print( "Manifold-step succeded in " + elapsedTime);
    else:
        print( "Manifold-step failed, aborting");
        return False;
        
    # Perform stitch step
    print( "Starting stitch-step");
    commandLine = _NavmeshGenerator + " -dir " + meshDir +  " -cmd stitch";
    #if (options.saveStitchSteps):
    #    commandLine += " -f saveStitchSteps";
        
    startTime = time.time();
    result = os.system(commandLine);
    elapsedTime = secsToTimeString(time.time() - startTime)
    if (result == 0):
        print( "Stitch-step succeded in " + elapsedTime);
    else:
        print( "Stitch-step failed, aborting");
        return False;

    # Perform opt-steps
    modes = [ "Infantry", "Vehicle"];
    for mode in modes:
        print( "Starting opt-step for " + mode);
        commandLine = _NavmeshGenerator + " -dir " + meshDir +  " -cmd opt -mode " + mode;
        
        startTime = time.time();
        result = os.system(commandLine);
        elapsedTime = secsToTimeString(time.time() - startTime)
        if (result == 0):
            print( "Opt-step succeded in " + elapsedTime);
        else:
            print( "Opt-step failed, aborting");
            return False;

    elapsedTime = secsToTimeString(time.time() - totalStartTime);
    print( "Generation-process was completed in " + elapsedTime);

    return True;    

################################################################################
def cleanupOldData(level, levelFolder):
    # Removing old data
    removeDirectory(levelFolder + "\\" + level + "\\GTSData\\Meshes")
    # Deleting oldos.pathfinding mesh...
    executeCommand("del /Q /F " + levelFolder + "\\" + level + "\\aiPathFinding\\*.*")


################################################################################
def exportGts(level, levelFolder):
    global _skipEditor
    if (_skipEditor): return True
    print ("-----------------------------------------------------------------------")
    print ("- Exporting gts-data...")
    # Export GTS data...
    runEditor(level, "exportGTS")
    print ("Done...")
    print ("")
    return True

################################################################################
def generateNavmesh(level, NavDir):
    #global _restart
    workingFolder = (NavDir +"\\work\\")
    #       + level + "\\GTSData\\Meshes");
    print ("-----------------------------------------------------------------------")
    print ("- Generating navmesh...")
    print ("Level: " + level)
    print ("workingFolder: " + workingFolder)
    if not(os.path.isdir(workingFolder)):
        print("Folder not found -- Can NOT continue")
        return False;

    # Copy GTS-files to working folder
    #if not _restart:
    #    moveDirectory(levelFolder + "\\" + level + "\\GTSData\\Meshes", workingFolder + "\\" + level + "\\GTSData\\Meshes")

    # Generate the navmesh
    result = runNavMeshControl(level, workingFolder)

    print ("Done...")
    print ("")

    if (result == 0):
        return True;
    else:
        return False;

################################################################################
def createQtrFiles(level, levelFolder, workingFolder):
    print ("-----------------------------------------------------------------------")
    print ("- Creating qtr-files...")

    print ("Copying navmesh-data to levelfolder")
    copyDirectory( workingFolder + "\\" + level + "\\GTSData\\Output", levelFolder + "\\" + level + "\\GtsData\\Output")


    print ("Converting to qtr-files")
    conScript = "saveQuadNoP4"

    #if (useP4 == True):
    #   conScript = "saveQuad"

    #runEditor(level, conScript)

    print ("Done...")
    print ("")

    return True

def getLargestFile(IslandDir):
		sofar = 0
		name = ""
		#Save current working directory
		owd = os.getcwd();
		#Change to Island directory
		os.chdir(IslandDir);
		objects = os.listdir(".")
		for item in objects:
			size = os.path.getsize(item)
			if size > sofar:
				sofar = size
				name = item
		
		#print ("Largest File Name:" + name);
		#print (IslandDir);
		#print "File size" + size
		# Reset to Original Working Directory
		os.chdir(owd);
		return name

def copyLargestFile(IslandDir, outputFile):
#set defaults
		print("Island Dir:" + IslandDir);
		print("Output File:" + outputFile);
		name = getLargestFile(IslandDir);
		if (name.endswith('.obj') and  name != "") :
			srcfile = IslandDir + "\\" + name
			print ("Copyied : " + outputFile);
			copyfile(srcfile, outputFile);	
		else:
			print(     "File not Copied - Invalid File name: ");
			print(     "Source file: " + srcfile);
			
def copyOutputFolderFiles(srcDir, outputDir):
	print(   "Copy Folder Files");
	print(   "From: " + srcDir);
	print(   "To: " + outputDir);
	#owd = os.getcwd();
	#os.chdir(srcDir);
	list = os.listdir(srcDir);
	#number_files = len(list);
	#if (number_files <= 1):
	#	print(   "Multiple Islands not found - nothing to do");
	#	os.chdir(owd);
	#	return;
	for file_Name in os.listdir(srcDir): 
		if file_Name != "":
			srcfile = os.path.join(srcDir, file_Name);
			dstfile = os.path.join(outputDir, file_Name);
			print(   "Source files:");
			print(   srcfile);
			#os.chmod(file_Name, 0o777);
			#backup obj file 
			copyfile(srcfile, dstfile);	
	#os.chdir(owd);
	return;	

def moveFolderFiles(srcDir, outputDir):
    print(   "Move Folder Files");
    print(   "From: " + srcDir);
    print(   "To: " + outputDir);
    owd = os.getcwd();
    os.chdir(srcDir);
    list = os.listdir(srcDir);
    number_files = len(list);
	#if (number_files <= 1):
	#	print(   "Multiple Islands not found - nothing to do");
	#	os.chdir(owd);
	#	return;
    if (number_files == 0):
        print(   "Folder is empty - Nothing to copy");
        print ("Source: ", srcDir);
        os.chdir(owd);
        return;    
    for file_Name in os.listdir(srcDir): 
        if file_Name != "":
            srcfile = os.path.join(srcDir, file_Name);
            dstfile = os.path.join(outputDir, file_Name);
            print(   "Source files:");
            print(   srcfile);
            os.chmod(file_Name, 0o777);
            #backup obj file 
            copyfile(srcfile, dstfile);
            os.remove(file_Name);			
    os.chdir(owd);
    return;	

def copyFolderFiles(srcDir, outputDir):
	print(   "Copy Folder Files");
	print(   "From: " + srcDir);
	print(   "To: " + outputDir);
	for file_Name in os.listdir(srcDir): 
		if file_Name != "":
			srcfile = os.path.join(srcDir, file_Name);
			dstfile = os.path.join(outputDir, file_Name);
			print(   srcfile);
			#os.chmod(file_Name, 0o777);
			#backup obj file 
			copyfile(srcfile, dstfile);	
	#os.chdir(owd);
	return;

def replaceMaterialsFile(materials_path):
	# check for materials.mtl and copy over with known good materials.mtl 
    if (os.path.exists(materials_path)):
        os.remove(materials_path);
        print(   "Remove old materials.mtl file");
        print(  "Creating New Materials.mtl file");	
    with open(materials_path, 'w') as output_file:
        output_file.write("newmtl ground\n");
        output_file.write("Ka 0.0000 0.1986 0.0000\n");
        output_file.write("Kd 0.0166 0.5922 0.0000\n");
        output_file.write("illum 1\n");
        output_file.write("\n");
        output_file.write("newmtl ladder\n");
        output_file.write("Ka 0.1986 0.1986 0.1986\n");
        output_file.write("Kd 0.5922 0.5922 0.5922\n");
        output_file.write("illum 1\n");
        output_file.write("\n");
        output_file.write("newmtl water\n");
        output_file.write("Ka 0.3200 0.3200 0.0000\n");
        output_file.write("Kd 0.9400 0.9400 0.1410\n");
        output_file.write("illum 1\n");
        output_file.write("\n");
        output_file.write("newmtl deepwater\n");
        output_file.write("Ka 0.0000 0.0000 0.3200\n");
        output_file.write("Kd 0.0000 0.0000 0.9400\n");
        output_file.write("illum 1\n");
        output_file.write("\n");
    return;

def ChangeNavmeshMode():
    cls();
    print(">>>>>>> Choose Navmesh Mode:");
    print("(0) Both Infantry and Vehicle");
    print("(1) Infantry");
    print("(2) Vehicle");
    choice = int(input());
    while ( True ):
        if ((choice < 1) or (choice > 2) ):
            print("Out of Range!  Try again:");
            choice = int(input());
        else:
            return choice
		#if (choice == "0"):
			#navmeshModeName = "Both Infantry and Vehicle";

		#elif (choice == "1"):
			#navmeshModeName = "Infantry Only";

			#break;
		#elif (choice == "2"):  
			#navmeshModeName = "Vehicle Only";


    
def CopyGTSdataWorkFiles ( levelDir, workDir):
	# check for empty source folder - 
    #      if the workdir is not empty ask to continue (using the existing data)
	# Check for target empty folder - if not delete files
	# remove readonly from file
	# xcopy ..\mods\%mod_name%\levels\%level_name%\GTSData\Meshes\*.* work\%level_name%\GTSData\Meshes\	    
    srclevelDir = levelDir + "\\GTSData\\Meshes";
    destWorkMeshesDir = workDir + "\\GTSData\\Meshes";
    print( "============");
    print( "Copy GTSdata");
    print( "From: " + srclevelDir);
    print( "To: " + destWorkMeshesDir);
    destDirStatus = False 
    srcDirStatus = False
    
    # check for no Src Dir
    if (os.path.isdir(srclevelDir)): 
        if (os.listdir(srclevelDir)): 
            srcDirStatus = True # source folder exists and  has data
    if (os.path.isdir(destWorkMeshesDir)):  
        if (os.listdir(destWorkMeshesDir)):
            destDirStatus = True # source folder exists and  has data
    #Check if there is no source to copy, check if there is dest data.  
    #  if so, ask if user wants to continue using the existing data.
    if not(srcDirStatus):  #Source dir is either empty or does not exist
        if (destDirStatus): #GTSdata exists in the dest folder
            print ("***************************************************************")
            print( "No GTSdata to copy, - Continue, but using Previous Pathfinding Data?");
            print ("Press Y to continue");
            choice = input();
            if (choice == "Y" or choice == "y"): 
                return True  # continue using existing Previous GTSdata
            else:
                generateGTSDataHelp();
                return False # Can not continue
        else:   # Dest Dir is either not empty
            generateGTSDataHelp();
            return False;                    
               
    if (srcDirStatus): #source folder has data
        if (destDirStatus): #dest folder has data that needs to backup before copy
            MoveToBackupFolder (destWorkMeshesDir); # backup dest before copying
        copyFolderFiles (srclevelDir, destWorkMeshesDir) 
        #MoveToBackupFolder (srclevelDir)  #backup the source files
        return True; 
    
    if (not srcDirStatus): 
        print ("Source Dir is either empty or has no data ")
    if (not destDirStatus): 
        print ("Dest Dir is either empty or has no data ")  
    generateGTSDataHelp();
    return False
		
	
def CopyGTSdataOutputFiles ( sourceDir, destDir):
    # Check for target empty folder - if not delete files
    sourceOutputDir = sourceDir + "\\GTSData\\output";
    destOutputDir = destDir + "\\GTSData\\output";
    print(   "Copy GTSdata Output folder files");
    print(   "Source     : " + sourceOutputDir);
    print(   "Destination: " + destOutputDir);
    owd = os.getcwd();
    if not (os.path.isdir(destOutputDir)):
        os.makedirs(destOutputDir);
        print(   "Output Folder did not exist - created");
	#os.chdir(destOutputDir);
		#for levelname in os.listdir(destWorkDir): 
			#levelpath = normpath(os.path.join(destWorkDir, levelname));
		#	os.chmod(levelname, 0o777);
			#print(filepath);
			#os.chmod(full_level_path, stat.S_IWRITE)
		#	os.remove(levelname);
		#os.chdir(owd);
        #(os.path.isfile(outputFile)):
	# Check for source empty folder - if not error and return     
    if (os.listdir(destOutputDir)):
        print( "deleting old files: ");
        for levelname in os.listdir(destOutputDir): 
            levelpath = os.path.abspath(os.path.join(destOutputDir, levelname));
            print( levelpath);
            os.remove(levelpath);    
        copyOutputFolderFiles(sourceOutputDir, destOutputDir);
    else: 	
        print(    "Failed to copy GTSdata Output files");
        print(    "Mod level folder: " );
        print(    sourceOutputDir );
        print(    "Mesh level folder: "  );
        print(    destOutputDir );
        print ("GTSdata output is empty - nothing copied");
        print ("Press a key to continue");
        choice = input();
    return;			

def	createNavmeshBackups(meshDir, meshMode):
	timestamp = datetime.now().strftime("%Y%m%d-%H%M%S");

	print(   "Backing up Navmesh obj files");
	backupFolder = (meshDir + "/GTSData/backup");	
	if (not os.path.isdir(backupFolder)):
		os.makedirs( backupFolder);
		
	if (meshMode == 1 or meshMode == 0): 
		print(   "Backing up Infantry.obj");
		outputFile = meshDir + "/GTSData/output/infantry.obj";
		backupName = ("Infantry_" + timestamp + ".obj");
		backupFile = (meshDir + "/GTSData/backup/" + backupName);
		
		#backup infantry.obj if it exists
		if (os.path.isfile(outputFile)): 
			copyfile(outputFile, backupFile);
			print(    "Saved a backup of infantry.obj to:");
			print(    backupFile);
		else:
			print(    "infantry.obj Not found at:");
			print(    backupFile);	

	if (meshMode == 2 or meshMode == 0): 
		print("Backing up Vehicle.obj");
		outputFile = meshDir + "/GTSData/output/vehicle.obj";
		backupName = ("Vehicle_" + timestamp + ".obj");
		backupFile = (meshDir + "/GTSData/backup/" + backupName);
		#backup vehicle.obj 
		if (os.path.isfile(outputFile)): 
			copyfile(outputFile, backupFile);
			print ( "Saved a backup of Vehicle.obj to:");
			print (  backupFile);
		else:
			print (  "Vehicle.obj Not found at:");
			print(   backupFile);	

def copyIslands(meshDir, meshMode):
    print ("Copy Largest Navmesh Islands") 
    print ("Meshdir:", meshDir )
    createNavmeshBackups(meshDir, meshMode);

    # Check for Infantry islands
        
    if (meshMode == 1 or meshMode == 0): 
        print(   "Checking Infantry Islands");
        IslandDir = meshDir + "\\GTSData\\debug\\islands\\infantry";
        outputFile = meshDir + "\\GTSData\\output\\infantry.obj";
        if not (os.path.isdir(IslandDir)):
            print(   "Island Dir:" + IslandDir); 
            print(   "Infantry Island not found - press any key to return to main menu");
            choice = input();
            return;
        if os.listdir(IslandDir):		
            copyLargestFile(IslandDir, outputFile);	
            print(    "Infantry island Navmesh Found and Copied");  
    # Check for vehicle islands
    if (meshMode == 2 or meshMode == 0): 
        print(   "Checking Vehicle Islands");
        IslandDir = meshDir + "\\GTSData\\debug\\islands\\vehicle\\";
        outputFile = meshDir + "\\GTSData\\output\\vehicle.obj";
        if not (os.path.isdir(IslandDir)):
            print(   "Island Dir:" + IslandDir);
            print(   "Vehicle Navmesh Island not found - press any key to return to main menu");
            choice = input();
            return;
        if os.listdir(IslandDir):
            copyLargestFile(IslandDir, outputFile);	
            print(    "Vehicle island Navmesh Found and Copied");	
    print("Navmesh Island Check Complete - press any key to return to main menu");
    return;
    
def backupNavWorkArea(level_name, navmesh_dir):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S");
    workFolder = "work" 
    print ("------------------------------")
    print ("Backing up Navmesh work area");
    #navmesh_dir = os.path.abspath(os.path.join(os.getcwd(),"."));
    print ("For selected Map: " + level_name);
    print ("Navmesh Dir: " + navmesh_dir);
    print ("!!! this can take a few seconds")
    print ("------------------------------")
    #workDir = navmesh_dir + "\\work\\";
    workDir = navmesh_dir + "\\work"
    workLevelDir = workDir + "\\" + level_name ; 
    workGTSdataDir = workLevelDir + "\\GTSData";
    workGTSdataDirBak = workLevelDir + "\\GTSData" + timestamp ;
    workMeshDir = workGTSdataDir + "\\meshes";
    #logDir = workLevelDir + "\\GTSData\\logfiles";
    #logFile = logDir + "\\navmeshcontrol.log";
    print ("From: " + workGTSdataDir)
    print ("To  : " + workGTSdataDirBak)
    
    # check for no Src Dir
    if not (os.path.isdir(workGTSdataDir)):
        print ("Not able to backup - From folder Does not exist")
        return 
    if not (os.listdir(workGTSdataDir)):  
        print ("Not able to backup - From folder is empty")
        return
    MoveToBackupFolderSubs(workGTSdataDir)
    print ("Backup completed")
    return;

def SetupNavWorkArea(level_name, navmesh_dir):
    #workFolder = "work"
    #modLevelDir = navmesh_dir + "\\" + level_folder;
    #print(    "Set up Nav Work Area");
    print ("------------------------------")
    print ("Setting up Navmesh work area");
    #navmesh_dir = os.path.abspath(os.path.join(os.getcwd(),"."));
    print ("Navmesh Dir : " + navmesh_dir);
    workDir = navmesh_dir + "\\work"
    #os.path.abspath(os.path.join(navmesh_dir,".."));
    print ("workDir : " + workDir);
    #print(    "Set up Nav Work Area" + workDir);
    workLevelDir = workDir + "\\" + level_name ; 
    workGTSdataDir = workLevelDir + "\\GTSData";
    workMeshDir = workGTSdataDir + "\\meshes";
    logDir = workLevelDir + "\\GTSData\\logfiles";
    #logFile = logDir + "/navmeshcontrol.log";
    #modLevelmesh = workMeshDir + levelName + "/GTSData/Meshes";
    #REM make sure work dir exists
    #check if navmesh folders exist - create if they don't
    if not (os.path.isdir(workDir)):
        os.makedirs(workDir);	
        print("Creating :" + workDir);	
    if not (os.path.isdir(workLevelDir)):
        os.makedirs(workLevelDir);	
        print("Creating :" + workLevelDir);		
    if not (os.path.isdir(workGTSdataDir)):
        os.makedirs(workGTSdataDir);
        print("Creating :" + workGTSdataDir);		
    if not (os.path.isdir(workMeshDir)):
        os.makedirs(workMeshDir);
        print("Creating :" + workMeshDir);
    if not (os.path.isdir(logDir)):
        os.makedirs(logDir);
        print("Creating :" + logDir);
    print ("Folder Setup completed")    
    return;

def cleanNavmesh(NavmeshInFilePath, NavmeshOutFilePath):
	#mtllib materials.mtl
	#g ground
	#usemtl ground 
	#g ladder
	#usemtl ladder
	#g water
	#usemtl water
	#g deepwater
	#usemtl deepwater
	
	ground_mtl_fix = 0;
	water_mtl_fix = 0;
	deepwater_mtl_fix = 0;
	ladder_mtl_fix = 0;
	print(   "Cleaning Navmesh");
	print(  "Input file:" + NavmeshInFilePath);
	print(  "Output file:" + NavmeshOutFilePath);
	with open(NavmeshInFilePath, 'r') as input_file, open(NavmeshOutFilePath, 'w') as output_file:
		for line in input_file:
			lineLC = line.lower();
			if "mtllib" in lineLC:
			#(line.strip() == "mtllib"):
				output_file.write("mtllib materials.mtl\n");
			elif (line[0] == "g"): #do nothing
				found_g = 1;
			
			elif "usemtl" in lineLC:
			
				if "deepwater" in lineLC: 
					output_file.write("g deepwater\n");
					output_file.write("usemtl deepwater\n");
					deepwater_mtl_fix = 1;	
				elif "water" in lineLC: 
					output_file.write("g water\n");
					output_file.write("usemtl water\n");
					water_mtl_fix = 1;	

				elif "ladder" in lineLC:  
					output_file.write("g ladder\n");
					output_file.write("usemtl ladder\n");	
					ladder_mtl_fix = 1;
				else:
					# default to ground
					output_file.write("g ground\n");
					output_file.write("usemtl ground\n");	
					ground_mtl_fix = 1;	
			
			else:
				line.replace('\n', '\r\n')
				output_file.write(line);
	if (ground_mtl_fix == 1): print(  "Ground Material Fixed");
	if (water_mtl_fix == 1): print(  "water Material Fixed");
	if (deepwater_mtl_fix == 1): print(  "deepwater Material Fixed");
	if (ladder_mtl_fix == 1): print(  "ladder Material Fixed");
	os.remove(NavmeshInFilePath);		
    #with open(path, 'r') as f:
    #    text = f.read()
    #    print path
    #with open(path, 'wb') as f:
    #    f.write(text.replace('\r', '').replace('\n', '\r\n'))	
    
def FixNavmesh(meshDir, meshMode, levelName, modDir):
    #meshMode = 0;
    materials_replaced = "N";
    print(   "Fix Navmesh ");
    # Create Navmesh backups
    materials_file = "materials.mtl";
    navmesh_dir = os.path.abspath(os.path.join(os.getcwd(),"."));
    createNavmeshBackups(meshDir, meshMode);
    materials_path = meshDir + "/GTSData/output/materials.mtl";
    replaceMaterialsFile(materials_path);
    navmeshFixLogFile = meshDir + "/GTSData/backup/navmeshFix.log";
    modLevelDir = modDir + "\\" + levelName;
    DestOutputFolder = (modDir + "\\" + "Levels" + "\\" + levelName)
    print ( "Navmesh Fix Log File: " + navmeshFixLogFile);

    if (meshMode == 1 or meshMode == 0): 
        infantryFile = meshDir + "/GTSData/output/infantry.obj";
        infantryFixFile = meshDir + "/GTSData/infantryfix.obj";
        infantryModGTSdata = modLevelDir + "/GTSData/infantry.obj";
        if not(os.path.exists(infantryFile)):
            print(   "Infantry file not found:" +infantryFile);
            print("Infantry.obj file not found - press any key to return to main menu");
            choice = input();
            return;
        if (os.path.exists(infantryFixFile)):
            os.remove(infantryFixFile);
            print(   "Delete Infantry_fix.obj");
            print(   infantryFixFile);
        print(   "Clean Infantry.obj file ");
        cleanNavmesh(infantryFile, infantryFixFile)
        print(   "Infantry.obj file fixed ");
        #os.remove(infantryFile);
        #navmesh.exe -dir work\%level_name%\gtsdata -cmd export -mode vehicle -in vehicle_fix.obj 
        commandLine = ("navmesh.exe -dir work/" + levelName + "/GTSData -cmd export -mode infantry -in infantryfix.obj >" + navmeshFixLogFile);
        #command_line = "navmesh.exe -dir work\" + levelName + "\gtsdata -cmd export -mode infantry -in vehiclefix.obj");
        print(   "launching Navmesh.exe")
        print(   "Command Line:" + commandLine);
        result = os.system(commandLine);
        if (os.path.exists(infantryFixFile)):
            os.remove(infantryFixFile);		
        if (result == 0):
            print(    "Infantry.obj fixed " );
            #copyfile (infantryFile, infantryModGTSdata);
        else:
            print(    "Infantry.obj fix failed, aborting");
            choice = input();
            return False;
 
    if (meshMode == 2 or meshMode == 0): 
        vehicleFile = meshDir + "/GTSData/output/vehicle.obj";
        vehicleFixFile = meshDir + "/GTSData/vehiclefix.obj";
        vehicleModGTSdata = modLevelDir + "/GTSData/vehicle.obj";
        if not(os.path.exists(vehicleFile)):
            print(    "vehicle.obj file not found - press any key to return to main menu");
            print(    vehicleFile);
            choice = input();
            return;
        if (os.path.exists(vehicleFixFile)):
            os.remove(vehicleFixFile);
            print(   "Delete vehicle_fix.obj");
            print(   vehicleFixFile);
        print(   "Clean vehicle.obj file ");
        cleanNavmesh(vehicleFile, vehicleFixFile)
        #os.remove(infantryFile);
        #navmesh.exe -dir work\%level_name%\gtsdata -cmd export -mode vehicle -in vehicle_fix.obj	
        commandLine = ("navmesh.exe -dir work/" + levelName + "/GTSData -cmd export -mode vehicle -in vehiclefix.obj >>" + navmeshFixLogFile);
        #command_line = "navmesh.exe -dir work\" + levelName + "\gtsdata -cmd export -mode infantry -in vehiclefix.obj");
        print(   "launching Navmesh.exe")
        print(   "Command Line:" + commandLine);		
        result = os.system(commandLine);
        if (os.path.exists(vehicleFixFile)):
            os.remove(vehicleFixFile);		
        if (result == 0):
            print(   "vehicle.obj fixed");
            #copyfile (infantryFile, infantryModGTSdata);
        else:
            print(    "vehicle.obj fix failed, aborting");
            print ("- Press any key to continue-");
            choice = input();
            return False;		

    clusterFolder = meshDir + "/GTSData/output/cluster"
    if (os.path.exists(clusterFolder)):
        os.rmdir(clusterFolder);
        print(   "Remove Cluster Folder");
    CopyGTSdataOutputFiles ( meshDir, DestOutputFolder);
    print ("\n");
    print(   "Fix Navmesh completed - Output files copied to map");
    #choice ="";
    #while choice != "r":
    #    print("- press [r] to return to main menu -");
    #    choice = input();	
    #    if choice == "r": return;
    return; 
  

def mainMenu(mod_folder, levelName):   
    #global _NavmeshModes
    navmeshMode = 0;  # 0 = both infantry and vehicle
    navmeshModes = {"Infantry and Vehicle", "Infantry", "Vehicle"};
    navmeshModeName = list (navmeshModes)[navmeshMode]
    mainMenuMode = 1
    choice = -1;
    MaxChoice = 4;
    workFolder = "\\work"    
    cwd = os.getcwd()
    print ("CWD: " + cwd);

    #mod_folder = os.path.abspath("..\\mods\\" + _ModName);
    #os.path.abspath  os.path.join
    #..\Navmesh\work\[levelname]
    navmesh_level_folder = os.getcwd() +"\\work\\" + levelName; 
    navmesh_dir = os.getcwd(); 
    #print ("navmesh_dir: " + navmesh_dir);
    BF2_dir = os.path.abspath(os.path.join(os.getcwd(),".."));
    #print ("BF2 DIR:" + BF2_dir);
    level_folder = ( mod_folder + "\\levels\\" +levelName )
    print ("CWD: " + os.getcwd())


    while (True):
        cls();
        print("*****************************");
        print("  Dnamro Navmesh Tool v3.4 Test ");
        print("        Main Menu ");
        print("*****************************");
        print("Current Level: " + levelName);
        #print("Navmesh Mode: " + list (navmeshModes)[navmeshMode]);
        print("Navmesh Folder: " + navmesh_dir); 
        print("Navmesh Level Folder: " + navmesh_level_folder); 
        print("Level Folder: " + level_folder); 
        print("(1) Generate Navmesh");
        print("(2) Fix Navmesh - Automatic");
        print("(3) Fix Navmesh - Manual");
        print("(4) Fix Navmesh - Help");
        #print("(3) Change navmesh mode - Infantry, Vehicle or Both");	
        #print("(3) Create New Navmesh");
        #print("(4) Fix Navmesh");
        #print("(5) Launch Editor Menu");
        #print("(8) Clean Editor GPO");
        print("");
        #print("(0) Go To the Advanced Menu");
        #print("(9) Quit");

        temp_input = input();
        if temp_input.isdigit(): 
            choice = int(temp_input);
        while ( choice < 0 or choice > MaxChoice):
            print("Value out of Range!  Try again:");
            temp_input = input();
            if temp_input.isdigit(): 
                choice = int(temp_input);
        #choose map level		
        if (choice == 1):
            preCreateNavmeshHelp() 
            backupNavWorkArea(levelName, navmesh_dir)
            SetupNavWorkArea(levelName, navmesh_dir)
            if (not CopyGTSdataWorkFiles ( level_folder, navmesh_level_folder)):
                return False;
            if (not generateNavmesh(levelName, navmesh_dir)):
                print ("Error: Failed to generate navmesh...")
                return False;
            postCreateNavmeshHelp()

        elif (choice == 3):
        #Fix namvesh in Manual Mode
            preFixNavMeshManualHelp()
            FixNavmesh(navmesh_level_folder, navmeshMode, levelName, mod_folder);
            postFixNavMeshHelp()
            #navmeshMode = ChangeNavmeshMode();
        #Create Navmesh	
        #fix navmesh
        elif (choice == 2):	
		#Fix namvesh in Automatic Mode
            preFixNavMeshAutoHelp()
            copyIslands(navmesh_level_folder, navmeshMode)
            FixNavmesh(navmesh_level_folder, navmeshMode, levelName, mod_folder);
            postFixNavMeshHelp()
        elif (choice == 4):    
            FixNavMenuHelp()
			#os.chdir(owd);
		#elif (choice == 0):	
		#	advancedMenu(mod_name, levelName, meshMode, meshLeveldir, modLevelDir,mod_folder);
			#copyIslands(meshLeveldir, meshMode);
		#elif (choice == 5):
		#	launchEditorMenu(mod_name, meshLeveldir, levelName)
			#LaunchEditor( mod_name, levelName," +forceLoadPlugin SinglePlayerEditor" );
		#elif (choice == 7):	
		#	break;
			#LaunchEditor(editorGenPathmaps, mod_name, levelName );

		#elif (choice == MaxChoice):
		#	break;
        else: 
            print("Whoops!  something went wrong:");
            return;
    return;	
  

def getLevelChoice(levelfolder):
    levelCnt = 0
    for levelname in os.listdir(levelfolder): 
        if os.path.isdir(os.path.join(levelfolder, levelname)):
            levelCnt = (levelCnt + 1);
            print ("<%d> %s" % (levelCnt, levelname));		
    MaxLevelCnt = levelCnt;	
    #print ("<<0>> All listed maps")
    print("Select a Level #:")
    choice = input();
    levelNum = int(choice)
    while ( levelNum < 1 or levelNum > MaxLevelCnt):
        print("Out of range!  Try again:");
        choice = input();
        levelNum = int(choice);			
    #process the listdir to get the level name
    levelCnt = 0;
    for levelname in os.listdir(levelfolder): 
        if os.path.isdir(os.path.join(levelfolder, levelname)):
            levelCnt = (levelCnt + 1);
            if (levelCnt == levelNum):
                if (levelCnt == levelNum):
                    return levelname;
    return""
    
################################################################################
def main():
    #global _skipEditor
    #global _cleanOldData
    #global _restart
    global _ModName

    
    levelFolder = os.path.abspath("..\\mods\\" + _ModName + "\\levels");
    mod_folder = os.path.abspath("..\\mods\\" + _ModName);
    levelName = getLevelChoice(levelFolder);
    levelNameFolder = levelFolder + "\\" + levelName

    print ("########################################################################")
    print ("#")
    #print ("# Navmesh Creation Toolkit" )
    print ("# Current Settings:")
    print ("# mod  = " + _ModName)
    print ("# level  = " + levelName)
    print ("# Folder  = " + levelNameFolder)
    print ("#")
    print ("########################################################################")

    # Make sure that the level exists
    #if ( not os.path.isdir(levelNameFolder)):
    #    print ("Error: Failed to find level-directory for " + level)
    #    print( "Press a Key to End")  
    #    choice = input();        
    #    return
    #SetupNavWorkArea(levelName)
    mainMenu(mod_folder, levelName )



    #if (_cleanOldData):
    #    cleanupOldData(level, levelFolder)

    #if (not _restart):
    #    if (not exportGts(level, levelFolder)):
    #        print ("Error: Failed to export gts-data...")
    #        return


        
    #if (not createQtrFiles(level, levelFolder, workingFolder)):
    #    print ("Error: Failed to create qtr-files...")

success = main();

if success:
    print("Press a Key to End")  
    choice = input();
    sys.exit(0);
else:
    print("Press a Key to End")  
    choice = input();
    sys.exit(1);


