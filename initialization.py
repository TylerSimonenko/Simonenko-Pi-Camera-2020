# ----------------------------------------------------- #
# Tyler Simonenko, Autonomous Pi Camera System
# Initialization file for mounting and running config file
# ----------------------------------------------------- #

from subprocess import call

# Check for proper mount
import os.path
path = '/mnt/storageDevice'
ismount = os.path.ismount(path)
print('The drive is mounted properly: ' + str(ismount))
print('Searching for config file...')

# Find config file
if ismount:
    import os
    for root, dirs, files in os.walk("/mnt/storageDevice/"):
        for name in files:
            if name == 'config.py':
                print('Config file recognized...')
                filePath = (os.path.join(root, name))
                print('Running config file...')
                call('python ' + filePath, shell=True)