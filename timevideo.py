from picamera import PiCamera
from datetime import datetime
from time import sleep

# take current time
currentTime = datetime.now()

# filepath of the pictures
filePath = '/home/pi/videos/'
vidTime = currentTime.strftime('%m.%d-%H.%M.%S')
vidName = vidTime + '.h264'
filePathFull = filePath + vidName

# setup camera
camera = PiCamera()

# take 10s video
camera.resolution = (1280, 720)
camera.start_preview()
camera.start_recording(filePathFull)
sleep(10)
camera.stop_recording()
camera.stop_preview()
print('Video taken')
