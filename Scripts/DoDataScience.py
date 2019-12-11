import DoDataScienceHelper as Helper
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pydotplus
import sys, os, argparse
from pathlib import Path
import numpy as np
import pandas

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--datafile", help="Location of file containing data to load")
parser.add_argument("-c", "--config", help="Include a configuration file to allow automated operation")
algorithm = parser.add_argument_group('Algorithm')
algorithm.add_argument("-t", "--tree", help="Decision Tree algorithm", action="store_true")
algorithm.add_argument("-k", "--knn", help="K-Nearest Neighbor algorithm", action="store_true")
algorithm.add_argument("-b", "--bayes", help="Naive Bayes algorithm", action="store_true")

args = parser.parse_args()

if not args.config is None:
    print("The --config option is not implemented at this time")

if not args.datafile is None and os.path.isfile(args.datafile):
    inFile = args.datafile
else:
    print("Input data file must be specified and accessible to use this script.  Exiting...")
    sys.exit(1)

if args.tree == False and args.knn == False and args.bayes == False:
    print("An algorithm must be specified!  Exiting...")
    sys.exit(1)

df = pandas.read_csv(inFile)

print("%d records loaded" % (df.shape[0]))
print(df.columns)

## One-hot encoding for X/Y/Z
print(df.shape)
df = Helper.axesToNumeric(df, Helper.axisMap)
print(df.shape)

# Remove unessecary/redundant features
df = df.drop(columns=['fileSize'])

# Move the column of labels to the end so it's easier to interact with
colsList = list(df.columns.values)
colsList.pop(colsList.index('label'))
df = df[colsList+['label']]

df, labelList = Helper.numberifyLabels(df, df.shape[1]-1)
print(labelList)

## Split data into training and testing
#TODO: Turn this into a function
dataColMin = 1  # Don't use ThingID as part of the algorithm
dataColMax = df.shape[1]-1
allData, allLabels = df.iloc[:,dataColMin:dataColMax], df.iloc[:,df.shape[1]-1]

dataTrain, dataTest, labelTrain, labelTest = train_test_split(allData, allLabels, test_size=0.30, random_state=0)

print("%d training and %d testing entries" % (len(labelTrain), len(labelTest)))

## Standardize the data
scaler = StandardScaler()
dataTrainStandardized = scaler.fit_transform(dataTrain)
dataTestStandardized = scaler.transform(dataTest)

## Decision Tree
if args.tree == True:
    from sklearn.tree import DecisionTreeClassifier, export_graphviz
    print("Decision Tree")
    clf = DecisionTreeClassifier(criterion="entropy", max_depth=5, random_state=0)

    decisionTree = clf.fit(dataTrain, labelTrain)

    print("Accuracy on training set: %.2f %% | Accuracy on test set: %.2f %%" % (
        100*clf.score(dataTrain, labelTrain), 100*clf.score(dataTest, labelTest)))

    # Create DOT data
    dot_data = export_graphviz(decisionTree, out_file=None,
                feature_names=df.columns[dataColMin:dataColMax], class_names=labelList)

    # Draw graph
    graph = pydotplus.graph_from_dot_data(dot_data)  

    # Create PNG
    #graph.write_png('D:\Dropbox\School\Graduate - LTU\Year 3\MCS 5623\Test.png')
    graph.write_png('C:/Users/carpe/Dropbox/School/Graduate - LTU/Year 3/MCS 5623/Test.png')

# K-Nearest Neighbors
elif args.knn == True:
    from sklearn.neighbors import KNeighborsClassifier
    print("K-Nearest Neighbor")
    knn = KNeighborsClassifier(n_neighbors=5, p=2, metric='minkowski')
    knn.fit(dataTrainStandardized, labelTrain)
    
    print("Accuracy on training set: %.2f %% | Accuracy on test set: %.2f %%" % (
        100*knn.score(dataTrainStandardized, labelTrain), 
        100*knn.score(dataTestStandardized, labelTest)))

# (Gaussian) Naive Bayes
elif args.bayes == True:
    from sklearn.naive_bayes import GaussianNB
    print("(Gaussian) Naive Bayes")
    nbayes = GaussianNB()
    nbayes.fit(dataTrainStandardized, labelTrain)

    print("Accuracy on training set: %.2f %% | Accuracy on test set: %.2f %%" % (
        100*nbayes.score(dataTrainStandardized, labelTrain), 
        100*nbayes.score(dataTestStandardized, labelTest)))

sys.exit(0)