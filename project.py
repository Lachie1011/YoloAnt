"""
    project.py
    WIP: A class that manages project related functionality within Yoloant
"""

import os
import yaml
from typing import Any

class Project:
    """
        gets project related information and provides related functionality
    """
    def __init__(self, project_name: str) -> None:
        """ init function"""
        # attempt to load project
        self.project_metadata = self.__load_project(project_name)
        if project_name is None:
            self.project_metadata = self.__create_project(project_name)
        
        # TODO: assign project values to class

    def __load_project(self, project_name: str) -> Any:
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

    def __create_project(self, project_name: str) -> Any:
        """ Private funtction to create a  project"""
        # create a folder wihtin yoloant's 'projects' dir TODO: this could be read from yoloants config
        os.makedirs(os.getcwd() + "/projects/" + project_name)

        # create project yaml
        open(os.getcwd() + "/projects/" + project_name + "/project.yaml", "x")

        # TODO: write projects name to yaml
        # TODO: get input from user to point towards images
