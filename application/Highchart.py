__author__ = 'Kaiqun'

import calendar
import datetime
import DBConnection


def highchartdata(acisa, TimeString):
	cnxn = DBConnection.connector()
	cursor = cnxn.cursor()

	StartTime = str(datetime.datetime.strptime(TimeString.split(' - ')[0], '%m/%d/%Y %I:%M %p'))
	EndTime = str(datetime.datetime.strptime(TimeString.split(' - ')[1], '%m/%d/%Y %I:%M %p'))

	#SQLcmd = "SELECT * FROM snaps.SNAPs_history WHERE Time > '" + StartTime + "' and Time < '" + EndTime + "'"

	cmd = "SELECT [ACISA],[laneDir],[VolSum],[avg_speed],[data_datetime] FROM [snaps].[dbo].[vw_aggredated_volume_speed] where [ACISA]=" + str(acisa) + " and [data_datetime]> '" + StartTime + "' and [data_datetime] < '" + EndTime + "'" + " order by [data_datetime], [laneDir]"

	cursor.execute(cmd)
	MainDict = {}

	while 1:
		row = cursor.fetchone()
		if not row:
			break
		tmpDict = {
			'type': 'area',
			'name': '',
			'pointInterval': 3600 * 1000,
			'pointStart': 0,
			'data': []
		}
		if str(row.ACISA) + row.laneDir in MainDict:
			MainDict[str(row.ACISA) + row.laneDir]['data'].append(row.VolSum)
		else:
			starttime = row.data_datetime
			tmpDict.update({
				'type': 'area',
				'name': str(row.ACISA) + '-' + row.laneDir,
				'pointInterval': 3600 * 1000,
				'pointStart': calendar.timegm(starttime.timetuple()),
				'data': [row.VolSum]
			})
			MainDict[str(row.ACISA) + row.laneDir] = tmpDict

	return [MainDict[i] for i in MainDict]