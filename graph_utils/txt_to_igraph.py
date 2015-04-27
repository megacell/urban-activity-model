# This module imports .txt available on Hillel Bar-Gera's page of test problems
# http://www.bgu.ac.il/~bargera/tntp/

from igraph import *

__author__ = "jeromethai"


def txt_to_igrah(filepath, name):
    # Construct igraph object from networks available as .txt files in
    # http://www.bgu.ac.il/~bargera/tntp/
    return edge_dict_to_igraph(txt_to_edge_dict(filepath), name)


def txt_to_edge_dict(filepath):
    # Construct edge data from networks available as .txt files in 
    # http://www.bgu.ac.il/~bargera/tntp/
    header_passed = False
    edge_dict = {}
    with open(filepath) as f:
        for line in f.readlines():
            if header_passed == True:
                line = line.split()
                if len(line) == 0: break
                edge_dict[(int(line[0]), int(line[1]))] = {
                    'capacity': float(line[2]),
                    'length': float(line[3]),
                    'fftt': float(line[4]),
                    'B': float(line[5]),
                    'power': int(line[6]),
                    'speed_limit': float(line[7]),
                    'toll': float(line[8]),
                    'type': int(line[9][0]),
                    'weight': float(line[4])
                    }
            else:
                if line[0] == '~': header_passed = True
    return edge_dict


def edge_dict_to_igraph(edge_dict, name):
    # construct an igraph from edge_dict
    # edge_dict is a dictionary of dictionaries of the format
    # edge_dict[(s,t)] = {edge_attrs: values}
    g = Graph(edges=edge_dict.keys(), directed=True)
    g["name"] = name
    edge_attrs = edge_dict.values()[0].keys()
    for attr in edge_attrs:
        g.es[attr] = [x[attr] for x in edge_dict.values()]
    return g


def main():
    pass


if __name__ == "__main__":
    main()
