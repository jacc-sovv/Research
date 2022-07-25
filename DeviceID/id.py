import subprocess
import os
import uuid

def get_id():
    if 'nt' in os.name:
        print("Hey)")
        id = str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()
        print((id))
        return id
    else:

        id = subprocess.Popen('hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid'.split())
        print(id)
        return id

get_id()