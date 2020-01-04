# WhatsThatThing
Identifying STLs with Machine Learning

## Overall Project Tasks
- [x] Download more datasets
  - [x] Cookie Cutters
  - [x] Rings
- [x] Remove redundant features
- [x] Standardize data
- [x] Research papers on 3D object identification
- [x] Compile results from algorithms
  - [x] Decision Trees
  - [x] Nearest Neighbor
  - [x] Naive Bayes
- [ ] Voxel-Based Model?
- [ ] Create project slides
- [ ] Write up report on my results

## Tasks for each script
### ThingFileManipulator - Performing file operations requred to prep data for processing
- [x] Unzipping
- [x] Removing non-STLs
- [ ] Determining which STLs in a folder to keep if multiple present
- [x] Renaming STLs

### MetadataGenerator - Read STL files and generate the metadata used for machine learning algorithm
- [x] Load in STLs
- [x] Retrieve number of triangles
- [x] Calculate volume of object
- [x] Calculate volume of bounding box
- [x] Ratio of part to bounding box volume
- [x] Aspect ratios
- [ ] Get data from thingiverse like item names and descriptions?
- [x] Overall file size? (Redundant w/ # triangles)
- [x] Add labels to all rows representing the grouo the data belongs to!
- [x] Export data to CSV
#### Metrics Functions
- [x] Count of folders with multiple STLs
- [x] Per-directory details
- [ ] Check units of each file

### FileVoxelizer - Convert all .stls in a directory into arrays of Voxels representing a normalized cube of volume
- [x] Scale each file (into 10cm cube volume)
- [x] Convert file into (filled) VoxelGrid
- [ ] Generate array of voxels
- [ ] Store Voxels, ThingID, and label, into csv

### DoDataScience - Frontend for applying different algorithms to the data
- [x] Load hardcoded datasets
- [x] Training/testing partitions
- [x] Decision Trees
- [x] Nearest Neighbor

## Order of operations
1. Get list of Thing #s (ThingiverseCaller w/ --list)
2. Download corresponding object files (ThingiverseCaller w/ --file)
3. Unzip files (ThingFileManipulator with --unzip)
4. Remove non-STLs from folders and relocate multi-STL folders for review (ThingFileManipulator w/ --prune)
5. Rename STLs to match thing number and relocate (ThingFileManipulator w/ --rename)
6. Generate CSV of metadata for objects (MetadataGenerator)
7. Combine desired datasets and run alrogithms (DoDataScience)
