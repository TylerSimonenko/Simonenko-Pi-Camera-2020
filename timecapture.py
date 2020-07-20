from picamera import PiCamera
from datetime import datetime
from time import sleep

# take current time
currentTime = datetime.now()

# filepath of the pictures
filePath = '/home/pi/photos/'
picTime = currentTime.strftime('%m.%d-%H.%M.%S')
picName = picTime + '.jpg'
filePathFull = filePath + picName

# setup camera
camera = PiCamera()

# take the picture
camera.resolution = (3280, 2464)
camera.start_preview()
sleep(3)
camera.capture(filePathFull)
camera.stop_preview()
print('Picture taken')
