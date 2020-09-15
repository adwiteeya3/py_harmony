from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from io import BytesIO
from flask_share import Share
import os

#VOLUME_PATH =  os.path.abspath(os.curdir)+'\static\songs'
#basedir = os.path.abspath(os.curdir)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_songs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
share = Share(app)

class Playlist(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), default='N/A')
    artist = db.Column(db.String(100), default='N/A')
    album = db.Column(db.String(100), default='N/A')
    data = db.Column(db.BLOB)
    #file_path = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<Song %r>' % self.title

@app.route('/')
def index():
    songs = Playlist.query.all()
    return render_template('index.html', songs=songs)

@app.route('/songs', methods=['GET'])
def collection():
    if request.method =='GET':
        songs = Playlist.query.all()
        return render_template('songs.html', songs=songs)

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        files= request.files.getlist('inputFile')
        for file in files:
            song_artist = request.form['artist']
            song_album = request.form['album']

            #file.save(os.path.join('D:/Github/python/py_harmony/static/songs/', file.filename))
            #file_path = os.path.join(VOLUME_PATH, file.filename)

            #file = Playlist(title=file.filename, artist=song_artist, album=song_album, data=file.read(), file_path=file_path)
            file = Playlist(title=file.filename, artist=song_artist, album=song_album, data=file.read())
            db.session.add(file)
            db.session.commit()
        return redirect('/songs')
    return render_template('upload.html', msg='Please choose a file')

@app.route('/songs/delete/<int:id>')
def delete(id):
    song = Playlist.query.get_or_404(id)
    db.session.delete(song)
    db.session.commit()
    return redirect('/songs')

@app.route('/songs/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    song = Playlist.query.get_or_404(id)
    if request.method == 'POST':
        #song.title = request.form['title']
        song.artist = request.form['artist']
        song.album = request.form['album']
        db.session.commit()
        return redirect('/songs')
    else:
        return render_template('edit.html', song= song)

@app.route('/songs/player/<int:id>', methods=['GET'])
def player(id):
    file_data = Playlist.query.filter_by(id=id).first()
    return send_file(BytesIO(file_data.data), mimetype='audio/mpeg', attachment_filename=file_data.title)
    #return render_template('player.html', song= song)

@app.route('/songs/download/<int:id>', methods=['GET','POST'])
def download(id):
    file_data = Playlist.query.filter_by(id=id).first()
    return send_file(BytesIO(file_data.data), as_attachment=True, mimetype='audio/mpeg', attachment_filename=file_data.title)

@app.route('/search_song')
def search_result():
    query = request.args.get('search')
    print(query)
    songs = Playlist.query.filter(Playlist.title.ilike('%'+query+'%')).all()
    if not songs:
        songs = Playlist.query.filter(Playlist.artist.ilike('%'+query+'%')).all()
        if not songs:
            songs = Playlist.query.filter(Playlist.album.ilike('%'+query+'%')).all()
    print(songs)
    return render_template('search.html', songs=songs)

if __name__ == "__main__":
    app.run(debug=True)