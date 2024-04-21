"""
    project.py
"""
import os
import yaml
from typing import Any
from datetime import datetime
from PyQt6.QtGui import QColor

from image import Image
from boundingBox import BoundingBox


class NoAliasDumper(yaml.SafeDumper):
    """ Keep yaml unique to increase readability """
    def ignore_aliases(self, data):
        return True


class Project:
    """
        Gets project related information and provides related functionality
    """
    def __init__(self) -> None:
        """ init """
        self.name = None
        self.datasetPath = None  # path to the directory that contains all of the images
        self.datasetFilePath = None  # path to the stored list of images to be worked on
        self.annotationsFilePath = None  # path to the annotations associated with the project
        self.description = None
        
        self.imageDataset = None
        self.annotationDataset = []
        self.projectValidated = False

    def loadProject(self, projectDir: str) -> None:
        """ Function to load a project's metadata """
        # check if project exists
        if not os.path.exists(projectDir):
            return None

        #TODO: Add some project validation: dataset.yaml exists, annotations.yaml exists, hash over dataset file is same as stored

        # attempt to load project yaml
        with open(projectDir + "/project.yaml", "r") as stream:
            try:
                project = yaml.safe_load(stream)
                self.name = project["name"]
                self.datasetPath = project["datasetPath"]
                self.datasetFilePath = project["datasetFilePath"]
                self.annotationsFilePath = project["annotationsFilePath"]
                self.description = project["description"]
                self.projectValidated = True
            except Exception as exc:
                print(exc)

        # read image dataset
        with open(self.datasetFilePath, "r") as stream:
            try:
                self.imageDataset = yaml.safe_load(stream)
            except Exception as exc:
                print(exc)
        
        # read annotation dataset
        with open(self.annotationsFilePath, "r") as stream:
            try:
                annotationsDataset = yaml.safe_load(stream)
            except Exception as exc:
                print(exc)

        # create dataset that is used for annotating
        self.createAnnotationDataset(self.imageDataset, annotationsDataset)
                
    def createProject(self, name: str, dataset: str) -> None:
        """ Creates a new project"""
        currDatetime = datetime.now()
        # check that project doesnt exist
        projectPath = os.getcwd() + "/projects/" + name
        if os.path.exists(projectPath):
            # TODO: return with more info lol 
            return None

        # create a folder within yoloant's 'projects' dir TODO: default setting
        os.makedirs(projectPath)
        
        # yaml file paths 
        projectFile = projectPath + "/project.yaml"
        annotationsFilePath = projectPath + "/annotations.yaml"
        datasetFilePath = projectPath + "/dataset.yaml"
        
        # dumping project info
        project = {"name": name, 
                   "datasetPath": dataset, 
                   "datasetFilePath":datasetFilePath, 
                   "annotationsFilePath":annotationsFilePath, 
                   "description": "TODO", 
                   "projectCreated":currDatetime, 
                   "lastUpdated":currDatetime }
        with open(projectFile, "x") as file:
            try:
                yaml.dump(project, file, sort_keys=False, Dumper=NoAliasDumper)  # Dont want sorting present
            except Exception as exc:
                print(exc)

        # create dataset yaml file and write out image paths
        imageDataset = []
        imageFiles = os.listdir(dataset)
        for image in imageFiles:
            imageDataset.append(dataset + "/" + image)

        with open(datasetFilePath, "x") as file:
            try:
                yaml.dump(imageDataset, file, sort_keys=False, Dumper=NoAliasDumper)
            except Exception as exc:
                print(exc)

        # create annotations file
        annotationInfo = {"Project": name, "LastUpdated":currDatetime, "Annotations":{}}
        with open(annotationsFilePath, "x") as file:
            try:
                yaml.dump(annotationInfo, file, sort_keys=False, Dumper=NoAliasDumper)
            except Exception as exc:
                print(exc)

        self.loadProject(projectPath)

    def createAnnotationDataset(self, imageDataset, annotationsDataset):
        """ Creates a list of image objects to be used for annotating """
        # create working annotation dataset from dataset.yaml
        for path in imageDataset:
            boundingBoxes = []
            # check for annotations on image, and generate bounding boxes if so
            annotations = annotationsDataset["Annotations"].get(path)
            if annotations:
                for annotation in annotations:
                    boundingBoxes.append(BoundingBox(annotation[0], 
                                                     annotation[1],
                                                     annotation[2],
                                                     annotation[3],
                                                     QColor(annotation[4][0], 
                                                            annotation[4][1],
                                                            annotation[4][2],
                                                            annotation[4][3])))
            
            self.annotationDataset.append(Image(path, boundingBoxes))          

    def writeAnnotations(self) -> None:
        """ Writes out all annotations """
        annotations = {} 
        for image in self.annotationDataset:
            if image.annotated:
                boundingBoxes = []
                for boundingBox in image.boundingBoxes:
                    boundingBoxes.append([boundingBox.x, boundingBox.y, boundingBox.height, boundingBox.width, boundingBox.colour.getRgb()])
                annotations.update({image.path:boundingBoxes})
        
        currDatetime = datetime.now() 
        annotationInfo = {"Project": self.name, "LastUpdated":currDatetime, "Annotations":annotations}
        with open(self.annotationsFilePath, "w") as file:
            try:
                yaml.dump(annotationInfo, file, sort_keys=False, Dumper=NoAliasDumper)
            except Exception as exc:
                print(exc)

