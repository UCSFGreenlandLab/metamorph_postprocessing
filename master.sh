### author: Angelo Pelonero
### email: angelo.pelonero@ucsf.edu
### Batch teloFISH xls to csv + pyprocess.py script
### Updated: 2019-08-21

### USAGE (run on local machine, in the correct dir structure):
# $ sh master.sh
###

### EXPECTED /DIR STRUCTURE:
# /scripts:
#   /python
#       xls2csv.py
#       process2.py
#   /XLS_WORKSPACE
#       [wokspace for .xls files]
###

# update these as scripts get updated (latest - 08-21-19):
xls_2_csv="08-21-19xls2csv.py"
process2="08-21-19process2.py"
XLS_folder="XLS_WORKSPACE"

echo ""
echo "WARNING: If your conversion encounters UTF encoding errors, it is likely due to a corrupt excel file. Please identify and remove the corrupted .xls file to use this software."
echo ""
sleep .1s
echo "Remember, you may use the included XLS directory as a workspace (copy all .xls files in, run pipeline, save results elsewhere, and empty folder for future use). If using script in other directories, please use option 6 to set new directory prior to running processes."
echo ""
sleep 1s
echo "Launching menu..."
echo ""
sleep .1s

while true
do
PS3='^^^ Please select an option - input a number from above ^^^ '
options=("Run xls2csv.py + pyprocess.py pipeline" "Run xls2csv.py only (batch conversion .xls -> .csv)" "Run pyprocess.py only (equivalent to running 'python process2.py -d [dir]')" "Change xls2csv.py" "Change process2.py" "Change .xls directory" "Exit")
select opt in "${options[@]}"
do
    case $opt in
        "Run xls2csv.py + pyprocess.py pipeline")
            echo ""
            echo "Running pipeline..."
            sleep 1s
            cp python/"$xls_2_csv" "$XLS_folder"/xls2csv.py
            cp python/"$process2" "$XLS_folder"/process2.py
            cd "$XLS_folder"
            python xls2csv.py
            python process2.py -d CSV
            rm xls2csv.py
            rm process2.py
            echo "Done, returning to menu..."
            echo ""
            break
            ;;
        "Run xls2csv.py only (batch conversion .xls -> .csv)")
            echo ""
            cp python/"$xls_2_csv" "$XLS_folder"/xls2csv.py
            cd "$XLS_folder"
            python xls2csv.py
            rm xls2csv.py
            echo "Returning to menu..."
            echo ""
            break
            ;;
        "Run pyprocess.py only (equivalent to running 'python process2.py -d [dir]')")
            echo ""
            echo "Please input the directory contatining .csv files:"
            read csvdir
            cp python/"$process2" "$csvdir"/../process2.py
            cd "$csvdir"/
            cd ..
            python process2.py -d "$csvdir"
            rm process2.py
            echo "Done, returning to menu..."
            echo ""
            break
            ;;
         "Change xls2csv.py")
            echo ""
            echo "Input path to new xls2csv.py:"
            read INPUT
            xls_2_csv=$(echo "$INPUT")
            echo ""
            echo "Path to xls2csv.py is now: "$INPUT""
            echo ""
            break
            ;;
         "Change process2.py")
            echo ""
            echo "Input path to new process2.py:"
            read INPUT
            process2=$(echo "$INPUT")
            echo ""
            echo "Path to process2.py is now: "$INPUT""
            echo ""
            break
            ;;
         "Change .xls directory")
            echo ""
            echo "Input new file path to .xls directory:"
            read INPUT
            XLS_folder=$(echo "$INPUT")
            echo ""
            echo "Path to new .xls directory is now: "$INPUT""
            echo ""
            break
            ;;
        "Exit")
            echo ""
            echo "Returning to prompt..."
            echo ""
            exit
            ;;
        *) echo "invalid option "$REPLY"";;
    esac
done
done