# Author: Maxime Cornaton
# Date: 2023-06

from cFormattedPage import FormattedPage
import fTools as Tools
from cReactElement import ReactElement
from cReactComponent import ReactComponent
import re

class ReactPage:
    def __init__(self, name: str):
        self.name = name
        self.stylePage = StylePage(self.name)
        self.import_style = []
        self.children = []
    
    ## Add a child to the page
    # @param child : ReactElement or ReactComponent
    def addChild(self, child : ReactElement or ReactComponent):
        self.children.append(child)

    ## Generate the imported code for the page
    # @return the imported code for the page
    def generateImportedCode(self):
        lines = []
        lines.append('import React from "react";')
        for child in self.children:
            if child.importCode() != "" and child.importCode() not in lines:
                #TODO: check if the import is already in the code
                #C'est pas opti du tout de reparcourir les enfants mais le probleme est que 
                #les imports sont générés par enfant il faudrait que chaque pas ait une
                #class contenu ("content") qui contient les enfants et qui génère les imports
                for line in child.importCode().split('\n'):
                    if line not in lines:
                        lines.append(line)
        return '\n'.join(lines)
    
    ## Generate the code for the page
    # @return the code for the page
    def generateCode(self):
        lines = []
        lines.append(self.generateImportedCode())
        lines.append('')
        lines.append(f'function {self.name}() {{')
        
        lines.append(f'    return (')
        lines.append(f'      <div>')
        
        for child in self.children:
            lines.append(child.callCode())
        
        lines.append(f'      </div>')
        lines.append(f'    );')
        lines.append(f'  }}')
        lines.append('')
        lines.append(f'export default {self.name};')
        return '\n'.join(lines)
    
    ## Generate the call code for the page
    # @return the call code for the page
    def callCode(self):
        return f'<{self.name} />'
    
    ## Generate the import code for the page
    # @return the import code for the page
    def importCode(self):
        return f'import {self.name} from "./{self.name}";'
    
    ## Load the page from a FormattedPage
    # @param page : the FormattedPage to load
    def load(self, page: FormattedPage):
        # if "../style/nav.css" in page.import_style:
        for child in page.children:
            reactElement = ReactElement(child.type, **child.attributes)
            reactElement.load(child)
            for style_page in page.import_style:
                print(style_page)
                newPage = StylePage(style_page)
                newPage.loadContentByOpeningFile("./defaultProject/style/"+Tools.getName(style_page))
                self.import_style.append(newPage)

            self.style = self.stylePage.loadContent(page.style, import_style=self.import_style)
            self.addChild(reactElement)
    
    ## Download the page
    # @param path : the path where the page will be downloaded
    # @param extension : the extension of the file
    def download(self, path: str, extension: str = ".tsx"):
        Tools.createFile(path, self.name, extension, self.generateCode())
        self.stylePage.download(path)
        for style_page in self.import_style:
            print(style_page.name)
            style_page.download("../src/A_CONVERTER/style/")
        
    ## Download the children of the page
    # @param path : the path where the children will be downloaded
    # @param extension : the extension of the file
    def downloadChildren(self, path: str, extension: str = ".tsx"):
        for child in self.children:
            child.download(path, extension)
    
    ## Download the page and its children
    # @param path : the path where the page and its children will be downloaded
    # @param extension : the extension of the file
    def downloadAll(self, path: str, extension: str = ".tsx"):
        if self.children != []:
            self.download(path, extension)
            self.downloadChildren(path+"components/", extension)
        
    def __str__(self):
        return f'Page {self.name} with {len(self.children)} children'

class NavigatePage(ReactPage):
    def __init__(self, name: str):
        super().__init__(name)
        
    def generateImportedCode(self):
        lines = []
        lines.append(super().generateImportedCode())
        lines.append('import { useEffect } from "react";')
        return '\n'.join(lines)

    def generateCode(self):
        lines = []
        lines.append(self.generateImportedCode())
        lines.append('')
        lines.append(f'function {self.name}({{handleAction,}}: {{handleAction: (action: string) => void;}}) {{')
        if self.stylePage.isUseless() == False:
            lines.append('useEffect(() => {')
            lines.append(f'   import("./{self.stylePage.name}.css");')
            for style in self.import_style:
                if "./" in style.name:
                    lines.append(f' import("{style.name}"); ')
            lines.append("  }, []);")
        lines.append(f'    return (')
        lines.append(f'      <div>')
        
        for child in self.children:
            lines.append(child.callCode())
        
        lines.append(f'      </div>')
        lines.append(f'    );')
        lines.append(f'  }}')
        lines.append('')
        lines.append(f'export default {self.name};')
        return '\n'.join(lines)

