# Author: Maxime Cornaton
# Date: 2023-06

import fTools as Tools
from cFormattedPage import FormattedPage

class FormattedSection:
    def __init__(self, name: str):
        self.name = name
        
        self.pages = []
        self.images = []
        
    def addPage(self, page: FormattedPage):
        self.pages.append(page)

    def addImage(self, image: str):
        self.images.append(image)
    
    def load(self, path: str):
        files = Tools.getFiles(path)
        for file in files:
            if Tools.isHTML(file):
                formattedPage = FormattedPage(Tools.removeExtension(file))
                formattedPage.loadHTML(path+"/"+file)
                self.addPage(formattedPage)
            elif Tools.isFolder(path+"/"+file):
                for image in Tools.getFiles(path+"/"+file):
                    if Tools.isImage(image):
                        self.addImage(path+"/"+file+"/"+image)
                    elif Tools.isFolder(path+"/"+file+"/"+image):
                        for image2 in Tools.getFiles(path+"/"+file+"/"+image):
                            if Tools.isImage(image2):
                                self.addImage(path+"/"+file+"/"+image+"/"+image2)
    
    ## Download the pages of the section
    # @param path : the path where the pages will be downloaded
    def downloadPages(self, path: str, extension: str = ".json"):
        Tools.createPath(path)
        for page in self.pages:
            page.download(path, extension)
        
    ## Download the images of the section
    # @param path : the path where the images will be downloaded
    def downloadImages(self, path: str):
        Tools.createPath(path  + "images/")
        for image in self.images:
            Tools.copyFile(image, path  + "images/" +Tools.formatImgName(Tools.getName(image)))

    def downloadAll(self, path: str):
        self.downloadPages(path)
        self.downloadImages(path)
        
    def download(self, path: str, extension: str = ".json"):
        Tools.createPath(path)
        Tools.toJSON(path, self.name, self.toDict(), extension)
        
    def toDict(self):
        return {
            "name": self.name,
            
            "numPages": len(self.pages),
            "numImages": len(self.images),
        }
        
    def toDictFull(self):
        return {
            "name": self.name,
            
            "numPages": len(self.pages),
            "numImages": len(self.images),
            
            "pages": [page.toDict() for page in self.pages],
            "images": self.images,
        }
        
        