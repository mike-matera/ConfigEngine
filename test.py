#! /usr/bin/python3

import cfge
import cfge.commands
import pkgutil
import sys

#print ('Loading pkgwithdata from', cfge.__file__)
#print (pkgutil.get_data('cfge', 'resources.db'))

foo = cfge.commands.ps()
foo = cfge.commands.ps()

cfge.persist()
