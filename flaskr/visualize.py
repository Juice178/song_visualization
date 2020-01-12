from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from spotipy import Spotify, SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOauthError
import pandas as pd

bp = Blueprint('viz', __name__)

@bp.route('/', methods=("GET", "POST"))
def get_data():
    if request.method == 'POST':
        error = None

        client_id = request.form['client_id']
        client_secret = request.form['client_secret']

        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)

        sp = Spotify(client_credentials_manager=client_credentials_manager)

        artist_id = request.form['artist_id']
        lz_uri = f'spotify:artist:{artist_id}'

        try:
            top_tracks = sp.artist_top_tracks(lz_uri)
        except SpotifyOauthError as e:
            error = e
        except SpotifyException as e:
            error = e
                
        if error:
            flash(error)
        else:
            json_file = toJson(sp, top_tracks)
            return render_template('visualize/index.html', data=json_file)


    return render_template('visualize/index.html')

def toJson(sp,top_tracks):

    feature_names = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
        'acousticness','instrumentalness', 'liveness',  'valence', 'tempo', 'duration_ms']

    rows = []
    for track in top_tracks['tracks']:
        row = []
        
        row.append(track['artists'][0]['name'])
        row.append(track['name'])
        row.append(track['popularity'])
        song_id = track['id']

        feature_values  = sp.audio_features(song_id)[0]
        features = [val for key, val in feature_values.items() if key in feature_names]

        row.extend(features)
        
        rows.append(row)

    columns = ['artist_name', 'song_name', 'popularity']
    columns.extend(feature_names)
    df = pd.DataFrame(rows, columns = columns)

    json_file = df.to_json(orient='records')
    
    return json_file