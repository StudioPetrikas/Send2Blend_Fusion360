import adsk.core, adsk.fusion, adsk.cam, traceback, shutil
import apper
import os, re, json

from apper import AppObjects
from .BaseLogger import logger

# export options
exportTypes = 'stl'

# stl options
StlStructure = 'One File Per Body In Occurrence'
StlRefinement = 'High'
includeRootBodies = False

# export directory options
exportDirectory = os.path.expanduser('~/Desktop/S2B_Temp') + '/'

# filename options
removeVersionTags = True
occurrenceIdSeparator = '_'
elementSeparator = ' '
replaceSpaces = True
replaceSpacesWith = '-'
bodyNameSuffix = False
#removeOccurrenceNumber = True

def getExportObjects(rootComponent :adsk.fusion.Component, selectedBodies):
    exportObjects = []
    rootBodies = []
    uniqueComponents = []
    isReferencedComponent = False

    # if bodies folder is visible add all visible bodies to the list of visible objects
    if rootComponent.isBodiesFolderLightBulbOn:
        # get root bodies
        body = adsk.fusion.BRepBody.cast(None)

        for body in rootComponent.bRepBodies:
            if not body.isLightBulbOn:
                logger.info("body %s in %s is not visible", body.name, "root")
                continue

            # add visible body to the list of root bodies
            if includeRootBodies:
                rootBodies.append(body)

        # if root component has bodies, add occurrence to the list of exportable objects
        if len(rootBodies) > 0:
            exportObjects.append({'occurrence': None, 'occurrencePath': "", 'bodies': rootBodies})
        else:
            logger.info("%s has no bodies", "root")
    else:
        logger.info("%s has no visible bodies folder", "root")

    # add visible bodies of all occurrences to the list of visible objects
    for occurrence in rootComponent.allOccurrences:
        isUnique = False

        occurrenceFullPathName = occurrence.fullPathName

        # check if occurrence is visible. if not jump to next occurrence
        if not occurrence.isLightBulbOn:
            logger.info("%s is hidden", occurrenceFullPathName)
            continue

        # check if bodies folder in occurrence is visible.  if not jump to next occurrence
        if not occurrence.component.isBodiesFolderLightBulbOn:
            logger.info("body %s in %s is not visible", body.name, occurrenceFullPathName)
            continue

        # check if component is unique
        if not occurrence.component in uniqueComponents:
            uniqueComponents.append(occurrence.component)
            isUnique = True
            logger.debug("%s is unique", occurrenceFullPathName)

        # check if occurrence is referencing a external component
        if occurrence.isReferencedComponent:
            isReferencedComponent = occurrence.isReferencedComponent

        # get visible occurrence bodies
        occurrenceBodies = []
        for body in occurrence.bRepBodies:
            # check if body is visible. if not jump to next body
            if not body.isLightBulbOn:
                logger.info("body %s in %s is not visible", body.name, occurrence.fullPathName)
                continue

            occurrenceBodies.append(body)

        # check if occurrence has bodies. if not jump to next occurrence
        if len(occurrenceBodies) == 0:
            logger.info("%s has no bodies", occurrenceFullPathName)
            continue

        # if occurrence has bodies, add occurrence to the list of exportable objects
        exportObjects.append({'occurrence': occurrence,
                              'occurrencePath': occurrenceFullPathName,
                              'isUnique': isUnique,
                              'isReferencedComponent': isReferencedComponent,
                              'bodies': occurrenceBodies})

    logger.debug(exportObjects)
    return exportObjects

def totalNumberOfObjects(exportObjects):
    components = 0
    componentBodies = 0
    occurrenceBodies = 0
    total = 0

    for exportObject in exportObjects:
        if exportObject.get('isUnique'):
            components = components + 1
            componentBodies = componentBodies + len(exportObject.get('bodies'))

        occurrenceBodies = occurrenceBodies + len(exportObject.get('bodies'))

    logger.debug("components: %s", components)
    logger.debug("componentBodies: %s", componentBodies)
    logger.debug("occurrenceBodies: %s", occurrenceBodies)
    logger.debug("total: %s", total)

    return total

