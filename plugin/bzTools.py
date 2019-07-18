import vim
import re
import sys
import os
from getpass import getuser

riggingRepoPath = 'C:/Users/{}/Documents/maya/scripts/rigging'.format(getuser())

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

    with open(filePath, 'r') as f:
        match = re.search(pattern, f.read())

    if not match:
        return False

    assetDict = {}
    assetDict['name'] = match.group(1)
    assetDict['type'] = match.group(2)
    assetDict['project'] = (
        static.queries.projectJobCodeFromName(filePath.partition('builds/')[-1].partition('/')[0])
    )

    return assetDict

def _getAssetClassFromBuffer():
    assetData = _getCurrentBufferAssetData()
    if not assetData:
        return False
    return Asset(assetData['name'], assetData['type'], Project(assetData['project']))


def appendNodesToDictionary():
    def parseFile(asciiFile):
        if not asciiFile or not os.path.isfile(asciiFile):
            return False

        pattern = re.compile("createNode \\w+ -n \"(\\w+_\\w+_\\w{3})\"")
        with open(dictionaryFilePath, 'w+') as dictionaryFile:
            with open(asciiFile, 'r') as f:
                nodeNames = re.findall(pattern, f.read())
            dictionaryFile.write('{}\n'.format('\n'.join(nodeNames)))
        return True

    dictionaryFilePath = vim.eval('g:bzTools_mayaAsciiDictionaryPath')
    buildAsset = _getAssetClassFromBuffer()
    if not buildAsset:
        return False

    ## Files to parse: published model, body components, face components
    parseFile(buildAsset.modelPublished())
    parseFile(buildAsset.bodyComponents())
    parseFile(buildAsset.faceComponents())


def mayaCommandToOpenComponentsFile():
    assetData = _getCurrentBufferAssetData()
    buildAsset = _getAssetClassFromBuffer()

    filePath = (buildAsset.bodyComponents() if assetData['name'] != 'face' else
                buildAsset.faceComponents())
    if filePath:
        filePath = filePath.replace('\\', '/')
    
    command = ('from maya import cmds as mc \n'
               'mc.file(\'{}\', o=1, f=1) \n').format(filePath)
    vim.command('let l:command = "{}"'.format(command))

