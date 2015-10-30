import os
import tempfile
import shutil
import atexit 
import sqlite3
import subprocess

class System : 
    """Class that enompasses live and recored transcripts"""

    def __init__(self) :

        # make temporary
        # self.workdir = tempfile.mkdtemp()
        self.workdir = '.'
        self.dbpath = self.workdir + '/resources.db'

        # initialize db
        do_create = not os.path.isfile(self.dbpath)
        self.db = sqlite3.connect(self.workdir + '/resources.db')
        if do_create :
            print("no resources, do it live!")
            c = self.db.cursor()
            c.execute('''create table blobs (id integer primary key, ref text, data blob)''')
            self.db.commit()
            self.check_output = self.live_check_output
            self.readfile = self.live_readfile
        else :
            print("using db")
            self.check_output = self.db_check_output 
            self.readfile = self.db_readfile 
            self.ref_num = 1

    
    def __del__(self) :
        self.db.close()
        #shutil.rmtree(self.workdir)

    def live_readfile(self, path) :
        f = open(path, 'r') 
        data = f.read()
        c = self.db.cursor()
        c.execute('''insert into blobs values (NULL, ?, ?)''', [path, data])    
        self.db.commit()
        f.close()
        return data

    def live_check_output(self, cmd) :
        cmdstring = ' '.join(cmd)
        output = subprocess.check_output(cmd)
        c = self.db.cursor()
        c.execute('''insert into blobs values (NULL, ?, ?)''', [cmdstring, output])
        self.db.commit()
        return output

    def db_readfile(self, path) :
        c = self.db.cursor()
        c.execute('''select data from blobs where id == ? and ref  == ?''', \
                  [self.ref_num, path])
        self.ref_num = self.ref_num + 1
        row = c.fetchone()
        return row[0]

    def db_check_output(self, cmd) :
        cmdstring = ' '.join(cmd);
        c = self.db.cursor()
        c.execute('''select data from blobs where id==? and ref==?''', \
                  [self.ref_num, cmdstring])
        self.ref_num = self.ref_num + 1
        row = c.fetchone()
        return row[0]
    
