import requests
from datetime import datetime

def fetchAlbumIds(artist_id):
    """Using the Spotify API, take an artist ID and 
    returns a list of album IDs in a list
    """
    url = "https://api.spotify.com/v1/artists/" + artist_id + "/albums?album_type=album&market=US"
    req = requests.get(url)
    if req.ok == False:
        return 'Error: bad Spotify API URL or similar error'
    data = req.json()
    albums_list = []
    #print len(data[u'items'])
    for album in data[u'items']:
        album_id = album[u'id']
        albums_list.append(album_id)
    return albums_list

def fetchAlbumInfo(album_id):
    """Using the Spotify API, take an album ID 
    and return a dictionary with keys 'artist_id', 'album_id' 'name', 'year', popularity'
    """
    url = "https://api.spotify.com/v1/albums/" + album_id
    req = requests.get(url)
    if req.ok == False:
        return 'Error: bad Spotify API URL or similar error'
    data = req.json()
    album_info = {}
    #print data[u'artists']
    album_info['artist_id'] = data[u'artists'][0][u'id']
    album_info['album_id'] = data[u'id']
    album_info['name'] = data[u'name']
    release_date = data[u'release_date']
    year = int(release_date[0:4])
    album_info['year'] = year
    album_info['popularity'] = data[u'popularity']
    
    return album_info

