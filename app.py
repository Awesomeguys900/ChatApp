from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room

app = Flask(__name__)
socketIO = SocketIO(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/chat')
def chat():
    # request args is a dict which contains all the url parameters
    username = request.args.get('username')
    room = request.args.get('room')
    if username and room:
        return render_template("chat.html", username=username, room=room)
    else:
        return redirect(url_for("home"))

@socketIO.on('join_room')
def handle_join_room_event(data):
    app.logger.info(f"{data['username']} has joined the {data['room']}") #prints data, allows to save logs, and prints time stamp
    join_room(data["room"])
    socketIO.emit("join_room_announcement", data)

@socketIO.on("send_message")
def handle_send_message(data):
    app.logger.info(f"{data['username']} has sent in the the {data['room']}:{data['message']}")
    socketIO.emit("receive_message", data, room=data['room']) #send to those with the same socket ID's/room ids

if __name__ == "__main__":
    socketIO.run(app, debug=True)
    
