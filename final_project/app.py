from flask import Flask, render_template, request
import pymysql
import pandas as pd
import numpy as np
import scipy.stats
from bokeh.plotting import figure
from bokeh.charts import Bar
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from gen_vars import ttest_2sample, createDiceDataFrame
from collections import OrderedDict, Counter

dbname="dicegame"
host="localhost"
user="root"
passwd="computers"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

app = Flask(__name__)


@app.route('/')
def index():
    return(render_template('index.html'))


@app.route('/results/')
def resultsPage():
    # request.args is a dictionary with the form values
    # (the keys are the "name" attributes of the form elements,
    #  and the values are the data from the form.)
	group1 = request.args['formGroup1']
	group2 = request.args['formGroup2']
	dv = request.args['formDv']
	#print dv
	results_tupl = ttest_2sample(group1, group2, dv)
	t_val = round(results_tupl[0],4)
	p_val = round(results_tupl[1],4)
	
	dice_df = createDiceDataFrame()
	#descriptive statistics of dv
	dvStats = dice_df[dv].describe()
	dvCount = dvStats[0]
	dvMean = round(dvStats[1], 2)
	dvStd = dvStats[2]
	dvMin = dvStats[3]
	dv25 = dvStats[4]
	dv50 = dvStats[5]
	dv75 = dvStats[6]
	dvMax = dvStats[7]

	# we filter by groups that match the request and sort
	if group1 == 'LS':
		df = dice_df[(dice_df['Loss'] == 1) & (dice_df['Salient'] == 1)]
	elif group1 == 'LC':
		df = dice_df[(dice_df['Loss'] == 1) & (dice_df['Computer'] == 1)]
	elif group1 == 'GS':
		df = dice_df[(dice_df['Gain'] == 1) & (dice_df['Salient'] == 1)]
	elif group1 == 'GC':
		df = dice_df[(dice_df['Gain'] == 1) & (dice_df['Computer'] == 1)]
	else:
		df = dice_df[dice_df[group1] == 1]
		
	#print df
	var1 = df[dv].values
	#print var1

	if group2 == 'LS':
		df = dice_df[(dice_df['Loss'] == 1) & (dice_df['Salient'] == 1)]
	elif group2 == 'LC':
		df = dice_df[(dice_df['Loss'] == 1) & (dice_df['Computer'] == 1)]
	elif group2 == 'GS':
		df = dice_df[(dice_df['Gain'] == 1) & (dice_df['Salient'] == 1)]
	elif group2 == 'GC':
		df = dice_df[(dice_df['Gain'] == 1) & (dice_df['Computer'] == 1)]
	else:
		df = dice_df[dice_df[group2] == 1]

	var2 = df[dv].values


	#convert to lists of counts
	var1counter = Counter(var1)
	var2counter = Counter(var2)
	#fill in blanks with 0s
	die_values = [1,2,3,4,5,6]
	var1countDict = {}
	var2countDict = {}
	for value in die_values:
		if var1counter[value] == 0:
			var1countDict[value] = 0
		else:
			var1countDict[value] = var1counter[value]
	for value in die_values:
		if var2counter[value] == 0:
			var2countDict[value] = 0
		else:
			var2countDict[value] = var2counter[value]


	var1counts = [x for x in var1countDict.values()]
	var2counts = [x for x in var2countDict.values()]

	#make ordered dictionary "bets"
	#bets = OrderedDict('%s'=var1counts,'%s'=var2counts) % group1, group2
	bets = {}
	bets[group1] = var1counts
	bets[group2] = var2counts
	#print "Bet %s" % dv
 	#print bets
 	die_sides = ['1','2','3','4','5','6']
 	#plotd = OrderedDict(group1 = Counter(bets['group1']), group2 = Counter(bets['group2']))
	# generate Bokeh HTML elements
    # create a `figure` object
	p = Bar(bets, die_sides,title="Bar Chart of Results", xlabel="Bet on Die(d6) Roll", ylabel="Frequency", width=800, height=600, legend = "top_left")
    # create the HTML elements to pass to template
	figJS,figDiv = components(p,CDN)



	return(render_template('results.html',
		group1=group1,group2=group2,dv=dv,
		t_val=t_val,p_val=p_val, dvCount=dvCount, dvMean = dvMean, dvStd = dvStd,
		dvMin = dvMin, dv25=dv25, dv50=dv50, dv75=dv75, dvMax=dvMax,
		figJS=figJS,figDiv=figDiv))


if __name__ == '__main__':
    app.debug=True
    app.run()