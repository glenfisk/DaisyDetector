import os.path
from time import time, sleep
from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime

class DaisyDetector():
	def __init__(self):
		self.recording=False
		self.motionStopped=None
		self.camera=None
		self.pir = self.GetMotionSensor()
		self.pir.when_no_motion = self.MotionStopped
		self.pir.when_motion = self.MotionStarted

	def MotionStarted(self):
		self.motionStopped = None
		if not self.recording:
			self.StartRecording()

	def MotionStopped(self):
		self.motionStopped = time()

	def GetMotionSensor(self):
		pir = MotionSensor(4)
		pir.when_motion = self.MotionStarted
		pir.when_no_motion = self.MotionStopped
		return pir

	def GetFilename(self):
		folder='/media/pi/8CD4-B1FF/'
		filename = "daisy{0:%Y}{0:%m}{0:%d}-{0:%H}{0:%M}{0:%s}.h264".format(datetime.now())
		target=os.path.join(folder, filename)
		return target

	def GetCamera(self):
		camera = PiCamera()
		camera.iso = 800 #400/800 for low-light 100/200 for normal daylight
		camera.rotation = 180
		camera.resolution = (1024, 768)
		return camera

	def StartRecording(self):
		if self.recording:
			return
		target=self.GetFilename()
		print (target)
		self.camera=self.GetCamera()
		sleep(2) # camera warmup
		self.camera.start_recording(target)
		self.camera.wait_recording(2) #use instead of sleep
		self.recording=True

	def StopRecording(self):
		self.motionStopped=None
		self.recording=False
		self.camera.stop_recording()
		self.camera.close()

	def Detect(self):
		while True:
			if self.recording:
				if self.motionStopped is None:
					continue
				else:
					if time() - self.motionStopped > 10:
						self.StopRecording()
			sleep(.02) #allow time for CPU to fire events

dd = DaisyDetector()
dd.Detect()
