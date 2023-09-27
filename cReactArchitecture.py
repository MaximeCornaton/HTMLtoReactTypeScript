# Author: Maxime Cornaton
# Date: 2023-06

from cFormattedArchitecture import FormattedArchitecture
from cReactSection import ReactSection
from cReactPage import RoutesPage
import fTools as Tools

class ReactArchitecture:
    def __init__(self, name):
        self.name = name
        
        self.sections = []
        self.imagesCommon = []
            
    def addSection(self, section):
        self.sections.append(section)
            
    def addImageCommon(self, image):
        self.imagesCommon.append(image)
        
    def toDict(self):
        return {
            "name": self.name,
            
            "numImagesCommon": len(self.imagesCommon),
            "numSubSections": len(self.sections),
        }
        
    def load(self, site: FormattedArchitecture):
        for section in site.sections:
            reactSection = ReactSection(section.name)
            reactSection.load(section)
            self.addSection(reactSection)
        for image in site.imagesCommon:
            self.addImageCommon(image)
             
    def downloadDefault(self, path: str):
        Tools.copyFolder("defaultProject/components", path + "components")
        Tools.copyFolder("defaultProject/imagesCommon", path + "imagesCommon")
        Tools.copyFile("defaultProject/ParamInterface.tsx", path + "ParamInterface.tsx")
        #Tools.copyFile("defaultProject/DynamicCSSLoader.tsx", path + "DynamicCSSLoader.tsx")
        #Tools.copyFile("defaultProject/ParamsManager.tsx", path + "ParamsManager.tsx")
        Tools.copyFolder("defaultProject/style", path + "style")
        Tools.copyFile("defaultProject/Routes_App.tsx", path + "Routes_App.tsx")

    def downloadSections(self, path: str, extension: str = ".tsx"):
        for section in self.sections:
            Tools.createPath(path)
            section.downloadAll(path + section.name + "/")
    
    def downloadImages(self, path: str):
        for image in self.imagesCommon:
            Tools.createPath(path + "imagesCommon/")
            Tools.copyFile(image, path + "imagesCommon/" + Tools.formatImgName(Tools.getName(image)))
            
    def downloadAll(self, path: str, reset: bool = False):
        if reset:
            Tools.resetPath(path)
            self.downloadDefault(path)
        self.downloadSections(path)
        self.downloadImages(path)
        
    def download(self, path: str, extension: str = ".tsx"):
        Tools.createPath(path)
        Tools.toJSON(path, self.name, self.toDict(), extension)
