"" bzTools.vim
"" Author:    Matt Jenkins
"" Version:   0.1

"" Checks
if exists("g:loaded_bzTools") || &cp
    finish
endif
let g:loaded_bzTools = 1

""===============
"" General settings
if !exists('*BzSendToMaya')
    function! BzSendToMaya(command)
        python import vim
        python vimyaRun(userCmd=vim.eval('a:command'))
    endfunction
endif

"" AutocompleteAssetDictionary settings
if !exists('g:bzTools_autocompleteAssetDictionaryFilePath')
    let g:bzTools_autocompleteAssetDictionaryFilePath = '/Users/'.$USERNAME.'/.vim/mayaAsciiDictionary'
endif

if !exists('g:bzTools_enableAutocompleteAssetDictionary')
    let g:bzTools_enableAutocompleteAssetDictionary = 1
endif

"" MayaPythonBuffer settings
if !exists('g:bzTools_mayaPythonBufferFilePath')
    let g:bzTools_mayaPythonBufferFilePath = '/Users/'.$USERNAME.'/Documents/tmpMayaPython.py'
endif

if !exists('g:bzTools_mayaPythonBufferTemplate')
    let g:bzTools_mayaPythonBufferTemplate = [
                \ 'from maya import cmds as mc', 
                \ 'from maya.api import OpenMaya as om2', 
                \ 'from rigging import *', 
                \ '']
endif

""===============

augroup bzTools
    autocmd!
    autocmd BufEnter,FocusGained *.py :call AutocompleteAssetDictionary()
augroup END

""===============

function! AutocompleteAssetDictionary()
    """ REQUIRES THE BZPIPELINE.
    """ Parse the current build asset's published model and components files and add the node
    """     names to the dictionary file.
    if g:bzTools_enableAutocompleteAssetDictionary == 1
        python bzTools.appendNodesToDictionary()
    endif
endfunction

function! OpenAssetComponentsSceneInMaya()
    """ REQUIRES THE BZPIPELINE.
    """ Query the asset open in the current buffer and send a command to Maya to open the asset's
    """     latest components scene file.
    let l:command = ''
    python bzTools.mayaCommandToOpenComponentsFile()
    if l:command != ''
        call BzSendToMaya(l:command)
    endif
endfunction

function! ToggleMayaPythonBuffer()
    """ Toggle a new split at the bottom of the window that can be used for temporary scripts to
    """     send to maya.
    
    "" If the buffer exists, wipe the buffer and delete the temp file.
    for bufId in range(1, bufnr('$'))
        if bufname(bufId) == g:bzTools_mayaPythonBufferFilePath
            w
            silent execute 'bwipeout' bufId
            call delete(g:bzTools_mayaPythonBufferFilePath)
            return
        endif
    endfor

    "" Otherwise, open a new buffer at the bottom of the window and write the template to it.
    wincmd b
    execute 'bel sp '.g:bzTools_mayaPythonBufferFilePath
    call append(0, g:bzTools_mayaPythonBufferTemplate)
    w
    wincmd J
endfunction


""===============

let s:path=expand('<sfile>:p:h')

function! s:BzTools_init()
    """ Add the current path to the python path, so that the python functions
    """     can be accessed
    "let l:path=expand('<sfile>:p:h')

python << EOF
import sys
import vim

sys.path.append(vim.eval('s:path'))
import bzTools
EOF

""= Set dictionary file
execute 'set dictionary+='.g:bzTools_autocompleteAssetDictionaryFilePath

endfunction

call s:BzTools_init()