def removeVersionTag(name):
    if not removeVersionTags:
        return name

    return re.sub(r'[^1]v[0-9]*', '', name)

def getExportName(projectName, designName, occurrenceFullPathName, bodyName, forceAddDesignName, removeOccurrenceNumber):
    nameElements = []

    if replaceSpaces:
        designName = designName.replace(" ", replaceSpacesWith)

    if (forceAddDesignName or 'addDesignNameToFilename') and designName:
        nameElements.append(removeVersionTag(designName))

    # render pathname
    if occurrenceFullPathName:
        
        # replace occurrence id
        pathName = occurrenceFullPathName
        if removeOccurrenceNumber:
            pathName = re.sub(r':[0-9]*', '', pathName)
        else:
            pathName = pathName.replace(":", occurrenceIdSeparator)

        # replace spaces in component names
        if replaceSpaces:
            pathName = pathName.replace(" ", replaceSpacesWith)
        
        # replace occurrences seperator
        pathName = pathName.replace("+", elementSeparator)

        nameElements.append(removeVersionTag(pathName))

    # add body's name
    if bodyNameSuffix:
        nameElements.append(bodyName)

    # assemble filename
    fileName = elementSeparator.join(nameElements)

    # assemble full path name
    fullFileName = exportDirectory + fileName

    logger.debug("fullPathName: %s", fullFileName)

    return fullFileName

def copyDesignToExportDocument(exportObjects):

    # create export document
    application = adsk.core.Application.get()
    fusionDocType = adsk.core.DocumentTypes.FusionDesignDocumentType
    document :adsk.fusion.FusionDocument = application.documents.add(fusionDocType)

    logger.debug("temporary document created")

    # set design type
    design :adsk.fusion.Design = document.design
    design.designType = adsk.fusion.DesignTypes.DirectDesignType

    # get root component
    rootComponent :adsk.fusion.Component = design.rootComponent

    logger.debug("temporary rootComponent created")

    # create 3d object wrapper for creation of occurrences
    matrix3d = adsk.core.Matrix3D.create()

    # create body manager for creating copies of bodies
    temporaryBRepManager = adsk.fusion.TemporaryBRepManager.get()

    # copy relevant occurrences to export document
    for exportObject in exportObjects:
        sourceOccurrence = exportObject.get('occurrence')

        # create occurrences path for export object
        baseComponent = rootComponent

        if exportObject.get('occurrencePath'):
            pathElements = exportObject.get('occurrencePath').split("+")

            for pathElement in pathElements:
                # get new component name and use the old instance id as part of it
                occurrenceInstanceId = pathElement.split(":")[-1]
                occurrenceName = pathElement.replace(":", occurrenceIdSeparator)

                foundOccurrence = rootComponent.allOccurrences.itemByName(occurrenceName + ":" + occurrenceInstanceId)

                # check if occurrence already exists
                if foundOccurrence:
                    # occurrences found, proceed with next element
                    baseComponent = foundOccurrence.component
                    continue

                # create new occurrence
                occurrence = baseComponent.occurrences.addNewComponent(matrix3d)
                component = occurrence.component

                # set component name
                component.name = occurrenceName
                logger.debug("occurrence %s created (part of %s)", occurrenceName, pathElements)

                # set new base
                baseComponent = component

        for body in exportObject.get('bodies'):
            # copy body
            copiedBody = temporaryBRepManager.copy(body)

            # insert body into new document
            baseComponent.bRepBodies.add(copiedBody)
            baseComponent.bRepBodies[-1].name = body.name

            logger.debug("body %s added to %s", body.name, exportObject.get('occurrencePath'))

    return document, rootComponent

