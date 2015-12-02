import os
import sys
import tempfile
import shutil
import atexit 
import sqlite3
import subprocess

class RealSystem :
    def __init__(self, wd) :
        # initialize db

        # make temporary
        self.workdir = wd

        # copy infrastructure
        pkgdir = os.path.abspath(__package__)
        shutil.copytree(pkgdir, self.workdir + "/cfge", ignore=shutil.ignore_patterns('__pycache__'))

        mainscript = os.path.abspath(sys.argv[0])
        shutil.copy(mainscript, self.workdir + "/__main__.py")

        self.dbpath = self.workdir + '/cfge/resources.db'
        self.db = sqlite3.connect(self.dbpath)
        c = self.db.cursor()
        c.execute('''create table meta (key text, value text)''')
        c.execute('''create table blobs (id integer primary key, ref text, data blob, flags integer)''')
        self.db.commit()

    def __del__(self) :
        self.db.close()

    def readfile(self, path) :
        f = open(path, 'r') 
        data = f.read()
        f.close()
        set_blob(path, data)
        return data
        
    def check_output(self, cmd) :
        cmdstring = ' '.join(cmd)
        output = subprocess.check_output(cmd)
        self.set_blob(cmdstring, output)
        return output
        
    def geteuid(self) : 
        euid = os.geteuid()
        self.set_meta('euid', euid)
        return euid

    def persist(self, filename) :    
        shutil.make_archive(filename, 'zip', self.workdir)
        
    def set_blob(self, ref, data, flags=0) :
        c = self.db.cursor()
        c.execute('''insert into blobs values (NULL, ?, ?, ?)''', [ref, data, flags])
        self.db.commit()

    def set_meta(self, key, value) :
        c = self.db.cursor()
        c.execute('''insert into meta values (?, ?)''', [key, value])
        self.db.commit()

