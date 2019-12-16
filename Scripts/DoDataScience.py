import DoDataScienceHelper as Helper
from sklearn.model_selection import train_test_split
import pydotplus
import sys, os, argparse
from pathlib import Path
import numpy as np
import pandas

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--datafile", help="Location of file containing data to load")
parser.add_argument("-c", "--config", help="Include a configuration file to allow automated operation")

# ML algorithm to apply
algorithm = parser.add_argument_group('Algorithm')
algorithm.add_argument("-t", "--tree", help="Decision Tree algorithm", action="store_true")
algorithm.add_argument("-k", "--knn", help="K-Nearest Neighbor algorithm", action="store_true")
algorithm.add_argument("-b", "--bayes", help="Naive Bayes algorithm", action="store_true")

# Features to strip out of data set
subset = parser.add_argument_group('Feature Subset')
subset.add_argument("-a", "--all", help="Use all features for training and testing", action="store_true")
subset.add_argument("-i", "--independent", help="Use independent features only", action="store_true")

# Data scaling strategy
parser.add_argument("-s", "--scaling", help="Scaling method (0=No scaling, 1=Standardize, 2=Normalize)")

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

if not args.scaling in ['0', '1', '2']:
    print("No data scaling method selected, assuming no scaling")
    dataScaling = 0
else:
    dataScaling = int(args.scaling)

if args.all == False and args.independent == False:
    print("Feature subset not specified, assuming all")
    featureSubset = 1
else:
    featureSubset = (args.all == True)

df = pandas.read_csv(inFile)

print("%d records loaded" % (df.shape[0]))
#print(df.columns)

## One-hot encoding for X/Y/Z
#print(df.shape)
df = Helper.axesToNumeric(df, Helper.axisMap)
#print(df.shape)

# Remove unessecary/redundant features
if featureSubset == 1:
    print("Using all features (except thingID)")
    df = df.drop(columns=['fileSize'])
else:
    print("Using indepenedent feature subset")
    df = df.drop(columns=['fileSize', 'cogX', 'cogY', 'cogZ', 'bboxCenterX', 'bboxCenterY', 'bboxCenterZ'])

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

## Scale the data
if dataScaling == 1:
    # Standardize
    print("Scaling Method: Standardizing")
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    dataTrain = scaler.fit_transform(dataTrain)
    dataTest = scaler.transform(dataTest)

elif dataScaling == 2:
    # Normalize
    print("Scaling Method: Normalizing")
    from sklearn.preprocessing import normalize
    dataTrain = normalize(dataTrain, norm='l2')
    dataTest = normalize(dataTest, norm='l2')
else:
    # Use Raw Data
    print("Scaling Method: No Scaling")

## Decision Tree
PLOT_TREE = False   # Plot each tree in a unique image

if args.tree == True:
    from sklearn.tree import DecisionTreeClassifier, export_graphviz
    print("Decision Tree")
    print("Depth , Train (%) , Test (%)")

    for depth in range(2,17):
        clf = DecisionTreeClassifier(criterion="entropy", max_depth=depth, random_state=0)
        decisionTree = clf.fit(dataTrain, labelTrain)
        print("%d,%.2f,%.2f" % (depth, 100*clf.score(dataTrain, labelTrain), 
        100*clf.score(dataTest, labelTest)))
        if PLOT_TREE:
            # Create DOT data
            dot_data = export_graphviz(decisionTree, out_file=None,
                feature_names=df.columns[dataColMin:dataColMax], class_names=labelList)

            # Draw graph
            graph = pydotplus.graph_from_dot_data(dot_data)  

            # Create PNG
            graph.write_png('D:\Dropbox\School\Graduate - LTU\Year 3\MCS 5623\Tree_Depth=%d.png'%depth)
            #graph.write_png('C:/Users/carpe/Dropbox/School/Graduate - LTU/Year 3/MCS 5623/Tree_Depth=%d.png'%depth)

# K-Nearest Neighbors
elif args.knn == True:
    from sklearn.neighbors import KNeighborsClassifier
    print("K-Nearest Neighbor")
    print("K, Train (%),Test (%)")
    for k in range(5, 301, 5):
        knn = KNeighborsClassifier(n_neighbors=k, p=2, metric='minkowski')
        knn.fit(dataTrain, labelTrain)

        print("%d,%.2f,%.2f" % (k, 100*knn.score(dataTrain, labelTrain), 
        100*knn.score(dataTest, labelTest)))

# (Gaussian) Naive Bayes
elif args.bayes == True:
    from sklearn.naive_bayes import GaussianNB

    print("(Gaussian) Naive Bayes")
    nbayesG = GaussianNB()
    nbayesG.fit(dataTrain, labelTrain)

    print("Gaussian Accuracy on training set: %.2f %% | Accuracy on test set: %.2f %%" % (
        100*nbayesG.score(dataTrain, labelTrain), 
        100*nbayesG.score(dataTest, labelTest)))

sys.exit(0)