import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from spotipy import Spotify, SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOauthError

bp = Blueprint('viz', __name__)

@bp.route('/', methods=("GET", "POST"))
def get_data():
    if request.method == 'POST':
        error = None

        client_id = request.form['username']
        client_secret = request.form['password']

        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)

        sp = Spotify(client_credentials_manager=client_credentials_manager)

        artist_id = request.form['artist_id']
        lz_uri = f'spotify:artist:{artist_id}'

        try:
            tracks = sp.artist_top_tracks(lz_uri)
        except SpotifyOauthError as e:
            error = e
        except SpotifyException as e:
            error = e
                
        if error:
            flash(error)
        else:
            pass

    return render_template('visualize/index.html')

def toJson(tracks):
    pass
