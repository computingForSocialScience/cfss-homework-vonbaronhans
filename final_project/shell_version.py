from flask import Flask, render_template, request
import pymysql
import pandas as pd
import numpy as np
import scipy.stats
from bokeh.plotting import figure
from bokeh.charts import BoxPlot
from bokeh.resources import CDN
from bokeh.embed import file_html, components
from gen_vars import ttest_2sample, createDiceDataFrame
from collections import OrderedDict, Counter

dbname="dicegame"
host="localhost"
user="root"
passwd="computers"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')


if __name__ == '__main__':
	group1 = "Loss"
	group2 = "Gain"
	dv = "bet5"
	results_tupl = ttest_2sample(group1, group2, dv)
	t_val = results_tupl[0]
	p_val = results_tupl[1]


	dice_df = createDiceDataFrame()

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



	#make ordered dictionary "bets"
	bets = OrderedDict(group1=var1,group2=var2)
	#bets[group1] = var1
	#bets[group2] = var2
	for key in bets.keys():
		l = bets[key]
		print Counter(l)
		
	# generate Bokeh HTML elements
    # create a `figure` object
	p = BoxPlot(bets, marker='circle', outliers=True, title="Boxplot of Results",
    xlabel="Experimental Group", ylabel="Bet", width=800, height=600,
    filename="boxplot.html")
    # create the HTML elements to pass to template
	figJS,figDiv = components(p,CDN)


