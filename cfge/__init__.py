import os
import sys
import tempfile
import shutil
import atexit 
import sqlite3
import subprocess
    
def __db_init() :
    # initialize db
    global db 
    global check_output
    global readfile 
    global workdir
    global dbpath 
    global ref_num

    # make temporary
    workdir = tempfile.mkdtemp()

    # copy infrastructure
    pkgdir = os.path.abspath(__package__)
    shutil.copytree(pkgdir, workdir + "/cfge", ignore=shutil.ignore_patterns('__pycache__'))
    mainscript = os.path.abspath(sys.argv[0])
    shutil.copy(mainscript, workdir + "/__main__.py")

    dbpath = workdir + '/cfge/resources.db'
    do_create = not os.path.isfile(dbpath)
    db = sqlite3.connect(dbpath)
    if do_create :
        print("no resources, do it live!")
        c = db.cursor()
        c.execute('''create table blobs (id integer primary key, ref text, data blob)''')
        db.commit()
        check_output = __live_check_output
        readfile = __live_readfile
    else :
        print("using db")
        check_output = __db_check_output 
        readfile = __db_readfile 
        ref_num = 1

@atexit.register    
def cleanup() :
    global db
    db.close()
    shutil.rmtree(workdir)

def __live_readfile(path) :
    f = open(path, 'r') 
    data = f.read()
    c = db.cursor()
    c.execute('''insert into blobs values (NULL, ?, ?)''', [path, data])    
    db.commit()
    f.close()
    return data

def __live_check_output(cmd) :
    cmdstring = ' '.join(cmd)
    output = subprocess.check_output(cmd)
    c = db.cursor()
    c.execute('''insert into blobs values (NULL, ?, ?)''', [cmdstring, output])
    db.commit()
    return output
    
def __db_readfile(path) :
    global ref_num
    c = db.cursor()
    c.execute('''select data from blobs where id == ? and ref  == ?''', \
              [ref_num, path])
    ref_num = ref_num + 1
    row = c.fetchone()
    return row[0]

def __db_check_output(cmd) :
    global ref_num
    cmdstring = ' '.join(cmd);
    c = db.cursor()
    c.execute('''select data from blobs where id==? and ref==?''', \
              [ref_num, cmdstring])
    ref_num = ref_num + 1
    row = c.fetchone()
    return row[0]
    
def persist() :    
    print ("persist!")
    shutil.make_archive('test', 'zip', workdir)

__db_init()
