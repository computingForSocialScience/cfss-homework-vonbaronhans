from flask import Flask, render_template, request, redirect, url_for
import pymysql
#import old code from HW6
import sys
import networkx as nx
import pandas as pd
import random
from artistNetworks import *
from analyzeNetworks import *
from fetchArtist import *
from fetchAlbums import *

dbname="playlists"
host="localhost"
user="root"
passwd="computers"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

app = Flask(__name__)

def createNewPlaylist(inputName):
    #Create the two tables in the database if they are not already there. You can do this by adding "IF NOT EXISTS" to an SQL create-table statement (e.g. CREATE TABLE IF NOT EXISTS playlists (...)). Look in the lecture slides (or this part of the MySQL Tutorial, as well as the somewhat obtuse MySQL "CREATE TABLE Syntax" documentation) for help constructing your create-table statements.
    cur = db.cursor()
    make_table_playlist = '''CREATE TABLE IF NOT EXISTS playlists (id INTEGER PRIMARY KEY AUTO_INCREMENT, rootArtist VARCHAR(256));'''
    make_table_songs = '''CREATE TABLE IF NOT EXISTS songs (playlistId INTEGER, songOrder INTEGER, artistName VARCHAR(256), albumName VARCHAR(256), trackName VARCHAR(256));'''
    cur.execute(make_table_playlist)
    cur.execute(make_table_songs)


    artistId = fetchArtistId(inputName)
    depth = 2
    edgeList = getEdgeList(artistId, depth)
    g = pandasToNetworkX(edgeList)

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
        print artist_id, artist_name

        album_id_list = fetchAlbumIds(artist_id)

        print artist_name,album_id_list
        if album_id_list == []:
            print "Fuck it, Spoofy and its stupid returning me shit-nothin for albums. I don't need anything from", artist_name, "anyway. Fuck'em."
            continue #fuck it, I'm skipping this shit.
        random_album = random.choice(album_id_list)
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

    #Add the artist's name to the playlists table and get the playlist ID associated with the new row (this will probably involve an INSERT statement to add the row to the table, followed by a SELECT statement to get the ID).

    cur = db.cursor()

    add_to_playlist = '''INSERT INTO playlists (rootArtist) VALUES ('%s')''' % (inputName)
    #print add_to_playlist
    cur.execute(add_to_playlist) 

    db.commit()
    #cur.close()
    #db.close()

    #Add the songs to the songs table, with the appropriate playlist ID in the playlistId column of the new rows and the appropriate order in the songOrder column.

    for i in range(len(random_track_list)):
        songOrder = i
        Artist_Name = '"' + artist_names[i] + '"'
        Artist_Name.replace("\'","")
        Artist_Name.replace("\"","")
        Album_Name = '"' + album_list[i][0] + '"'
        Album_Name.replace("\'","")
        Album_Name.replace("\"","")
        Track_Name = '"' + random_track_list[i] + '"'
        Track_Name.replace("\'","")
        Track_Name.replace("\"","")

        get_id_number = """SELECT MAX(id) from playlists;"""
        cur.execute(get_id_number)
        playlist_id = cur.fetchall()
        #print Artist_Name
        #print "Playlist ID", i, playlist_id
        playlistId = playlist_id[0][0]


        sql = '''INSERT INTO songs (playlistId, songOrder, artistName, albumName, trackName) VALUES (%d, %d, %s, %s, %s)''' % (playlistId, songOrder, Artist_Name, Album_Name, Track_Name)

        cur.execute(sql)

        db.commit()


createNewPlaylist("Busta Rhymes")
createNewPlaylist("Starbomb")

@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/    
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():
    return render_template('playlists.html',playlists=playlists)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']
        # YOUR CODE HERE
        return(redirect("/playlists/"))



if __name__ == '__main__':
    app.debug=False
    app.run()