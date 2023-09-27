# Author: Maxime Cornaton
# Date: 2023-06

import fTools as Tools
from cFormattedSection import FormattedSection

class FormattedArchitecture:
    def __init__(self, name: str):
        self.name = name
        
        self.sections = []
        self.imagesCommon = []
    
    ## Add a common image to the architecture
    # @param image : str (path)
    def addImageCommon(self, image: str):
        self.imagesCommon.append(image)
        
    ## Add a section to the architecture
    # @param section : FormattedArchitecture
    def addSection(self, section: str):
        self.sections.append(section)
        
    ## Convert the architecture to a dictionary
    # @return the dictionary
    def toDict(self):
        return {
            "name": self.name,
            
            "numImagesCommon": len(self.imagesCommon),
            
            "numSubSections": len(self.sections),
        }
        
    def toDictFull(self):
        return {
            "name": self.name,
            
            "numImagesCommon": len(self.imagesCommon),
            "numSubSections": len(self.sections),
            
            "subSections": [section.toDictFull() for section in self.sections],
            "imagesCommon": [Tools.formatImgName(Tools.getName(image)) for image in self.imagesCommon],
        }
        
    ## Load the architecture from a Folder (HTML Project)
    # @param path : the path of the folder
    def load(self, path: str):
        files = Tools.getFiles(path)
        for file in files:
            if Tools.isFolder(path+file):
                if Tools.hasHTML(path+file):
                    formattedSection = FormattedSection(file)
                    formattedSection.load(path+file)
                    self.addSection(formattedSection)
                else:
                    for image in Tools.getFiles(path+file):
                        if Tools.isImage(image):
                            self.addImageCommon(path+file+"/"+image)
                
        
    ## Download the architecture as a JSON file
    # @param path : the path where the architecture will be downloaded
    def download(self, path: str, extension: str = ".json"):
        Tools.createPath(path)
        Tools.toJSON(path, self.name, self.toDict(), extension)

    ## Download the common images of the architecture
    # @param path : the path where the common images will be downloaded
    def downloadCommonImages(self, path: str):
        Tools.createPath(path)
        for image in self.imagesCommon:
            Tools.copyFile(image, path+ Tools.formatImgName(Tools.getName(image)))
            
    def downloadSections(self, path: str):
        Tools.createPath(path)
        for section in self.sections:
            section.downloadAll(path + section.name + "/")

    ## Download all the files of the architecture
    # @param path : the path where the files will be downloaded
    # @param reset : if the path must be reset
    def downloadAll(self, path: str, reset: bool = False):
        if reset: Tools.resetPath(path)
        self.downloadCommonImages(path + "commonImages/")
        self.downloadSections(path)
        
    ## Download the architecture as a JSON file
    # @param path : the path where the architecture will be downloaded
    def downloadAllFull(self, path: str):
        Tools.toJSON(path, self.name+'_Full', self.toDictFull(), ".json")
        
        
    
        