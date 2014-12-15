import pandas as pd
import os
import json
import glob
import string

# create data frame to capture top venues for each location
df_ = pd.DataFrame()


# pulls names of top 5 venues for each json file
def top_venues(json_data):
	venue_array = json_data['response']['venues']
	range_i = range(len(json_data['response']['venues']))
	venue_i_array = []
	for i in range_i:
		venue_name = venue_array[i]['name'].encode('ascii', 'ignore');
		venue_count = int(venue_array[i]['stats']['checkinsCount'])
		venue_categories = venue_array[i]['categories']
		venue_type = ""
		if venue_categories:
			venue_type = venue_categories.pop()['name'].encode('ascii', 'ignore');
		venue_tuple = (venue_name, venue_count, venue_type)
		venue_i_array.append(venue_tuple)
	venue_i_array = sorted(venue_i_array, key=lambda tup: tup[1], reverse=True)
	return venue_i_array[0:5]

# imports noisy locations csv to dataframe
csv = pd.read_csv('noisy_top.csv')

# completes null values for incident address as location of intersections
for i in range(csv['Latitude'].count()):
	if pd.isnull(csv['Incident Address'][i]):
		csv['Incident Address'][i] = csv['Intersection Street 1'][i] + " AND " + csv['Intersection Street 2'][i]


csv['Latitude'] = [round(csv['Latitude'][i], 6) for i in range(len(csv['Latitude']))]
csv['Longitude'] = [round(csv['Longitude'][i], 6) for i in range(len(csv['Longitude']))]

# read each file
path = "C:\Users\Angel\Documents\Coursera\Noise\locations"
for file in glob.glob(os.path.join (path, '*.txt')):
	fo = open(file, "r+")
	data = fo.read()
	location_json = json.loads(data)
	# pull lat_long from filename
	basename = os.path.basename(file)
	lat_long = os.path.splitext(basename)[0]
	lat_long_split = lat_long.split(',')
	latitude = round(float(lat_long_split[0]), 6)
	longitude = round(float(lat_long_split[1]), 6)

	# find row in csv that matches lat/long of file
	csv_row = csv.ix[(csv['Latitude'] == latitude) & (csv['Longitude'] == longitude)]
	addr = string.join(csv_row['Incident Address'].values, "")

	row = pd.Series([addr,int(csv_row['count(location)']), latitude, longitude, top_venues(location_json)])
	df_ = df_.append(row, ignore_index=True)
	fo.close()

result = df_.sort(1, ascending = False)
result = result.reset_index(drop=True)
result.columns = ['Address', 'Noise Count', 'Latitude', 'Longitude', 'Venues']
print result
result.to_csv('noisy_top_venues.csv', sep='\t')