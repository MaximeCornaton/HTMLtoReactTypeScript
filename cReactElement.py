# Author: Maxime Cornaton
# Date: 2023-06

import re
import fTools as Tools

class ReactElement:
    
    def __init__(
        self, type_: str = "div", **kwargs):
        self.type = type_
        
        self.style = kwargs.get("style", "")
        self.id = kwargs.get("id", "")
        self.class_ = kwargs.get("class", [])
        
        if isinstance(self.class_, list):
            self.class_ = ",".join(self.class_)
        self.children = kwargs.get("children", [])
        
        self.src_back_img = ""
        self.id = self.format_id()
        self.style = self.format_style()

    def format_id(self):
        return self.id

    def format_style(self):
        IMAGES_MISSING = ["./images/commonengineparameter.png",'./images/hppsymbolIZOxIZZ.png','./images/pagename.png','./images/softecunavairpathZ.png','./images/']
        if self.style:
            newStyle = ""
            style = self.style.split(";")
            for i,val in enumerate(style):
                # Use a generic regex pattern to extract the background-image property
                background_image_match = re.search(r"background-image:", val, re.IGNORECASE)
                if background_image_match:
                    start_index = background_image_match.end()
                    background_image = val[start_index:].split("(")[-1].replace(")", "").replace('\\', "/")
                    if background_image in IMAGES_MISSING:
                        pass
                    else:
                        # Remplacer la propriété background-image par BackgroundImage
                        #style = self.style.replace(background_image_match.group(), f"BackgroundImage: `url({background_image})`")
                        self.src_back_img = background_image
                        newStyle += f"backgroundImage: `url(${{{Tools.getNameWithoutExtension(self.src_back_img)}}})`, "
                
                newProp,newValProp = val.split(":")[0], val.split(":")[-1]
                if "-" in newProp:
                    newProp = newProp.split("-")[0] + newProp.split("-")[1][0].upper() + newProp.split("-")[1][1:]
                if newValProp.strip().isdigit():
                    newValProp = newValProp.strip() + "px"
                if newProp.replace(" ", "") != "" and newValProp.replace(" ", ""):
                    newVal = newProp + ': "'+newValProp+'"'
                    if "backgroundImage" not in newVal:
                        newStyle += newVal+","
            if newStyle != "" and newStyle[-1] != " ": 
                newStyle = newStyle[:-1]
                    
            return newStyle if newStyle == "" or newStyle[-1] != "," else newStyle[:-1]
        return ""
        
    def isNotUseless(self):
        if self.type in ["div", "tr", "td", "table", "object"] and len(self.children) < 1:
            return False
        return True

    ## Add a child to the component
    # @param child : ReactComponent or ReactElement
    def addChild(self, child):
        self.children.append(child)

    ## Generate the call code for the element
    # @return the call code for the element
    def callCode(self):
        style = f'style={{{{{ self.style }}}}}' if self.style != "" else ""
        id_ = f'id="{ self.id }"' if self.id != "" else ""
        className = f'className="{ self.class_ }"' if self.class_ != "" else ""
        lines = []
        lines.append(f"<{self.type} {id_} {style} {className}>")
        for child in self.children:
            lines.append(child.callCode())
        lines.append(f"</{self.type}>")
        return "\n".join(lines)

    ## Generate the import code for the element
    # @return the import code for the element
    def importCode(self):
        lines = []
        if self.src_back_img != "":
            lines.append(f'import {Tools.getNameWithoutExtension(self.src_back_img)} from "{self.src_back_img}";')
        for child in self.children:
            if child.importCode() != "" and child.importCode() not in lines:
                lines.append(child.importCode())
        return "\n".join(lines)
    
    ## Load the element from a FormattedElement
    # @param element : FormattedElement
    # @param RoutesPage
    def load(self, element):
        for child in element.children:
            # if child.type in ["div", "tr", "td", "table", "object"] and len(child.children) < 1:
            #     pass
            if child.type in ["span", "p", "h1", "h2", "h3", "h4", "h5", "h6", "a"] and child.attributes.get("text", "none")=="":
                pass
            else:
                if "dsdestination" in child.attributes and child.type == "button":
                    reactElement = NavigationButton(child.type, **child.attributes)
                elif child.type in ["span", "p", "h1", "h2", "h3", "h4", "h5", "h6", "a", "button"]:
                    reactElement = TextElement(child.type, **child.attributes)
                elif child.type in ["img"]:
                    reactElement = ImageElement(**child.attributes)
                elif child.type == "input" and "dsparampath" in child.attributes:
                    reactElement = InputElement(child.type, **child.attributes)
                elif child.type == "input":
                    reactElement = InputElement(child.type, **child.attributes)
                else:
                    reactElement = ReactElement(child.type, **child.attributes)
                reactElement.load(child)
                self.addChild(reactElement)
    
    def download(self, path: str, extension: str):
        pass
    
    def __str__(self):
        return self.callCode()
    



