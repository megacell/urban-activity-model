import unittest
from graph_utils.txt_to_supernetwork import *

__author__ = 'jeromethai'


edges = [(0,1),(1,0),(1,2),(2,1),(0,3),(3,0),
        (1,4),(4,1),(2,5),(5,2),(3,4),(4,3),
        (4,5),(5,4)]


weights = [[5, 10, 15, 15, 15, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 15, 15, 15, 10, 5],
            [5, 10, 15, 15, 15, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 15, 15, 15, 10, 5],
            [5, 7, 10, 10, 10, 7, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 7, 10, 10, 10, 7, 5],
            [5, 7, 10, 10, 10, 7, 5, 5, 5, 5, 7, 10, 10, 10, 7, 5],
            [5, 7, 10, 10, 10, 7, 5, 5, 5, 5, 7, 10, 10, 10, 7, 5],
            [5, 10, 15, 15, 15, 10, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 15, 15, 15, 10, 5],
            [5, 7, 10, 10, 10, 7, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 7, 10, 10, 10, 7, 5],
            [5, 7, 10, 10, 10, 7, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 7, 10, 10, 10, 7, 5]]


class TestTxtToSupernetwork(unittest.TestCase):

    def test_txt_to_superedge_dict(self):
        # test that edge data for the super network composed of road edges
        # is constructed correctly by txt_to_superedge_dict())
        # supernetwork has following geometry: 
        # (0)--(1)--(2)
        #  |    |    |
        # (3)--(4)--(5)
        # multilpied by 16 time steps of one hour between 5am and 9pm
        # each slice represents travel times during [5am, 6am], [6am, 7am] ...
        edge_dict = txt_to_superedge_dict('networks/SmallGrid_net_times.txt')
        num_steps = 16
        num_nodes = 6
        for j,(s,t) in enumerate(edges):
            for i in range(num_steps):
                edge = (s+i*num_nodes, t+i*num_nodes)
                self.assertTrue(edge_dict[edge]['weight'] == weights[j][i])
                self.assertTrue(edge_dict[edge]['type'] == -1)


    def test_add_activities_to_superedge_dict(self):
        # test that edge data for the super network composed of activity edges
        # is constructed correctly by txt_to_activities_edge_dict
        # see test_txt_to_superedge_dict(self) for details on the supernetwork
        # the home is at node 0
        # the mall is at node 2
        # the work is at mode 5
        num_nodes = 6
        num_steps = 16
        filepath = 'networks/SmallGrid_activities.txt'
        edge_dict = txt_to_activities_edge_dict(filepath, shifting=False)
        # check the work activity edges
        # they have type -1 (no counter needed) since they can be visited
        # at most once
        for start in [1, 2, 3]:
            for delta, reward in zip([9, 10, 11, 12], [320., 360., 400., 440.]):
                edge = (5 + start*num_nodes, 5 + (start+delta)*num_nodes)
                self.assertTrue(edge_dict[edge]['weight'] == -reward)
                self.assertTrue(edge_dict[edge]['type'] == -1)
        # check the home activity edges
        for i in range(num_steps-1):
            edge = (i*num_nodes, (i+1)*num_nodes)
            self.assertTrue(edge_dict[edge]['weight'] == 0.)
            self.assertTrue(edge_dict[edge]['type'] == -1)
        # check the mall activity edges
        for i in range(10):
            edge = (2 + (i+3)*num_nodes, 2 + (i+6)*num_nodes)
            self.assertTrue(edge_dict[edge]['weight'] == -200.)
            self.assertTrue(edge_dict[edge]['type'] == 0)


if __name__ == '__main__':
    unittest.main()