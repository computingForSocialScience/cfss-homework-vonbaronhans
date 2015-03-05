import sys
import networkx as nx
import pandas as pd
import random
from io import open
from artistNetworks import *
from analyzeNetworks import *
from fetchArtist import *
from fetchAlbums import *

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names

    #print type(artist_names)

    artist_list = []
    #make list of artist IDs based on passed args
    for name in artist_names:
    	artistId = fetchArtistId(name)
    	artist_list.append(artistId)

    #make list of dataframes to use later
    #list_index = 0
    edgeList_list = []
    depth = 2 #change to 2 later
    for artistId in artist_list:
    	edgeList = getEdgeList(artistId, depth)
    	#list_index += 1
    	edgeList_list.append(edgeList)

    #concatenate the dataframes together
    concat_edgeLists = edgeList_list[0]
    for edgeList in edgeList_list[1:]:
    	stitch = combineEdgeLists(concat_edgeLists, edgeList)
    	concat_edgeLists = stitch

    #add headers to concat_edgeLists
    concat_edgeLists.columns = ['Artist','Related_Artist']

    # change dataframe to nx DiGraph
    g = pandasToNetworkX(concat_edgeLists)
    #print type(g)
    #print g.nodes()
    #print g.edges(data=True)
    #print g.number_of_edges()
    #print randomCentralNode(g)

    random_artists = []
    for i in range(30):
        random_artist = randomCentralNode(g)
        random_artists.append(random_artist)

    artist_names = []
    album_list = []
    for artist_id in random_artists:
        artist = fetchArtistInfo(artist_id)
        artist_name = artist['name']
        artist_names.append(artist_name)
        album_id_list = fetchAlbumIds(artist_id)
        random_album = (random.choice(album_id_list))
        random_album_info = fetchAlbumInfo(random_album) 
        random_album_name = random_album_info['name']
        tupl = (random_album_name, random_album)
        album_list.append(tupl)

    random_track_list = []
    for album in album_list:
        get_album_tracks_url = 'https://api.spotify.com/v1/albums/' + album[1] + '/tracks'
        req = requests.get(get_album_tracks_url)
        if req.ok == False: 
            print "Error in get_album_tracks_url Request"
        req.json()
        myjson = req.json()
        get_items = myjson.get('items')
        track_list = []
        for i in range(len(get_items)):
            get_track_name = get_items[i]['name']
            track_list.append(get_track_name)
            random_track = (random.choice(track_list))
        random_track_list.append(random_track)
    #print random_track_list

    f = open('playlist.csv', 'w', encoding = 'utf-8')
    f.write(u'ARTIST_NAME,ALBUM_NAME,TRACK_NAME\n')
    for i in range(len(random_track_list)):
        Artist_Name = artist_names[i]
        Album_Name = album_list[i][0]
        Track_Name = random_track_list[i]
        s = '"'+Artist_Name+'"'+','+'"'+Album_Name+'"'+','+'"'+Track_Name+'"'+'\n'
        f.write(s) 
    f.close()









