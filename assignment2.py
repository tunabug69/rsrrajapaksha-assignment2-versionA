#!/usr/bin/env python3

'''
OPS445 Assignment 2
Program: assignment2.py 
Author: "Ranmunige Senitha Ransen Rajapaksha"
Semester: "Fall 2024"

The python code in this file is original work written by
"Ramunige Senitha Ransen Rajapaksha". No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This script visualizes memory usage for system processes. It supports displaying the total system memory usage, 
individual process memory usage, and offers the ability to display this information in a human-readable format.

'''

import argparse
import os, sys

def parse_command_args() -> object:
    "The function will return an object (argparse.Namespace).It is designed to parse command-line arguments when called in the main function."

    parser = argparse.ArgumentParser(description="Memory Visualiser -- See Memory Usage Report with bar charts", epilog="Copyright 2023")
    # This creates an ArgumentParser object named `parser` and `description`: Describes the purpose of the script, displayed when the user runs `python script_name.py -h`.
    # `epilog`: is the piece of text displayed at the end of the help message.
    
    parser.add_argument("-H", "--human-readable", action="store_true", help="Display memory usage in a human-readable format.")
    # This adds the argument for `-H` and `--human-readable`. `action="store_true"` means if `-H` is provided, the value of `args.human_readable` will be `True`; otherwise, it will be `False`.
    # `help`: A short description that will be shown in the help message when `-h` is typed.

    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # This adds the argument for `-l` and `--length`. `type=int`: Specifies that the argument expects an integer value. `default=20`: If the user doesn't provide a value for `-l`, the default value of `20` will be used.
    # `help`: This shows a description of what the argument does.

    parser.add_argument("program", type=str, nargs='?', help="If a program is specified, show memory use of all associated processes. Show only total use if not.")
    # This adds the positional argument `program` and `nargs='?'`: means the argument is optional, and if not provided, it will be `None`. `type=str`: Specifies that the argument expects a string (the program name).
    # `help`: Describes what this argument does.

    args = parser.parse_args() # Calls `parse_args()` to parse the command-line arguments provided by the user.
    # It returns an object containing the parsed arguments which is stored as attributes.

    return args # returns the `args` object, which contains the parsed command-line arguments.


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
    " This function takes an app name (a string) as input and returns a list of process IDs (PIDs) associated with the given app name."

    try:
        pid_output = os.popen(f"pidof {app_name}").read().strip() #The `os.popen()` function is used to run the shell command `pidof {app_name}` and capture the output.
        # `pidof {app_name}` returns the PIDs of the running processes that match the provided app name.`.read()` reads the command's output, and `.strip()` removes any leading or trailing whitespace and including newlines.
        
        if pid_output: # what this does is if `pid_output` is not empty ,split the output by spaces into a list of PIDs.
            pid_list = pid_output.split()
        else:
            pid_list = []  # what this does is if the output is empty then it returns an empty list.
        
    except Exception as e:
        # This block handles any exceptions that might occur when executing the command.
        print(f"Error while fetching PIDs for {app_name}: {e}")
        # Print the error message if an exception occurs, including the exception message.
        pid_list = []  # Return an empty list if an error occurs.

    return pid_list
    # Return the list of PIDs found for the app or an empty list if no PIDs were found or if an error occurred.


def rss_mem_of_pid(proc_id: str) -> int:
    "given a process id, return the resident memory used, zero if not found"
    rss = 0 # This sets the `rss` to 0. This variable will store the Resident Set Size memory usage for the process.

    try:
        # Open the smaps file for the given process ID
        with open(f'/proc/{proc_id}/smaps', 'r') as f:
            # Iterate through each line in the file
            for line in f:
                # Look for the line starting with "Rss" which contains the RSS memory info
                if line.startswith('Rss'):
                    # Extract the RSS value in kilobytes from the line
                    rss += int(line.split()[1])  # Splits value of the second item, which is in kilobytes
    except Exception as e: # this handles all errors and prints an error message
        print(f"Error while fetching RSS memory for PID {proc_id}: {e}")
    
    return rss



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

    args = parse_command_args() # Call the `parse_command_args()` function to parse the command-line arguments passed to the script

    # Total System Memory Section 
    total_memory = get_sys_mem()  # Fetch the total system memory
    available_memory = get_avail_mem()  # Fetch the available system memory

    if total_memory is None or available_memory is None:
        sys.exit(1)  # Exit the program if fetching memory info failed.

    used_memory = total_memory - available_memory  # This is to calculate used memory
    mem_percent = (used_memory / total_memory) * 100  # This is to calculate the percentage of memory used

    # Display memory usage as a graph
    print(f"Total Memory: {total_memory} kB")
    print(f"Used Memory: {used_memory} kB")
    print(f"Available Memory: {available_memory} kB")

    # Graphically display memory usage
    print(f"Memory Usage: {percent_to_graph(mem_percent, args.length)}")
    print(f"Memory Usage Percentage: {mem_percent:.2f}%")

    # ---- Program-Specific Memory Section ----
    if args.program:  # If a program name is provided
        program_name = args.program
        print(f"\nMemory usage for processes related to {program_name}:")
        pids = pids_of_prog(program_name)  # Get all PIDs for the program

        if pids:
            total_prog_mem = 0  # To store the total memory used by all processes of the program
            for pid in pids:
                total_prog_mem += rss_mem_of_pid(pid)  # Add RSS memory of each PID
            
            print(f"Total Memory Used by {program_name}: {total_prog_mem} kB")
            
            if args.human_readable: # This prints the total memory in a human readable format
                print(f"Total Memory Used by {program_name} (Human Readable): {bytes_to_human_r(total_prog_mem)}")
        else:
            print(f"No running processes found for {program_name}.")

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
