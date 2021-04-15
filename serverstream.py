# Tyler Simonenko, PiCamera Project 2020
# File for running the setup for the system

# ----------------------------------------------------- #
# Import library for functions later in the script
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
hostName = '192.168.8.125'  # Change this to your Raspberry Pi's IP address or your preferred IP
hostPort = 8080             # Change this to your preferred port, defaults are "8000" or "8080"
# ----------------------------------------------------- #


# ----------------------------------------------------- #
# This is the section that is rendered by the web browser - what the user sees as GUI
# What is still needed:
# If system will take pics, videos, or both (checkbox); How many pics/videos will be taken; Preview changes made
HTML = """
<html>
<head>
<title>PiCamera System</title>
</head>
<body>
<body style="width:960px; margin: 20px auto;">
<h1>Pi System Setup</h1>
<h2>Tyler Simonenko</h2>
<hr/>
<p>Refresh to see if the storage device is connected.</p>
<input type="submit" name="camera_check" value="Refresh">
<p>Edit the deployment schedule below or use UUGear's ScriptGen to create one.</p>
<a href="http://www.uugear.com/app/wittypi-scriptgen/" target="_blank"><b>WittyPi's Script Generator</b></a>
<p>You can simply copy and paste your schedule into this text box if you've created a new schedule.</p>
<textarea rows="8" cols="131">
BEGIN YYYY-mm-DD HH:MM:SS
END   YYYY-mm-DD HH:MM:SS
ON    D_ H_ M_ S_
OFF   D_ H_ M_ S_
</textarea>
<input type="submit" name="set_deploy" value="Update">
<hr/>
<center><h1>Real Time Camera Footage</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""
# ----------------------------------------------------- #


# ----------------------------------------------------- #
# This is what takes care of the streaming on the Pi camera, "StreamingOutput" allows for constant refresh of image?
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)
# ----------------------------------------------------- #


# ----------------------------------------------------- #
# Could be what handles the connection requests between the connecting user and the pi
# This could be the spot where do_POST is used to post information to the server?
class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = HTML.encode('utf-8')  # The "content" that the self.wfile.write command writes
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)       # Tells the webpage to render the HTML file above
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()
# ----------------------------------------------------- #


# ----------------------------------------------------- #
# This section will POST information to the webserver
# Show user if storage is connected, will show errors or successful writes, "are you sure?"
#    def do_POST(self):

# ----------------------------------------------------- #


# ----------------------------------------------------- #
# This is the actual class setup for the usage of "PiServer" -
# which is simply the name of the server, but it uses the parameters set forth within the parenthesis (imports)
class PiServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
# ----------------------------------------------------- #


# ----------------------------------------------------- #
# From what I can tell, this is required to run the webserver - sets up the camera, binds the ports, etc.
print("Server Starts - %s:%s" % (hostName, hostPort))
with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = (hostName, hostPort)
        server = PiServer(address, StreamingHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        camera.stop_recording()
        server.server_close()
# ----------------------------------------------------- #
