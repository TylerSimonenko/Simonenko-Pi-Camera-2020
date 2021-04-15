from picamera import PiCamera
from datetime import datetime
from time import sleep
from subprocess import call

# current time and file time
currentTime = datetime.now()
fileTime = currentTime.strftime('%y.%m.%d-%H.%M.%S')

# create filepath (picture)
picPath = "/mnt/storageDevice/photos/"
picName = fileTime + '.jpg'
picPathFull = picPath + picName

# create filepath (video)
vidPath = "/mnt/storageDevice/videos/"
vidName = fileTime + ".h264"
vidPathFull = vidPath + vidName

# camera setup
camera = PiCamera()

# take 5s video
print('Taking Video...')
camera.resolution = (1080, 720)
camera.start_recording(vidPathFull)
sleep(15)
camera.stop_recording()
print('Video Taken.')

# take picture
print('Taking Picture...')
camera.resolution = (3280, 2464)
camera.start_preview()
sleep(3)
camera.capture(picPathFull)
camera.stop_preview()
print('Picture Taken.')

# Shutdown the system
call('sudo shutdown -h now', shell=True)