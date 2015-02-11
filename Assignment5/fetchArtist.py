import sys
import requests
import csv

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    #make sure spaces in artist name are replaced with %20
    artist_name_api = str.replace(name," ", "%20")
    url = "https://api.spotify.com/v1/search?q=" + artist_name_api + "&type=artist"
    req = requests.get(url)
    if req.ok == False: 
        return 'Error: bad Spotify API URL or similar error' 
    data = req.json()
    #print data
    artist_info = data[u'artists']
    items = artist_info['items']
    #forgive use of x... not sure what to call it otherwise
    x = items[-1]
    uri = x[u'id']
    return uri


def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
`   returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    pass

