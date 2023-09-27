# Author: Maxime Cornaton
# Date: 2023-06

from cReactPage import ReactPage, RoutesPage, NavigatePage
import fTools as Tools

class ReactSection:
    def __init__(self, name):
        self.name = name
        
        self.pages = []
        self.images = []
        
        self.routesPage = RoutesPage("Routes_"+self.name)
        
    def addPage(self, page):
        self.pages.append(page)
    
    def addImage(self, image):
        self.images.append(image)
    
    def load(self, section):
        for page in section.pages:
            reactPage = NavigatePage(page.name)
            reactPage.load(page)
            self.addPage(reactPage)
            self.routesPage.addRoute(page, self)
        for image in section.images:
            self.addImage(image)
    
    def downloadPages(self, path: str, extension: str = ".tsx"):
        Tools.createPath(path)
        for page in self.pages:
            page.downloadAll(path, extension)
            
    def downloadRoutes(self, path: str, extension: str = ".tsx"):
        Tools.createPath(path)
        self.routesPage.download(path, extension)
            
    def downloadImages(self, path: str):
        Tools.createPath(path  + "images/")
        for image in self.images:
            Tools.copyFile(image, path  + "images/" +Tools.formatImgName(Tools.getName(image)))
            
    def downloadAll(self, path: str):
        self.downloadPages(path)
        self.downloadImages(path)
        self.downloadRoutes(path)
        
    def toDict(self):
        return {
            "name": self.name,
            
            "numImages": len(self.images),
            
            "numPages": len(self.pages),
        }
        
    def download(self, path: str, extension: str = ".tsx"):
        Tools.createPath(path)
        Tools.toJSON(path, self.name, self.toDict(), extension)