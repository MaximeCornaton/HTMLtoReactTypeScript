# HTML to TypeScript Conversion Tool Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Features](#features)
5. [File Architecture Creation](#file-architecture-creation)
6. [HTML to TypeScript Conversion](#html-to-typescript-conversion)
7. [Image Handling](#image-handling)
8. [Routing Files](#routing-files)
9. [Viewing results](#results)
10. [Conclusion](#conclusion)

---

## 1. Introduction <a name="introduction"></a>

The **HTML** to **TypeScript** Conversion Tool is a utility designed to streamline the process of creating **TypeScript** web pages from existing **HTML** pages. This tool automates the conversion process, optimizes project organization, and enhances routing management.

---

## 2. Installation <a name="installation"></a>

Before you can use the **HTML** to **TypeScript** Conversion Tool, make sure you have the following prerequisites installed on your system:

### Python 3.x

If you don't have Python 3.x installed :

- Download the latest version of Python from the [Python website](https://www.python.org/downloads/).

### Python Libraries

The **HTML** to **TypeScript** Conversion Tool relies on the following Python libraries:

- `os` : This library provides a way of using operating system-dependent functionality like reading or writing to the file system.

- `json`: This library is used for working with **JSON** (JavaScript Object Notation) data, which is commonly used for storing structured data.

- `Beautiful Soup 4`: This library, often abbreviated as BeautifulSoup4 or BS4, is used for parsing **HTML** and **XML** documents. It provides tools for scraping information from web pages.

- `shutil`: This library is a part of the Python standard library and provides file operations that allow you to copy, move, and remove files and directories.

You can install Beautiful Soup 4 using the Python package manager, pip. Open a terminal or command prompt and execute the following command:

```shell
pip install beautifulsoup4
```

The other libraries (os, json, and shutil) are typically included with Python and do not need separate installations.

## 3. Getting Started <a name="getting-started"></a>

To get started with the **HTML** to **TypeScript** Conversion Tool, follow these initial steps:

1. **Prerequisites**: Ensure you have the following prerequisites installed on your system:

   - Python 3.x
   - [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

2. **Download the Tool**: Clone or download the HTML to TypeScript Conversion Tool from the GitHub repository.

3. **Configuration**:

   - Open the `main.py` script in a text editor.
   - Customize the following variables in the script:
     - `REACT_APP_NAME`: Specify the name of your React app.
     - `FROM`: Set the path to your **HTML** project directory.
     - `TO`: Define the destination path where your React app will be generated.

4. **Run the Script**:

   - Open a terminal.
   - Navigate to the tool's directory.
   - Run the script using the following command:
     ```shell
     python main.py
     ```

5. **Optional JSON Output**:
   - By default, the tool converts **HTML** to **TypeScript** without saving **JSON** files. If you wish to save JSON files as well, uncomment the relevant lines in the `main.py` script (see [Recuperation old content](#recuperation-old-content) for details).

You've now converted your first **HTML** project into **TypeScript** files using the HTML to TypeScript conversion tool.

**Note**: One way to exploit this is detailed in the [Viewing results](#results) section.

## 4. Features <a name="features"></a>

### 4.1 File Architecture Creation

The **HTML** to **TypeScript** Conversion Tool automatically generates a file architecture structured by components. This promotes a clean and organized project layout.

By default, this architecture is imported from the `defaultProject/` folder:

```
├── TO/
│   ├── components/
│   │   ├── NavigationButton.tsx
│   │   └── ParameterInput.tsx
│   ├── imagesCommon/
│   ├── style/
│   ├── ParamInterface.tsx
│   └── Routes_App.tsx
└── ReadMe.md
```

**Note**: ParamInterface.tsx and Routes_App.tsx are only used to visualize a [prototype](#results) of the conversion and not in the final project.

### 4.2 HTML to TypeScript Conversion

Simplify the process of converting **HTML** pages to **TypeScript**. The tool ensures consistency in your codebase and saves development time.

Here's a possible project instance diagram:

```console
└── ReactArchitecture
    ├── ReactSection
    │   ├── ReactPage
    │   │   ├── ReactElement
    │   │   └── ReactElement
    │   │       ├── ReactElement
    │   │       └── ReactElement
    │   ├── ReactPage
    │   │   ├── ReactElement
    │   │   └── ReactElement
    │   └── ReactPage
    │       └── ReactElement
    ├── ...
    └── ReactSection
        ├── ReactPage
        ├── ...
        └── ReactPage

```

### 4.3 Image Organization

All images used in your project are intelligently grouped within their respective sections. This feature aids in asset management and maintains a tidy project directory.

### 4.4 Routing Files

To facilitate navigation, the tool automatically generates routing files for each section. This results in a smoother user experience and simplifies route management.

## 5. File Architecture Creation <a name="file-architecture-creation"></a>

### 5.1 Folder Structure

The tool creates a folder structure for your project, grouping components, images, and routing files. This organized layout enhances code maintainability and project scalability.

```console
├── TO/
│   ├── components/
│   │   ├── NavigationButton.tsx
│   │   └── ParameterInput.tsx
│   ├── ReactSection_1/
│   │   ├── images/
│   │   ├── ...
│   │   └── Routes_ReactSection_1.tsx
│   ├── ...
│   ├── imagesCommon/
│   ├── style/
│   ├── ParamInterface.tsx
│   └── Routes_App.tsx
└── ReadMe.md
```

### 5.2 Component Files

Each **HTML** page is converted into a **TypeScript** component file _.tsx_ with corresponding stylesheets _.css_. These components are organized within folders (sections) for easy access and modification.

## 6. HTML to TypeScript Conversion <a name="html-to-typescript-conversion"></a>

### 6.1 Consistent Code

The tool ensures that the **TypeScript** code generated from **HTML** is consistent and adheres to best practices. This includes proper indentation, naming conventions, and code structure.

### 6.2 Handling Events

HTML browsing events are adapted to **Typescript** without the need for a React Router involving url access.

### 6.3 How does it work ?

Pages are created in 2 stages + 1 bonus stage:

- [Recuperation of old page content](#recuperation-old-content)
- [Production of typescript pages](#production-typescript)
- [Style management](#style-management)

#### 6.3.1 Recuperation of old page content <a name="recuperation-old-content"></a>

The first step is to create a `FormattedPage` instance for each **html** document found in the sections.

Recovering all the content of a page is done recursively. Thanks to [BeautifulSoup](#getting-started)'s parsing, we're able to find the elements that make up the page, as well as recovering all the properties.
From here, we create `FormattedElement` instances that we add to the `FormattedPage`. These element instances will themselves create `FormattedElement` instances inside them, if they contain anything.

The download functions of these instances will create **JSON** files of these formatted pages in order to view and examine the sequencing of the **HTML** pages.

#### 6.3.2 Production of Typescript pages <a name="production-typescript"></a>

`ReactPage` instances are produced using `FormattedPage` instances.

Using the FormattedPage information, new pages are constructed as follows:
A static page base is hard-coded into the script. It waits for the code of all its children to be added, as well as everything else required for proper compilation.

The static part of the page looks like this:

```typescript
import React from "react";
//Code will be added here...
import { useEffect } from "react";

function PAGE_NAME({ handleAction, }: { handleAction: (action: string) => void; }) {
  useEffect(() => {
      //...and here...
  }, []);
  return (
      //...and here
  );
}

export default PAGE_NAME;
```

- In the return we'll place the page content, i.e. all the `callCode()` of the `ReactElement` instances that make it up. The latter are obviously based on the `FormattedElement` instances.

- At the top of the file, we'll add the necessary imports for the page elements. We will place the `importCode()` of each of them.

- In the useEffect, we place the style imports for the page. (This is only useful for the [prototype](#results); see [Style management](#style-management) to get to the heart of the matter).

**Note**: handleAction will be used for navigation; it's a function passed on by the parent that will be called when buttons are clicked in page navigation. <a name="note-handle-action"></a>

#### 6.3.3 Style management <a name="style-management"></a>

Currently, there are 2 ways of defining style in these **typescript** pages:

- By simply entering style file paths to be imported from the `defaultProject` folder
- By loading the page style in the `StylePage` instance created when `ReactPage` is initialized

The first point is simply retrieved from the `FormattedPage`,

The second is done in 2 ways. Either the style is written in the initial **html** page, or it is in a **.css** file with the same name as the **html** file.

In both cases, the content of the style is retrieved and processing begins:

- removal of **HTML** comments
- correction of a few hard-coded errors (such as using "=" instead of ":")
- style processing to modify the way elements are positioned on width and positioning types

When you download the **typescript** file for the new page, you also download the associated style files.

> ⚠ <a name="style-warning"></a> For the [prototype](#results), the file is produced in **.css**, which is not optimal but was sufficient to see the first results. One solution would be not to separate the style file and the typescript file and to directly put the style in the tags of each element, adapting the **css** style into **ReactJS** style.

## 7. Image Handling <a name="image-handling"></a>

### 7.1 Image Grouping

Images used within each section are grouped together in a dedicated folder. This ensures that images are easily accessible and organized.

### 7.2 Automatic Imports

Image paths in the **TypeScript** code are automatically updated to reflect the new project structure. This eliminates broken image links and saves development time.

The script is able to overcome numerous problems such as:

- different file names and paths in **html** files (upper/lower case)
- image names starting with numbers (leading to **react** errors)
- problematic characters in names (such as "-", which leads to **react** errors)

## 8. Routing Files <a name="routing-files"></a>

### 8.1 Routing Configuration

Routing files are generated for each section, making navigation between pages seamless. Routes are configured to match the new **TypeScript** components.

Each `ReactSection` instance created is initialized with the creation of a `RoutesPage` instance and uses its corresponding `FormattedSection` instance.

For each instance of the [ReactPage](#production-typescript) class created in these section instances, a match is made between the "action" designing the destination address and the component designing the page.

Like other generated pages, route pages contain a static part to which we add code via the script :

```typescript
import React from "react";
import { ComponentType } from "react";
//Code will be added here...

interface Routes_SECTION_NAMEProps {
  action: string;
  component: ComponentType<any>;
}

const Routes_SECTION_NAME: Routes_SECTION_NAMEProps[] = [
  //...and here
];

export default Routes_SECTION_NAME;
```

**Note**: the interface could be exported at the beginning of the project architecture to avoid repeating the code

When the page is downloaded, the routes are written to the file and the imports of the components to which the routes point are added.

Routes are written to the typescript file in this way:

```typescript
{ action: "DESTINATION_PATH", component: COMPONENT_NAME },
```

### 8.2 Customization

You can customize routing options, such as route names and default pages, to suit your project's specific requirements.

## 9. Viewing results <a name="results"></a>

### 9.1 Prototype

#### 9.1.1 Launch default project

To view a prototype of the conversion results in a basic React project:

To start a new Create React App with **TypeScript** project, you can run this command at the location where you want to create the project:

```console
npx create-react-app my-app --template typescript
```

Then simply add your `TO/` folder, obtained from the script output, to the `src` directory:

```console
└── src
    ├── TO/
    │   ├── components/
    │   │   ├── NavigationButton.tsx
    │   │   └── ParameterInput.tsx
    │   ├── imagesCommon/
    │   ├── ...
    │   ├── style/
    │   ├── ParamInterface.tsx
    │   └── Routes_App.tsx
    ├── App.tsx
    ├── ...
    └── index.tsx
```

Modifying your App.tsx to import the `ParamInterface` component, your file should look like this:

```typescript
import React from "react";
import "./App.css";
//Replace TO with your folder name
import ParamInterface from "./TO/ParamInterface";

function App() {
  return (
    <div className="App">
      <ParamInterface />
    </div>
  );
}

export default App;
```

Finally, from the `my-app` folder, run :

```console
npm run start
```

**Note**: If you get errors related to the style and format of the **css** file, simply add a `globals.d.ts` file to your `src` directory containing this code:

```typescript
declare module "*.css";
```

**Note 2**: Tt's normal to have to reload the page to see the page style change, which is one of the reasons why the style import needs to be reviewed. [ReactStyle warning!](#style-warning)

#### 9.1.2 Understanding `Routes_App.tsx` and `ParamInterface.tsx` <a name="understanding-routes-interface-prototype"></a>

- `Routes_App.tsx` : like the other [routes files](#routing-files), it lets you associate destination addresses with components to be loaded for navigation. However, you need to fill this in manually to create the navigation to the different sections of the prototype.

- `ParamInterface.tsx` : it is the parent component of our entire page transformation project. It is responsible for displaying the right pages, and for maintaining the prototype's navigation logic. `handleAction()` is placed as a page parameter and is called when a button is clicked. It is responsible for updating the destination value in the parent component. In our return, we call `renderComponent()`, which displays the correct page from the destination currently in memory. It will search all route files (update according to your sections!), and load the associated component if the destination address exists, otherwise display `DefaultPage`.

## 10. Conclusion <a name="conclusion"></a>

In conclusion, the **HTML** to **TypeScript** Conversion Tool is a valuable asset for simplifying web development tasks. It streamlines the conversion of **HTML** pages to **TypeScript**, optimizes project organization, handles images efficiently, and helps manage routing files effectively.

Happy Coding !
# HtmlToReactTypescript
