#!/usr/bin/python

import csv
import sys
import os
import shutil
from collections import namedtuple
from optparse import OptionParser

NUM_COLS = 17
TELO_COLS_START_IDX = 8
DAPI_COLS_START_IDX = 11
FLUR_COLS_START_IDX = 14


## just like constructOutput except necessary
def constructSimple(sets, content):
    output = []
    for s in sets:
        new_set_content = content[s.start_idx:s.end_idx+1]
        
        for line in new_set_content:
            input_num_cols = len(line)
            assert input_num_cols == 6, "Something other than 6 input columns provided"
            line += [""]*(NUM_COLS - input_num_cols)

        new_set_content += [[""]*NUM_COLS]*2

        # Fill up set name line and header line
        new_set_content[0][TELO_COLS_START_IDX:] = [""]*(NUM_COLS-TELO_COLS_START_IDX)
        # Set labels
        new_set_content[1][TELO_COLS_START_IDX:TELO_COLS_START_IDX+2] = ["telo_intens - bg_intens", "Telo: num_pixels * intens/pixel"]
        new_set_content[1][DAPI_COLS_START_IDX:DAPI_COLS_START_IDX+3] = ["DAPI_intens - bg_intens", "DAPI: num_pixels * intens/pixel", "DAPI area"]
        
        for (i, (diff, prod)) in enumerate(zip(s.telo_diffs, s.telo_prods)):
            new_set_content[i+2][TELO_COLS_START_IDX:TELO_COLS_START_IDX+2] = [diff, prod]

        new_set_content[2][DAPI_COLS_START_IDX:DAPI_COLS_START_IDX+3] = [s.nucl_diff, s.nucl_prod, s.nucl_data[0].threshold_area]

        new_set_content[3][FLUR_COLS_START_IDX:] = [s.telo_fluor, s.telo_nucl_div, s.telo_area_div]

        ## is this what I want?
        print s.telo_area_div
	
        # csv write what we care about into another file
        ##print s.telo_fluor, s.telo_nucl_div, s.telo_area_div
	
        output += new_set_content[:]

    return s.telo_area_div




def readContent(file_name):
    print "Reading contents of file: " + file_name
    with open(file_name, "rU") as f:
        reader = csv.reader(f)
        raw_content = [line for line in reader]
        if len(raw_content[0]) > 6:
            print "Warning: Found more than 6 columns in the input file. Only the first 6 columns will be used as input"
        return [line[:6] for line in raw_content]


def isEmptyLine(l):
        return sum([len(token) for token in l]) == 0

def isHeader(l):
        return len(l[0]) != 0 and isEmptyLine(l[3:])

def isPath(l):
	return len(l[1]) != 0 and isEmptyLine(l[2:])

def getSets(content):
    print "Reading data sets..."
    set_start_indices = [i for i, line in enumerate(content) if isHeader(line)]
    set_names = [content[start_idx][0] for start_idx in set_start_indices]
    paths = [content[start_idx][2] for start_idx in set_start_indices]
    print "Found sets: " + ", ".join(set_names)
    ##print set_names
    ##print paths

    set_end_indices = []
    for i, start_idx in enumerate(set_start_indices):
        end_idx = len(content)-1 if i == len(set_start_indices) - 1 else (set_start_indices[i+1] - 2)
        while (end_idx != len(content) and isEmptyLine(content[end_idx])):
            end_idx -= 1
        print "Set " + str(set_names[i]) + " spans non-empty lines " + str(start_idx) + " to " + str(end_idx)
        set_end_indices.append(end_idx)

    return set_names,paths,[Set(set_names[i], set_start_indices[i], set_end_indices[i], content) for i in range(len(set_start_indices))]

class Set:
    def __init__(self, name, start_idx, end_idx, content):
        self.name = name
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.data = [line for line in content[start_idx+2:end_idx+1] if not isEmptyLine(line)]
        self.telo_bg_data = self.getTeloBackgroundData()
        self.telo_data = self.getTeloData()
        if self.telo_data != None:
            assert len(self.telo_data) == len(self.telo_bg_data), "Mismatched number of lines in set " + name
        self.nucl_data = self.getNuclData()

    def getTeloBackgroundData(self):
        if len(self.data) > 2:
            all_telo_data = self.data[:-2]
            telo_data = all_telo_data[:len(all_telo_data)/2]
            for line in telo_data:
                assert line[0] == "Copy of telomere background intensity", "[Set " + self.name + " at line " + str(self.start_idx) + "] Expected telomere background intensity line, but got: " + str(line)
            return [DataLine(*line) for line in telo_data]

    def getTeloData(self):
        if len(self.data) > 2:
            all_telo_data = self.data[:-2]
            telo_data = all_telo_data[len(all_telo_data)/2:]
            for line in telo_data:
                assert line[0] == "Copy of telomere intensity", "[Set " + self.name + " at line " + str(self.start_idx) + "] Expected telomere intensity line, but got: " + str(line)
            return [DataLine(*line) for line in telo_data]

    def getNuclData(self):
        nucl_data = self.data[-2:]
        assert(len(nucl_data) == 2)
        assert(nucl_data[0][0] == "nuclei intensity")
        assert(nucl_data[1][0] == "nuclei background intensity")
        return [DataLine(*line) for line in nucl_data]

    def calcTeloData(self):
        if self.telo_data == None:
            self.telo_diffs = [0]*2
            self.telo_prods = [0]*2
        else:
            diffs = []
            prods = []
            for (i, (telo_bg_d, telo_d)) in enumerate(zip(self.telo_bg_data, self.telo_data)):
                avg_intensity_diff = float(telo_d.avg_intensity) - float(telo_bg_d.avg_intensity)
                telo_prod = max(0, avg_intensity_diff * float(telo_d.threshold_area))
                diffs.append(avg_intensity_diff)
                prods.append(telo_prod)
            self.telo_diffs = diffs
            self.telo_prods = prods

    def calcNuclData(self):
        self.nucl_diff = float(self.nucl_data[0].avg_intensity) - float(self.nucl_data[1].avg_intensity)
        self.nucl_prod = float(self.nucl_data[0].threshold_area) * self.nucl_diff
        assert self.nucl_prod >= 0, "Bad nucleic_data: " + str(self.nucl_data)

    def calcFluorData(self):
        self.telo_fluor = sum(self.telo_prods)
        if (self.nucl_prod != 0):
            self.telo_nucl_div = self.telo_fluor/self.nucl_prod
        else:
            self.telo_nucl_div = 0
        if (float(self.nucl_data[0].threshold_area) != 0):
            self.telo_area_div = self.telo_fluor/float(self.nucl_data[0].threshold_area)
        else:
            self.telo_area_div = 0

    

