## Description: This script will automatically create the React App from the HTML Project.
# Author: Maxime Cornaton
# Date: 2023-06

from cFormattedArchitecture import FormattedArchitecture
from cReactArchitecture import ReactArchitecture

REACT_APP_NAME = "DEMO"

FROM = "./HTML/"
JSON = "./JSON/"
TO = "./"+ REACT_APP_NAME +"/"

FORMATTED_SITE = FormattedArchitecture("HTML")

FORMATTED_SITE.load(FROM)

FORMATTED_SITE.downloadAll(JSON, reset=True)

REACT_SITE = ReactArchitecture(REACT_APP_NAME)

REACT_SITE.load(FORMATTED_SITE)

REACT_SITE.downloadAll(TO, reset = True)
