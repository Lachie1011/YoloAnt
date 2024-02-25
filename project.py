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

        self.loadProject(projectFile)


    def loadImages(self):
        """ Creates image metadata for every image in a specified directory """
        # load every file in the directory as an image TODO: probably need to like not assume evry file is an image 
        dataset = []
        for file in os.listdir(self.datasetPath):
            image = Image(self.datasetPath + "/" + file)
            if image.isValid:
                dataset.append(image) 
        return dataset

