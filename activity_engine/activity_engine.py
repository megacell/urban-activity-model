# This module find optimal activities using a modification of Dijkstra's algorithm
# the urban network is described by two txt files
# file networks/SmallGrid_net_times.txt describes geometry with varying travel times
# file networks/SmallGrid_activities.txt describes the activities
# see module txt_to_supernetwork.py for mode details

from graph_utils.txt_to_supernetwork import txt_to_supernetwork


__author__ = "jeromethai"


def activity_engine(filepath_net, filepath_act, name="SuperNetwork", alpha=1.0):
    # alpha is a coefficient to translate travel times to travel costs
    g = txt_to_supernetwork(filepath_net, filepath_act, name)
    num_types = 
    num_nodes =
    num_steps =

    def modifier(edge=None, a=None):
        # a modifier that takes an edge and an activity in argument
        if edge is None and a is None:  
            return num_types # number of types
        w = edge['weight']
        i = edge['type']
        u = edge.tuple[1]
        if i == -1: return w, (u, a)
        if i >= 0 and a[i] == 0: return w, (u, a[:i]+(1,)+a[i+1:])
        if i >= 0 and a[i] == 1: return np.inf, -1

    to = None