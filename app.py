from flask import Flask,render_template, redirect, url_for, request,jsonify
app = Flask(__name__)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import os

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


@app.route('/',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		search_text = request.form['song_name']

		results = sp.search(q=search_text, limit=10)
		songlist = results['tracks']['items']

		return render_template('home.html', tracks=songlist)
	else:
		user = request.args.get('song_name')
		return render_template('home.html')


if __name__ == '__main__':
	app.run(debug = True)