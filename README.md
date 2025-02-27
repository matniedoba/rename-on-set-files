# About this action

This action let's you select files, that you want to batch rename. It renames all the files based on the following rule

`[parentParentFolder]_[parentParentParentFolder]_[increment].fileExtension`

So in case of:

cathegory
- location
  - RAW
    - file.png

the name will be location_cathegory_##.png

Files are batched (stacked) based on file types. So in a rename you can have a stack of exr files and png files.
