# This module imports .txt to build a supernetwork

# What is a supernetwork? Here is an example:

# file networks/SmallGrid_net_times.txt describes a network of geometry
# (0)--(1)--(2)
#  |    |    |
# (3)--(4)--(5)
# multilpied by 16 time steps of one hour between 5am and 9pm
# slice 0 is the following with travel time during (5am, 6am]:
# (0)--(1)--(2)
#  |    |    |
# (3)--(4)--(5)
# slice 1 is the following with travel time during (6am, 7am]:
# (6)--(7)---(8)
#  |    |     |
# (9)--(10)--(11)
# and so on ...

# file networks/SmallGrid_activities.txt describes the activities
# activity edges are edges across time slices
# staying at home is following path 0-6-12-...
# staying at mall located at node 2 between 8am amd 10am means taking edge
# from vertex loc + (start-1) * num_nodes = 2+2*6 = 14 
# to vertex loc + end * num_nodes = 2+5*6 = 32 
# loc = 2 because mall is at node 2, num_nodes = 6
# start-1=2 because activity starts sometime in (7am,8am]
# end=5 because activity ends at 10am and driver is on the road at (10am,11am]
# edge of type -1 means that user can take edge any number of times
# edge of type 0,1,... means user can only take it a limited number of times
# hence mall is of type 0
# work is type -1 because user can only take it once (start times < end times)

from igraph import *
from graph_utils.txt_to_igraph import edge_dict_to_igraph
import numpy as np

__author__ = "jeromethai"


def txt_to_supernetwork(filepath_net, filepath_act, name="SuperNetwork", 
    alpha=1.0, shifting=True):
    # alpha is a coefficient to translate travel times to travel costs
    # Construct supernetwork from *_net_times.txt files
    # and from *_activities.txt file
    edge_dict = txt_to_superedge_dict(filepath_net, alpha)
    edge_activities_dict = txt_to_activities_edge_dict(filepath_act, shifting)
    edge_dict.update(edge_activities_dict)
    return edge_dict_to_igraph(edge_dict, name)


def txt_to_superedge_dict(filepath, alpha=1.0):
    # Contruct super edge data from *_net_times.txt files
    # alpha is a coefficient to translate travel times to travel costs
    # see networks/SmallGrid_net_times.txt for example
    metadata = read_metadata(filepath)
    num_nodes = metadata['num_nodes']
    num_steps = metadata['num_steps']

    header_passed = False
    edge_dict = {}
    with open(filepath) as f:
        for line in f.readlines():
            if header_passed == True:
                line = line.split()
                if len(line) == 0: break
                line[-1] = line[-1][:-1]
                s = int(line[0])
                t = int(line[1])
                for i in range(num_steps):
                    edge_dict[(s+i*num_nodes, t+i*num_nodes)] = {'weight': alpha*float(line[i+2]),
                                                                'type': -1}
            else:
                if line[0] == '~': header_passed = True
    return edge_dict


def txt_to_activities_edge_dict(filepath, shifting=True):
    # Add activity edges to edge_dict generated from txt_to_superedge_dict()
    # filepath contains list of activities from *_activities.txt
    # see networks/SmallGrid_activities.txt for example
    # activity weights are < 0 because equal to minus reward
    # if shifting is True, the activity weights are shifted by 
    # (end-start+1)*shift to make activity edges positive
    metadata = read_metadata(filepath)
    num_nodes = metadata['num_nodes']
    start_time = metadata['start_time']
    home = metadata['home_location']
    num_steps = metadata['num_steps']

    header_passed = False
    edge_dict = {}
    tmp = []
    shift = 0.0
    with open(filepath) as f:
        for line in f.readlines():
            if header_passed == True:
                line = line.split()
                if len(line) == 0: break
                line[-1] = line[-1][:-1]
                node = int(line[0])
                start = int(line[1]) - start_time
                end = int(line[2]) - start_time
                assert 0 < start < end < num_steps
                type_edge = int(line[3])
                reward = float(line[4])
                # note that we take start-1 since being on vertex v slice t
                # means only starting the activity at v at slice t+1
                duration = 1+end-start
                if shifting and shift < reward/duration: 
                    shift = np.ceil(reward/duration)
                edge = (node + (start-1)*num_nodes, node + end*num_nodes)
                tmp.append([edge, type_edge, reward, duration])
            else:
                if line[0] == '~': header_passed = True
        for edge, type_edge, reward, duration in tmp:
            edge_dict[edge] = {'weight': -reward + duration*shift, 'type': type_edge}
        for i in range(num_steps-1):
            edge = (home+i*num_nodes, home+(i+1)*num_nodes)
            edge_dict[edge] = {'weight': shift, 'type': -1}
    return edge_dict


def read_metadata(filepath):
    # read metadata in .txt files
    # entries is a list of entries, 
    # e.g. ['num_nodes', 'start_time', 'home_location', 'num_steps']
    metadata = {}
    with open(filepath) as f:
        for line in f.readlines():
            if line[0] == '~': break
            if line[:17] == '<NUMBER OF NODES>': 
                metadata['num_nodes'] = int(line[17:])
            if line[:12] == '<START TIME>': 
                metadata['start_time'] = int(line[12:])
            if line[:15] == '<HOME LOCATION>': 
                metadata['home_location'] = int(line[15:])
            if line[:17] == '<NUMBER OF STEPS>': 
                metadata['num_steps'] = int(line[17:])
            if line[:17] == '<NUMBER OF TYPES>':
                metadata['num_types'] = int(line[17:])
            if line[:10] == '<END TIME>':
                metadata['end_time'] = int(line[10:])
    return metadata

