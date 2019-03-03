#! /user/bin/python
import yaml
import os
import sys
import argparse

class YamlReader:

    def __init__(self,parser):
        """
        The constructor reads the argument and sets the path variable to represent the directory structure.

        The constructor verifies if the file path is provided by the user and then assigns it to a variable. If not,
        it displays the usage of the script.

        :param parser: Takes in the command line argument for the file path
        """
        if parser.parse_args().path is None:
            self.showHelp()
        else:
            self.path = parser.parse_args().path[0]
        self.pathList = self.path.split('/')[1:] if self.path.startswith('/') else self.path.split('/')
        self.fileName=self.pathList[len(self.pathList) - 1]

    path = ""
    pathList = []
    fileName = ""
    mergedFile=''
    mergedDic = {}

    def showHelp(self):
        """
        This function is called when the commandline argument is not present.

        :return: Nothing, exit the program
        """
        print "usage: YamlReader.py [-h] [--path PATH]"
        exit()

    def validations(self):
        """
        Validates the directory and the path provided.

        The function checks the following:
        1) The file is a present or not
        2) The file should be a .yaml file
        3) The directory is a valid.
        If any of the conditions are not met, the program would exit.

        :return: None
        """
        if not self.fileName.endswith('yaml') or self.fileName=="":
            print ("File not in YAML format or File not specified")
            sys.exit(404)
        elif not os.path.exists(self.path):
            print ("Invalid Path or File does not exit")
            exit()

    def traverseAndMerge(self):
        """
        Traverses the path of the directory and merges the yaml file

        This function traverses the directory and merges all the yaml file until the top most directory
        is reached or until it finds a directory that does not have the yaml file. This functions works as follows:-
        1) Reads the pathList variable which stores all directories in order
        2) Starts from the last child directory and checks if the input file exists.
        3) If the file exist it would move to it's parent folder and check for the fle with same name.
        4) If this file exists as well, both the files would be merged and the resultant would be stored in
        the variable mergedDic.
        5) The program would then move one level up and again run the same check. If a file is found, it is merged with
        the already merged file, mergedDic.
        6) If at any level the file is not found, the execution stops and the current mergedDic is printed in yaml
        format.

        :return: None
        """
        self.validations()
        length = len(self.pathList)
        previousFile={}
        for i in range (0,len(self.pathList))[::-1]:
            path = '/'.join(self.pathList[0:i])
            # print path
            if os.path.isfile(path+"/"+self.fileName):
                currentFile = path+"/"+self.fileName
                with open(currentFile, 'r') as fileC:
                    currentFileDic = yaml.load(fileC)
                if any(previousFile.values()):
                    self.mergeDic(currentFileDic,previousFile,self.mergedDic)
                    previousFile = self.mergedDic
                else:
                    previousFile = currentFileDic
            else:
                break

    def mergeDic(self, currentFileDic, childFileDic,dic):
        """
        Merges two dictionary.

        This function merges two dictionary while preserving the child directory's primary data type. The merge Behaves
        as follows:
        1) The child's primary data type supersedes parent's, however all values that are missing in child would be
        added to the merged file
        2) The parent's anc the child's list would be concatenated.
        3) For nested values, everything is preserved, however rule 1) and rule 2) still holds.

        :param currentFileDic: File with the same name as input file in dictionary format, present at the current
                                hierarchical level.
        :param childFileDic: File whose primary data types supersedes the parent file's data types.
        :param dic: The self.mergedDic.
        :return: None
        """
        for key in currentFileDic.keys():
            if key not in childFileDic.keys():
                dic[key] = currentFileDic[key]

        for key, value in childFileDic.iteritems():
            if key in currentFileDic.keys():
                if isinstance(currentFileDic[key], float) or isinstance(childFileDic[key], str) or isinstance(childFileDic[key], int):
                    dic[key] = childFileDic[key]
                elif isinstance(childFileDic[key], list) and isinstance(currentFileDic[key], list):
                    dic[key] = currentFileDic[key] + childFileDic[key]
                elif isinstance(childFileDic[key], dict) and isinstance(currentFileDic[key], dict):
                    if (key not in dic.keys()):
                        dic[key] = {}
                    self.mergeDic(currentFileDic[key], childFileDic[key], dic[key])
            elif key not in currentFileDic.keys() and key in childFileDic.keys():
                dic[key] = childFileDic[key]
    @property
    def getMergedYaml(self):
        """
        Getter method for retrieving the merged file

        :return: Merged YAML file
        """
        return yaml.dump(self.mergedDic, default_flow_style=False)

if __name__ == "__main__":
    """
    This is the main function which reads the argument.
    """
    parser = argparse.ArgumentParser(description="The file path")
    parser.add_argument('--path', nargs=1,)
    obj = YamlReader(parser)
    obj.traverseAndMerge()
    print obj.getMergedYaml
