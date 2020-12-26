import requests
import pandas as pd
import sys
from dateutil import parser

def scrape_site(station_code,start_date,end_date):
	url = "https://api.weather.com/v2/pws/history/daily?stationId={}&format=json&units=e&startDate={}&endDate={}&numericPrecision=decimal&apiKey=6532d6454b8aa370768e63d6ba5a832e".format(station_code,start_date,end_date)
	r = requests.get(url)
	print (r)
	try:
		obj = r.json()
		observations = obj['observations']
	except Exception as e:
		print (e)
		print (r.content)
		print ("download error")
		observations = []
	return observations



def parse_observations(observations):
	endlist = []
	for i in observations:
		tempdict = {}
		tempdict['date'] = parser.parse(i['obsTimeLocal']).strftime("%Y%m%d")
		tempdict['solarRad'] = i['solarRadiationHigh']
		measures = i['imperial']
		tempdict['high temp'] = measures['tempHigh']
		tempdict['low temp'] = measures['tempLow']
		endlist.append(tempdict)
	return endlist
	
	
def get_city_year(year,station):
	endDateList = ["0131","0228","0331","0430","0531","0630","0731","0831","0930","1031","1130","1231"]
	startDateList = ["0101","0201","0301","0401","0501","0601","0701","0801","0901","1001","1101","1201"]
	final_list = []
	for i in endDateList:
		end_date = year+i
		start_date = end_date[:-2]+"01"
		try:
			obs = scrape_site(station,start_date,end_date)
			parse_list = parse_observations(obs)
			final_list += parse_list
		except Exception as e:
			print (e)
			print (i)
	return final_list
	
	
if __name__ == "__main__":
	theyear = sys.argv[2]
	thestation = sys.argv[1]
	endlist = get_city_year(theyear,thestation)
	print (len(endlist))
	pd.DataFrame(endlist).to_csv("{}-{}_testheat.csv".format(theyear,thestation),index=False)
	
	