class RoutesPage(ReactPage):
    def __init__(self, name: str):
        super().__init__(name)
        self.route = {}
        
    def generateImportedCode(self):
        lines = []
        lines.append('import React from "react";')
        lines.append(f"import {{ ComponentType }} from 'react';")
        for key, value in self.route.items():
            lines.append(f'import {value} from "./{value}";')
        return '\n'.join(lines)
    
    def generateInterfaceCode(self):
        lines = []
        lines.append(f'')
        lines.append(f'interface {self.name}Props {{')
        lines.append(f'  action: string;')
        lines.append(f'  component: ComponentType<any>;')
        lines.append(f'}}')
        return '\n'.join(lines)
        
    def addRoute(self, page, section):
        path = section.name+"."+page.name
        self.route[path] = page.name
        
    def generateCode(self):
        lines = []
        lines.append(self.generateImportedCode())
        lines.append(self.generateInterfaceCode())
        lines.append('')
        lines.append(f'const {self.name}: {self.name}Props[] = [')
        for key, value in self.route.items():
            lines.append(f'  {{ action: "{key}", component: {value} }},')
        lines.append(f'];')
        lines.append('')
        lines.append(f'export default {self.name};')
        return '\n'.join(lines)


class StylePage():
    def __init__(self, name):
        self.name = name
        self.content = ""
        self.import_style = []
        self.width = None
        self.height = None

    def loadContent(self, content: str, import_style):
        self.import_style = import_style
        self.parent = self.import_style[0]
        if content != None:
            self.content = content
        self.width = self.parent.width
        self.height = self.parent.height
        self.formatStyle()
            
    def loadContentByOpeningFile(self, path):
        try:
            with open(path, "r") as file:
                self.content = file.read()
        except FileNotFoundError:
            print(f'File {path} not found.')
        self.formatStyle()

    ## Download the page
    # @param path : the path where the page will be downloaded
    # @param extension : the extension of the file
    def download(self, path: str, extension: str = ".css"):
        if self.isUseless() == False:
            name = self.name.replace(".css", "")
            Tools.createFile(path, name, extension, self.content)

    def remove_html_comments(self):
        # <!-- ... --> du contenu CSS
        self.content = re.sub(r'<!--[\s\S]*?-->', '', self.content)

        
    def formatStyle(self):
        self.remove_html_comments()
        
        newContent = self.content
        base_match = re.search(r'#base\s*{([^}]+)}', newContent)
        if base_match:
            base_style = base_match.group(1)
            self.width = re.search(r'width\s*:\s*(\d+)px;', base_style)
            self.height = re.search(r'height\s*:\s*(\d+)px;', base_style)

            if self.width:
                self.width = int(self.width.group(1))
            else: 
                self.width = 1000
            if self.height:
                self.height = int(self.height.group(1))

            updated_base_style = re.sub(r'\b(top|left)\s*:\s*([\d.]+)px;', r'\1: 0;', base_style)
            updated_base_style = re.sub(r'width\s*:\s*\d+px;', 'width: 100%;', updated_base_style)
            updated_base_style = re.sub(r'height\s*:\s*\d+px;', 'height: 100%;', updated_base_style)
            updated_base_style = re.sub(r'overflow\s*:\s*([^;]+);', 'overflow-x: hidden; overflow-y: scroll;', updated_base_style)
            updated_base_style = updated_base_style.replace('absolute', 'relative')  # Remplacer absolute par relative

            newContent = newContent.replace(base_style, updated_base_style)
        self.content = newContent

        self.absoluteToRelative()

    def absoluteToRelative(self):
        newContent = self.content

        newContent = self.updatePageCenter(newContent)
        newContent = self.updateImageRules(newContent)

        self.content = newContent

    def updateLeftValues(self, content):
        return re.sub(r'(\bleft\s*:\s*)(\d+)px;',
                    lambda match: f'{match.group(1)}{self.convertToPercentage(match.group(2), self.width)}%;',
                    content)

    def updateLeftValuesFromCenter(self, content, diff):
        return re.sub(r'(\bleft\s*:\s*)(\d+)px;',
                    lambda match: f'{match.group(1)} calc(50% + {int(match.group(2)) - self.width/2 + diff}px);',
                    content)

    def updateTopValuesFromCenter(self, content, diff):
        return re.sub(r'(\btop\s*:\s*)(\d+)px;',
                    lambda match: f'{match.group(1)} calc(50% + {int(match.group(2)) - self.height/2 + diff}px);',
                    content)

    def updateTopValuesWidthDiff(self, content, diff):
        return re.sub(r'(\btop\s*:\s*)(\d+)px;',
                    lambda match: f'{match.group(1)} {int(match.group(2)) + diff}px;',
                    content)

    def updateTopValues(self, content):
        return re.sub(r'(\btop\s*:\s*)(\d+)px;',
                    lambda match: f'{match.group(1)}{self.convertToPercentage(match.group(2), self.height)}%;',
                    content)

    def updateHeightValues(self, content):
        return re.sub(r'(\bheight\s*:\s*)(\d+)px;',
                    lambda match: f'{match.group(1)}{self.convertToPercentage(match.group(2), self.height)}%;',
                    content)

    def updateWidthValues(self, content):
        return re.sub(r'(\bwidth\s*:\s*)(\d+)px;',
                    lambda match: f'{match.group(1)}{self.convertToPercentage(match.group(2), self.width)}%;',
                    content)


    def updatePageCenter(self, content):
        pagecenter_rule = re.search(r'#pagecenter\s*{[^}]*}', content)
        if pagecenter_rule:
            pagecenter_rule_text = pagecenter_rule.group()
            pagecenter_rule_text = re.sub(r'top\s*:\s*[^;]+;', 'top: 0;', pagecenter_rule_text)
            pagecenter_rule_text = re.sub(r'left\s*:\s*[^;]+;', 'left: 0;', pagecenter_rule_text)
            if 'height' not in pagecenter_rule_text:
                pagecenter_rule_text = pagecenter_rule_text[:-1] + '; height: 100%; }'
            else:
                pagecenter_rule_text = re.sub(r'height\s*:\s*[^;]+;', 'height: 100%;', pagecenter_rule_text)
            pagecenter_rule_text = pagecenter_rule_text.replace('absolute', 'relative')
            return content.replace(pagecenter_rule.group(), pagecenter_rule_text)
        return content
    
    def updateImageRules(self, content):
        image_rules = re.findall(r'#image(?:_\w+)?\s*{[^}]*}', content)

        for rule in image_rules:
            if "../style/nav.css" == self.parent.name:
                left_diff_content = 0
                top_diff_content = 0

                print("Image avec suffixe:", self.name)
                rule_with_updated_dimensions = re.sub(r'width\s*:\s*[^;]+', 'width: 100%', rule)
                
                
                old_bg_position_match = re.search(r'background-position\s*:\s*([^;]+)', rule)
                if old_bg_position_match:
                    old_bg_position = old_bg_position_match.group(1).replace("px", "")
                    
                    left_diff_content = float(old_bg_position.split()[0])
                    top_diff_content = float(old_bg_position.split()[1])

                    # Construct the new background position value
                    rule_with_updated_dimensions = re.sub(
                        r'background-position\s*:\s*[^;]+;', 
                        f'background-position: 50% calc(50% + 50px);', 
                        rule_with_updated_dimensions
                    )

                rule_with_updated_dimensions = re.sub(r'height\s*:\s*[^;]+', f'height: calc(100% + {top_diff_content-50}px);', rule_with_updated_dimensions)

                content = content.replace(rule, rule_with_updated_dimensions)

                if self.width:
                    content = self.updateLeftValuesFromCenter(content, diff = left_diff_content)
                # if self.height:
                #content = self.updateTopValuesWidthDiff(content, diff = -left_diff_content)
                
            else:
                print("Image sans suffixe:", self.name)
                #rule_with_updated_dimensions = re.sub(r'height\s*:\s*([^;]+)', lambda match: f'height : {min(self.convertToPercentage(match.group(1).replace("px", ""), self.height), 100)}%;', rule)

                #rule_with_updated_dimensions = re.sub(r'height\s*:\s*([^;]+)', lambda match: f'height : {min(float(match.group(1).replace("px", "")), self.height)}px;', rule)
                rule_with_updated_dimensions = re.sub(r'height\s*:\s*([^;]+)', lambda match: f'height : 100%', rule)
                rule_with_updated_dimensions = re.sub(r'width\s*:\s*([^;]+)', lambda match: f'width : 100%', rule_with_updated_dimensions)
                
                # Check for the presence of position property
                # if not re.search(r'position\s*:', rule_with_updated_dimensions):
                #     rule_with_updated_dimensions = rule_with_updated_dimensions.replace('{', '{ position: absolute;')

    
                # Check for the presence of top, left property
                top_match = re.search(r'top\s*:\s*([^;]+)', rule)
                left_match = re.search(r'left\s*:\s*([^;]+)', rule)
                if top_match:
                    top_value = top_match.group(1)
                    
                    if left_match:
                        left_value = left_match.group(1)
                        rule_with_updated_dimensions = re.sub(r'top\s*:\s*[^;]+;', f'background-position: {self.convertToPercentage(left_value.replace("px", ""), self.width)}% {top_value};', rule_with_updated_dimensions)
                        rule_with_updated_dimensions = re.sub(r'left\s*:\s*[^;]+;', '', rule_with_updated_dimensions)
                    else:
                        rule_with_updated_dimensions = re.sub(r'top\s*:\s*[^;]+;', f'background-position: center {top_value};', rule_with_updated_dimensions)
                        
                else:
                    # Check for the presence of top property
                    if left_match:
                        left_value = left_match.group(1)
                        rule_with_updated_dimensions = re.sub(r'left\s*:\s*[^;]+;', f'background-position: {left_value} center;', rule_with_updated_dimensions)


                content = content.replace(rule, rule_with_updated_dimensions)
                
                if self.width:
                    content = self.updateLeftValues(content)
                    content = self.updateWidthValues(content)
                
        return content


    def convertToPercentage(self, value, base):
        value = value.replace(" ", "")
        return (float(value) / base) * 100

    def isUseless(self):
        if self.content == "":
            return True
        return False