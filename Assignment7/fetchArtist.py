import sys
import requests
import csv

def fetchArtistId(name):
    """Using the Spotify API search method, take a string that is the artist's name, 
    and return a Spotify artist ID.
    """
    #make sure spaces in artist name are replaced with %20
    artist_name_api = str.replace(str(name)," ", "%20")
    url = "https://api.spotify.com/v1/search?q=" + artist_name_api + "&type=artist"
    req = requests.get(url)
    if req.ok == False: 
        return 'Error: bad Spotify API URL or similar error' 
    data = req.json()
    #print data
    artist_info = data[u'artists']
    items = artist_info['items']
    #forgive use of x... not sure what to call it otherwise
    x = items[0]
    uri = x[u'id']
    return uri


def fetchArtistInfo(artist_id):
    """Using the Spotify API, takes a string representing the id and
    returns a dictionary including the keys 'followers', 'genres', 
    'id', 'name', and 'popularity'.
    """
    url = "https://api.spotify.com/v1/artists/" + artist_id
    req = requests.get(url)
    if req.ok == False:
        return 'Error: bad Spotify API URL or similar error'
    data = req.json()
    #print data
    artist_dict = {}
    artist_dict['followers'] = int(data[u'followers']['total'])
    artist_dict['genres'] = data[u'genres']
    artist_dict['id'] = data[u'id']
    artist_dict['name'] = data[u'name']
    artist_dict['popularity'] = int(data[u'popularity'])
    return artist_dict

if __name__ == '__main__':
    print fetchArtistInfo(fetchArtistId('Daft Punk'))
    print fetchArtistInfo('')