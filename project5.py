#! /usr/bin/python3 

import os
import re
import cfge
import cfge.commands 

engine = cfge.instance()

if engine.geteuid() != 0 :
    print ("You must run this as root!")
    exit (1)

lvm = cfge.commands.lvmstat()
mounts = cfge.commands.mounts()

#lvs = lvscan()
#vgs = vgscan()
#mnts = getmounts()

# look for snapshot 
snapvolume = ""
for uuid, lv in lvm['lvs'].items() :
    if lv['origin'] != '' :
        snapvolume = uuid
        break

if snapvolume == "" :
    print ("No snapshot found!")
    exit (1)

print ("snapshot found, device:", lvm['lvs'][snapvolume]['mountpath'])

# Make sure there are no free extents in the volume group
free = int(lvm['lvs'][snapvolume]['free'])
if free == 0 : 
    print ("there are no free extents in volume group", lvm['lvs'][snapvolume]['vg'], "(good)")
elif free < 10 : 
    print ("there are some extents in volume group", lvm['lvs'][snapvolume]['vg'], "(warning)")
else :
    print ("there too many free extents in volume group", lvm['lvs'][snapvolume]['vg'], "(error)")
    
# find where snapshot is mounted
if lvm['lvs'][snapvolume]['mountpath'] not in mounts['by_device'] : 
   print ("Your snapshot is not mounted") 
   exit (2)

print ("snapshot is mounted on", mounts['by_device'][lvm['lvs'][snapvolume]['mountpath']])


engine.persist("project5.sub")
