#! /usr/bin/python3 

import subprocess
import tempfile
import random
import sys
import os 
import time 
import cfge 

def get_procs() :
    ps = {}
    pso = cfge.instance().check_output(["ps", "-elfy"]).splitlines(True)    
    headers = pso[0].split()
    for line in pso[1:] :
        row = line.split()
        pid = row[2].decode()
        ps[pid] = {}
        num = 0
        for num in range(0, 14, 1) :
            ps[pid][headers[num].decode()] = row[num].decode();
    return ps

def find_max_field(name) :
    procs = get_procs()
    pmax = procs['1']
    for pid, proc in procs.items() : 
        if name=='PID' or name=='PPID' or name=='C' \
           or name=='PRI' or name =='NI' or name=='RSS' or name=='SZ' :
            if int(proc[name]) > int(pmax[name]) :
                pmax = proc
        elif name=='TIME' or name=='STIME' :
            # fixme: this probably doesn't alwyas work...
            if proc[name] > pmax[name] :
                pmax = proc            
        else :
            if proc[name] > pmax[name] :
                pmax = proc
    return pmax


engine = cfge.instance()
score = 0

# memory usage
print ("\n1) What is the PID of the process occupying the most memory?")
got = engine.input()
rmax = find_max_field('RSS')
if got == rmax['PID'] :
    print ("Correct! (+5)")
    score += 5
else :
    debug = get_procs()
    print ("You guessed PID", got) 
    if got not in debug : 
        print ("That doesn't seem to be a valid PID anymore.")
    else :
        print ("That process has", debug[got]['RSS'], "k bytes in memory, it's not the most");

# runtime
correct = False
print ("\n2) What process has accumulated the longest runtime?")
got = engine.input()
rmax = find_max_field('TIME')
if got == rmax['PID'] :
    print ("Correct! (+5)")
    score += 5
else :
    debug = get_procs()
    print ("You guessed PID", got) 
    if got not in debug : 
        print ("That doesn't seem to be a valid PID anymore.")
    else :
        print ("That process has run for", debug[got]['TIME']);
    

files = []
for n in range(0, random.randint(1,10)) :
    files.append(tempfile.TemporaryFile())

proc = engine.getpid()
fdpath = '/proc/' + str(proc) + '/fd'
fds = engine.listdir(fdpath)
print (fds)

# get the # of fds
print ("\n3) How many files does this python script have open?")
got = engine.input()
if int(got) == len(fds)-1 : 
    print ("Correct! (+5)")
    score += 5
else :
    print ("That's not correct.")

# stderr
print ("\n4) What is STDERR for this python script?")
got = engine.input()
if got == engine.readlink(fdpath + '/' + fds[2]) :
    print ("Correct! (+5)")
    score += 5
else :
    print ("That's not correct.")

print ("\n\nYou scored", score, "of 20 on the process challenge.")

t = int(time.time())
b0 = t & 0xff
b1 = t & 0xff00 >> 8
b2 = t & 0xff0000 >> 16
b3 = t & 0xff000000 >> 24
c = (b1 << 24) | (b2 << 16) | (b3 << 8) | (score & 0xff)
c = c ^ 0xaa995566

print ("Your confirmation number is", c)

engine.persist('project7')