def getStlExportOptions(ao, geometry, fullFileName, refinement):
    # get stl export options
    stlExportOptions = ao.export_manager.createSTLExportOptions(geometry, fullFileName)

    # set export resolution
    if refinement == 'Low':
        stlExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementLow

    elif refinement == 'Medium':
        stlExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium

    elif refinement == 'High':
        stlExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh

    elif refinement == 'Ultra':
        stlExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementCustom
        # TODO Remove hardcoded values
        stlExportOptions.surfaceDeviation = 0.000508
        stlExportOptions.normalDeviation = 5.0000

    return stlExportOptions

def exportStlAsOneFilePerBodyInOccurrence(exportObjects, projectName, designName, ao):
    # copy exportObjects into a temporary document and convert all occurrences into unique components.
    tmpDocument, tmpRootComponent = copyDesignToExportDocument(exportObjects)
    saveChanges = False

    # regenerate list of export objects based
    tmpExportObjects = getExportObjects(tmpRootComponent, [])

    
    # generate exports for each selected refinement
    for refinement in StlRefinement:

        # iterate over list of occurrences
        for tmpExportObject in tmpExportObjects:

            # iterate over list of bodies
            for body in tmpExportObject.get('bodies'):

                # create filename but remove occurrence id unless they're part of the occurrence name in the temporary document
                fullFileName = getExportName(projectName, designName, tmpExportObject.get('occurrencePath'), body.name, False, True)

                # get stl export options
                stlExportOptions = getStlExportOptions(ao, body, fullFileName, refinement)

                # export body as single stl file
                exportResult = ao.export_manager.execute(stlExportOptions)
            
    logger.debug("Closing tmpDocument")
    tmpDocument.close(saveChanges)

class Send2BlendExportDesignCommand(apper.Fusion360CommandBase):
    def on_preview(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        pass

    def on_destroy(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, reason, input_values):
        try:
            ao = AppObjects()
            designName = ao.design.rootComponent.name
            projectName = ao.app.activeDocument.dataFile.parentProject.name

            logger.info("--------------------------------------------------------------------------------")
            logger.info("Finished processing of %s - %s", projectName, designName)
            logger.info("--------------------------------------------------------------------------------")

        except:
            logger.info("--------------------------------------------------------------------------------")
            logger.info("Finished")
            logger.info("--------------------------------------------------------------------------------")

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        try:
            ao = AppObjects()          
            rootComponent = ao.design.rootComponent
            designName = rootComponent.name
            activeDocument = ao.app.activeDocument
            projectName = activeDocument.dataFile.parentProject.name
            saveChanges = False

            logger.info("--------------------------------------------------------------------------------")
            logger.info("Starting processing of %s - %s", projectName, designName)
            logger.info("--------------------------------------------------------------------------------")

            logger.info("Making Temp Directory")
            if not os.path.exists(exportDirectory):
                os.mkdir(exportDirectory)
            path = exportDirectory

            logger.info("Deleting files in the Temp Directory if any")
            folder = exportDirectory
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

            # get list of bodies for the exports
            exportObjects = []

            # get list of occurrences and bodies
            logger.debug("getting list of export objects")
            exportObjects = getExportObjects(rootComponent, 'bodies')

            exportStlAsOneFilePerBodyInOccurrence(exportObjects, projectName, designName, ao)

        except:
            logger.error(traceback.format_exc())

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        ao = AppObjects()
        designName = ""
        projectName = ""

        try:

            designName = ao.design.rootComponent.name
            projectName = ao.app.activeDocument.dataFile.parentProject.name

            logger.info("--------------------------------------------------------------------------------")
            logger.info("Initializing processing of %s - %s", projectName, designName)
            logger.info("--------------------------------------------------------------------------------")

        except AttributeError as err:
            logger.error("--------------------------------------------------------------------------------")
            logger.error("Error: No active document found.")
            logger.error("--------------------------------------------------------------------------------")

            if ao.ui:
                ao.ui.messageBox("Error: No active document found.")
        except:
            logger.error("--------------------------------------------------------------------------------")
            logger.error("Error:")
            logger.error("--------------------------------------------------------------------------------")

            logger.error(traceback.format_exc())
    
    def on_stop(self):
        try:
            logger.info("Deleting Temp")
            shutil.rmtree(exportDirectory)
        except:
            return