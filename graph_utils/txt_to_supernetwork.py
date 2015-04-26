# This module imports .txt to build a supernetwork

from igraph import *

__author__ = "jeromethai"


def txt_to_supernetwork(filepath, name):
    # Construct supernetwork from *_net_times.txt files
    pass


def txt_to_superedge_dict(filepath, alpha=1.0):
    # Contruct super edge data from *_net_times.txt files
    # alpha is a coefficient to translate travel times to travel costs
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
                    edge_dict[(s+i*num_nodes, t+i*num_nodes)] = {'weight': float(line[i+2]),
                                                                'type': -1}
            else:
                if line[0] == '~': header_passed = True
                if line[:17] == '<NUMBER OF NODES>':
                    num_nodes = int(line[17:])
                if line[:17] == '<NUMBER OF STEPS>':
                    num_steps = int(line[17:])
    return edge_dict


def txt_to_activities_edge_dict(filepath, shifting=True):
    # Add activity edges to edge_dict generated from txt_to_superedge_dict()
    # filepath contains list of activities from *_activities.txt
    header_passed = False
    edge_dict = {}
    with open(filepath) as f:
        for line in f.readlines():
            if header_passed == True:
                line = line.split()
                if len(line) == 0: break
                line[-1] = line[-1][:-1]
                node = int(line[0])
                start = int(line[1]) - start_time
                end = int(line[2]) - start_time
                t, r = int(line[3]), float(line[4])
                # note that we take start-1 since being on vertex v slice t
                # means only starting the activity at v at slice t+1
                edge = (node + (start-1)*num_nodes, node + end*num_nodes)
                edge_dict[edge] = {'weight': -r, 'type': t}
            else:
                if line[0] == '~': header_passed = True
                if line[:17] == '<NUMBER OF NODES>':
                    num_nodes = int(line[17:])
                if line[:12] == '<START TIME>':
                    start_time = int(line[12:])
                if line[:15] == '<HOME LOCATION>':
                    home = int(line[15:])
                if line[:17] == '<NUMBER OF STEPS>':
                    num_steps = int(line[17:])
        for i in range(num_steps-1):
            edge = (home+i*num_nodes, home+(i+1)*num_nodes)
            edge_dict[edge] = {'weight': 0., 'type': -1}
    return edge_dict


def compute_activity_weight_shifting(filepath):
    pass
