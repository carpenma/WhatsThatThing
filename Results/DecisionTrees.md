# Decision Trees

## Test 1
### Data
Benchys_v1, Vases_First-200_v1
### Settings
* Max Depth = 3
* Criteria = Entropy
### Results
* Training: 98/105 correctly classified (93.3%)
* Testing: 88.9% Accurate
### Notes
Initial test demonstrates reasonable accuracy.  Appears to make considerable use of Z-axis parameters (CoG, bounding box, symmetry) as well as aspect ratios in decisionmaking.

## Test 2
### Data
Benchys_v1, Vases_First-200_v1
### Settings
* Max Depth = 2
* Criteria = Entropy
### Results
* Training: 86.7% correct
* Testing: 84.4% correct
### Notes
As expected, decreasing the number of tree layers degrades accuracy on both data sets.

## Test 3
### Data
Benchys_v1, Vases_First-200_v1
### Settings
* Max Depth = 4
* Criteria = Entropy
### Results
* Training: 97.1% correct
* Testing: 86.7% correct
### Notes
Allowing the alrogithm to introduce a 4th layer of decisions begins to demonstrate overfitting.  This is clearly visibile because the training set accuracy increases but the percent of data points in the testing set classified correctly actually _shrinks_.