# Author: Maxime Cornaton
# Date: 2023-06

import fTools as Tools
import re

class FormattedElement:
    def __init__(self, type_: str = "div", **kwargs):
        self.children = []
        self.attributes = kwargs or {}
        
        if "type" in self.attributes:
            self.attributes["input_type"] = self.attributes.pop("type")

        self.type = type_
        
        self.oldImagesPath = "/"
        self.oldImagesCommonPath = "common/"
        self.imagesPath = "./images/"
        self.imagesCommonPath = "./imagesCommon/"
        
        self.formatAttributes()
        
    ## Add an element to the element
    # @param child : FormattedElement
    def addChild(self, child):
        self.children.append(child)
        
    ## charge the element from HTML and its children
    # @param element : BeautifulSoup element
    def loadHTML(self, element):
        children = element.find_all(True, recursive=False)
        for child in children:
            # if child.name in ["center", "strong", "br", "font", "sub"]:
            #     continue
            if child.string:
                child.attrs["text"] = child.string.strip().replace("\n", " ")
            elif child.contents:
                text = child.get_text(separator="\n", strip=True)
                if text and child.name in ["p", "span", "a", "h1", "h2", "h3", "h4", "h5", "h6"]:
                    child.attrs["text"] = text.strip().replace("\n", " ")
            formatted_child = FormattedElement(type_=child.name, **child.attrs)
            formatted_child.loadHTML(child)
            self.addChild(formatted_child)
    
    ## download the element as a JSON file
    # @param path : str
    # @param extension : str
    def download(self, path: str, extension: str = ".json"):
        Tools.toJSON(path, self.name, self.toDict(), extension)

    ## convert the element to a dictionary
    # @return the dictionary
    def toDict(self):
        return {
            "type": self.type,
            **self.attributes, 
            "children": [child.toDict() for child in self.children],
        }
        
    ## format the attributes of the element
    def formatAttributes(self):        
        for key, value in self.attributes.items():
            if key == "src":
                new_value = Tools.replaceBackslash(value)
                new_value = Tools.formatImgName(new_value)
                if self.oldImagesCommonPath in new_value:
                    new_value = new_value.replace(self.oldImagesCommonPath, self.imagesCommonPath)
                else:
                    if "images" in new_value:
                        new_value = new_value.split("/")[-1]
                    new_value = self.imagesPath+new_value
                self.attributes[key] = new_value    
            elif key == "text":
                self.attributes[key] = value.replace(">", "").replace("<", "")
                #if self.type == "p": just because it's faster 
                if self.type == "p":
                    self.attributes[key] = value.replace(">", "").replace("<", "")
            elif key == "dsdestination":
                # if "Navigation" in value:
                #     self.attributes[key] = value.split("Navigation")[-1].lower()
                # elif "*" in value:
                #     name_folder = value.split("Nav")[-1]
                #     self.attributes[key] = ("/Nav"+name_folder).lower()
                # else:
                #     self.attributes[key] = value.split(".")[-1].lower()
                pass
                # print(value)
                # print(self.attributes[key])
            elif key == "style":
                style = value.split(";")
                newStyle = ""
                for i,val in enumerate(style):
                    background_image_match = re.search(r"background-image:", val, re.IGNORECASE)
                    if background_image_match:
                        start_index = background_image_match.end()
                        background_image = val[start_index:].split("(")[1].replace(")", "")
                        new_background_image = Tools.replaceBackslash(background_image)
                        new_background_image = Tools.formatImgName(new_background_image)
                        if self.oldImagesCommonPath in new_background_image:
                            new_background_image = new_background_image.replace(self.oldImagesCommonPath, self.imagesCommonPath)
                        else:
                            if "images" in new_background_image:
                                new_background_image = new_background_image.split("/")[-1]
                            new_background_image = self.imagesPath+new_background_image
                        #print(background_image, new_background_image)
                        newStyle += " background-image: url("+new_background_image+");"
                    else:
                        newVal =  val.replace("=",":")
                        newStyle += newVal+";"
                
                self.attributes["style"] = newStyle
        if self.type == "img":
            if not "src" in self.attributes:
                self.attributes["src"] = "../imagesCommon/default.jpg"
                
                    
                
            
                

