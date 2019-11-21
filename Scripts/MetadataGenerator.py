import MetadataGeneratorHelper as Helper
from pathlib import Path
import sys, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--object", help="Folder where object files are stored")
parser.add_argument("-m", "--metadata", help="File to store metadata")
parser.add_argument("-l", "--label", help="Label assigned to the elements of this data set")

args = parser.parse_args()

if args.object is None or not os.path.isdir(Path(args.object)):
    print("Directory of object files must be provided and exist in this mode")
    sys.exit(1)
else:
    objectFName = Path(args.object)

if args.metadata is None:
    print("Desired metadata CSV file location must be specified")
    sys.exit(1)
else:
    metaDataFName = Path(args.metadata)

if args.label is None:
    print("Dataet label is an important argument used to properly discern groups training data belongs to!")
    label = 'UNLABELED'
else:
    label = args.label

metaList = Helper.getMetaData(objectFName)

#TODO: Apply the labels passed in -l argument

Helper.writeMetaData(metaDataFName, metaList)

sys.exit(0)
