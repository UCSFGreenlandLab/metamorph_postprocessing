### AUTHOR: Angelo Pelonero
### EMAIL: angelo.pelonero@ucsf.edu
### LAST UPDATE: 04-04-2019

##### INTRO:

This software can batch-convert Metamorph .xls files and run the Metamorph analysis python  script on an entire directory of .xls files.

The easiest implementation of this software is to use the /master directory itself as a tool!

This means copying and pasting Metamorph .xls files into the /XLS_WORKSPACE directory, running the master.sh shell script, and then copying your results OUT of the space. For any subsequent runs, delete all content of /XLS and paste new data in place.

You may also run the pipeline on other directories with your .xls files of interest. This has caveats, though:
	1. Whitespaces are disallowed in filepaths. Ensure that NO WHITESPACE is present in the path to the directory of interest.
	2. Option 6 must be run every time the /XLS_WORKSPACE directory isn't used

Please do not rename or rearrange folders within /master as the script is hard-coded to accept these files/directory structure as-is.

You may rename the "master" parent directory to whatever you would like and place it anywhere on your local disk. All paths are relative to INSIDE this directory.
##

##### USAGE:
1. Open Terminal and change directory into this directory ( cd ~/master/ )
2. Invoke the master.sh script ( sh master.sh )
3. Follow the on-screen prompts.
##

##### KNOWN ISSUES
- whitespaces in filepaths are not handled by master.sh
- menu options cannot be run multiple times in a row, therefore the script exits to menu after any one process
- xls2csv.py can crash out due to UTF encoding issues. Only caused by corrupted .xls files in testing... a quarantine system for these problematic files should be implemented
##

##### CHANGELOG:

04-04-2019: Debugged UTF encoding issues in xls2csv.py, made small fixes to pyprocess2.py, and implemented menu-based shell script (master.sh).

##