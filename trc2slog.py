import string

MAX_COLUMNS = 9
COL_CONS=6
COL_MESS=MAX_COLUMNS-1
START_TAG = "%%"
START_TAG_COUNT = 2
CONSOLE_LIST = set('L*')

results = []

start_count = 0;
def Contents_Filter(contents, lineNumber, totalLines):
    global start_count

    stripped_line = contents.strip()
    if len(stripped_line) == 0 and len(contents) != 0:
        return 1

    if stripped_line == START_TAG:
        start_count += 1
    if start_count < START_TAG_COUNT:
        return 1

    columns = string.split(stripped_line, '\t', MAX_COLUMNS)
    if len(columns) < MAX_COLUMNS:
        return 1

    if columns[COL_CONS] in CONSOLE_LIST:
        try:
            results.append(columns[COL_MESS])
        except IndexError:
            console.write(string.join(columns, "##"))
            console.write("\nnumber of columns: %d" % len(columns))
            return 1

        return 1

    return 1
### end Contents_Filter

# First we'll start an undo action, then Ctrl-Z will undo the actions of the whole script
editor.beginUndoAction()

editor.forEachLine(Contents_Filter)

new_contents = string.join(results, '\n')
editor.selectAll()
editor.replaceSel(new_contents)
del results
del new_contents

# Inform the user that we've done it
notepad.messageBox("Finished!!!", "trc2slog Convertor", 0)

# End the undo action, so Ctrl-Z will undo the above two actions
editor.endUndoAction()
