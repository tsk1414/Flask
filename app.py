# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 5000

from imutils.video import VideoStream
from flask import Flask, Response, render_template, request, url_for
import threading
import datetime
import imutils
import time
import cv2
#newwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
import os


# Let's keep a global outputFrame around,
# a bool flag to know when we are recording,
# and a lock so we are threadsafe multiple connected clients.
outputFrame = None
isRecording = False
lock = threading.Lock()

# Flask up
app = Flask(__name__)

# Init the connection to the camera with a video stream,
# and let camera warmup for 2sec.
vs = VideoStream(src=0).start()
time.sleep(2.0)
  
def face_detect():

	# Local dir for cascades: 
	# C:\\Users\\Craig\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\cv2\\data\\
	fCascPath = "C:\\Users\\XXXXX\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(fCascPath)

	eCascPath = "C:\\Users\\XXXXX\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\cv2\\data\\haarcascade_eye.xml"
	eyeCascade = cv2.CascadeClassifier(eCascPath)

	mCascPath = "C:\\Users\\XXXXX\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\cv2\\data\\haarcascade_smile.xml"
	mouthCascade = cv2.CascadeClassifier(mCascPath)
	
	# Grab global references to the video stream, output frame, and lock variables.
	global vs, outputFrame, lock

	# Loop over camera frames indefinitely.
	while True:

		# Get a frame from the videostream, resize it,
		# convert the frame to grayscale, and blur it.
		frame = vs.read()
		frame = imutils.resize(frame, width=900)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (7, 7), 0)

		# Draw timestamp on the frame
		timestamp = datetime.datetime.now()
		cv2.putText(frame, timestamp.strftime(
			"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		# Get a list of faces outputVid of the image
		faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors = 5,
        minSize = (30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

		# Draw a bounding box around each face found.
		for(x,y,w,h) in faces:
			frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)

			# The regions of interest are kept for both gray and color images:
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = frame[y:y+h, x:x+w]

			# grey roi is used to more efficiently find mouths and eyes
			# (we know those features are only located on a face, 
			# so we only look there),
			mouth = mouthCascade.detectMultiScale(roi_gray)
			eyes = eyeCascade.detectMultiScale(roi_gray)

			# color roi is used to draw bounding boxes around found features.
			for (mx,my,mw,mh) in mouth:
				cv2.rectangle(roi_color, (mx,my), (mx+mw,my+mh), (0,255,0),2)
			for (ex,ey,ew,eh) in eyes:
				cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,255,0),2)

		# Take the lock, set the output frame, and release the
		# lock
		with lock:
			outputFrame = frame.copy()

def no_detect():
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock

	# loop over frames from the video stream
	while True:

		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame = vs.read()
		frame = imutils.resize(frame, width=900)

		# grab the current timestamp and draw it on the frame
		timestamp = datetime.datetime.now()
		cv2.putText(frame, timestamp.strftime(
			"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		# acquire the lock, set the output frame, and release the
		# lock
		with lock:
			outputFrame = frame.copy()
		
# Route decorators are used to trigger functions when certain URLs are visited.
# In this case, '/' calls for the index.html to be built and returned.
@app.route("/")
def index():
	return render_template("index.html")

def getLastModFileName(dest):
    if (dest == "img"):
        folder = "C:\\Users\\XXXXX\\Desktop\\project\\static\\images"
    else:
        folder = "C:\\Users\\XXXXX\\Desktop\\project\\static\\videos"
    os.chdir(folder)
    if len(os.listdir(folder) ) == 0:
        return 1
    else:
        files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
        newest = files[-1]
        newest = newest.split('_')
        newest = newest[1].split('.')
        num = int(newest[0])
        num = num + 1
        return (num)
@app.route("/snapshot_button")
def snapshot():
	
	# The filename, when written, should contain an absolute path to the saved file.
	# A unique filename is generated using time.
	imageFolder = "C:\\Users\\XXXXX\\Desktop\\project\\static\\images"
	index = getLastModFileName("img")

	# Save the current frame as the filename in the image folder.
	cv2.imwrite(filename, outputFrame)
	# These button-tied functions will fail if they don't return OR return a None type...
	return 'none'

@app.route("/start_record")
def vidcapture():

	# Set a path and filename for video
	videoFolder = "C:\\Users\\XXXXX\\Desktop\\project\\static\\videos"
	index = getLastModFileName("vid")
	filename = videoFolder + "\\vid_" + str(index) + ".avi"

	global outputVid
	global isRecording
	outputVid = cv2.VideoWriter(filename,cv2.VideoWriter_fourcc('M','J','P','G'), 30, (900,675))
	isRecording = True
	return 'none'

@app.route("/stop_record")
def stoprecord():
	global outputVid
	global isRecording
	isRecording = False

	# Using outputVid.release() causes a seg fault here sometimes when closing the videowriter,
	# del seems to do better
	del outputVid
	return 'none'

def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock

	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue

			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

			# check the state of the bool tied to record button,
			# and write frame to output video
			if isRecording == True:
				outputVid.write(outputFrame)

			# ensure the frame was successfully encoded
			if not flag:
				continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':

	# start a thread that will perform motion detection
	t = threading.Thread(target=no_detect, args=())
	t.daemon = True
	t.start()
	
	# start the flask app
	app.run(host='localhost', port=5000, debug=True,
		threaded=True, use_reloader=False)

# release the video stream
vs.stop()