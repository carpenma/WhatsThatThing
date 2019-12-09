import numpy, os, glob
from stl import mesh
import numpy as np

HEADERS = ["ThingID", "File Size (bytes)", "Triangle Count", "Volume (?)", "Volume Ratio", "CoG X", "CoG Y", "CoG Z", "Bounding Box Center X", "Bounding Box Center Y", "Bounding Box Center Z", "Bounding Box Size X", "Bounding Box Size Y", "Bounding Box Size Z", "Axis Symmetry X", "Axis Symmetry Y", "Axis Symmetry Z", "Aspect Ratio Large:Mid", "Largest Dimension", "Aspect Ratio Mid:Small", "Smallest Dimension", "Label"]

class objectFile:
    def __init__(self, thingID, fileSize, triangleCount, volume, volumeRatio, centerOfGravity, boundingBoxCenter, boundingBoxSize, symmetry, aspectRatio1, aspectRatio2, label):
        self.thingID = thingID
        self.fileSize = fileSize
        self.triangleCount = triangleCount
        self.volume = volume
        self.volumeRatio = volumeRatio
        self.centerOfGravity = centerOfGravity
        self.boundingBoxCenter = boundingBoxCenter
        self.boundingBoxSize = boundingBoxSize
        self.symmetry = symmetry
        self.aspectRatio1 = aspectRatio1
        self.aspectRatio2 = aspectRatio2
        self.label = label
    
    def getAttributes(self):
        return [self.thingID, 
        '%d' % self.fileSize,
        '%d' % self.triangleCount, 
        '%.2f' % self.volume, 
        '%.2f' % self.volumeRatio,
        '%.2f' % self.centerOfGravity[0],
        '%.2f' % self.centerOfGravity[1],
        '%.2f' % self.centerOfGravity[2],
        '%.2f' % self.boundingBoxCenter[0],
        '%.2f' % self.boundingBoxCenter[1],
        '%.2f' % self.boundingBoxCenter[2],
        '%.2f' % self.boundingBoxSize[0],
        '%.2f' % self.boundingBoxSize[1], 
        '%.2f' % self.boundingBoxSize[2], 
        '%.2f' % self.symmetry[0],
        '%.2f' % self.symmetry[1],
        '%.2f' % self.symmetry[2],
        '%.2f' % self.aspectRatio1[0],
        '%s' % self.aspectRatio1[1],
        '%.2f' % self.aspectRatio2[0],
        '%s' % self.aspectRatio2[1],
        '%s' % self.label]

def getMetaData(fName, label):
    metaList = []
    stlList = glob.glob(os.path.join(fName, "*.stl"))
    for item in stlList:
        thingID = os.path.splitext(os.path.basename(item))[0]
        print(thingID)
        fileSize = os.path.getsize(item)
        try:
            thisMesh = mesh.Mesh.from_file(item)
        except:
            print("%s is too large to be tested, skipping it" % item)
            continue
        triangleCount = len(thisMesh.normals)
        volume, cog, inertia = thisMesh.get_mass_properties()

        ## Bounding Box Calculations
        boundingBox = abs(thisMesh.max_ - thisMesh.min_)
        boundingBoxVolume = boundingBox[0] * boundingBox[1] * boundingBox[2]
        midpoint = thisMesh.min_ + (boundingBox/2)

        ## Ratio of bounding box to actual material volume
        volumeRatio = volume / boundingBoxVolume

        ## Approximate symmetry using midpoint v. COG calculation
        ## 1 - abs(distance CoG to midpoint) / object size
        ## 1 = Perfect symmetry -> 0 = No symmetry
        symmetry = [1, 1, 1] - abs(cog - midpoint)/boundingBox

        aspectRatio1, aspectRatio2 = getAspectRatios(boundingBox)

        thisElement = objectFile(thingID, fileSize, triangleCount, volume, volumeRatio, cog, midpoint, boundingBox, symmetry, aspectRatio1, aspectRatio2, label)
        metaList.append(thisElement)

    return metaList

## Since the "front" of objects may vary depending on how they were uploaded, this function returns the aspect ratio of largest:middle dimension (AR1) and middle:smallest dimension (AR2)
def getAspectRatios(boundingBox):
    def getKey(element):
        return element[1]

    augmentedBoundingBox = [['X', boundingBox[0]], ['Y', boundingBox[1]], ['Z', boundingBox[2]]]
    augmentedBoundingBox = sorted(augmentedBoundingBox, key=getKey)

    aspectRatio1 = augmentedBoundingBox[0][1] / augmentedBoundingBox[1][1]
    aspectRatio2 = augmentedBoundingBox[1][1] / augmentedBoundingBox[2][1]
    returnArray = [
        [aspectRatio1, augmentedBoundingBox[0][0], augmentedBoundingBox[1][0]],
        [aspectRatio2, augmentedBoundingBox[1][0], augmentedBoundingBox[2][0]] ]

    return returnArray

def writeMetaData(fName, metaData):
    import csv
    with open(fName, mode='w', newline='') as outFptr:
        writer = csv.writer(outFptr, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(HEADERS)
        for objectFile in metaData:
            writer.writerow(objectFile.getAttributes())

    return