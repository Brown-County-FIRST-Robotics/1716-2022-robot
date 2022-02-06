from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)



camera = cv2.VideoCapture(0)
# for local webcam use cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        cv2.waitKey(125)
        success, frame = camera.read()  # read the camera frame
        resizedframe = cv2.resize(frame,(640,360),fx=0,fy=0)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', resizedframe)
            resizedframe = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + resizedframe + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

