import DoDataScienceHelper as Helper
from sklearn.model_selection import train_test_split
import sys, os, argparse
from pathlib import Path
import numpy as np
import pandas

VASE_FNAME = Path('C:/Users/carpe/Dropbox/School/Graduate - LTU/Year 3/MCS 5623/Data/Vases_First-200_v1.csv')
BENCHY_FNAME = Path('C:/Users/carpe/Dropbox/School/Graduate - LTU/Year 3/MCS 5623/Data/Benchys_v1.csv')

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help="Include a configuration file to allow automated operation")

args = parser.parse_args()

if not args.config is None:
    print("The --config option is not implemented at this time")

vaseData = pandas.read_csv(VASE_FNAME)
benchyData = pandas.read_csv(BENCHY_FNAME)

print("%d vase and %d benchy records loaded" % (vaseData.shape[0], benchyData.shape[0]))

# if not vaseData.columns == benchyData.columns:
#     print("Error, columns in provided data sets do not match!  Aborting")
#     sys.exit(1)

## Update column names
vaseData.columns = ['thingID',
    'fileSize',
    'triangleCount',
    'volume',
    'volumeRatio',
    'cog_X', 'cog_Y', 'cog_Z',
    'bboxCenter_X', 'bboxCenter_Y', 'bboxCenter_Z',
    'bboxSize_X', 'bboxSize_Y', 'bboxSize_Z',
    'symmetry_X', 'symmetry_Y', 'symmetry_Z',
    'AR1', 'largestDimension',
    'AR2', 'smallestDimension']

benchyData.columns = vaseData.columns

## Convert X/Y/Z => 0,1,2 Keeping things numeric
vaseData = Helper.axesToNumeric(vaseData, Helper.axisMap)
benchyData = Helper.axesToNumeric(benchyData, Helper.axisMap)

## Apply data labels
Helper.assignLabels([vaseData, benchyData], ['vase', 'benchy'])

## Merge the data sets
df = vaseData.append(benchyData, ignore_index=True)

## Split data into training and testing
dataColMax = df.shape[1]-2
allData, allLabels = df.iloc[:,0:dataColMax], df.iloc[:,df.shape[1]-1]

dataTrain, dataTest, labelTrain, labelTest = train_test_split(allData, allLabels, test_size=0.30, random_state=0)

sys.exit(0)