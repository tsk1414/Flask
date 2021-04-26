Thermal Camera Based Real Time Automated UAV Detection

This application uses Flask to render a HTML page for users to observe a drone's view as it detects other UAVs. Our team trained a Machine Learning Algorithm with a large collection of thermal pictures of drones. The web pages offers functions such as saving an image from the command drone's camera, saving a video clip from the drone's camera, and ability to view said images and videos.




Required dependencies: Flask, NumPy, OpenCV, Imutils
How to download the dependencies: All dependencies can be installed via the command line using the pip command.
	
	pip install (flask | numpy | opencv-python | imutils)
	
Flask: Utilized for its easy integration into HTML webpages, more specifically, we used the flask library to integrate the video feed into the frontend webpage.

OpenCV, NumPy, Imutils: These three libraries were used in conjunction for a variety of tasks: Creating video feed to send to frontend, recording the video being retrieved from the drone, taking snapshots of the video feed, reshaping and manipulating image and video sizes. 

Integrating Flask into Frontend
Flask operates by declaring an API of server-side ‘routes’ that clients can visit to activate functions.

For example, when visiting the ‘/’ route, you’re activating a function that returns the home-page. Similarly, we created API routes to allow functions to be activated that save photos or videos, query what .jpg or .mp4 files exist on the server, and return the video streamed by the camera.

If one were to open the .html files alone, without running the Flask app, they would be devoid of content. Flask dynamically populates html files at runtime which allows Python variables to be injected into Javascript seamlessly.

How to Utilize the Front-End Webpage
The live-stream is located on the left-hand side of the webpage. Live-stream video requires no user input and will show video as soon as web page is opened.

Image capture is available on the right-hand side with a “camera” icon. To capture image of live-stream, click the “camera” icon. A message will appear “SNAPSHOT TAKEN” in green text color. The photo will be saved locally inside the drone’s on-board computer.

Video capture is available on the right-hand side of the webpage with a “record” icon. To start recording the live-stream, click the “record’ icon. A message will appear “BEGIN RECORDING” in green text color.To stop recording, click the “record” icon. A message will appear “END RECORDING” in green text color.

How to Save Videos and Images
To save pictures, function “snapshot()” is required. In “app.py”, “snapshot()” will open “images” folder under the directory “static”. Import library “cv2”, use method “imwrite(filename, outputFrame) to save images remotely. 

To call function “snapshot()” from front-end, JQuery is required. Use JQuery method “getJSON” to call function “snapshot()” in app.py. Clicking the snapshot button will call the snapshot() function inside “app.py”.

To save video recordings, function “startRecord()” and ‘stopRecord()” is required. In “app.py”, “vidcapture()” will open “videos” folder under the directory “static”. Import library “cv2”, use method “VideoWriter(filename,cv2.VideoWriter_fourcc('M','J','P','G'), 30, (900,675)) to save videos remotely. 

To call function “vidcapture()” from front-end, JQuery is required. Use JQuery method “getJSON” to call function “vidcapture()” in app.py. Clicking the record button will call the snapshot() function inside “app.py”. Clicking the record button again, will let the application know when to stop saving recording.


How to Fetch Images
All images are saved locally inside the drone’s computer under directory “images” inside directory “static”. Use a function to access the “static/images/” directory and call images individually into a table. To access videos, user must have direct access to drone’s computer and all record videos will be found in “static/videos/” directory.
