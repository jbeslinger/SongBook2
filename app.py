from flask import Flask,render_template, redirect, url_for, request,jsonify
app = Flask(__name__)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import os
import json

client_id = "2299de3db00442eba2d6bdb9bb9b0127"
client_secret = "6b78cccaacae4a52809b1f49ecd6c9dc"

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def getTrackFeatures(id):
	meta = sp.track(id)
	features = sp.audio_features(id)

	# meta
	name = meta['name']
	album = meta['album']['name']
	artist = meta['album']['artists'][0]['name']
	release_date = meta['album']['release_date']
	length = meta['duration_ms']
	popularity = meta['popularity']

	# features
	acousticness = features[0]['acousticness']
	danceability = features[0]['danceability']
	energy = features[0]['energy']
	instrumentalness = features[0]['instrumentalness']
	liveness = features[0]['liveness']
	loudness = features[0]['loudness']
	speechiness = features[0]['speechiness']
	tempo = features[0]['tempo']
	time_signature = features[0]['time_signature']

	track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
	return track


@app.route('/',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		song_name = request.form['song_name']
		artist_name = request.form['artist_name']
		#print(song_name)
		#print(artist_name)
		results = sp.search(q='artist:' + artist_name + ' track:' + song_name, limit=1, type='track')
		# for idx, track in enumerate(results['tracks']['items']):
		# 	print(idx, track['name'])
		#print(results)
		items = results['tracks']['items']
		#print(json.dumps(items[0]['album']['external_urls']['spotify'], indent= 4))
		if not items:
			print("No results found")
			return render_template('index.html', no_results_err=True)
		song_url = items[0]['external_urls']['spotify']
		album_url = items[0]['album']['external_urls']['spotify']
		song_uri = items[0]['uri']
		track_info = getTrackFeatures(song_uri)
		track_info.append(song_url)
		track_info.append(album_url)
		print(track_info)
		return render_template('index.html', track=track_info)
		# return jsonify(results)
	else: # GET
		user = request.args.get('song_name')
		return render_template('index.html')


if __name__ == '__main__':
	app.run(debug = True)
