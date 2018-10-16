import os.path
from time import time, sleep
from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime

recording=False
motionStopped=None
camera=None

def MotionStarted():
	global recording
	global motionStopped
	motionStopped = None
	if not recording:
		StartRecording()

def MotionStopped():
	global motionStopped
	motionStopped = time()

def GetMotionSensor():
	pir = MotionSensor(4)
	pir.when_motion = MotionStarted
	pir.when_no_motion = MotionStopped
	return pir

def GetFilename():
	folder='/media/pi/8CD4-B1FF/'
	filename = "daisy{0:%Y}{0:%m}{0:%d}-{0:%H}{0:%M}{0:%s}.h264".format(datetime.now())
	target=os.path.join(folder, filename)
	return target

def GetCamera():
	global camera
	camera = PiCamera()
	camera.iso = 800 #400/800 for low-light 100/200 for normal daylight
	camera.rotation = 180
	camera.resolution = (1024, 768)
	return camera

def StartRecording():
	global recording
	global camera
	if recording:
		return
	target=GetFilename()
	print (target)
	camera=GetCamera()
	sleep(2) # camera warmup
	camera.start_recording(target)
	camera.wait_recording(2) #use instead of sleep
	recording=True

def StopRecording():
	global camera, motionStopped, recording
	motionStopped=None
	recording=False
	camera.stop_recording()
	camera.close()

pir = GetMotionSensor()
pir.when_no_motion = MotionStopped
pir.when_motion = MotionStarted

while True:
	if recording:
		if motionStopped is None:
			continue
		else:
			if time() - motionStopped > 10:
				StopRecording()
	sleep(.02) #allow time for CPU to fire events

