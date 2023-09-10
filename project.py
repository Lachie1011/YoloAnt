"""
    project.py
    WIP: A class that manages project related functionality within Yoloant
"""

import os
import yaml
from typing import Any

class Project:
    """
        Gets project related information and provides related functionality
    """
    def __init__(self) -> None:
        """ init """
        self.projectValidated = False
        self.projectName = None

    def loadProject(self, projectName: str) -> Any:
        """ Private function to load a project's metadata """
        # check if project exists
        projectPath = os.getcwd() + "/projects/" + projectName
        if not os.path.exists(projectPath):
            return None
        
        # attempt to load project yaml
        with open(projectPath + "/project.yaml", "r") as stream:
            try:
                project = yaml.safe_load(stream)
                return project
            except Exception as exc:
                print(exc)
        
        # TODO: update member values with values from yaml
        self.projectValidated = True

    def createProject(self, projectName: str, image_dir: str) -> None:
        """ Private funtction to create a  project"""
        # check that project doesnt exist
        projectPath = os.getcwd() + "/projects/" + projectName
        if os.path.exists(projectPath):
            return None
        
        # create a folder wihtin yoloant's 'projects' dir TODO: this could be read from yoloants config
        os.makedirs(os.getcwd() + "/projects/" + projectName)
        
        # create project yaml
        open(os.getcwd() + "/projects/" + projectName + "/project.yaml", "x")
        
        # TODO: write to yaml 
        # TODO: call load project