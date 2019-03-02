#! /user/bin/python
import yaml
import os
import sys
from collections import defaultdict

class YamlReader:
    path = ""
    pathList = []
    fileName = ""
    mergedFile=''
    mergedDic = {}

    def showHelp(self):
        print "usage:"+" yamlReader <Path to input file>"

    def validations(self):
        if len(sys.argv) < 2:
            print "Error: file path not provided"
            self.showHelp()
            exit(1)
        else:
            self.path = sys.argv[1]
            self.pathList = self.path.split('/')[1:] if self.path.startswith('/') else self.path.split('/')
            self.fileName=self.pathList[len(self.pathList) - 1]
            self.checkIfFileExits()

    def checkIfFileExits(self):
        if not self.fileName.endswith('yaml') or self.fileName=="":
            print ("File not in YAML format or File not specified")
            exit(2)
        elif not os.path.exists(self.path):
            print ("Invalid Path or File does not exit")
            exit(3)

    def traverseAndMerge(self):
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
                    # dic[key] = defaultdict(dict)
                    if (key not in dic.keys()):
                        dic[key] = {}
                    self.mergeDic(currentFileDic[key], childFileDic[key], dic[key])
            elif key not in currentFileDic.keys() and key in childFileDic.keys():
                dic[key] = childFileDic[key]

    @property
    def getMergedYaml(self):
        return self.mergedDic

if __name__ == "__main__":
    obj = YamlReader()
    # obj.validations()
    obj.traverseAndMerge()
    print obj.getMergedYaml
    print obj.fileName
