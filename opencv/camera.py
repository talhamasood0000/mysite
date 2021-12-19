import cv2
import mediapipe as mp
import time
import urllib.request
import numpy as np
from numpy.core.arrayprint import DatetimeFormat
from datetime import datetime


class LiveWebCam(object):
	def __init__(self, minDetectionCon=0.5):
		# self.url = "http://192.168.2.103:8080/shot.jpg"
		# self.url = "http://10.5.8.153:8080/shot.jpg"
		# self.url=r"C:\Users\Talha Masood\Desktop\video.mp4"
		self.url='./media/test/test.mp4'

		self.cap=cv2.VideoCapture(self.url)

		self.minDetectionCon = minDetectionCon
		self.mpFaceDetection = mp.solutions.face_detection
		self.mpDraw = mp.solutions.drawing_utils
		self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

	def __del__(self):
		cv2.destroyAllWindows()
	
	def findFaces(self, draw=True):
		success, img = self.cap.read()
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.faceDetection.process(imgRGB)
		bboxs = [0]
		c: int = 0
		ext_time=datetime.now()
		ext_time=ext_time.strftime("%I:%M %p")
		cv2.putText(img, f'Time: {ext_time}', (250, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
		if self.results.detections:
			c: int = 0
			for id, detection in enumerate(self.results.detections):
				bboxC = detection.location_data.relative_bounding_box
				ih, iw, ic = img.shape
				bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
        	           int(bboxC.width * iw), int(bboxC.height * ih)
				bboxs.append([id, bbox, detection.score])
				if draw:
					img = self.fancyDraw(img, bbox)
					cv2.putText(img, f'{int(detection.score[0] * 100)}%',
        	                    (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
        	                    2, (255, 0, 255), 2)
					c = c + 1
					cv2.putText(img, f'People: {c}', (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)	

		ret, jpeg = cv2.imencode('.jpg', img)
		return jpeg.tobytes()
		
	def fancyDraw(self, img, bbox, l=30, t=5, rt=1):
		x, y, w, h = bbox
		x1, y1 = x + w, y + h

		cv2.rectangle(img, bbox, (255, 0, 255), rt)
        # Top Left  x,y
		cv2.line(img, (x, y), (x + l, y), (255, 0, 255), t)
		cv2.line(img, (x, y), (x, y + l), (255, 0, 255), t)
        # Top Right  x1,y
		cv2.line(img, (x1, y), (x1 - l, y), (255, 0, 255), t)
		cv2.line(img, (x1, y), (x1, y + l), (255, 0, 255), t)
        # Bottom Left  x,y1
		cv2.line(img, (x, y1), (x + l, y1), (255, 0, 255), t)
		cv2.line(img, (x, y1), (x, y1 - l), (255, 0, 255), t)
        # Bottom Right  x1,y1
		cv2.line(img, (x1, y1), (x1 - l, y1), (255, 0, 255), t)
		cv2.line(img, (x1, y1), (x1, y1 - l), (255, 0, 255), t)
		
		return img

	def time_people(self):

		
		success, img = self.cap.read()
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.faceDetection.process(imgRGB)
		bboxs = []
		ext_time=datetime.now()
		ext_time=ext_time.strftime("%M %S")
		if self.results.detections:
			for id, detection in enumerate(self.results.detections):
				bboxC = detection.location_data.relative_bounding_box
				ih, iw, ic = img.shape
				bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)
				bboxs.append([id, bbox, detection.score])

		return len(bboxs),str(ext_time)