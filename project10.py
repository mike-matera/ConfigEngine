#! /usr/bin/python3 

import os
import re
import cfge
import cfge.commands 

engine = cfge.instance()
score = 0; 

print ("\n---- This is the project 10 grader ----\n")

def do_kernel() : 
    kernel = engine.check_output(["uname", "-r"]).decode().strip()
    print ('Your kernel version is:', kernel);
    parts = kernel.split('-')
    if len(parts) < 3 : 
        print ("ERROR: Your kernel doesn't seem to have an extra version string")

        print ("\tUpstream kernel version:", parts[0]);
        print ("\tBuild number:", parts[1]);
        print ("\tExtra version:", parts[2]);
        print ("");

    if parts[2] == 'generic': 
        print ("ERROR: You do not seem to have customized this kernel.")
        return False
    else :
        print ("SUCCESS: This kernel is customized (+10)")
        return True;

def do_module() :
    print ("\nLooking for scull kernel module.");
    modules = engine.check_output(["lsmod"]).decode()
    found = False
    for line in modules.splitlines(True) :
        parts = line.split(' '); 
        if parts[0] == 'scull' :
            print ("FOUND:", line.strip())
            return True

        print ("ERROR: The scull driver is not loaded.")
        return False

score = 0 
if do_kernel() : 
    score += 10
    if do_module() :
        score += 10

print ("\n\nYour score for is", score, "of 20\n");

print ("Submit the file project10.sub.zip to blackboard for credit.")
print ("You may run this program again after fixing any problems.");

engine.persist("project10.sub")
