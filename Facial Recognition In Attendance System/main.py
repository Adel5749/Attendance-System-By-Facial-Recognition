from camera import VideoCamera
from flask import Flask,render_template,Response, request,redirect, url_for
import database
import attendanceMark


app=Flask(__name__)


@app.route('/attend')
def index():
    return render_template('attend.html')

def gen(camera):

    while True:
        frame=camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+ frame
               + b'Content-Type: \r\n\r\n'
               + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def First():
    return render_template('First.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL
        database.cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))

        # Fetch one record and return result
        user = database.cur.fetchone()

        # If account exists in accounts table in out database
        if user:
            # Redirect to home page
            return redirect(url_for('pickDate'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('First.html', msg=msg)

@app.route('/calender')
def pickDate():
    return render_template('Calender4.html')

@app.route('/list',methods=['POST','GET'])
def list():
    rows=[]
    if request.method=='POST':
        day=request.form['day']
        database.cur.execute(f"Select * From Attendees where Date='{day}'")
        rows=database.cur.fetchall()
    return render_template('list.html',rows=rows)


if __name__=="__main__":
    app.run(debug=True)