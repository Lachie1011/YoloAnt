"""
    project.py
"""
import os
import yaml
from typing import Any
from datetime import datetime
from PyQt6.QtGui import QColor

from model import Model
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
        self.description = None
        self.datasetDir = None  # path to the directory that contains all of the images
        self.datasetFilePath = None  # path to the stored list of images to be worked on
        self.annotationsFilePath = None  # path to the annotations associated with the project
        self.modelsDir = None  # path to the directory which stores all of the models
        
        self.imageDataset = None
        self.annotationDataset = []
        self.projectValidated = False
        self.modelDataset = []

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
                self.description = project["description"]
                self.datasetDir = project["datasetDir"]
                self.datasetFilePath = project["datasetFilePath"]
                self.annotationsFilePath = project["annotationsFilePath"]
                self.modelsDir = project["modelsDir"]
                self.projectValidated = True
            except Exception as exc:
                print(exc)

        # read image dataset
        with open(self.datasetFilePath, "r") as stream:
            try:
                self.imageDataset = yaml.safe_load(stream)
            except Exception as exc:
                print(exc)

        # load models stored
        availableModels = os.listdir(self.modelsDir)
        for modelFile in availableModels:
            with open(self.modelsDir + "/" + modelFile, "r") as stream:
                try:
                    modelYaml = yaml.safe_load(stream)
                    model = Model(modelYaml["Name"])
                    model.modelType = modelYaml["Type"]
                    model.device = modelYaml["Device"]
                    model.dimensions = modelYaml["Dimensions"]
                    model.epochs = modelYaml["Epochs"]
                    model.batchSize = modelYaml["BatchSize"]
                    model.workers = modelYaml["Workers"]
                    if model.isValid():
                        self.modelDataset.append(model)
                    else:
                        print(f"Could not load model from {modelFile}")
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

        # create a projects directory
        os.makedirs(projectPath)
        
        # create a machine learning models directory
        modelsDir = projectPath + "/models"
        os.makedirs(modelsDir)

        # yaml file paths 
        projectFile = projectPath + "/project.yaml"
        annotationsFilePath = projectPath + "/annotations.yaml"
        datasetFilePath = projectPath + "/dataset.yaml"

        # create project file
        project = {"name": name,  
                   "description": "TODO", 
                   "datasetDir": dataset, 
                   "datasetFilePath":datasetFilePath, 
                   "annotationsFilePath":annotationsFilePath,
                   "modelsDir":modelsDir,
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

        # load project
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
        """ Writes out all annotations to disk """
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

    def writeModels(self) -> None:
        """ Writes out all models to disk """
        currDatetime = datetime.now()
        for model in self.modelDataset:
            modelFilePath = self.modelsDir + "/" + model.modelName + ".yaml"
            modelInfo = {"Name": model.modelName, "Type": model.modelType, "Device": model.device,
                         "Dimensions": model.dimensions, "Epochs": model.epochs, "BatchSize": model.batchSize, 
                         "Workers": model.workers, "LastUpdated": currDatetime}
            with open(modelFilePath, "w") as file:
                try:
                    yaml.dump(modelInfo, file, sort_keys=False, Dumper=NoAliasDumper)
                except:
                    print(exc)

