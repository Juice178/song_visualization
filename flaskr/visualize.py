from flask import (
    Blueprint, flash,render_template, request
)

from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOauthError
from flaskr.api.spotify import Spotipy
import pandas as pd

bp = Blueprint('viz', __name__)

@bp.route('/', methods=("GET", "POST"))
def get_data():
    """
    Works differently depending on a HTTP method

    IF GET  : Return html file for username, password, artist id inputs
    IF POST : Get data and convert it to a json file, which then is passed to html file
    """
    # show a form to enter client id and secret key only when an user loggin for the first time
    is_first_time_login = True

    if request.method == 'POST':
        error = None

        # Instantiate object only when logged in for the first time
        if is_first_time_login:
            client_id = request.form['client_id']
            client_secret = request.form['client_secret']
            # get an client throught which an user get spotify music data
            sp_client = Spotipy(client_id, client_secret)

        artist_id = request.form['artist_id']

        try:
            # get top 10 songs of an artist
            top_tracks = sp_client.get_artist_top_tracks(artist_id)
        except SpotifyOauthError as e:
            error = 'Either client id or client secret you entered is wrong.'
        except SpotifyException as e:
            error = e
            is_first_time_login = False
        except Exception as e:
            error = e
        else:
            is_first_time_login = False
                
        if error:
            flash(error)
        else:
            json_file = toJson(sp_client, top_tracks)
            return render_template('visualize/index.html', data=json_file, is_first_time_login=is_first_time_login)

    return render_template('visualize/index.html', data=None, is_first_time_login=is_first_time_login)

def toJson(sp_client, top_tracks):
    """
    Convert dictionary to json file

    Params
    ______
    sp_client: An instance to get music data 
    top_traicks (dict): Information about an artist and his/her songs

    Returns
    _______
    json_file(json): Data with 15 columns
    """

    # features about a song
    feature_names = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
        'acousticness','instrumentalness', 'liveness',  'valence', 'tempo', 'duration_ms']

    rows = []
    for track in top_tracks['tracks']:
        row = []
        
        row.append(track['artists'][0]['name'])
        row.append(track['name'])
        row.append(track['popularity'])
        song_id = track['id']

        feature_values  = sp_client.get_audio_features(song_id)[0]
        features = [val for key, val in feature_values.items() if key in feature_names]

        row.extend(features)
        
        rows.append(row)

    columns = ['artist_name', 'song_name', 'popularity']
    columns.extend(feature_names)
    df = pd.DataFrame(rows, columns = columns)

    json_file = df.to_json(orient='records')
    
    return json_file