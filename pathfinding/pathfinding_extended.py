# This module implements some extensions of the pathfinding algorithms
# In particular, we allow some edges to have varying weights
# more specifically, each edge is associated with a type i in {0..N}
# we maintain a counter a=(2,1,...) meaning that
# edges of type 0 has been traversed twice, edges of type 1 traversed once etc.
# at the exception we do not count how many times edge of type -1 has been traversed
# we assume edges of type -1 do not have varying weights
# for each edge we have function modifier(edge, a) that modifies the weight of edge
# given the counter a.
# by convention modifier(edge, a) is constant for all a if edge is of type 0
# The pseudo-code is:

# Q = {(v,a): 0.0}
# while len(Q)>0:
#     get element (u,a) with least value (i.e. dist[u,a]) in Q
#     for all neighbor vertices n of u:
#         weight, (n,an) = modifier((u,n), a) // where (n,an) is neighbor element
#         if weight == np.inf: continue
#         alt = dist[u,a] + weight
#         if alt < dist[n, an]:
#             dist[n,an] = alt
#             prev[n,an] = u
#             Q(n,an) = alt

import numpy as np

__author__ = "jeromethai"


def dijkstra_extended(graph, v, to, modifier, mode="OUT", output="vpath"):
    # extension of dijkstra algorithm described at the beginning of file
    # v is a start vertex with a = (0,...,0)
    # to is a list of targets [(u,a)] with u the vertex and a the activity counter
    num_vs = graph.vcount()
    num_types = modifier()
    zero_tuple = tuple([0]*num_types)
    dist = [{} for i in range(num_vs)]
    dist[v][zero_tuple] = 0.0 # dist[v] = {a: dist} with a the activity counter
    prev = [{} for i in range(num_vs)]
    prev[v][zero_tuple] = -1 # prev[v] = {a: previous} with a the activity counter
    Q = {(v, zero_tuple): 0.0} # set of visited neighbors
    targets = dict.fromkeys(to,None) # set of target vertices

    while len(Q) > 0 and len(targets) > 0:
        e = min(Q, key=Q.get) # Get element e=(u,a) with the least value from Q
        dist_e = Q.pop(e) # pop key and get value
        if e in targets.keys(): targets.pop(e)
        for nv in graph.neighbors(e[0], mode="out"):
            edge = graph.es[graph.get_eid(e[0], nv)]
            weight, ne = modifier(edge, e[1]) # ne = (nv, nva)
            if weight == np.inf: continue
            alt = dist_e + weight
            if ne[1] not in dist[ne[0]].keys() or alt < dist[ne[0]][ne[1]]:
                dist[ne[0]][ne[1]] = alt
                prev[ne[0]][ne[1]] = e
                Q[ne] = alt
    if output == "vpath": return get_vpaths(prev, to)
    if output == "epath": pass


def get_vpaths(prev, to):
    vpaths = {} # constructed vpaths
    for e in to:
        if e[1] not in prev[e[0]].keys() or e in vpaths.keys() or prev[e[0]][e[1]]==-1: 
            continue
        previous  = prev[e[0]][e[1]]
        vpath = [e]
        while previous != -1 and previous not in vpaths.keys():
            vpath.append(previous)
            previous = prev[previous[0]][previous[1]]
        if previous in vpaths.keys(): vpath += vpaths[previous]
        vpaths[e] = vpath
        for i in range(1, len(vpath)-1):
            if vpath[i] not in vpaths.keys():
                vpaths[vpath[i]] = vpath[i:]
            else: break
    out = []
    for e in to:
        if e in vpaths.keys():
            # out.append(vpaths[e][::-1])
            out.append([i[0] for i in vpaths[e][::-1]])
        else:
            out.append([])
    return out



