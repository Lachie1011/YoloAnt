"""
    theme.py
"""
import os
import yaml
from enum import Enum

class ThemePaths(Enum):
    darkTheme = 'colourThemes/darkTheme.yaml'

class Theme:
    """
        Gets colour theme for the app
    """
    def __init__(self) -> None:
        """ init """
        self.themeName = None
        self.colours = None
        self.loadTheme(os.getcwd() + "/assets/" + ThemePaths.darkTheme.value)

    def loadTheme(self, themePath: str) -> None:
        """ Function to load a theme's metadata """
        # check if theme exists
        if not os.path.exists(themePath):
            return None
        
        # attempt to load theme yaml
        with open(themePath, "r") as stream:
            try:
                theme = yaml.safe_load(stream)
                self.themeName = theme["name"]
                self.colours = theme["colours"]

            except Exception as exc:
                print(exc)