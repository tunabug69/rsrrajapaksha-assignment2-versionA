#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: "Ranmunige Senitha Ransen Rajapaksha"
Semester: "Fall 2024"

The python code in this file is original work written by
"Student Name". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: <Enter your documentation here>

'''

import argparse
import os, sys

def parse_command_args() -> object:
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts",epilog="Copyright 2023")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    # check the docs for an argparse option to store this as a boolean.
    parser.add_argument("program", type=str, nargs='?', help="if a program is specified, show memory use of all associated processes. Show only total use is not.")
    args = parser.parse_args()
    return args
# create argparse function
# -H human readable
# -r running only

#---------------------------------------------------------------MILESTONE 1------------------------------------------------------------------------------------------------------

def percent_to_graph(percent: float, length: int=20) -> str:
    "turns a percent 0.0 - 1.0 into a bar graph"
    percent = max(0.0, min(1.0, percent)) # This function ensures the percentage is within bounds (0.0 to 1.0)
    
    num_hashes = int((percent - 0.0) / (1.0 - 0.0) * (length - 0) + 0) # This calculates the number of '#' symbols
   
    num_spaces = length - num_hashes # This calculates the number of spaces

    return '#' * num_hashes + ' ' * num_spaces # This constructs and returns the bar graph

def get_sys_mem() -> int:
    "return total system memory (used or available) in kB"
    try:
        with open("/proc/meminfo", "r") as meminfo_file: #This code opens the /proc/meminfo file in read only mode and we name the file meminfo_file
            # The below code helps us read the file line by line
            for line in meminfo_file:
                # This checks if the lines contain "MemTotal"
                if "MemTotal" in line:
                    # The below captures the memory value and converts it to an integer and return it
                    total_memory = int(line.split()[1])  # we split the output and the second element,  the memory value is converted to an integer and then is returned as total_memory
                    return total_memory
    except FileNotFoundError: #this is here in case we do not find the meminfo file
        print("Error: /proc/meminfo file not found.")
        return None
    except Exception as e: # this is here in case any other error other than the file not found happens 
        print(f"An error occurred: {e}")
        return None
    
def get_avail_mem() -> int:
    "return total memory that is available"
    try:
        with open("/proc/meminfo", "r") as meminfo_file: #This code opens the /proc/meminfo file in read only mode and we name the file meminfo_file
            # to read the file line by line
            for line in meminfo_file:
                # to check if the line contains "MemAvailable"
                if "MemAvailable" in line:
                    # The below captures the memory value and converts it to an integer and return it
                    available_memory = int(line.split()[1])  # we split the output and the second element,  the memory value is converted to an integer and then is returned as available_memory
                    return available_memory
    except FileNotFoundError: #this is here in case we do not find the meminfo file
        print("Error: /proc/meminfo file not found.")
        return None
    except Exception as e: # this is here in case any other error other than the file not found happens 
        print(f"An error occurred: {e}")
        return None

#------------------------------------------------------------MILESTONE 2----------------------------------------------------------------------
def pids_of_prog(app_name: str) -> list:
    "given an app name, return all pids associated with app"
    ...

def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the resident memory used, zero if not found"
    ...

def bytes_to_human_r(kibibytes: int, decimal_places: int=2) -> str:
    "turn 1,024 into 1 MiB, for example"
    suffixes = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB']  # iB indicates 1024
    suf_count = 0
    result = kibibytes 
    while result > 1024 and suf_count < len(suffixes):
        result /= 1024
        suf_count += 1
    str_result = f'{result:.{decimal_places}f} '
    str_result += suffixes[suf_count]
    return str_result

if __name__ == "__main__":
    args = parse_command_args()
    if not args.program:
        ...
    else:
        ...


    # process args
    # if no parameter passed, 
    # open meminfo.
    # get used memory
    # get total memory
    # call percent to graph
    # print

    # if a parameter passed:
    # get pids from pidof
    # lookup each process id in /proc
    # read memory used
    # add to total used
    # percent to graph
    # take total our of total system memory? or total used memory? total used memory.
    # percent to graph.
