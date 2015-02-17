from fetchArtist import fetchArtistId
import requests
import pandas as pd

#print "Busta Rhymes", fetchArtistId("Busta Rhymes")
# 1YfEcTuGvBQ8xSD1f53UnK
#Part 1.1
def getRelatedArtists(artistID):
	relatedArtistIDs = []
	url = "https://api.spotify.com/v1/artists/" + artistID + "/related-artists"
	req = requests.get(url)
	if req.ok == False:
		return 'Error: bad Spotify API URL or similar error'
	data = req.json()
	#print data["artists"]
	for relartist in data["artists"]:
		relartist_id = relartist["id"]
		relatedArtistIDs.append(relartist_id)
	return relatedArtistIDs

#print getRelatedArtists("1YfEcTuGvBQ8xSD1f53UnK")

#Part 1.2
def getDepthEdges(artistID, depth):
	"""Takes an Artist ID and an integer for depth, returns list of edges"""
	tuple_artist_list = []
	related_ids = []
	related_ids.append(artistID)
	for i in range(depth):
		for ids in related_ids:
			depth_artist_list = getRelatedArtists(ids)
			for artist in depth_artist_list:
				tupl = (ids, artist)
				tuple_artist_list.append(tupl)
			related_ids = depth_artist_list
	remove_duplicates_list = tuple_artist_list
	set(remove_duplicates_list) #set removes exact duplicates
	list(set(remove_duplicates_list))
	return(remove_duplicates_list)

#print getDepthEdges("1YfEcTuGvBQ8xSD1f53UnK", 1)

def getDepthList(artistID, depth):
	depth_edges = getDepthEdges(artistID, depth)
	edgeList = pd.DataFrame(depth_edges)
	return edgeList

#df = getDepthList("1YfEcTuGvBQ8xSD1f53UnK", 1)
#print df.shape

def writeEdgeList(artistID, depth, filename):
	x = getDepthList(artistID, depth)
	x.to_csv(filename, index=False)

#writeEdgeList("1YfEcTuGvBQ8xSD1f53UnK", 1, "Busta's Bruthas.csv")