import os
import shutil
import atexit 
import tempfile 
import cfge.sys_wrapper
import cfge.db_wrapper 


# Create a temp directory 
__workdir = tempfile.mkdtemp()

@atexit.register
def __cleanup() :
    shutil.rmtree(__workdir)

def instance() :
    global __instance
    if not '__instance' in globals() :
        try :
            dbdata = __loader__.get_data(os.path.join('cfge','resources.db'))
            __instance = db_wrapper.DBSystem(__workdir)
        except FileNotFoundError :
            __instance = sys_wrapper.RealSystem(__workdir)
    return __instance
