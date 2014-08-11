__author__ = 'Kaiqun'

from datetime import datetime
import math
import DBConnection


def SNAPS_Former():
	#StartTime = str(datetime.strptime(TimeRange.split(' - ')[0], '%m/%d/%Y %I:%M %p'))
	#EndTime = str(datetime.strptime(TimeRange.split(' - ')[1], '%m/%d/%Y %I:%M %p'))

	cnxn = DBConnection.connector()
	cursor = cnxn.cursor()

	#cmd = "SELECT [snaps].[dbo].[vw_aggredated_volume_speed].[ACISA],SUM([VolSum]) as Vol,AVG([avg_speed]) as Speed,[data_datetime],AVG([Latitude]) as Lat,AVG([Longitude]) as Lon FROM [snaps].[dbo].[vw_aggredated_volume_speed], [snaps].[dbo].[SNAPsLocation] where [snaps].[dbo].[vw_aggredated_volume_speed].[ACISA] = [snaps].[dbo].[SNAPsLocation].[ACISA] and [data_datetime] > '" + StartTime + "' and [data_datetime] < '" + EndTime + "' group by [snaps].[dbo].[vw_aggredated_volume_speed].[ACISA],[data_datetime]"

	cmd = "SELECT TOP 1000 [snaps].[dbo].[vw_aggredated_volume_speed].[ACISA],SUM([VolSum]) as Vol,AVG([avg_speed]) as Speed,[data_datetime],AVG([Latitude]) as Lat,AVG([Longitude]) as Lon FROM [snaps].[dbo].[vw_aggredated_volume_speed], [snaps].[dbo].[SNAPsLocation] where [snaps].[dbo].[vw_aggredated_volume_speed].[ACISA] = [snaps].[dbo].[SNAPsLocation].[ACISA] group by [snaps].[dbo].[vw_aggredated_volume_speed].[ACISA],[data_datetime]"
	cursor.execute(cmd)

	MainReturnDict = {
		"bbox": [
			171.65283, -43.9078,
			173.09492, -42.04222
		],
		"crs": {
			"properties": {
				"code": "4326"
			},
			"type": "EPSG"
		},
		"type": "FeatureCollection",
		"features": []
	}

	while 1:
		initDict = {
			"geometry": {
				#"coordinates": [-77.07570999999999, 38.86651],
				"coordinates": [],
				"type": "Point"
			},
			"geometry_name": "origin_geom",
			"id": "",
			"properties": {
				"agency": "WEL(GNS_Primary)",
				#"bbox": [-77.07570999999999, 38.86651, -77.07570999999999, 38.86651],
				"bbox": [],
				#"depth": 14.23,
				"depth": 14.23,
				"latitude": 38.86651,
				"longitude": -77.07570999999999,
				#"magnitude": 3.56,
				"magnitude": 3.56,
				"magnitudetype": "Ml",
				#"origintime": "2010-09-30T19:59:10Z",
				"origintime": "2010-09-30T19:59:10Z",
				"phases": 15,
				"publicid": "3380927",
				"status": "reviewed",
				"type": "earthquake",
				"updatetime": "2012-04-26T09:01:00Z"
			},
			"type": "Feature"
		}
		row = cursor.fetchone()
		if not row:
			break
		if row.Vol < 50:
			continue
		if not row.Speed:
			continue
		initDict.update({'geometry': {'coordinates': [row.Lon, row.Lat], "type": "Point"}})
		initDict.update({'id': str(row.ACISA) + '.' + str(row.data_datetime)})
		initDict.update({'properties': {
			"agency": "WEL(GNS_Primary)",
			"bbox": [row.Lon, row.Lat, row.Lon, row.Lat],
			#"depth": 14.23,
			"depth": row.Speed / 5.0,
			"latitude": row.Lat,
			"longitude": row.Lon,
			#"magnitude": 3.56,
			"magnitude": math.log(row.Vol / 50.0) * 1.5,
			"magnitudetype": "Ml",
			#"origintime": "2010-09-30T19:59:10Z",
			"origintime": str(row.data_datetime),
			"phases": 15,
			"publicid": "3380927",
			"status": "reviewed",
			"type": "earthquake",
			"updatetime": "2012-04-26T09:01:00Z"
		}})
		MainReturnDict["features"].append(initDict)

	return  MainReturnDict