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
    edge_activities_dict = txt_to_activities_edge_dict(filepath_act, 
        read_metadata(filepath_net), shifting)
    edge_dict.update(edge_activities_dict)
    return edge_dict_to_igraph(edge_dict, name)


def txt_to_superedge_dict(filepath_net, alpha=1.0):
    # Contruct super edge data from *_net_times.txt files
    # alpha is a coefficient to translate travel times to travel costs
    # see networks/SmallGrid_net_times.txt for example
    # the format is edge_dict =
    # {(start_node, end_node): {'weight': x, 'type': y, 'raw_weight': z}}
    metadata = read_metadata(filepath_net)
    num_nodes = metadata['num_nodes']
    num_steps = metadata['num_steps']
    header_passed = False
    edge_dict = {}
    with open(filepath_net) as f:
        for line in f.readlines():
            if header_passed == True:
                line = line.split()
                if len(line) == 0: break
                line[-1] = line[-1][:-1]
                s = int(line[0])
                t = int(line[1])
                for i in range(num_steps):
                    edge_dict[(s+i*num_nodes, t+i*num_nodes)] = {'weight': alpha*float(line[i+2]),
                                                                'type': -1,
                                                                'raw_weight': float(line[i+2])}
            else:
                if line[0] == '~': header_passed = True
    return edge_dict


def txt_to_activities_edge_dict(filepath_act, metadata, shifting=True):
    # generate dictionary of activity edges from file *_activities.txt
    # see networks/SmallGrid_activities.txt for example
    # activity weights are < 0 because equal to minus reward
    # if shifting is True, the activity weights are shifted by 
    # (end-start+1)*shift to make activity edges positive
    edge_dict = {}
    metadata_act = read_metadata(filepath_act)
    home = metadata_act['home_location']
    explicit = metadata_act['explicit']
    num_steps = metadata['num_steps']
    num_nodes = metadata['num_nodes']
    if explicit == 1:
        activities, shift = snap_activities_to_time_grid_get_shift(filepath_act, metadata)
    else:
        activities, shift = txt_to_activities(filepath_act, metadata)
    if shifting is False: shift = 0.0
    # add normal activity edges
    for edge, (type_edge, reward, duration) in activities.items():
        edge_dict[edge] = {'weight': -reward + duration*shift, 'type': type_edge, 
                            'raw_weight': -reward}
    # add home activity edges
    for i in range(num_steps-1):
        edge = (home+i*num_nodes, home+(i+1)*num_nodes)
        edge_dict[edge] = {'weight': shift, 'type': -1, 'raw_weight': 0.0}
    return edge_dict


def snap_activities_to_time_grid_get_shift(filepath_act, metadata):
    # read a file *_activities.txt and metadata on the supernetwork
    # when *_activities.txt gives EXPLICIT TIMES
    # returns list of processed activities
    # activities[edge] = [type_edge, reward, duration]
    # where edge = (start_node, end_node) in the supernetwork
    # type_edge is the type of the activity and reward = -cost
    # duration = number of time steps between end_node and start_node
    start_time = metadata['start_time']
    end_time = metadata['end_time']
    num_steps = metadata['num_steps']
    num_nodes = metadata['num_nodes']
    delta_t = float(end_time - start_time) / num_steps
    header_passed = False
    activities = {}
    shift = 0.0
    with open(filepath_act) as f:
        for line in f.readlines():
            if header_passed == True:
                line = line.split()
                if len(line) == 0: break
                line[-1] = line[-1][:-1]
                node = int(line[0])
                # snap start to the closest time slice
                start = int(round((float(line[1]) - start_time) / delta_t))
                # snap end to the closest time slice
                end = int(round((float(line[2]) - start_time) / delta_t))
                # check if the activity is within the time span of the supernetwork
                if 0 < start <= end < num_steps:
                    type_edge = int(line[3])
                    reward = float(line[4])
                    # note that we take start-1 since being on vertex v slice t
                    # means only starting the activity at v at slice t+1
                    duration = 1+end-start
                    if shift < reward/duration: shift = np.ceil(reward/duration)
                    edge = (node + (start-1)*num_nodes, node + end*num_nodes)
                    activities[edge] = [type_edge, reward, duration]
            else:
                if line[0] == '~': header_passed = True
    return activities, shift


def txt_to_activities(filepath_act, metadata):
    # read a file *_activities.txt and metadata on the supernetwork
    # when *_activities.txt gives IMPLICIT TIMES, 
    # i.e. only start time, end time, min time, max time
    # return list of possible activities in the same of format as
    # snap_activities_to_time_grid_get_shift()
    start_time = metadata['start_time']
    end_time = metadata['end_time']
    num_steps = metadata['num_steps']
    num_nodes = metadata['num_nodes']
    delta_t = float(end_time - start_time) / num_steps
    header_passed = False
    activities = {}
    shift = 0.0
    with open(filepath_act) as f:
        for line in f.readlines():
            if header_passed == True:
                line = line.split()
                if len(line) == 0: break
                line[-1] = line[-1][:-1]
                # get attributes of each line
                node = int(line[0])
                type_edge = int(line[1])
                # reward per unit of time
                reward = float(line[2]) * delta_t
                deprecation = float(line[3])
                # snap start and end times to the closest time slice
                start = int(round((float(line[4]) - start_time) / delta_t))
                start = max(start, 1)
                end = int(round((float(line[5]) - start_time) / delta_t))
                end = min(end, num_steps-1)
                if start >= end: continue
                # snap min and max times to the grid
                min_time = int(round(float(line[6]) / delta_t))
                max_time = int(round(float(line[7]) / delta_t))
                if min_time > max_time or min_time >= num_steps: continue
                base_reward = reward*min_time
                # all possible combinations of start and end times
                for s,t in all_times_combinations(start, end, min_time, max_time):
                    # note that we take start-1 since being on vertex v slice t
                    # means only starting the activity at v at slice t+1
                    edge = (node + (s-1)*num_nodes, node + t*num_nodes)
                    duration = 1+t-s
                    extra_time = duration-1-min_time
                    # compute extra_reward given deprecation
                    if extra_time > 0 and deprecation == 1.0:
                        extra_reward = reward * extra_time
                    if extra_time > 0 and deprecation != 1.0:
                        alpha = (deprecation - deprecation**(extra_time+1)) / (1-deprecation)
                        extra_reward = reward * alpha
                    # append activity edge information to the list
                    total_reward = base_reward + reward * extra_time
                    activities[edge] = [type_edge, total_reward, duration]
                    if shift < total_reward/duration: 
                        shift = np.ceil(total_reward/duration)
            else:
                if line[0] == '~': header_passed = True
    return activities, shift


def all_times_combinations(start, end, min_time, max_time):
    # compute all time combinations of activities of min_time, max_time
    # available between start and end when all are integers
    times = []
    for i in range(start, end - min_time + 1):
        for j in range(min_time, 1+ min(max_time , end-i)):
            times.append((i, i+j))
    return times


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
            if line[:17] == '<NUMBER OF LINKS>': 
                metadata['num_links'] = int(line[17:])
            if line[:10] == '<EXPLICIT>':
                metadata['explicit'] = int(line[10:])
    return metadata

