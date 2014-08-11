from flask import Flask, render_template, request, jsonify
import json
from SNAP import SNAPS_Former
from Highchart import highchartdata
import db_access

app = Flask(__name__)


@app.route("/")
def mapping():
	return render_template('index.html')


@app.route("/mapps")
def mapps():
	return render_template('mapps.html')


@app.route('/_snap_form')
def formSNAPs():
	return jsonify(SNAPS_Former())


@app.route('/highchart')
def hightchart():
	return render_template('highchart.html')


@app.route('/_high_chart')
def hightchartData():
	return jsonify(result = highchartdata())


@app.route('/nze')
def nze():
	return render_template('plot_nze.html')


@app.route('/bubble')
def bubble():
	return render_template('plot_bubble.html')


@app.route('/smx')
def smx():
	return render_template('plot_scatter_matrix.html')


@app.route('/tree')
def tree():
	return render_template('plot_treemap.html')


@app.route('/_query_by_corridor_group')
def query_by_corridor_group():
	target_plot = request.args.get('target_plot', 'NZE', type = str)
	if target_plot == 'NZE':
		corridor_id = request.args.get('corridor_id', 0, type = int)
		start_date = request.args.get('start_date', 'NZE', type = str)
		end_date = request.args.get('end_date', 'NZE', type = str)
		output_format = request.args.get('output_format', 'Nothing', type = str)
		if output_format is 'Nothing':
			return db_access.query_by_corridor_group(corridor_id, start_date, end_date, target_plot = target_plot)
		else:
			return db_access.query_by_corridor_group(corridor_id, start_date, end_date, output_format = output_format,
			                                         target_plot = target_plot)


@app.route('/_query_by_acisa')
def query_by_acisa():
	#TimeString = request.args.get('TRange', 'Nothing', type = str)
	return jsonify(result = highchartdata())


@app.route('/_query_by_time_region')
def query_by_time_region():
	target_plot = request.args.get('target_plot', 'NZE', type = str)
	start_date = request.args.get('start_date', 'NZE', type = str)
	end_date = request.args.get('end_date', 'NZE', type = str)
	dir = request.args.get('dir', 'nothing', type = str)
	output_format = request.args.get('output_format', 'nothing', type = str)
	if dir == 'nothing':
		return jsonify(result = db_access.query_by_time_region(start_date, end_date, output_format = 'json', target_plot = target_plot))
	else:
		return jsonify(result = db_access.query_by_time_region(start_date, end_date, direction = dir, output_format = 'json',
		                                     target_plot = target_plot))


@app.route('/_query_corridor_intersections')
def query_corridor_intersections():
	corridor_id = request.args.get('corridor_id', 'NZE', type = str)
	start_date = request.args.get('start_date', 'NZE', type = str)
	end_date = request.args.get('end_date', 'NZE', type = str)
	output_format = request.args.get('output_format', 'NZE', type = str)
	target_plot = request.args.get('target_plot', 'NZE', type = str)
	dir = request.args.get('dir', 'NZE', type = str)
	return db_access.query_corridor_intersections(corridor_id, start_date, end_date, direction=dir, target_plot=target_plot)


@app.route('/_getcorridor')
def getcorridor():
	return db_access.getcorridor()


if __name__ == "__main__":
	app.run(debug = True, port = 5020)