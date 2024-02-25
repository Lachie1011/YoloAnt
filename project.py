"""
    project.py
"""

import os
import yaml
from typing import Any

from image import Image


class Project:
    """
        Gets project related information and provides related functionality
    """
    def __init__(self) -> None:
        """ init """
        self.projectValidated = False
        self.name = None
        self.dataset = None
        self.datasetPath = None
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
                self.dataset = project["images"]
                self.datasetPath = project["dataset"]
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

        # create a folder within yoloant's 'projects' dir TODO: default setting
        os.makedirs(projectPath)

        # create project yaml and write out default info 
        projectFile = projectPath + "/project.yaml"         
        project = {"name": name, "dataset": dataset, "description": ""}
        with open(projectFile, "x") as file:
            try:
                yaml.dump(project, file, sort_keys=False)  # Dont want sorting present
            except Exception as exc:
                print(exc)

        # create file to keep track of images in dataset
        datasetFile = projectPath + "/dataset.yaml"
        images = os.listdir(dataset)
        with open(datasetFile, "x") as file:
            try:
                yaml.dump(images, file, sort_keys=False)
            except Exception as exc:
                print(exc)

        self.loadProject(projectFile)

