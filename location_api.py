import pandas as pd
from urllib2 import Request, urlopen, URLError
import json
import config
import os

# imports csv to dataframe
csv = pd.read_csv('noisy_top.csv')
#converts latitude/longitude into url for api endpoint
lat_long = [str(csv['Latitude'][i]) + "," + str(csv['Longitude'][i]) for i in range(csv['Latitude'].count())]


for i in range(csv['Latitude'].count()):
	
	# creates api endpoint	
	url = "https://api.foursquare.com/v2/venues/search?ll=" + lat_long[i] + "&radius=30&client_id=" + config.CLIENT_ID + "&client_secret=" + config.CLIENT_SECRET + "&v=20141112"

	request = Request(url)

	try:
		#save json to file for each lat_long
		response = urlopen(request)
		json_data = response.read()
		path = "C:\Users\Angel\Documents\Coursera\Noise\locations"
		filename = lat_long[i] + ".txt"
		fullpath = os.path.join(path, filename)
		fo = open(fullpath, "wb")
		fo.write(json_data)
		fo.close()
	except URLError, e:
		print '' , e