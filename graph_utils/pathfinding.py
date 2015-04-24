# This module implements some pathfinding algorithms
import numpy as np
import heapq as hq

__author__ = "jeromethai"


def dijkstra(graph, v, to=None, weights=None, mode="OUT", output="vpath"):
    # simple python implementation of the get_shortest_paths() from igraph
    # https://pythonhosted.org/python-igraph/igraph.GraphBase-class.html#get_shortest_paths
    # check: http://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    num_vs = graph.vcount()
    dist = np.array([np.inf] * num_vs)
    dist[v] = 0.0
    prev = [-1] * num_vs
    Q = {v: 0.0} # set of visited neighbors

    while len(Q) > 0:
        u = min(Q, key=Q.get) # Get key with the least value from Q
        dist_u = Q.pop(u) # pop key and get value
        for neighbor in graph.neighbors(u, mode="out"):
            if weights is None: 
                weight = 1.0
            else:
                weight = graph.es[graph.get_eid(u, neighbor)][weights]
                assert weight >= 0.0
            alt = dist_u + weight
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = u
                Q[neighbor] = alt
    if output == "vpath": return get_vpaths(prev, to)
    if output == "epath": return get_epaths(graph, prev, to)


def dijkstra_with_heap(graph, v, to=None, weights=None, mode="OUT", output="vpath"):
    # improve implementation of dijkstra() with heap (or priority queue)
    # https://pythonhosted.org/python-igraph/igraph.GraphBase-class.html#get_shortest_paths
    # check: http://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    num_vs = graph.vcount()
    dist = np.array([np.inf] * num_vs)
    dist[v] = 0.0
    prev = [-1] * num_vs
    Q = {v: 0.0} # set of visited neighbors
    h = []
    hq.heappush(h, (0.0, v))

    while len(Q) > 0:
        #u = min(Q, key=Q.get) # Get key with the least value from Q
        u = hq.heappop(h)[1]
        dist_u = Q.pop(u) # pop key and get value
        for neighbor in graph.neighbors(u, mode="out"):
            if weights is None: 
                weight = 1.0
            else:
                weight = graph.es[graph.get_eid(u, neighbor)][weights]
                assert weight >= 0.0
            alt = dist_u + weight
            if alt < dist[neighbor]:
                prev[neighbor] = u
                Q[neighbor] = alt
                # update heap
                if dist[neighbor] == np.inf: # insert vertex
                    hq.heappush(h, (alt, neighbor))
                else: # to update vertex, have to reconstruct heap
                    h = []
                    for key,value in Q.items(): hq.heappush(h, (value, key))
                dist[neighbor] = alt

    if output == "vpath": return get_vpaths(prev, to)
    if output == "epath": return get_epaths(graph, prev, to)


def get_vpaths(prev, to=None):
    # if output == "vpath"
    # returns list of vertex IDs, one path for each target vertex
    # executed in dijkstra(ouput=="vpath")
    if to is None: to = range(len(prev))
    vpaths = {} # constructed vpaths
    for u in to:
        if u in vpaths.keys() or prev[u] == -1: continue # found path or u unreachable
        previous = prev[u]
        vpath = [u]
        while previous >= 0 and previous not in vpaths.keys():
            vpath.append(previous)
            previous = prev[previous]
        if previous in vpaths.keys(): vpath += vpaths[previous] # found subpath
        vpaths[u] = vpath # add it the constructed vpaths
        for i in range(1, len(vpath)-1): # add all subpaths to constructed paths
            if vpath[i] not in vpaths.keys():
                vpaths[vpath[i]] = vpath[i:]
            else: break
    out = []
    for u in to:
        if u in vpaths.keys(): 
            out.append(vpaths[u][::-1])
        else: 
            out.append([])
    return out


def get_epaths(graph, prev, to=None):
    # if output == "vpath" (resp. "epath")
    # returns list of vertex (resp. edge) IDs, one path for each target vertex
    # executed in dijkstra(ouput=="vpath") (resp. dijkstra(ouput=="epath"))
    if to is None: to = range(len(prev))
    epaths = {} # constructed paths
    for u in to:
        if u in epaths.keys() or prev[u] == -1: continue # found path or u unreachable
        previous = u
        epath, vpath = [], []
        while previous not in epaths.keys():
            tmp = previous
            previous = prev[previous]
            if previous == -1: break
            epath.append(graph.get_eid(previous, tmp))
            vpath.append(tmp)
        if previous in epaths.keys(): epath += epaths[previous] # found subpath
        epaths[u] = epath # add it the constructed paths
        for i in range(1, len(vpath)-1): # add all subpaths to constructed paths
            if vpath[i] not in epaths.keys():
                epaths[vpath[i]] = epath[i:]
            else: break
    out = []
    for u in to:
        if u in epaths.keys(): 
            out.append(epaths[u][::-1])
        else: 
            out.append([])
    return out
