import pandas as pd
import networkx as nx
import numpy as np

def readEdgeList(filename):
	edgeList = pd.read_csv(filename)
	edgeList.columns = ['Artist','Related_Artist']
	if len(edgeList.columns) != 2 :
		return "Edge List should only have 2 columns"
	return edgeList

def degree(edgeList, in_or_out):
	if in_or_out == 'out':
		degree = edgeList['Artist'].value_counts()
	if in_or_out == 'in':
		degree = edgeList['Related_Artist'].value_counts()
	#print "degree is", degree
	return degree

def combineEdgeLists(edgeList1, edgeList2):
	pieces = [edgeList1, edgeList2]
	concatenated = pd.concat(pieces)
	concat_nodup = concatenated.drop_duplicates()
	return concat_nodup

def pandasToNetworkX(edgeList):
	g = nx.DiGraph()
	for Artist, Related_Artist in edgeList.to_records(index=False):
		g.add_edge(Artist,Related_Artist)
	return g

def randomCentralNode(inputDiGraph):
	eigen_nodes_dict = nx.eigenvector_centrality(inputDiGraph)
	normal_denominator = 0
	#print eigen_nodes_dict
	for node in eigen_nodes_dict:
		#print node
		#print eigen_nodes_dict[node]
		normal_denominator += eigen_nodes_dict[node]
		#print normal_denominator
	for node in eigen_nodes_dict:
		#print eigen_nodes_dict, normal_denominator
		try: 
			newval = eigen_nodes_dict[node]/normal_denominator
		except ZeroDivisionError:
			newval = 1.0 / len(eigen_nodes_dict)
		eigen_nodes_dict[node] = newval
	#return eigen_nodes_dict
	random_node = np.random.choice(eigen_nodes_dict.keys(), p=eigen_nodes_dict.values())
	return random_node


#tests

#x = readEdgeList("Busta's Bruthas.csv")
#y = readEdgeList("Punch Bruthas.csv")
#print x
#print x.shape
#print len(x.columns)

#xy = combineEdgeLists(x,y)
#print xy.shape

#g = pandasToNetworkX(xy)
#print g.nodes()
#print g.edges(data=True)
#print g.number_of_edges()

#print randomCentralNode(g)




