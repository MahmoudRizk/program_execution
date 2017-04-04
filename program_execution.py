import subprocess
from subprocess import PIPE
from threading import Thread
#from queue import Queue, Empty
import time
import os
import threading
import json


class ProcessCaller(threading.Thread):
    def __init__(self,name,args,table):
        threading.Thread.__init__(self)
        self.table = table
        self.name = name
        args = 'nohup ' + args
        self.p = subprocess.Popen(args.split(),stderr=PIPE, stdout=PIPE)
        try:
            self.p.communicate(timeout = 0.01)
        except:
            pass
        if(self.p.poll() != None):
            raise Exception()
        table[self.p.pid] = args.split()[1]

    def run(self):
        print (self.name,":is running.")
        self.p.communicate()
        if(self.p.poll != None):
            del self.table[self.p.pid]
            print(self.name,":is terminated.")

class SystemCaller:
    def __init__(self):
        self.running_processes_table = {}
        with open('cach.json', 'r') as fp:
            try:
                self.alias_table = json.load(fp)
            except:
                self.alias_table = {}

    def open(self,args):
        try:

            if args in self.alias_table:
                args = self.alias_table[args]

            ProcessCaller("p",args,self.running_processes_table).start()
        except(Exception):
            print ("The command you Entered is unknown:'",args,"'.")
            print ("You can define '",args,"' to be used as shortcut for an existing program.")

    def kill(self,pid):
        subprocess.Popen(['kill' ,str(pid)])

    def close(self,args):
        for pid, name in self.running_processes_table.items():
            if name == args:
                subprocess.Popen(['kill' ,str(pid)])
                return

    def print_table(self):
        print(self.running_processes_table)

    def add_to_alias_table(self,shortcut,program_name):
        self.alias_table[shortcut] = program_name
        with open('cach.json', 'w') as fp:
            json.dump(self.alias_table, fp)

#args = 'gedit'
s = SystemCaller()
s.add_to_alias_table('browser','firefox')
s.add_to_alias_table('text_editor','gedit')
s.open('text_editor')
s.print_table()
s.open('vlc')
s.print_table()
s.open('firefox')
s.print_table()

while(True):
    string = input()
    if(string == 'table'):
        s.print_table()
    elif(string.split()[0] == 'kill'):
	    s.kill(string.split()[1])




"""
counter = 1
args=""
while(args != 'exit()'):
    args = input()
    counter = counter + 1
    if(args == 'table'):
        print (table)
    elif(args.split()[0] == 'kill'):
        killer = subprocess.Popen(['kill' , args.split()[1]])
    elif(args.split()[0] == 'threads'):
        p.print_stderr
    else:
        try:
            #args = [args]
            p = ProcessCaller("p"+str(counter),args)
            p.start()
            #threads.append(p)
            p.print_stderr
        except:
            print("Program not found.")

print('closed')
"""
