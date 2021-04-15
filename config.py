# ----------------------------------------------------- #
# Tyler Simonenko, Autonomous Pi Camera System
# Config file for download and integration onto system
# ----------------------------------------------------- #

import os
from subprocess import call

# To set begin/end dates and times - This will tell the system when to start and stop recording data
my_file = open('/home/wittypi/schedule.wpi', 'w')
my_file.write('BEGIN 2021-03-22 18:30:00\n')  # Input deployment START date/time in the form: YYYY-mm-DD HH:MM:SS
my_file.write('END   2021-03-22 16:30:00\n')  # Input deployment END date/time in the form: YYYY-mm-DD HH:MM:SS

# To set on/off period lengths - This will tell the system how long to stay ON and how long to stay OFF
my_file.write('ON    M2\n')                   # Input ON state duration in the form: D H M S
my_file.write('OFF   M58')                     # Input OFF state duration in the form: D H M S

# Completes write onto schedule.wpi
my_file = open('/home/wittypi/schedule.wpi')

# Run command to set schedule within WittyPi Mini
call('bash /home/wittypi/runScript.sh', shell=True)
print('Schedule has been set.')  # (this can be removed later on)

# Create "photos" and "videos" directories on USB stick
storagePath = '/mnt/storageDevice/'
photoDir = os.path.join(storagePath, "photos")
videoDir = os.path.join(storagePath, "videos")
if not os.path.exists(photoDir):
    call('sudo mkdir ' + storagePath + 'photos', shell=True)
if not os.path.exists(videoDir):
    call('sudo mkdir ' + storagePath + 'videos', shell=True)
print('The directories "photos" and "videos" have been added to the Storage Device.')

# Create image/video script in "afterStartup.sh" and SD card
# newPath = '/home/pi/'
