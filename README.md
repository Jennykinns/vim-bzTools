# vim-bzTools

## USAGE

### Autocomplete Asset Dictionary
Detects when the current buffer contains a valid Asset build script, then 
populates the dictionary file with node names from the asset's latest 
published model as well as both body and face component scenes.


### Maya Python Buffer
Toggles a temporary python file to quickly send commands to maya. Before
the command opens this file the contents gets deleted, so don't store any
valuable scripts in it. 


### Open Asset Components
Queries the asset's latest components scene from the current buffer and sends
a command to Maya to open that scene.


## CONFIGURATION

### Send to maya command
To allow bzTools to send commands to maya it uses the function 
`BzSendToMaya(str:command)`, this way it can be easily overrided depending 
on the plugin used by the user. By default, bzTools uses Vimya.

### Variables
`g:bzTools_enableAutocompleteAssetDictionary`
`default = 1`

Set g:bzTools_enableAutocompleteAssetDictionary to 0 to disable the autocmd
for autocompleting the current asset's model & components files.


`g:bzTools_autocompleteAssetDictionaryFilePath`
`default = '/Users/'.$USERNAME.'/.vim/mayaAsciiDictionary'`

Set g:bzTools_autocompleteAssetDictionaryFilePath to the file to contain the
asset autocompletion dictionary.

`g:bzTools_mayaPythonBufferFilePath`
`default = '/Users/'.$USERNAME.'/Documents/tmpMayaPython.py'`

Set g:bzTools_mayaPythonBufferFilePath to the file to use for the maya python 
buffer.

`g:bzTools_mayaPythonBufferTemplate`
```
    default = ['from maya import cmds as mc',
             \ 'from maya.api import OpenMaya as om2',
             \ 'from rigging import *',
             \ '']
 ```
g:bzTools_mayaPythonBufferTemplate is a list containing all the lines to 
write to the empty maya python buffer.


## ISSUES
None that I'm aware of... Yay!
