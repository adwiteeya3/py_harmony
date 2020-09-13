from flask import Flask, render_template
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
    #songs = Songs.query.all()
    return render_template('index.html')

@app.route('/songs')
def songs():
    return render_template('songs.html')

if __name__ == "__main__":
    app.run(debug=True)