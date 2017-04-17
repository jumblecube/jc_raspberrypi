#Car Camera 
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.resolution = (640, 480)
camera.framerate = 15
camera.rotation = 180
camera.brightness = 60
camera.contrast = 60
camera.awb_mode = 'off'
camera.awb_gains = [1.2, 1.8]
camera.start_preview()
sleep(2)
camera.capture('/home/pi/Documents/jumblecube_repo/jc_car/CameraImage/Image1.jpg')
camera.stop_preview()
