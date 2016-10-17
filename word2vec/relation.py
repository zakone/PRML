#coding:utf-8
import networkx as nx
import simplejson as json
import sys
import numpy
with open('word2vec/word2vec.model', 'r') as f:
	ss = f.readline().split()
	n_vocab, n_units = int(ss[0]), int(ss[1])
	word2index = {}
	index2word = {}
	w = numpy.empty((n_vocab, n_units), dtype=numpy.float32)
	for i, line in enumerate(f):
		ss = line.split()
		assert len(ss) == n_units + 1
		word = ss[0]
		word2index[word] = i
		index2word[i] = word
		w[i] = numpy.array([float(s) for s in ss[1:]], dtype=numpy.float32)

graph = nx.DiGraph()
d = json.load(open('network/graph.json'))
graph.add_nodes_from(d['nodes'])
graph.add_edges_from(d['edges'])


def  similarity(p,q):
	v = w[word2index[p]]
	similarity = w.dot(v)
	return similarity[word2index[q]]

def output(p, q) :
	if p not in word2index:
		print "can't find word p"
		print p
		return
	if q not in word2index:
		print "can't find word q"
		print q
		return

	graph.remove_edge(p, q)
	data = nx.dijkstra_path(graph, p,q)
	wait = pow(1 - similarity(p, q),2)
	graph.add_edge(p, q, weight=wait)
	for x in data:
	      print x.encode('utf-8')

try:
	while True:
	    	inputs = sys.stdin.readline().strip().split(',')
	    	output(inputs[0], inputs[1])
except EOFError:
	pass

