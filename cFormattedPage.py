# Author: Maxime Cornaton
# Date: 2023-06

import fTools as Tools
import re
from cFormattedElement import FormattedElement

class FormattedPage:
    def __init__(self, name):
        self.name = name[:1].upper() + name[1:]
        self.style = ""
        self.import_style = []
        self.children = []
        
    ## Add an element to the page
    # @param element : FormattedElement
    def addElement(self, element: FormattedElement):
        self.children.append(element)
    
    ## Load the page from HTML
    # @param path : the path of the HTML file
    def loadHTML(self, path: str):
        html_page = Tools.getHtmlPage(path)
        self.style = html_page.find("style").string
        if self.style is not None:
            self.style = (
                self.style.replace("=", ":")
                .replace("left0px", "left:0px")
                .replace("}}", "}")
                .replace("159px   right", "159px ;  right")
            )

        # Parse the 'link' tags to identify and add stylesheets to the 'self.import_style' list
        link_tags = html_page.find_all("link", rel="stylesheet")
        for link_tag in link_tags:
            href = link_tag.get("href")
            if href:
                if "./" not in href:
                    try:
                        with open(path.replace(".html", ".css"), "r") as file:
                            self.style = file.read().replace("=", ":").replace("}}", "}")
                    except FileNotFoundError:
                        print(f'File {path} not found.')
                else:
                    # Use regular expressions to remove any query parameters from the URL
                    clean_href = re.sub(r"\?.*", "", href).replace('common/', 'style/')
                    if "common.css" not in clean_href:
                        self.import_style.append(clean_href)

        body = html_page.find("body")
        children = body.find_all(True, recursive=False)
        for element in children:
            formatted_element = FormattedElement(element.name, **element.attrs)
            formatted_element.loadHTML(element)
            self.addElement(formatted_element)
            
    ## Convert the page to a dictionary
    # @return the dictionary
    def toDict(self):
        return {
            "name": self.name,
            "children": [element.toDict() for element in self.children],
        }

    ## Download the page as a JSON file
    # @param path : the path where the page will be downloaded
    # @param extension : the extension of the file
    def download(self, path: str, extension: str = ".json"):
        Tools.toJSON(path, self.name, self.toDict(), extension)        
            