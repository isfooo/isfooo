from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'isfo21'
app.config['MYSQL_HOST'] = 'gcp.connect.psdb.cloud'
app.config['MYSQL_USER'] = 'txsmgecytqt2863a4dxw'
app.config['MYSQL_PASSWORD'] = 'pscale_pw_ffv52e4ZGy3Gk1XDsCDALlYk2LQLSGT70V7rEG2izkB'
app.config['MYSQL_DB'] = 'app'

mysql = MySQL(app)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()

        return jsonify({'success': True, 'message': 'Registration successful!'})
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            return jsonify({'success': True, 'message': 'Login successful!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password.'})
    
    return render_template('login.html')

@socketio.on('message')
def handle_message(data):
    message = data['message']
    username = 'Some User'  # Replace with the actual username logic
    
    # Process the message and broadcast it to all connected clients
    emit('message', {'username': username, 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
