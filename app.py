from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///playlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), default='N/A')
    artist = db.Column(db.String(100), default='N/A')
    album = db.Column(db.String(100), default='N/A')
    data = db.Column(db.BLOB)
    
    def __repr__(self):
        return '<Song %r>' % self.title

@app.route('/')
def index():
    songs = Songs.query.all()
    return render_template('index.html')

@app.route('/songs')
def songs():
    return render_template('songs.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        files= request.files.getlist('inputFile')
        for file in files:
            #song_title = request.form['title']
            song_artist = request.form['artist']
            song_album = request.form['album']
            #file = Songs(title=file.filename, artist=file.filename, album=file.filename, data=file.read())
            file = Songs(title=file.filename, artist=song_artist, album=song_album, data=file.read())
            db.session.add(file)
            db.session.commit()
        return redirect('/songs')
    return render_template('upload.html', msg='Please choose a file')


if __name__ == "__main__":
    app.run(debug=True)