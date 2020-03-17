import vim
import re
import sys
import os
from getpass import getuser

riggingRepoPath = 'C:/Users/{}/Documents/maya/scripts/rigging/framework'.format(getuser())

sys.path.append(riggingRepoPath)
import static

sys.path.append('{}/workspace'.format(riggingRepoPath))
from project import Asset, Project

def _getCurrentBufferAssetData():
    filePath = vim.eval('expand("%:p")')
    fileName = vim.eval('expand("%:p:t:r")')

    pattern = re.compile("build\\((?:'|\")(\\w+)(?:'|\"),\\s(?:'|\")(\\w+)(?:'|\"),\\s\\w+\\)")

    if not os.path.isfile(filePath):
        return False

    try:
        f = open(filePath, 'r')
        match = re.search(pattern, f.read())
    except:
        match = False
    finally:
        f.close()
    # with open(filePath, 'r') as f:
    #     match = re.search(pattern, f.read())

    if not match:
        return False

    assetDict = {}
    assetDict['name'] = match.group(1)
    assetDict['type'] = match.group(2)
    projectName = filePath.partition('builds/')[-1].partition('/')[0]
    assetDict['project'] = (static.projects.ProjectsData().getJobCode(
        filePath.partition('builds/')[-1].partition('/')[0]))
    assetDict['fileName'] = fileName

    return assetDict

def _getAssetClassFromBuffer():
    assetData = _getCurrentBufferAssetData()
    if not assetData:
        return False
    try:
        assetClass = Asset(assetData['name'], assetData['type'], Project(assetData['project']))
    except:
        return False

    return assetClass


def appendNodesToDictionary():
    def parseFile(asciiFile):
        if not asciiFile or not os.path.isfile(asciiFile):
            return False

        pattern = re.compile("createNode \\w+ -n \"(\\w+_\\w+_\\w{3})\"")
        with open(asciiFile, 'r') as f:
            nodeNames = re.findall(pattern, f.read())
        dictionaryFile.write('{}\n'.format('\n'.join(nodeNames)))
        return True

    dictionaryFilePath = vim.eval('g:bzTools_autocompleteAssetDictionaryFilePath')
    buildAsset = _getAssetClassFromBuffer()
    if not buildAsset:
        return False

    ## Files to parse: published model, body components, face components
    with open(dictionaryFilePath, 'w+') as dictionaryFile:
        parseFile(buildAsset.modelPublished())
        parseFile(buildAsset.bodyComponents())
        parseFile(buildAsset.faceComponents())


def mayaCommandToOpenComponentsFile():
    assetData = _getCurrentBufferAssetData()
    buildAsset = _getAssetClassFromBuffer()

    if not assetData:
        return False

    if not buildAsset:
        return False

    filePath = (buildAsset.bodyComponents() if assetData['fileName'] != 'face' else
                buildAsset.faceComponents())
    if filePath:
        filePath = filePath.replace('\\', '/')
    
    print 'Opening {} component scene for {}'.format(assetData['type'], assetData['name'])
    command = ('from maya import cmds as mc \n'
               'mc.file(\'{}\', o=1, f=1) \n').format(filePath)
    vim.command('let l:command = "{}"'.format(command))

