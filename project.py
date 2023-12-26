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
        self.name = None
        self.dataset = None
        self.description = None

    def loadProject(self, projectPath: str) -> None:
        """ Function to load a project's metadata """
        # check if project exists
        if not os.path.exists(projectPath):
            return None
        
        # attempt to load project yaml
        with open(projectPath, "r") as stream:
            try:
                project = yaml.safe_load(stream)
                self.name = project["name"]
                self.dataset = project["dataset"]
                self.description = project["description"]
                self.projectValidated = True
            except Exception as exc:
                print(exc)
        

    def createProject(self, name: str, dataset: str) -> None:
        """ Function to create a  project"""
        # check that project doesnt exist
        projectPath = os.getcwd() + "/projects/" + name
        if os.path.exists(projectPath):
            return None

        # create a folder within yoloant's 'projects' dir
        os.makedirs(os.getcwd() + "/projects/" + name)

        # create project yaml and write project name and image dir to file, desc at this point is nothing
        project = {"name": name, "dataset": dataset, "description": ""}
        with open(os.getcwd() + "/projects/" + name + "/project.yaml", "x") as file:
            try:
                yaml.dump(project, file, sort_keys=False)  # Dont want sorting present
            except Exception as exc:
                print(exc)
        
        self.name = name
        self.dataset = dataset
        self.projectValidated = True
