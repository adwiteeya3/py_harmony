from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from io import BytesIO
#import flask_whooshalchemy as wa
#from forms import SearchForm
#from wtforms import Form, StringField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///playlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['WHOOSH_BASE'] = 'whoosh'

db = SQLAlchemy(app)

class Songs(db.Model):
    #__searchable__ = ['title', 'artist', 'album']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), default='N/A')
    artist = db.Column(db.String(100), default='N/A')
    album = db.Column(db.String(100), default='N/A')
    data = db.Column(db.BLOB)
    
    def __repr__(self):
        return '<Song %r>' % self.title

#wa.whoosh_index(app, Songs)

@app.route('/')
def index():
    songs = Songs.query.all()
    return render_template('index.html', songs=songs)

@app.route('/songs', methods=['GET', 'POST'])
def collection():
    if request.method =='GET':
        songs = Songs.query.all()
        return render_template('songs.html', songs=songs)
    elif request.method == 'POST':
        song_data = request.form
        result = add_song(song_data['title'], song_data['artist'], song_data['year'])
        return redirect('/songs')

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

@app.route('/songs/delete/<int:id>')
def delete(id):
    song = Songs.query.get_or_404(id)
    db.session.delete(song)
    db.session.commit()
    return redirect('/songs')

@app.route('/songs/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    song = Songs.query.get_or_404(id)
    if request.method == 'POST':
        #song.title = request.form['title']
        song.artist = request.form['artist']
        song.album = request.form['album']
        db.session.commit()
        return redirect('/songs')
    else:
        return render_template('edit.html', song= song)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/songs/download/<int:id>', methods=['GET','POST'])
def download(id):
    file_data = Songs.query.filter_by(id=id).first()
    #file_data.title = request.form['title']
    #return send_file(BytesIO(file_data.data), attachment_filename=file_data.title, as_attachment=True)
    return send_file(BytesIO(file_data.data), as_attachment=True, mimetype='audio/mpeg', attachment_filename=file_data.title)

if __name__ == "__main__":
    app.run(debug=True)