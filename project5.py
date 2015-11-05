import re
import cfge
import cfge.commands 

def xxvgscan() :
    vgs = subprocess.check_output(["vgs", "-a", "-o", "name,uuid,vg_extent_count,vg_free_count"]).splitlines(True)
    headers = ['name', 'uuid', 'extents', 'free']
    cfg = {}
    for line in vgs[1:] :
        row = line.split();
        name = row[0].decode()
        cfg[name] = {}
        for num, field in enumerate(row[1:]) :
            cfg[name][headers[num+1]] = field.decode()
    return cfg

def xxlvscan() :
#    lvs = subprocess.check_output(["lvs", "-a", "-o", "uuid,lv_name,vg_name,path,attr,lv_size,origin"]).splitlines(True)
    lvs = config_engine.check_output(["lvs", "-a", "-o", "uuid,lv_name,vg_name,path,attr,lv_size,origin"]).splitlines(True)
    headers = ['uuid', 'name', 'vg', 'path', 'attr', 'size', 'origin']
    cfg = {}
    for line in lvs[1:] :
        row = line.split();
        uuid = row[0].decode()
        cfg[uuid] = {}
        for num, field in enumerate(row[1:]) :
            cfg[uuid][headers[num+1]] = field.decode()
        cfg[uuid]['mountpath'] = "/dev/mapper/" \
                                + re.sub('-', '--', cfg[uuid]['vg']) \
                                + "-" + re.sub('-', '--', cfg[uuid]['name'])
    return cfg

def xxgetmounts() : 
    out = subprocess.check_output(["mount"])
    mnt = {}
    mnt['fwd'] = {}
    mnt['rev'] = {}
    for line in out.splitlines(True) : 
        s = line.split()
        mnt['fwd'][s[0].decode()] = s[2].decode()
        mnt['rev'][s[2].decode()] = s[0].decode()
    return mnt;

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

