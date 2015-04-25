import unittest
from graph_utils.txt_to_igraph import *

__author__ = 'jeromethai'


edge_attrs = ['capacity', 'length', 'fftt', 'B', 'power', 'speed_limit', 'toll', 
                'type']

# edge attributes of the Braess network
edge_data_braess = [[1.0, 100.0, 0.00000001, 1000000000.0, 1, 0.0, 0.0, 1],
             [1.0, 100.0, 50.0, 0.02, 1, 0.0, 0.0, 1],
             [1.0, 100.0, 50.0, 0.02, 1, 0.0, 0.0, 1],
             [1.0, 100.0, 10.0, 0.1, 1, 0.0, 0.0, 1],
             [1.0, 100.0, 0.00000001, 1000000000.0, 1, 0.0, 0.0, 1]]

# edges of the Braess network
edge_ids_braess = [(1,3), (1,4), (3,2), (3,4), (4,2)]

# a sample of edge attributes of the SiouxFalls network
edge_data_sioux = [[25900.20064, 6.0, 6.0, 0.15, 4, 0.0, 0.0, 1],
             [23403.47319, 4.0, 4.0, 0.15, 4, 0.0, 0.0, 1],
             [25900.20064, 6.0, 6.0, 0.15, 4, 0.0, 0.0, 1],
             [5078.508436, 2.0, 2.0, 0.15, 4, 0.0, 0.0, 1]]

# a sample of edges of the SiouxFalls network
edge_ids_sioux = [(1,2), (1,3), (2,1), (24,23)]


class TestTxtToIgraph(unittest.TestCase):


    def test_txt_to_edge_dict_Braess(self):

        edge_dict = txt_to_edge_dict('networks/Braess_net.txt')        
        for edge_id, data in zip(edge_ids_braess, edge_data_braess):
            edge = edge_dict[edge_id]
            for attr, value in zip(edge_attrs, data):
                self.assertTrue(edge[attr] == value)


    def test_txt_to_edge_dict_Sioux(self):

        edge_dict = txt_to_edge_dict('networks/SiouxFalls_net.txt')        
        for edge_id, data in zip(edge_ids_sioux, edge_data_sioux):
            edge = edge_dict[edge_id]
            for attr, value in zip(edge_attrs, data):
                self.assertTrue(edge[attr] == value)


    def test_edge_dict_to_igraph_Braess(self):
        edge_dict = {(4, 2): {'length': 100.0, 'B': 1000000000.0, 
            'capacity': 1.0, 'power': 1, 'toll': 0.0, 'fftt': 1e-08, 'type': 1, 
            'speed_limit': 0.0}, (3, 2): {'length': 100.0, 'B': 0.02, 
            'capacity': 1.0, 'power': 1, 'toll': 0.0, 'fftt': 50.0, 'type': 1, 
            'speed_limit': 0.0}, (1, 3): {'length': 100.0, 'B': 1000000000.0, 
            'capacity': 1.0, 'power': 1, 'toll': 0.0, 'fftt': 1e-08, 'type': 1, 
            'speed_limit': 0.0}, (3, 4): {'length': 100.0, 'B': 0.1, 
            'capacity': 1.0, 'power': 1, 'toll': 0.0, 'fftt': 10.0, 'type': 1, 
            'speed_limit': 0.0}, (1, 4): {'length': 100.0, 'B': 0.02, 
            'capacity': 1.0, 'power': 1, 'toll': 0.0, 'fftt': 50.0, 'type': 1, 
            'speed_limit': 0.0}}
        g = edge_dict_to_igraph(edge_dict, 'Braess')
        for edge in g.es:
            ind = edge_ids_braess.index(edge.tuple)
            for attr, data in zip(edge_attrs, edge_data_braess[ind]):
                self.assertTrue(edge[attr] == data)
            self.assertTrue(edge['weight'] >= edge['fftt'])


    def test_txt_to_igrah_Braess(self):
        g = txt_to_igrah('networks/Braess_net.txt', 'Braess')
        for edge in g.es:
            ind = edge_ids_braess.index(edge.tuple)
            for attr, data in zip(edge_attrs, edge_data_braess[ind]):
                self.assertTrue(edge[attr] == data)   
            self.assertTrue(edge['weight'] >= edge['fftt'])


    def test_txt_to_igrah_Sioux_2(self):
        g = txt_to_igrah('networks/SiouxFalls_net.txt', 'Sioux')
        for i, (source, target) in enumerate(edge_ids_sioux):
            edge = g.es[g.get_eid(source, target)] # find edge by source and target nodes
            for attr, data in zip(edge_attrs, edge_data_sioux[i]):
                self.assertTrue(edge[attr] == data)
            self.assertTrue(edge['weight'] >= edge['fftt'])



if __name__ == '__main__':
    unittest.main()
