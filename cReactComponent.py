# Author: Maxime Cornaton
# Date: 2023-06

import fTools as Tools

class ReactComponent:
    def __init__(self, **kwargs):
        self.name = self.__class__.__name__
        self.style = kwargs.get("style", "")
        self.id = kwargs.get("id", "")
        self.children = kwargs.get("children", [])

    ## Add a child to the component
    # @param child : ReactComponent or ReactElement
    def addChild(self, child):
        self.children.append(child)

    ## Generate the imported code for the component
    # @return the imported code for the component
    def generateImportedCode(self):
        lines = []
        for child in self.children:
            if child.importCode() not in lines:
                lines.append(child.importCode())
        return "\n".join(lines)

    ## Generate the code for the component
    # @return the code for the component
    def generateCode(self):
        lines = []
        lines.append(self.generateImportedCode())
        lines.append("")
        lines.append(f"function {self.name}() {{")
        lines.append(f"    return (")
        lines.append(f"      <div>")

        for child in self.children:
            lines.append(child.callCode())

        lines.append(f"      </div>")
        lines.append(f"    );")
        lines.append(f"  }}")
        lines.append("")
        lines.append(f"export default {self.name};")
        return "\n".join(lines)

    ## Generate the call code for the component
    # @return the call code for the component
    def callCode(self):
        return f"<{self.name} />"

    ## Generate the import code for the component
    # @return the import code for the component
    def importCode(self):
        # TODO: add the path
        return f'import {self.name} from "./components/{self.name}";'

    ## Download the component
    # @param path : the path where the component will be downloaded
    # @param extension : the extension of the file
    def download(self, path: str, extension: str = ".tsx"):
        Tools.createFile(path, self.name, extension, self.generateCode())

    def __str__(self):
        return f"{self.name} : {self.children}"
    

