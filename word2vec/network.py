# coding:utf-8
import networkx as nx
import simplejson as json
import numpy
import six


with open('../word2vec/word2vec.model', 'r') as f:
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

count = 0
sample_words = []
for x in word2index:
	sample_words.append(x)
	count += 1
	if count > 10:
		break
print sample_words

for x in sample_words:
	graph.add_node(x)

for x in sample_words:
	v = w[word2index[x]]
	similarity = w.dot(v)
	for i in (-similarity).argsort():
		wait = pow(1 - similarity[i], 2)
		graph.add_edge(x, index2word[i], weight=wait)

json.dump(dict(nodes=[[n, graph.node[n]] for n in graph.nodes()],
                   edges=[[u, v, graph.edge[u][v]] for u,v in graph.edges()]),
              open('graph.json', 'w'), indent=2 )