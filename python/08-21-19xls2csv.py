import glob,os,pandas as pd,subprocess

# FUNCTIONS

# INITIALIZATIONS
x = 1

# SCRIPT
for xls_file in glob.glob(os.path.join(os.getcwd(),"*.xls*")):
    data_xls = pd.read_excel(xls_file, index_col=None)
    # data_xls = data_xls.dropna(how='all') # Run ONLY if downstream processes DO NOT depend on blank rows
    new_header = data_xls.iloc[0]
    data_xls = data_xls[1:]
    data_xls.columns = new_header
    csv_file = os.path.splitext(xls_file)[0] + ".csv"
    data_xls.to_csv(csv_file, encoding='utf-8', index=False)
    print("Generating CSV # ", x, xls_file)
    x = x + 1

subprocess.call('mkdir CSV', shell=True)
subprocess.call("find . -name '*.csv' -exec mv {} CSV \;", shell=True)

print("")
print("")
print("DONE...")
print("Please run process.py manually, as detailed in your protocol.")
print("Please let me know of any errors you encounter and I will attempt to resolve them ASAP.")