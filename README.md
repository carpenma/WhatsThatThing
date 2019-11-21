# WhatsThatThing
Identifying STLs with Machine Learning

## Tasks for each script

### ThingFileManipulator - Performing file operations requred to prep data for processing

- [x] Unzipping
- [ ] Removing non-STLs
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
- [ ] Add labels to all rows representing the grouo the data belongs to!
- [x] Export data to CSV

### Metrics Functions
- [ ] Count of folders with multiple STLs
- [ ] Per-directory details

## Order of operations
1. Get list of Thing #s (ThingiverseCaller w/ --list)
2. Download corresponding object files (ThingiverseCaller w/ --file)
3. Unzip files (ThingFileManipulator with --unzip)
4. Remove non-STLs from folders and relocate multi-STL folders for review (ThingFileManipulator w/ --prune)
5. Rename STLs to match thing number and relocate (ThingFileManipulator w/ --rename)
6. Generate CSV of metadata for objects (MetadataGenerator)
### ========= Implemented up to this line ========
7. Combine desired datasets and run alrogithms ()
