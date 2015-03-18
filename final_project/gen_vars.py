#fetch variables from mysql and turn them into useful lists
import pymysql
import pandas as pd
import numpy as np
import scipy.stats

dbname="dicegame"
host="localhost"
user="root"
passwd="computers"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')

cur = db.cursor()

#condition
#get_condition = """SELECT cond from dicegame;"""
#cur.execute(get_condition)
#cond_tupl = cur.fetchall()
#cond = []
#for i in cond_tupl:
#	extract = i[0]
#	cond.append(extract)

#bets 1-10 for each person
#tuples of id, condition, 10bets(for each condition, to be sorted later)



def createDiceDataFrame():
	get_bets = '''SELECT v1, cond, Q316, LS12, LS22, LS32, LS42, LS52, LS62, LS72, LS82, LS92, LC3_1, LC10, LC19, LC28, LC37, LC45, LC54, LC63, LC72, LC81, GC1, Q93, Q101, GC7, GC11, GC15, GC19, GC23, GC27, GC31, GS1, GS5, GS8_1, GS10, GS14, GS18, GS22, GS26, GS30, GS34, V10, Q114
			FROM dicegame;
			'''
	cur.execute(get_bets)
	dataTuples = cur.fetchall()

	#convert tuples to lists
	dataList = []
	for i in dataTuples:
		tuple_asList = []
		for x in i:
			entry = x
			tuple_asList.append(entry)
		dataList.append(tuple_asList)
	
	#get rid of extraneous quotations marks
	for i in dataList:
		for x in range(1,44):
			remove_quotes = i[x].replace("\'", "")
			i[x] = remove_quotes
	
	#drop nonfinishers (V10==0), and those who thought the dice were rigged (Q114==2)
	for i in dataList:
		if int(i[42]) == 0:
			dataList.remove(i)
			#print "Nonfinisher", i[0], "removed from dataset."
		elif int(i[43]) == 2:
			dataList.remove(i)
			#print "Participant", i[0], "removed from dataset due to suspicion of dice being rigged."
	
	#CREATE A LIST OF DICTIONARIES (TO USE IN DATAFRAME)
	subjectDicts_list = []
	for i in dataList:
		dictName = {}
		betList = ['bet1', 'bet2', 'bet3', 'bet4', 'bet5', 'bet6', 'bet7', 'bet8', 'bet9', 'bet10']
		dictName['subId'] = i[0]
		dictName['condition'] = i[1]
		if i[1] == "Loss Salient":
			dictName['Loss'] = 1
			dictName['Gain'] = 0
			dictName['Salient'] = 1
			dictName['Computer'] = 0
			indexCounter = 2
			for bet in betList:
				try:
					dictName[bet] = int(i[indexCounter])
				except ValueError:
					print "Encountered ValueError in", i[0], ". Entry added as 'missing'."
					dictName[bet] = 'missing'
				indexCounter += 1
		elif i[1] == "Loss Computer":
			dictName['Loss'] = 1
			dictName['Gain'] = 0
			dictName['Salient'] = 0
			dictName['Computer'] = 1
			indexCounter = 12
			for bet in betList:
				dictName[bet] = int(i[indexCounter])
				indexCounter += 1
		elif i[1] == "Gain Computer":
			dictName['Loss'] = 0
			dictName['Gain'] = 1
			dictName['Salient'] = 0
			dictName['Computer'] = 1
			indexCounter = 22
			for bet in betList:
				dictName[bet] = int(i[indexCounter])
				indexCounter += 1
		elif i[1] == "Gain Salient":
			dictName['Loss'] = 0
			dictName['Gain'] = 1
			dictName['Salient'] = 1
			dictName['Computer'] = 0
			indexCounter = 32
			for bet in betList:
				dictName[bet] = int(i[indexCounter])
				indexCounter += 1
		else:
			print "ERROR: Subject", i[0], "was not assigned to a condition."
	
		subjectDicts_list.append(dictName)
	
	#print len(subjectDicts_list), "entries added to list."
	#print subjectDicts_list
	
	dice_dataframe = pd.DataFrame(subjectDicts_list)

	return dice_dataframe

#print dice_df.describe()
#print dice_df


#PERFORM STATISTICAL TESTS

def ttest_2sample(group1, group2, dv):
	dice_df = createDiceDataFrame()
	#conditions = ['LS', 'LC', 'GS', 'GC', 'Loss', 'Gain', 'Salient', 'Computer']
	if group1 == 'LS':
		var1 = dice_df[(dice_df['Loss'] == 1) & (dice_df['Salient'] == 1)][dv]
	elif group1 == 'LC':
		var1 = dice_df[(dice_df['Loss'] == 1) & (dice_df['Computer'] == 1)][dv]
	elif group1 == 'GS':
		var1 = dice_df[(dice_df['Gain'] == 1) & (dice_df['Salient'] == 1)][dv]
	elif group1 == 'GC':
		var1 = dice_df[(dice_df['Gain'] == 1) & (dice_df['Computer'] == 1)][dv]
	elif group1 == 'Loss':
		var1 = dice_df[(dice_df['Loss'] == 1)][dv]
	elif group1 == 'Gain':
		var1 = dice_df[(dice_df['Gain'] == 1)][dv]
	elif group1 == 'Salient':
		var1 = dice_df[(dice_df['Salient'] == 1)][dv]
	elif group1 == 'Computer':
		var1 = dice_df[(dice_df['Computer'] == 1)][dv]

	#print var1

	if group2 == 'LS':
		var2 = dice_df[(dice_df['Loss'] == 1) & (dice_df['Salient'] == 1)][dv]
	elif group2 == 'LC':
		var2 = dice_df[(dice_df['Loss'] == 1) & (dice_df['Computer'] == 1)][dv]
	elif group2 == 'GS':
		var2 = dice_df[(dice_df['Gain'] == 1) & (dice_df['Salient'] == 1)][dv]
	elif group2 == 'GC':
		var2 = dice_df[(dice_df['Gain'] == 1) & (dice_df['Computer'] == 1)][dv]
	elif group2 == 'Loss':
		var2 = dice_df[(dice_df['Loss'] == 1)][dv]
	elif group2 == 'Gain':
		var2 = dice_df[(dice_df['Gain'] == 1)][dv]
	elif group2 == 'Salient':
		var2 = dice_df[(dice_df['Salient'] == 1)][dv]
	elif group2 == 'Computer':
		var2 = dice_df[(dice_df['Computer'] == 1)][dv]

	#print var2
	
	return scipy.stats.ttest_ind(var1, var2)

	#old var1 var2 code for only quadrants, not flexible
	#var1 = dice_df[dice_df['condition'] == group1][dv]
	#var2 = dice_df[dice_df['condition'] == group2][dv]

def ttest_2sample_display(group1, group2, dv):
	results_tupl = ttest_2sample(group1, group2, dv)
	t_val = results_tupl[0]
	p_val = results_tupl[1]
	print "The results of your t-test of", group1, "and", group2, "on", dv, "are as follows: \nt-value =", t_val, "\n", "p-value =", p_val



#ttest_2sample_display('Loss','Gain', 'bet10')
#ttest_2sample_display('Loss','Gain', 'bet10')