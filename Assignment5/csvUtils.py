from io import open
from fetchArtist import *
from fetchAlbums import *
#from fetchAlbumInfo import *

def writeArtistsTable(artist_info_list):
    """Given a list of dictionaries, each as returned from 
    fetchArtistInfo(), write a csv file 'artists.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
    """
    f = open('artists.csv', 'w', encoding='utf-8')
    f.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY\n')
    for artist_dict in artist_info_list:
        a = artist_dict[u'id']
        b = artist_dict[u'name']
        c = unicode(artist_dict[u'followers'])
        d = unicode(artist_dict[u'popularity'])
        e = '\n'
        entry = '%s,"%s",%s,%s%s' % (a,b,c,d,e)
        f.write(entry)
    f.close()

#writeArtistsTable(test_list_dicts)

def writeAlbumsTable(album_info_list):
    """
    Given list of dictionaries, each as returned
    from the function fetchAlbumInfo(), write a csv file
    'albums.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
    """
    f = open('albums.csv', 'w', encoding='utf-8')
    f.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY\n')
    for album_info in album_info_list:
        a = album_info[u'artist_id']
        b = album_info[u'album_id']
        c = album_info[u'name']
        d = unicode(album_info[u'year'])
        e = unicode(album_info[u'popularity'])
        g = '\n'
        entry = '%s,%s,"%s",%s,%s%s' % (a,b,c,d,e,g)
        f.write(entry)
    f.close()
