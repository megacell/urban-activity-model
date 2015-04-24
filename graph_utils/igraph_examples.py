from igraph import *

# Possibly interesting examples of igraph usage
# http://laclefyoshi.blogspot.com/2011/08/basic-network-analysis-and.html
# https://gist.github.com/rbnvrw/c2424fe3ff812da892a0
# http://stackoverflow.com/questions/12058917/simple-python-igraph-usage

# Create the graph
print "Construct weighted directed graph with 7 vertices and 19 directed edges"
vertices = [i for i in range(7)]
edges = [(0,2),(0,1),(0,3),(1,0),(1,2),(1,3),(2,0),(2,1),(2,3),(3,0),(3,1),(3,2),(2,4),(4,5),(4,6),(5,4),(5,6),(6,4),(6,5)]
g = Graph(vertex_attrs={"label":vertices}, edges=edges, directed=True)
g["name"] = "Example graph"

print "\nGraph summary with verbosity=0"
# Check documentation: 
# http://igraph.org/python/doc/igraph.summary%27.GraphSummary-class.html
print g.summary()
print "\nGraph summary with verbosity=1"
print g.summary(verbosity=1)

print "\nAdd weight attibute to all edges at once"
g.es["weight"] = range(g.ecount())
print g.summary()

# Check documentation for shortest paths:
# http://igraph.org/python/doc/igraph.GraphBase-class.html#get_shortest_paths
print "\nCompute shortest (vertex) paths from vertex 2"
out = g.get_shortest_paths(2)
print out

print "\nCompute shortest (edge) paths from vertex 2"
out = g.get_shortest_paths(2, output="epath")
print out

print "\nCount number of vertices"
print g.vcount()

print "\nGet neighbors of vertex of index 0"
print g.neighbors(0,  mode="out")

print "\nGet weight of specific edge from source to target"
print g.es[g.get_eid(2, 3)]['weight']
# A C-implementation of k-shortest paths is available here:
# http://thinkingscale.com/k-shortest-paths-cpp-version/
