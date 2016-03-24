import string
import re

# keep lines which contain one of keywords in filter-ins
filter_ins = ["dev-ioamp-router"]

filter_outs = ["usbPowerMonitorOM5|_iomodule_create|vdev-medialaunch|pid \d+:"]

# ["io-media-(generic|cinemo)|dev-(navsens|i2c|spi|omappowermgmt|videocapture|((display-)?|dsp)ipc)",
#               " (mmr|libmldr|pid [0-9]+( t)?|mdp|mme|gnc|EventLog|mdi|io-ipc|(mm)?sync|plst):", 
#               "DSI request|AVRCP|tuning_data|HDD power|multicored|qnet\(|udi_(at|de)tach|EIDE driver",
#               "class_|usb|navengine|omap5|mv8787|Navigation|Extproc|VirtQueue|vcapture",
#               "vdev-medialaunch|sdio|ICU-CONVERSION|Watchdog|scsi_|io-fs-media",
#               " (s?cp|mm|procmon|avt|adl|k?sh|DIS2_MSM_App|mm-sync|mdnsd|(Rear)?HMI|(lvds_|devi-)touch)\([0-9]+\)", 
#               " IO_(OPEN|READ|NOTIFY|DEVCTL|CLOSE)[ _]", 
#               " (OSCAR|EHCI|DTC|NmeAudioBuffer) ", 
#               "[a-z]+ ?\[[0-9]+\]"]

filters = {}
filters["ins"] = []
filters["outs"] = []

handled_lines = 0
#total_lines = editor.getLineCount()

for flt in filter_ins:
    filters["ins"].append(re.compile(flt, re.IGNORECASE))

for flt in filter_outs:
    filters["outs"].append(re.compile(flt, re.IGNORECASE))

results = []

col_delimiter = re.compile(" +")
def Column_Filter(line):
    cols = col_delimiter.split(line)

    if len(cols) < 6:
        return 0

    try:
        major = int(cols[4], 10)
        minor = int(cols[5], 10)
    except ValueError as e:
        #console.write(str.format("Error: {}\n", e))
        #console.write(str.format(">> {}\n", line))
        return 0

    if [major, minor] in ([8, 0], [21, 0], [10000, 0], [20002, 480], [20003, 490]):
        return 0 # will check in next step

    if major <= 10000 or (major >= 20000 and major <= 20011):
        return 1 # will be filter-out
### end Contents_Filter

def Contents_Filter(contents, lineNumber, totalLines):
    #global handled_lines
    #handled_lines += 1

    stripped_line = contents.strip()
    if (len(stripped_line) == 0) and (len(contents) != 0):
        return 1

    for flt_in in filters["ins"]:
        if flt_in.search(stripped_line):
            #if handled_lines < 100:
            #    console.write("*** matched in filter_ins, skip it\n");
            results.append(stripped_line)
            return 1

    if Column_Filter(stripped_line) == 1:
        return 1

    out_index = 0
    for flt_out in filters["outs"]:
        if flt_out.search(stripped_line):
            #if handled_lines < 100:
            #    console.write("+++ matched on " + filter_outs[out_index] + "\n")
            return 1
        #out_index += 1

    results.append(stripped_line)
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
notepad.messageBox("Finished!!!", "syslog Filter", 0)

# End the undo action, so Ctrl-Z will undo the above two actions
editor.endUndoAction()
