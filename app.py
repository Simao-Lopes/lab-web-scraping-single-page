import streamlit as st
from PIL import Image
import random
import pickle
import pandas as pd
import spotipy
from random import randint
import webbrowser
from IPython.display import clear_output
import streamlit.components.v1 as components

# Add css to make text bigger
st.markdown(
    """
    <style>
    div[class*="stTextInput"] label {
      font-size: 26px;
    }
    text{
      font-size: 200% !important;
      text-align: center !important;
    }
    input {
        font-size: 2rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
image = Image.open('logo/Gnoosic.PNG')
st.image(image)

from spotipy.oauth2 import SpotifyClientCredentials

secrets_file = open("spotkey.txt","r")
string = secrets_file.read()

secrets_dict={}
for line in string.split('\n'):
    if len(line) > 0:
        secrets_dict[line.split(':')[0]]=line.split(':')[1]

#Initialize SpotiPy with user credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=secrets_dict['cid'],
                                                           client_secret=secrets_dict['csecret']))

# Import previously saved models
def import_component(path):
    return pickle.load(open(path, 'rb'))

transformer = import_component('Model_data/scaler.sav')
model = import_component('Model_data/model_clustering.sav')
df_top100 = pd.read_csv('Data/Final/Top100.csv')
df_clustered = pd.read_csv('Data/Final/Spotify dataset clustered.csv')

# Function to obtain an uri from a song name
def song_uri(song_id):
    try:
        # Creating the spotipy element for the playlist URI
        querry = 'track:'+str(song_id)
        track = sp.search(q=song_id, limit=1)
        return track['tracks']['items'][0]['uri'].split('spotify:track:')[1]                 
    except:
        return 'Null'

# Function to get the song details of a specific URI
def get_details(uri):
    # Creatinga a dataframe with the columns that we need
    playlist_lst = ['danceability','energy','key','loudness','mode', 'speechiness',
                    'instrumentalness','liveness','valence','tempo',
                    'duration_ms','time_signature']
    
    playlist_df = pd.DataFrame(columns = playlist_lst)
    # Get audio features and adding them to the respective columns
    audio_features = sp.audio_features(uri)[0]
    playlist_df.loc[len(playlist_df)] = [audio_features[i] for i in playlist_lst]
    return playlist_df

uri = ''

state = True

if True:
    
    search = st.text_input(
        "Insert song or search term 👇", key = '<txt>'
    )   
    # User inserts search term
#     print('Insert song or search term:')
    if search != '':
        # flag that controls if the search string exists in the songs dataset
        exist = False

        # testing if the search string exists
        for i in ['song', 'artist', 'genre']:
            if len(df_top100[df_top100[i].str.contains(search, case = False, regex = False)]) != 0:
                exist = True
        # if the song or search term exists in the dataset we sugest a random song, otherwise we search spotify
        if exist == True:
            index = random.randint(0,len(df_top100))
            st.write('#### You got a top100 song!')
            uri = df_top100['uri'].values[index]
        else:
            # Using a try calause because the user can insert a song that's not on spotify, and the app will crash
            try:
                # creating a single row dataframe with all the audio features from the song the user inserted
                df = get_details(song_uri(search))
                # calculating the cluster number for the song the user sugested
                cluster = model.predict(pd.DataFrame(transformer.transform(df), columns = df.columns))
                st.write('#### Spotify recomended!')
                # filtering our dataset to a new dataset just containing the rows of the matching cluster of the user input song
                element = df_clustered[df_clustered['cluster'] == int(cluster)]
                # randomizing a row number from the subset
                index = random.randint(0,len(element))
                uri = element['track_id'].values[index]
                st.write('###    ')
            except:
                # Exception in the case that the song doesn't exists in spotify
                st.write('### Invalid song. Sorry!')

if uri != '':
    
    html_string = """<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/"""+uri+"""#42?utm_source=generator&theme=0" width="100%" height="80" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>"""
#     st.write(html_string)
    
    components.html(html_string,height=600)

