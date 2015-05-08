# This module find optimal activities using a modification of Dijkstra's algorithm
# the urban network is described by two txt files
# file networks/SmallGrid_net_times.txt describes geometry with varying travel times
# file networks/SmallGrid_activities.txt describes the activities
# see module txt_to_supernetwork.py for mode details

from pathfinding.pathfinding_extended import dijkstra_extended
from graph_utils.txt_to_supernetwork import txt_to_supernetwork, read_metadata
import itertools
import numpy as np
import time

__author__ = "jeromethai"


def activity_engine(filepath_net, filepath_act, name="SuperNetwork", alpha=1.0):
    # alpha is a coefficient to translate travel times to travel costs
    # construct super network
    g = txt_to_supernetwork(filepath_net, filepath_act, name, alpha)
    # read metadata
    metadata = read_metadata(filepath_net)
    metadata.update(read_metadata(filepath_act))
    num_types = metadata['num_types']
    num_nodes = metadata['num_nodes']
    num_steps = metadata['num_steps']
    home = metadata['home_location']

    # construct modifier using metadata information
    # it modifies the weight of activity edge of type i to infinity if a[i]=1
    # if a[i]=0, it sets a[i] to 1
    def modifier(edge=None, a=None):
        # a modifier that takes an edge and an activity counter in argument
        # activity counter a is s.t. a[i] = #times activity of type i has been done
        if edge is None and a is None:  
            return num_types # number of types
        w = edge['weight']
        i = edge['type']
        u = edge.tuple[1]
        if i == -1: return w, (u, a)
        if i >= 0 and a[i] == 0: return w, (u, a[:i]+(1,)+a[i+1:])
        if i >= 0 and a[i] == 1: return np.inf, -1

    # initialize the targets (to, a) with 'a' all the possible activity vectors
    to = home + (num_steps-1)*num_nodes
    combinations = list(itertools.product([0, 1], repeat=num_types))
    targets = [(to,a) for a in combinations]

    # solves using a generalization of dijkstra algorithm
    raw = dijkstra_extended(g, home, targets, modifier)

    # translates back into trajectories on a time slice basis
    # format {activity: [(start, end, nodes visited)]}
    activities = raw_to_activity(raw, metadata)
    # get the costs {activity: costs}
    costs = raw_to_cost(raw, g, metadata)
    return activities, costs


def raw_to_activity(raw, metadata):
    # translates raw trajectory on the supernetwork 
    # into trajectories on a time slice basis 
    # format {activity: [(start, end, nodes visited)]}
    start_time = metadata['start_time']
    end_time = metadata['end_time']
    num_steps = metadata['num_steps']
    num_nodes = metadata['num_nodes']
    num_types = metadata['num_types']
    delta_t = float(end_time - start_time) / num_steps
    combinations = list(itertools.product([0, 1], repeat=num_types))
    out = {}
    for traj, a in zip(raw, combinations):
        if len(traj) == 0: 
            out[a] = []
            continue
        # start_time + v/num_nodes is the time slice associated to v
        # v%num_nodes is the location of vertex v
        pairs = [(start_time + delta_t * (v/num_nodes), v%num_nodes) for v in traj]
        # group by times
        starts = sorted(set(map(lambda x:x[0], pairs)))
        ends = [t + delta_t for t in starts]
        tmp = zip(starts, ends, [[y[1] for y in pairs if y[0]==x] for x in starts])
        out[a] = [e for e in tmp if len(e[2])>1]
    return out


def raw_to_cost(raw, graph, metadata):
    # get the costs of each raw trajectory {activity: costs}
    num_types = metadata['num_types']
    combinations = list(itertools.product([0, 1], repeat=num_types))
    out = {}
    for traj, a in zip(raw, combinations):
        if len(traj) == 0:
            out[a] = np.inf
            continue
        cost = 0.0
        for s,t in zip(traj[:-1],traj[1:]):
            cost += graph.es[graph.get_eid(s, t)]['raw_weight']
        out[a] = cost
    return out


def main():
    print "solves activity engine for a small grid network"
    filepath_net = 'networks/SmallGrid_net_times.txt'
    filepath_act = 'networks/SmallGrid_activities.txt'
    trajs, costs = activity_engine(filepath_net, filepath_act)
    print "optimal activity paths"
    print trajs[(0,)], costs[(0,)]
    print trajs[(1,)], costs[(1,)]
    print "optimal activity paths with finer time grid"
    filepath_net = 'networks/SmallGrid_net_times_32_steps.txt'
    filepath_act = 'networks/SmallGrid_activities_reduced.txt'
    trajs, costs = activity_engine(filepath_net, filepath_act)
    print trajs[(0,)], costs[(0,)]
    print trajs[(1,)], costs[(1,)]


if __name__ == '__main__':
    main()
