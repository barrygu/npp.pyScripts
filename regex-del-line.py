import string
import re

results = []
filter

def Contents_Filter(contents, lineNumber, totalLines):
    stripped_line = contents.strip()

    if filter.search(stripped_line):
        return 1

    results.append(stripped_line)
    return 1
### end Contents_Filter

input_text = editor.getSelText()
input_text = notepad.prompt("regex: ", "Delete lines with regex: ", input_text)

if input_text != None and len(input_text) != 0:

    filter = re.compile(input_text, re.IGNORECASE)

    # First we'll start an undo action, then Ctrl-Z will undo the actions of the whole script
    editor.beginUndoAction()

    editor.forEachLine(Contents_Filter)

    new_contents = string.join(results, '\n')
    editor.selectAll()
    editor.replaceSel(new_contents)
    del results
    del new_contents

    # Inform the user that we've done it
    # notepad.messageBox("Finished!!!", "Delete lines", 0)

    # End the undo action, so Ctrl-Z will undo the above two actions
    editor.endUndoAction()