class TextElement(ReactElement):
    def __init__(self, type, **kwargs):
        super().__init__(type, **kwargs)
        self.text = kwargs.get("text", "")
       

    def callCode(self):
        style = f'style={{{{{ self.style }}}}}' if self.style != "" else ""
        id_ = f'id="{ self.id }"' if self.id != "" else ""
        className = f'className="{ self.class_ }"' if self.class_ != "" else ""
        lines = []
        lines.append(f"<{self.type} {id_} {style} {className}>")
        lines.append(self.text)
        for child in self.children:
            lines.append(child.callCode())
        lines.append(f"</{self.type}>")
        return "\n".join(lines)


class ImageElement(ReactElement):
    def __init__(self, **kwargs):
        super().__init__("img", **kwargs)
        self.src = kwargs.get("src", "") if kwargs.get("src", "") != "./images/" else "../imagesCommon/default.jpg"
        self.name = Tools.getNameWithoutExtension(self.src)+"_img"

    def callCode(self):
        style = f'style={{{{{ self.style }}}}}' if self.style != "" else ""
        id_ = f'id="{ self.id }"' if self.id != "" else ""
        className = f'className="{ self.class_ }"' if self.class_ != "" else ""
        return f'<img {id_} {style} {className} src={{{self.name}}} alt="{self.name}"/>'
    
    def importCode(self):
        lines = []
        lines.append(f'import {self.name} from "{self.src}";')
        for child in self.children:
            if child.importCode() != "" and child.importCode() not in lines:
                lines.append(child.importCode())
        return "\n".join(lines)

    
class NavigationButton(ReactElement):
    def __init__(self, type, **kwargs):
        super().__init__(type, **kwargs)
        self.text = kwargs.get("text", "")
        self.destination = kwargs.get("dsdestination", "")
        
    def importCode(self):
        lines = []
        lines.append('import NavigationButton from "../components/NavigationButton";')
        if self.src_back_img != "":
            lines.append(f'import {Tools.getNameWithoutExtension(self.src_back_img)} from "{self.src_back_img}";')
        return "\n".join(lines)
    
    def callCode(self):
        className = f'className="{ self.class_ }"' if self.class_ != "" else ""
        for child in self.children:
            if child.type == "span":
                self.text = child.text
        if self.text == "":
            self.text = self.destination.split(".")[-1]
        style = f'style={{{{{ self.style }}}}}' if self.style != "" else ""
        return f'<NavigationButton destination="{self.destination}" text="{self.text}" onNavigate={{handleAction}} {style} {className}/>'


class InputElement(ReactElement):
    def __init__(self, type, **kwargs):
        super().__init__(type, **kwargs)
        self.text = kwargs.get("text", "")
        self.dsparampath = kwargs.get("dsparampath", "")
        self.dsvaluechecked = kwargs.get("dsvaluechecked", "")
        self.param = self.dsparampath+"_"+self.dsvaluechecked if self.dsvaluechecked != "" else self.dsparampath
        self.input_type = kwargs.get("input_type", "")
        #print(self.dsparampath, self.dsvaluechecked)
        
    def importCode(self):
        return 'import ParameterInput from "../components/ParameterInput";'
    
    def callCode(self):
        type_ = f'inputType="{ self.input_type }"'
        style = f'style={{{{{ self.style }}}}}' if self.style != "" else ""
        id_ = f'id="{ self.id }"' if self.id != "" else ""
        className = f'className="{ self.class_ }"' if self.class_ != "" else ""
        return f'<ParameterInput parameter="{self.param}" {type_} {id_} {style} {className}/>'