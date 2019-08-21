### INTRO:

###### Author: Angelo Pelonero | Email: [angelo.pelonero@ucsf.edu](mailto:angelo.pelonero@ucsf.edu) | Latest update: 08-21-2019

This software can batch-convert Metamorph .xls files and run the included Metamorph analysis python  script on an entire directory of .xls files.

Python scripts in workflow have been translated from Python 2.x to Python 3.x. Hooray.

### USAGE:

The easiest implementation of this software is to use the /master directory itself as a tool!

1. Open Terminal and change directory into this directory ( cd ~/master/ )
2. Copy and paste .xls files into the "XLS_WORKSPACE" directory
3. Invoke the master.sh script ( sh master.sh )
3. Copy contents of "XLS_WORKSPACE" to another folder for safekeeping
4. Empty "XLS_WORKSPACE"
5. rinse and repeat ad nauseam
6. Use menu option "Exit" to end session

> NOTE: You may pass other directories to the script, but option 6 must be run every session that the /XLS_WORKSPACE directory isn't used as detailed above


### FYI:
- Do not rename or rearrange folders within "/master" as the script is hard-coded to accept these files/directory structure as-is.

- You may rename the "master" parent directory to whatever you would like and place it anywhere on your local disk. All paths are relative to INSIDE this directory.

### KNOWN ISSUES:

- xls2csv.py can crash out due to UTF encoding issues. Only caused by corrupted .xls files in testing... a quarantine system for these problematic files should be implemented

#### CHANGELOG:

##### 08-21-19:
- Update Python scripts from 2.x to 3.x
- Add support for whitespace in filepaths passed to master.sh
- master.sh returns to menu using "break" instead of "exit" to prompt
- Add example datasets in "XLS_WORKSPACE"
- Update README

##### 04-04-2019:
- Debug UTF encoding issues in xls2csv.py
- Apply small fixes to pyprocess2.py
- Implement menu-based shell script (master.sh)
