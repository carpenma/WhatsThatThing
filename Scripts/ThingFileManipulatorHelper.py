import zipfile, os, shutil, glob
from pathlib import Path

#TODO: Switch to using glob to locate files by extension
#TODO: Make all functions robust to non-directory elements in object directory

def unzipper(fName, keepZips):
    singleItemDirs = []
    for item in os.listdir(fName):
        # If it isn't a zip we can't unzip it
        if item.endswith(".zip"):       
            zipPath = os.path.join(fName, item)
            dirPath = zipPath.replace('.zip', '')
            # Another folder by that name, don't need to unzip
            if os.path.isdir(dirPath):
                print("%s already inflated in this directory, skipping..." % item)
            # It's a zip and it hasn't been inflated yet.  Show time!
            else:       
                with zipfile.ZipFile(os.path.join(fName, item), 'r') as zipped:
                    print("Directory %s contains %d files" % (item,len(zipped.namelist())))
                    zipped.extractall(os.path.join(fName, item.replace('.zip','')))

                    if len(zipped.namelist() <= 1):
                        singleItemDirs.append(item)
            
            # Even if we didn't extract it during this run, the fact it's already in the 
            # directory means we're safe to remove the original .zip
            if not keepZips:
                os.remove(os.path.join(fName, item))

    if len(singleItemDirs) > 0:
        print("The following directories contain one or fewer items.  This may indicate an unexpoected folder structure.  It is advised these directories be reviewed or they may be removed in the next step.")
        print(singleItemDirs)
    return

def removeNonObjects(fName, keepReadMe, keepLicense, keepImages):
    for directory in os.listdir(fName):
        dirPath = Path(os.path.join(fName, directory))

        for item in os.listdir(dirPath):
            itemPath = Path(os.path.join(dirPath, item))
            if item == "README.txt" and keepReadMe or item == "LICENSE.txt" and keepLicense or item == "images" and keepImages or item.endswith(".stl"):
                pass
            elif item == "files" and os.path.isdir(itemPath):   #TODO: Confirm it is a directory as well?
                copied = 0
                objectFiles = os.listdir(itemPath)
                for obj in objectFiles:
                    try:
                        shutil.copy(os.path.join(itemPath, obj), dirPath)
                    except Exception as e:
                        print("Couldn't copy %s in %s" % (obj, directory))
                        print(e)
                    else:
                        copied = copied + 1
                if len(objectFiles) == copied:
                    shutil.rmtree(itemPath)
            else:
                try:
                    os.remove(itemPath)
                except:
                    if os.path.isdir(itemPath):
                        print("Failed to delete %s in %s, copying contents, re-running the prune operation is advised"
                    % (item, directory))
                        nestedFiles = os.listdir(itemPath)
                        print(nestedFiles)
                        for i in nestedFiles:
                            iPath = os.path.join(itemPath, i)
                            if os.path.isdir(iPath):
                                shutil.copytree(iPath, os.path.join(dirPath, i))
                            else:
                                shutil.copy(iPath, dirPath)
                        shutil.rmtree(itemPath)
    return

def pruneSTLs(fName):
    # Relocate multi-STL directories
    for directory in os.listdir(fName):
        dirPath = Path(os.path.join(fName, directory))
        if len(glob.glob(os.path.join(dirPath,"*.stl"))) > 1:
            newDir = buildPathAbove(fName, "-MultiSTL")
            print("Moving %s to %s" % (directory, os.path.join(newDir, directory)))
            shutil.copytree(dirPath, os.path.join(newDir, directory))
            if os.path.isdir(newDir):
                # Only delete the directory if the copy was succesful
                shutil.rmtree(dirPath)
    return

def renameSTLs(fName):
    # Find single remaining STL in each directory, name it to match directory name
    for directory in os.listdir(fName):
        dirPath = Path(os.path.join(fName, directory))
        if os.path.isdir(dirPath):  
            # If we've made it this far and there aren't any STLs the directory needs to go away
            stlList = glob.glob(os.path.join(dirPath, "*.stl"))
            if len(stlList) == 0:
                shutil.rmtree(dirPath)
            elif len(stlList) == 1:
                if not os.path.isfile(os.path.join(fName, directory+".stl")):
                    print("Copying %s to %s" % (os.path.join(dirPath, stlList[0]), os.path.join(fName, directory+".stl")))
                    shutil.copy(os.path.join(dirPath, stlList[0]), os.path.join(fName, directory+".stl"))
                else:
                    print("Skipping %s - Already in object directory" % directory)
    return

def findEmptySubfolders(fName):
    
    return

def buildPathAbove(rootDir, newDirSuffix="-New"):
    rootPath = Path(rootDir)
    newDirPath = os.path.join(rootPath.parent, "%s%s" % (rootPath.parent.name, newDirSuffix))
    if not os.path.isdir(newDirPath):
        os.mkdir(newDirPath)
    return newDirPath

def metricSelector(fName):
    optionDict = {0: "Quit", 1: "STL Counts", 2: "File Structure Metrics"}
    while True:
        print("=== Select an option from the list ===")
        for element in optionDict.keys():
            print(" %d => %s" % (element, optionDict[element]))

        selection = input("Would you kindly make a selection? ")

        if int(selection) == 1:
            metricsSTL(fName)
        elif int(selection) == 2:
            metricsFile(fName)
        else:
            return

def metricsSTL(fName):
    totalSTLs = 0
    totalDirs = 0
    multiSTLDirs = 0
    for directory in os.listdir(fName):
        dirPath = Path(os.path.join(fName, directory))
        if not os.path.isdir(dirPath):
            continue
        totalDirs = totalDirs + 1
        localSTLCount = 0
        for item in os.listdir(dirPath):
            if item.endswith(".stl"):
                totalSTLs = totalSTLs + 1
                localSTLCount = localSTLCount + 1
        if localSTLCount > 1:
            multiSTLDirs = multiSTLDirs + 1
            print("Multi-STL Directory: %s" % directory)
        if localSTLCount == 0:
            print("No STLs in %s" % directory)
    print("%d STLs found in %d directores averaging %0.2f STLs/directory | %d directories with multiple STLs" % 
    (totalSTLs, totalDirs, totalSTLs/totalDirs, multiSTLDirs))
    return

def metricsFile(fName):
    dirCount = 0
    readmeCount = 0
    licenseCount = 0
    imageCount = 0
    emptyCount = 0
    for directory in os.listdir(fName):
        dirPath = Path(os.path.join(fName, directory))
        if os.path.isdir(dirPath):
            dirCount = dirCount + 1
            if len(os.listdir(dirPath)) == 0:
                emptyCount = emptyCount + 1
            for item in os.listdir(dirPath):
                itemPath = os.path.join(dirPath, item)
                item = item.upper()
                if "README" in item:
                    readmeCount = readmeCount + 1
                elif "LICENSE" in item:
                    licenseCount = licenseCount + 1
                elif os.path.isdir(itemPath) and "IMAGE" in item:
                    imageCount = imageCount + 1
    print("%d directories scanned"%dirCount)
    print("%d with READMEs | %d LICENSE files | %d Image directories| %d empty diretories" % 
    (readmeCount, licenseCount, imageCount, emptyCount))

    return