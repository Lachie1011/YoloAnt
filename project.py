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
    def __init__(self, new_project: bool, project_name: str) -> None:
        """ init function"""
        if new_project:
            self.__createProject(project_name)

        self.project_metadata = self.__loadProject(project_name)
        
        if self.project_metadata is None: 
            return None

        # TODO: assign project values to class

    def __loadProject(self, project_name: str) -> Any:
        """ Private function to load a project's metadata """
        # check if project exists
        project_path = os.getcwd() + "/projects/" + project_name
        if not os.path.exists(project_path):
            return None
        
        # attempt to load project yaml
        with open(project_path + "/project.yaml", "r") as stream:
            try:
                project = yaml.safe_load(stream)
                return project
            except Exception as exc:
                print(exc)

    def __createProject(self, project_name: str) -> None:
        """ Private funtction to create a  project"""
        # check that project doesnt exist
        project_path = os.getcwd() + "/projects/" + project_name
        if os.path.exists(project_path):
            return None
        
        # create a folder wihtin yoloant's 'projects' dir TODO: this could be read from yoloants config
        os.makedirs(os.getcwd() + "/projects/" + project_name)
        
        # create project yaml
        open(os.getcwd() + "/projects/" + project_name + "/project.yaml", "x")
        
        # TODO: write projects name to yaml
        # TODO: get input from user to point towards images
