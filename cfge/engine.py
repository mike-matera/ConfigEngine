import os
import tempfile
import shutil
import atexit 
import sqlite3
import subprocess

# make temporary
# workdir = tempfile.mkdtemp()
workdir = '.'

# initialize db
db = sqlite3.connect(workdir + '/resources.db')
c = db.cursor()
c.execute('''create table files (path text, data blob)''')
c.execute('''create table commands (cmdline text, data blob)''')

def check_output(cmd) :
    cmdstring = ' '.join(cmd)
    output = subprocess.check_output(cmd)
    c = db.cursor()
    c.execute('''insert into commands values (?, ?)''', [cmdstring, output])
    db.commit()
    return output

def readfile(name) : 
    name = os.path.abspath(name)
    f = open (name, 'r') 
    data = f.read()
    c.execute('''insert into files values (?, ?)''', [name, data])    
    f.close()
    return data


@atexit.register
def cleanup() :
    c = db.cursor()
    db.close()
    #shutil.rmtree(workdir)
