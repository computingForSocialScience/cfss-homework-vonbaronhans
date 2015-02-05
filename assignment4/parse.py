import csv
import sys

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)

hp_permits = readCSV("permits_hydepark.csv")
### enter your code below

def get_avg_latlng(permits_list):
    sum_lats = 0
    sum_lngs = 0
    for permit in permits_list:
        lat = float(permit[-3])
        #print lat
        lng = float(permit[-2])
        #print lng
        sum_lats += lat
        sum_lngs += lng
    avg_lats = sum_lats / len(permits_list)
    avg_lngs = sum_lngs / len(permits_list)
    avg_latlng = "(" + str(avg_lats) + ',' + str(avg_lngs) + ")"
    print avg_latlng

#get ready for the plot makin'

from matplotlib import pyplot as plt
import re
import Image

#plot makin' time
def zip_code_barchart(permits_list):
    """plots and saves as a .jpg a bar chart of contractor zip codes"""
    #First, create list of zip codes
    zipcodes = []
    zip_indeces = [28,35,42,49,56,63,70,77] #indeces for zip codes for contractors
    for permit in permits_list:
        for index in zip_indeces:
            if permit[index] == '':
                continue
            zip_match = re.match('[0-9]{5}', permit[index])
            if zip_match:
                z = int(zip_match.group())
                zipcodes.append(z)
    #print zipcodes
    #print len(zipcodes)
    
    #Create histogram of zipcodes
    plt.hist(zipcodes, bins=50)
    plt.title('Zipcode Histogram')
    plt.xlabel('Contractor Zipcodes')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.draw()
    plt.savefig('histogram.png')
    Image.open('histogram.png').save('histogram.jpg', 'JPEG')


if sys.argv[1] == 'latlong':
	get_avg_latlng(hp_permits)
elif sys.argv[1] == 'hist':
	zip_code_barchart(hp_permits)
else:
	print "Error. So many Error."