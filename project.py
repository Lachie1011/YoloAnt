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
        self.imageDir = None

    def loadProject(self, projectName: str) -> None:
        """ Function to load a project's metadata """
        # check if project exists
        projectPath = os.getcwd() + "/projects/" + projectName
        if not os.path.exists(projectPath):
            return None
        
        # attempt to load project yaml
        with open(projectPath + "/project.yaml", "r") as stream:
            try:
                project = yaml.safe_load(stream)
                self.projectName = project["ProjectName"]
                self.imageDir = project["Images"]
                self.projectValidated = True
            except Exception as exc:
                print(exc)
        

    def createProject(self, projectName: str, imageDir: str) -> None:
        """ Function to create a  project"""
        # check that project doesnt exist
        projectPath = os.getcwd() + "/projects/" + projectName
        if os.path.exists(projectPath):
            return None

        # create a folder within yoloant's 'projects' dir
        os.makedirs(os.getcwd() + "/projects/" + projectName)

        # create project yaml and write project name and image dir to file
        project = {"Images": imageDir, "ProjectName": projectName}
        with open(os.getcwd() + "/projects/" + projectName + "/project.yaml", "x") as file:
            try:
                yaml.dump(project, file)
            except Exception as exc:
                print(exc)
        
        self.projectName = projectName
        self.imageDir = imageDir
        self.projectValidated = True
