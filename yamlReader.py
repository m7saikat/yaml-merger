#! /user/bin/python
import json
import csv
from collections import defaultdict
import re
import yaml
import os
# import requests
import sys

class YamlReader:
    path = ""
    pathList = []
    fileName = ""
    mergedFile=''

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
        # print self.fileName.endswith('yaml')
        if not self.fileName.endswith('yaml') or self.fileName=="":
            print ("File not in YAML format or File not specified")
            exit(2)
            # print self.path
            # print os.path.exists(self.path)
        elif not os.path.exists(self.path):
            print ("Invalid Path or File does not exit")
            exit(3)
        # elif not os.path.isfile(self.path):
        #     print ("File does not exist")

    def traverse(self):
        self.validations()
        length = len(self.pathList)
        previousFile=''
        # currentFile = self.fileName
        for i in range (0,len(self.pathList))[::-1]:
            path = '/'.join(self.pathList[0:i])
            # print path
            if os.path.isfile(path+"/"+self.fileName):
                currentFile = path+"/"+self.fileName
                with open(currentFile, 'r') as fileC:
                    currentFileDic = yaml.load(fileC)
                if previousFile!='':
                    with open(previousFile, 'r') as fileP:
                        previousFileDic = yaml.load(fileP)
                    # print ("merge: " + currentFile + " : "+ previousFile )
                    previousFile = self.mergeDic(currentFileDic,previousFileDic)
                    # print previousFile
                else:
                    previousFile = currentFile
            else:
                break

    def mergeDic(self, currentFileDic, childFileDic,):

        def merge(key, valueChild, valueCurrent, mergeDic):
            if isinstance(valueChild, float) or isinstance(valueChild, str):
                mergeDic[key] = valueChild
            elif isinstance(valueChild, list) and isinstance(valueChild, list):
                mergeDic[key] = valueCurrent + valueChild
            elif type(valueChild) == type({}) and type(valueCurrent) == type({}):
                for k, val in valueChild.iteritems():
                    if (k in valueCurrent.keys()):
                         mergeDic[k] ={}
                         print "==> ",valueChild, "\n" ,valueCurrent


        mergedDic ={}
        visited = []
        for key, value in childFileDic.iteritems():
            if key in currentFileDic.keys():
                # print type(childFileDic[key]), childFileDic[key]
                # == type(currentFileDic[key])
                merge(key,childFileDic[key], currentFileDic[key], mergedDic)
                # if isinstance(currentFileDic[key],dict) a



        # print mergedDic
        # mergedDic.update(previousFileDic)
        # print mergedDic
        exit(1)
        return currentFileDic



if __name__ == "__main__":
    obj = YamlReader()
    # obj.validations()
    obj.traverse();
    print obj.fileName