DataLine = namedtuple("DataLine", ["img_name","region","threshold_area","avg_intensity","intensity_std_dev","max_intensity"])

def constructOutput(sets, content):
    output = []
    whatIwant = []
    for s in sets:
        new_set_content = content[s.start_idx:s.end_idx+1]
        
        for line in new_set_content:
            input_num_cols = len(line)
            assert input_num_cols == 6, "Something other than 6 input columns provided"
            line += [""]*(NUM_COLS - input_num_cols)

        new_set_content += [[""]*NUM_COLS]*2

        # Fill up set name line and header line
        new_set_content[0][TELO_COLS_START_IDX:] = [""]*(NUM_COLS-TELO_COLS_START_IDX)
        # Set labels
        new_set_content[1][TELO_COLS_START_IDX:TELO_COLS_START_IDX+2] = ["telo_intens - bg_intens", "Telo: num_pixels * intens/pixel"]
        new_set_content[1][DAPI_COLS_START_IDX:DAPI_COLS_START_IDX+3] = ["DAPI_intens - bg_intens", "DAPI: num_pixels * intens/pixel", "DAPI area"]
        
        for (i, (diff, prod)) in enumerate(zip(s.telo_diffs, s.telo_prods)):
            new_set_content[i+2][TELO_COLS_START_IDX:TELO_COLS_START_IDX+2] = [diff, prod]

        new_set_content[2][DAPI_COLS_START_IDX:DAPI_COLS_START_IDX+3] = [s.nucl_diff, s.nucl_prod, s.nucl_data[0].threshold_area]

        new_set_content[3][FLUR_COLS_START_IDX:] = [s.telo_fluor, s.telo_nucl_div, s.telo_area_div]

        whatIwant.append(s.telo_area_div)
	
        output += new_set_content[:]
    # Put one line of labels for the result columns
    output[1][FLUR_COLS_START_IDX:FLUR_COLS_START_IDX+3] = ["Telo Fluor", "Telo Fluor/DAPI Fluor", "Telo Fluor/DAPI Area"]
    return whatIwant, output

def writeOutput(file_name, content):
    print "Finished!"
    print "Writing output to file: " + file_name
    with open(file_name, 'w') as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerows(content)

def main(options, args):
    if options.directory:
        dir_name = args[0]
        file_names = filter(lambda fn: fn.endswith(".csv"), os.listdir(dir_name))
    else:
        dir_name = "."
        file_names = [args[0]]

    out_dir = dir_name + "_out"
    print "Emptying directory (including contents): " + out_dir
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir, ignore_errors=True)
    os.mkdir(out_dir)
 

    for file_name in file_names:
        assert file_name.endswith(".csv"), "File name must end with .csv"
        print "#"*100
        content = readContent(dir_name + "/" + file_name)
        print "#"*100
        set_names, paths, sets = getSets(content)
        print "#"*100
        
        for s in sets:
            s.calcTeloData()
            s.calcNuclData()
            s.calcFluorData()

        telo_data, output = constructOutput(sets, content)
        
        filepieces = (paths[0].split('\\')[-1]).split('_')
        outsummary = filepieces[0] + '_' + filepieces[1] + '_' + filepieces[2] + '_summary.txt'
        

        out_file_name = out_dir + "/" + file_name[:file_name.find(".csv")] + "_out.csv"
        writeOutput(out_file_name, output)

        if 'out_file_summary' in locals():
            with open(out_file_summary, 'a') as file:
                for i in range(len(paths)):
                    file.write(str(paths[i]) + ' ' + str(set_names[i]) + ' ' + str(telo_data[i]) + '\n')
        else: 
            out_file_summary = out_dir + "/" + outsummary
            with open(out_file_summary, 'a') as file:
                for i in range(len(paths)):
                    file.write(str(paths[i]) + ' ' + str(set_names[i]) + ' ' + str(telo_data[i]) + '\n')
 

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", "--dir", action="store_true", dest="directory", help="Look for and process files in the provided directory name instead of a file.")
    (options, args) = parser.parse_args()
    main(options, args)
