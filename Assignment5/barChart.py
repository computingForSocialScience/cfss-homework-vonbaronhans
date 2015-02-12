#importing csv reader and plotting modules
import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
    f_artists = open('artists.csv') #opening csv files
    f_albums = open('albums.csv')

    artists_rows = csv.reader(f_artists) #loading rows of csv's into vars
    albums_rows = csv.reader(f_albums)

    artists_header = artists_rows.next() #loading first row (headers) into variables
    albums_header = albums_rows.next()

    artist_names = [] #new list

    decades = range(1900,2020, 10) #list of years 1900-2020 by 10's (e.g. 1920, 1930...)
    decade_dict = {}
    for decade in decades:
        decade_dict[decade] = 0 #setting decades as keys with the value zero for all
    
    for artist_row in artists_rows:
        if not artist_row: #skip rest of loop here if current row is empty
            continue
        artist_id,name,followers, popularity = artist_row #unloading into variables contents of a row
        artist_names.append(name) #make list of names of artists

    for album_row  in albums_rows:
        if not album_row:
            continue
        artist_id, album_id, album_name, year, popularity = album_row
        for decade in decades: #if year falls within the decade, dict value += 1
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)):
                decade_dict[decade] += 1
                break #once year is counted for a decade, break back to iterating over rows 

    x_values = decades
    y_values = [decade_dict[d] for d in decades] #pull counted values for each decade into a list
    return x_values, y_values, artist_names

def plotBarChart():
    x_vals, y_vals, artist_names = getBarChartData()
    fig , ax = plt.subplots(1,1) #creates figure with one subplot

    ax.bar(x_vals, y_vals, width=10) #creates bars corresponding to x=decade, y=number of albums
    ax.set_xlabel('decades') #labels
    ax.set_ylabel('number of albums')
    ax.set_title('Totals for ' + ', '.join(artist_names)) #generate a title e.g. Totals for Busta Rhymes
    plt.show() #make-a-da-graph


    
