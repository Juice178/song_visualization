import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from spotipy import Spotify, SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOauthError

bp = Blueprint('viz', __name__)

# def toJson(tracks):
#     flash(tracks)
#     print("hello")

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

    json_file = toJson('hello')

    return render_template('visualize/index.html', data=json_file)


def toJson(tracks):
    return 'some json file'

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)

    return wrapped_view
