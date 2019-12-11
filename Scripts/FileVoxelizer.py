import sys, os, argparse, glob
import FileVoxelizerHelper as Voxelizer
from pathlib import Path
import numpy as np
import trimesh

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input folder of STLs to test")
parser.add_argument("-o", "--output", help="Output file to store voxel arrays")
parser.add_argument("-l", "--label", help="Label to be applied to these entries")
 
args = parser.parse_args()

if args.input is None or not os.path.isdir(Path(args.input)):
    print("Directory of STL not provided.  Exitting...")
    sys.exit(1)
else:
    objectFName = Path(args.input)

if args.output is None:
    print("Output file must be specified.  Exitting...")
    sys.exit(1)
else:
    outputFName = Path(args.output)

if args.label is None:
    print("No label specified, the items will be labeled 'UNLABELED")
    label = "UNLABELED"
else:
    label = args.label

outFptr = open(outputFName, 'w')

for item in glob.glob(os.path.join(objectFName, "*.stl")):
    print(item)
    try:
        thisMesh = trimesh.load_mesh(item)

        print(thisMesh.extents)
        scaleFactor = 15/max(thisMesh.extents)
        thisMesh = thisMesh.apply_transform([[scaleFactor, 0, 0, 0],
        [0, scaleFactor, 0, 0],[0, 0, scaleFactor, 0],[0, 0, 0, 1]])
        # print("Scale Factor: %.2f" % (scaleFactor))
        # print(thisMesh.extents)

        thisVoxelizedMesh = thisMesh.voxelized(pitch=1)
        thisVoxelizedMesh = thisVoxelizedMesh.fill()
        # print("%d filled Voxels = %.2f volume" % (thisVoxelizedMesh.filled_count, thisVoxelizedMesh.volume))
        # thisMesh.show()
        # thisVoxelizedMesh.show()
        print(thisVoxelizedMesh.matrix)

    except Exception as e:
        print("Encountered error: '%s' Skipping..." % e)
        continue

outFptr.close()

sys.exit(0)