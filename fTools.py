# Author: Maxime Cornaton
# Date: 2023-06

import os
import json
from bs4 import BeautifulSoup
import shutil


## Get files from path
# @param path: path to the folder
# @return list of files
def getFiles(path: str):
    return os.listdir(path)

## Get html page from path
# @param path: path to the html page
# @return html page
def isHTML(file: str):
    return file.endswith(".html")

def hasHTML(path: str):
    files = getFiles(path)
    for file in files:
        if isHTML(file):
            return True
    return False

## create a JSON file 
# @param path: path to the folder
# @param name: name of the file
# @param data: data to write in the file
# @param extension: extension of the file
def toJSON(path: str, name: str, data: dict, extension: str = ".json"):
    with open(path + name + extension, "w") as json_file:
        json.dump(data, json_file, indent=2)


## Create path if it doesn't exist
# @param path: path to create
def createPath(path):
    if not os.path.exists(path):
        os.makedirs(path)

## Remove path if it exists
# @param path: path to remove
def removePath(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

## Reset path: remove then create
# @param path: path to reset
def resetPath(path):
    removePath(path)
    createPath(path)
    
## Copy file from source to destination
# @param source: source file
# @param destination: destination file
def copyFile(source, destination):
    shutil.copy2(source, destination)
    
## Copy folder from source to destination
# @param source: source folder
# @param destination: destination folder
def copyFolder(source, destination):
    shutil.copytree(source, destination)
    
## Create file
# @param path: path to create
# @param name: name of the file
# @param extension: extension of the file
# @param content: content of the file
def createFile(path, name, extension, content):
    file = open(path + name + extension, "w", encoding="utf-8")
    file.write(content)
    file.close()
    
## Read html file and return BeautifulSoup object
# @param path: path to the html file
# @return: BeautifulSoup object
def getHtmlPage(path: str):
    with open(path, "r") as html_file:
        html_data = html_file.read()
    return BeautifulSoup(html_data, "html.parser")

## Remove extension from file
# @param file: file name    
# @return: file name without extension
def removeExtension(file: str):
    return file.split(".")[-2]

## Check if file is an image
# @param file: file name    
# @return: True if file is an image
def isImage(file: str):
    return file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))

## Check if file is a folder
# @param file: file name
# @return: True if file is a folder
def isFolder(file: str):
    return os.path.isdir(file)

## Get name of the folder and the file
# @param path: path to the file
# @return: name of the folder and the file
def getName(path: str):
    return path.split("/")[-1]

## Get name of the folder and the file without extension
# @param path: path to the file
# @return: name of the folder and the file without extension
def getNameWithoutExtension(path: str):
    if path[-1] != "/":
        return removeExtension(getName(path))
    else:
        return ""

## Replace the backslash by a slash
# @param path: path to the file
# @return: path with slash
def replaceBackslash(path: str):
    return path.replace("\\", "/")


def formatImgName(name:str):
    return name.lower().replace("_", "").replace("-", "_").replace("[" , "").replace("]", "").replace("1", "I").replace("2", "Z").replace("3", "E").replace("4", "A").replace("5", "S").replace("6", "G").replace("7", "T").replace("8", "B").replace("9", "P").replace("0", "O")