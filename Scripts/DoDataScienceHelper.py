import pandas

axisMap = {'X': 0, 'Y': 1, 'Z': 2}
labelMap = {}

## TODO: There has to be a better way to do this
def axesToNumeric(df, mapArray):
    if not 'largestDimension' in df or not 'smallestDimension' in df:
        print("Warning!  Both largest and smallest dimension columns must be in the data frame.  Unexpected behavior may result")
        return df

    largest = {'X': [], 'Y': [], 'Z': []}
    smallest = {'X': [], 'Y': [], 'Z': []}

    for i in range(df.shape[0]):
        # Expand largest dimension column
        if df.loc[i,'largestDimension'] == 'X':
            largest['X'].append(1)
            largest['Y'].append(0)
            largest['Z'].append(0)
        elif df.loc[i,'largestDimension'] == 'Y':
            largest['X'].append(0)
            largest['Y'].append(1)
            largest['Z'].append(0)
        elif df.loc[i,'largestDimension'] == 'Z':
            largest['X'].append(0)
            largest['Y'].append(0)
            largest['Z'].append(1)
        else:
            print('Unrecognized largest dimension: %s' % df.loc[i,'largestDimension'])
            largest['X'].append(0)
            largest['Y'].append(0)
            largest['Z'].append(0)

        # Expand smallest dimension column
        if df.loc[i,'smallestDimension'] == 'X':
            smallest['X'].append(1)
            smallest['Y'].append(0)
            smallest['Z'].append(0)
        elif df.loc[i,'smallestDimension'] == 'Y':
            smallest['X'].append(0)
            smallest['Y'].append(1)
            smallest['Z'].append(0)
        elif df.loc[i,'smallestDimension'] == 'Z':
            smallest['X'].append(0)
            smallest['Y'].append(0)
            smallest['Z'].append(1)
        else:
            print('Unrecognized smallest dimension: %s' % df.loc[i,'smallestDimension'])
            smallest['X'].append(0)
            smallest['Y'].append(0)
            smallest['Z'].append(0)

    # Add new columns to dataframe
    df['largestX'] = smallest['X']
    df['largestY'] = smallest['Y']
    df['largestZ'] = smallest['Z']
    df['smallestX'] = smallest['X']
    df['smallestY'] = smallest['Y']
    df['smallestZ'] = smallest['Z']

    df = df.drop(columns=['smallestDimension', 'largestDimension'])
    return df

def numberifyLabels(df, labelCol):
    labelDict = {}
    labelIndex = 0
    for label in sorted(df.iloc[:,labelCol].unique()):
        labelDict[label] = labelIndex
        labelIndex = labelIndex + 1

    for i in range(df.shape[0]):
        df.iloc[i,labelCol] = labelDict[df.iloc[i,labelCol]]

    return [df, list(labelDict.keys())]