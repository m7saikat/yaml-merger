# Nokia-Coding-Challenge

This program takes in two yaml file and merges them. 

The script takes in the path of the file as an argument. It traverses the directory and merges all the yaml file until the top most directory is reached or until it finds a directory that does not have the required yaml file.

The merge behaves as follows:-
  1) The child's primary data type supersedes parent's, however all values that are missing in child would be
    added to the merged file
  2) The parent's anc the child's list would be concatenated.
  3) For nested values, everything is preserved, however rule 1) and rule 2) still holds.
  
The usage of the script is as follows:
python YamlReader.py [-h] [--path PATH], for example
 
root@DESKTOP-F30JNBN:/folder# python ./yamlReader.py ./dir1/dir2/dir3/dir4/input.yaml
 
Dependencies: The script uses pyyaml to convert the yaml file into Python's dictonary data type.
To install pyyaml: pip install pyyaml


