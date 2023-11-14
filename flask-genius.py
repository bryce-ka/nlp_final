
from flask import Flask, jsonify, request
import lyricsgenius
from flask import redirect, url_for
import requests

app = Flask(__name__)
access_token = ""
@app.route('/')
def index():
    return redirect("https://api.genius.com/oauth/authorize?client_id=QM8AxT7eVtOS1SSTQGzYFnwZlo0bU9ZO9nsmi26h1vZHh4VrkjPKpdliZpO1iauC&redirect_uri=http://localhost:5000/redirect&state=1738&response_type=token")

@app.route('/redirect')
def redirect_uri():
    access_token = request.args.get('access_token')
    
@app.route('/search')
def search():
    query = request.args.get('q')
    
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get('https://api.genius.com/some-endpoint', headers=headers)
    genius = lyricsgenius.Genius(access_token)
    artist = genius.search_artist("Andy Shauf", max_songs=3, sort="title")
    print(artist.songs)
    song = artist.song("To You")
    # or:
    # song = genius.search_song("To You", artist.name)
    print(song.lyrics)
    artist.save_lyrics()
    




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
