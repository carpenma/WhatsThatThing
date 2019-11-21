import sys, argparse, os
from pathlib import Path
import ThingFileManipulatorHelper as Helper

parser = argparse.ArgumentParser()
modeGroup = parser.add_mutually_exclusive_group()
modeGroup.add_argument("-u", "--unzip", help="Unzip the archive files in the indicated directory", action="store_true")
modeGroup.add_argument("-r", "--rename", help="Rename the STL files in each directory to match the Thing #", action="store_true")
modeGroup.add_argument("-p", "--prune", help="Remove all but one STL file in each directory", action="store_true")
modeGroup.add_argument("-a", "--auto", help="Run each step in order to automatically handle file processing", action="store_true")
modeGroup.add_argument("-m", "--metrics", help="Metrics review mode", action="store_true")
parser.add_argument("-o", "--object", help="Folder where object files are stored")

args = parser.parse_args()

if args.object is None or not os.path.isdir(Path(args.object)):
    print("Directory of object files must be provided and exist in this mode")
    sys.exit(1)
else:
    objectFName = Path(args.object)

if args.unzip:
    print("Unzip Mode")
    Helper.unzipper(objectFName, False)

elif args.rename:
    print("Rename Mode")
    Helper.renameSTLs(objectFName)
    
elif args.prune:
    print("Prune Mode")
    Helper.removeNonObjects(objectFName, keepImages=True, keepLicense=True, keepReadMe=True)
    Helper.pruneSTLs(objectFName)
    # Add options for indicating what files to remove?

elif args.auto:
    print("Automatic Mode")

    if input("Remove Zip files after unzipping? (T/F): ").lower() == "t":
        keepZips = False
    else:
        keepZips = True

    if input("Remove image directories if they exist? (T/F): ").lower() == "t":
        keepImages = False
    else:
        keepImages = True

    if input("Remove License files if they exist? (T/F): ").lower() == "t":
        keepLicense = False
    else:
        keepLicense = True

    if input("Remove README files if they exist? (T/F): ").lower() == "t":
        keepReadMe = False
    else:
        keepReadMe = True
    
    Helper.unzipper(objectFName, keepZips)
    Helper.removeNonObjects(objectFName, keepImages=keepImages, keepLicense=keepLicense, keepReadMe=keepReadMe)
    Helper.pruneSTLs(objectFName)
    Helper.renameSTLs(objectFName)

elif args.metrics:
    print("Metrics Mode")
    Helper.metricSelector(objectFName)

else:
    print("Unrecognized mode selected, aborting")
    sys.exit(1)

sys.exit(0)