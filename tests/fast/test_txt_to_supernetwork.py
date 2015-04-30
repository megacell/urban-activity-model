import unittest
from graph_utils.txt_to_supernetwork import *
import numpy as np

__author__ = 'jeromethai'


# edges in the base network
edges = [(0,1),(1,0),(1,2),(2,1),(0,3),(3,0),
        (1,4),(4,1),(2,5),(5,2),(3,4),(4,3),
        (4,5),(5,4)]

# travel times in the super network with 16 time slices
# this is contained in networks/SmallGrid_net_times.txt
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
        # each slice represents travel times during (5am, 6am], (6am, 7am] ...
        edge_dict = txt_to_superedge_dict('networks/SmallGrid_net_times.txt')
        num_steps = 16
        num_nodes = 6
        for j,(s,t) in enumerate(edges):
            for i in range(num_steps):
                edge = (s+i*num_nodes, t+i*num_nodes)
                self.assertTrue(edge_dict[edge]['weight'] == weights[j][i])
                self.assertTrue(edge_dict[edge]['raw_weight'] == weights[j][i])
                self.assertTrue(edge_dict[edge]['type'] == -1)


    def test_txt_to_superedge_dict_2(self):
        # test that edge data for the super network composed of road edges
        # is constructed correctly by txt_to_superedge_dict())
        # supernetwork has following geometry: 
        # (0)--(1)--(2)
        #  |    |    |
        # (3)--(4)--(5)
        # note that it is multiplied by 32 time steps for 30min between
        # 5am and 9pm, each slice representing travel times during 
        # (5am, 5:30am], (5:30am, 6pm] ...
        edge_dict = txt_to_superedge_dict('networks/SmallGrid_net_times_32_steps.txt')
        num_steps = 32
        num_nodes = 6
        for j,(s,t) in enumerate(edges):
            for i in range(num_steps/2):
                edge = (s+2*i*num_nodes, t+2*i*num_nodes)
                self.assertTrue(edge_dict[edge]['weight'] == weights[j][i])
                self.assertTrue(edge_dict[edge]['raw_weight'] == weights[j][i])
                self.assertTrue(edge_dict[edge]['type'] == -1)
                edge = (s+(2*i+1)*num_nodes, t+(2*i+1)*num_nodes)
                if i < 15:
                    weight = np.floor((weights[j][i] + weights[j][i+1]) / 2)
                else:
                    weight = 5.
                self.assertTrue(edge_dict[edge]['weight'] == weight)
                self.assertTrue(edge_dict[edge]['raw_weight'] == weight)
                self.assertTrue(edge_dict[edge]['type'] == -1)


    def test_txt_to_activities_edge_dict_without_shift(self):
        # test that edge data for the super network composed of activity edges
        # is constructed correctly by txt_to_activities_edge_dict
        # note that shifting = False
        # see test_txt_to_superedge_dict(self) for details on the supernetwork
        # the home is at node 0
        # the mall is at node 2
        # the work is at node 5
        metadata = {'start_time': 5,
                    'end_time': 21,
                    'num_steps': 16,
                    'num_nodes': 6}
        num_nodes = 6
        num_steps = 16
        filepath = 'networks/SmallGrid_activities.txt'
        edge_dict = txt_to_activities_edge_dict(filepath, metadata, shifting=False)
        # check the work activity edges
        # they have type -1 (no counter needed) since they can be visited
        # at most once
        for start in [1, 2, 3]:
            for delta, reward in zip([9, 10, 11, 12], [320., 360., 400., 440.]):
                edge = (5 + start*num_nodes, 5 + (start+delta)*num_nodes)
                # we recall that for this test, shifting = False
                self.assertTrue(edge_dict[edge]['weight'] == -reward)
                self.assertTrue(edge_dict[edge]['raw_weight'] == -reward)
                self.assertTrue(edge_dict[edge]['type'] == -1)
        # check the home activity edges
        for i in range(num_steps-1):
            edge = (i*num_nodes, (i+1)*num_nodes)
            self.assertTrue(edge_dict[edge]['weight'] == 0.)
            self.assertTrue(edge_dict[edge]['raw_weight'] == 0.)
            self.assertTrue(edge_dict[edge]['type'] == -1)
        # check the mall activity edges
        for i in range(11):
            edge = (2 + (i+2)*num_nodes, 2 + (i+5)*num_nodes)
            self.assertTrue(edge_dict[edge]['weight'] == -200.)
            self.assertTrue(edge_dict[edge]['raw_weight'] == -200.)
            self.assertTrue(edge_dict[edge]['type'] == 0)


    def test_txt_to_activities_edge_dict_with_shift(self):
        # test that edge data for the super network composed of activity edges
        # is constructed correctly by txt_to_activities_edge_dict
        # see test_txt_to_superedge_dict(self) for details on the supernetwork
        # the home is at node 0
        # the mall is at node 2
        # the work is at mode 5
        metadata = {'start_time': 5,
                    'end_time': 21,
                    'num_steps': 16,
                    'num_nodes': 6}
        num_nodes = 6
        num_steps = 16
        shift = 67.0
        filepath = 'networks/SmallGrid_activities.txt'
        edge_dict = txt_to_activities_edge_dict(filepath, metadata)
        # check the work activity edges
        # they have type -1 (no counter needed) since they can be visited
        # at most once
        for start in [1, 2, 3]:
            for delta, reward in zip([9, 10, 11, 12], [320., 360., 400., 440.]):
                edge = (5 + start*num_nodes, 5 + (start+delta)*num_nodes)
                shifted_reward = -reward + delta*shift
                self.assertTrue(shifted_reward > 0)
                self.assertTrue(edge_dict[edge]['weight'] == shifted_reward)
                self.assertTrue(edge_dict[edge]['raw_weight'] == -reward)
                self.assertTrue(edge_dict[edge]['type'] == -1)
        # check the home activity edges
        for i in range(num_steps-1):
            edge = (i*num_nodes, (i+1)*num_nodes)
            self.assertTrue(edge_dict[edge]['weight'] == shift)
            self.assertTrue(edge_dict[edge]['raw_weight'] == 0.)
            self.assertTrue(edge_dict[edge]['type'] == -1)
        # check the mall activity edges
        self.assertTrue(-200. + 3*shift > 0.)
        for i in range(10):
            edge = (2 + (i+3)*num_nodes, 2 + (i+6)*num_nodes)
            self.assertTrue(edge_dict[edge]['weight'] == -200. + 3*shift)
            self.assertTrue(edge_dict[edge]['raw_weight'] == -200.)
            self.assertTrue(edge_dict[edge]['type'] == 0)


    def test_txt_to_supernetwork(self):
        num_steps = 16
        num_nodes = 6
        shift = 67.0
        filepath_net = 'networks/SmallGrid_net_times.txt'
        filepath_act = 'networks/SmallGrid_activities.txt'
        g = txt_to_supernetwork(filepath_net, filepath_act, 'SmallGrid')
        # check road edges
        for j,(s,t) in enumerate(edges):
            for i in range(num_steps):
                edge = g.es[g.get_eid(s+i*num_nodes, t+i*num_nodes)]
                self.assertTrue(edge['weight'] == weights[j][i])
                self.assertTrue(edge['type'] == -1)
        # check work activity edges
        for start in [1, 2, 3]:
            for delta, reward in zip([9, 10, 11, 12], [320., 360., 400., 440.]):
                edge = g.es[g.get_eid(5+start*num_nodes, 5+(start+delta)*num_nodes)]
                shifted_reward = -reward + delta*shift
                self.assertTrue(shifted_reward > 0)
                self.assertTrue(edge['weight'] == shifted_reward)
                self.assertTrue(edge['type'] == -1)
        # check home activity edges
        for i in range(num_steps-1):
            edge = g.es[g.get_eid(i*num_nodes, (i+1)*num_nodes)]
            self.assertTrue(edge['weight'] == shift)
            self.assertTrue(edge['type'] == -1)
        # check the mall activity edges
        self.assertTrue(-200. + 3*shift > 0.)
        for i in range(11):
            edge = g.es[g.get_eid(2+(i+2)*num_nodes, 2+(i+5)*num_nodes)]
            self.assertTrue(edge['weight'] == -200. + 3*shift)
            self.assertTrue(edge['type'] == 0)


    def test_txt_to_supernetwork_2(self):
        num_steps = 32
        num_nodes = 6
        shift = 40.0
        filepath_net = 'networks/SmallGrid_net_times_32_steps.txt'
        filepath_act = 'networks/SmallGrid_activities.txt'
        g = txt_to_supernetwork(filepath_net, filepath_act, 'SmallGrid')
        # check road edges
        for j,(s,t) in enumerate(edges):
            for i in range(num_steps/2):
                edge = g.es[g.get_eid(s+2*i*num_nodes, t+2*i*num_nodes)]
                self.assertTrue(edge['weight'] == weights[j][i])
                self.assertTrue(edge['raw_weight'] == weights[j][i])
                self.assertTrue(edge['type'] == -1)
                edge = g.es[g.get_eid(s+(2*i+1)*num_nodes, t+(2*i+1)*num_nodes)]
                if i < 15:
                    weight = np.floor((weights[j][i] + weights[j][i+1]) / 2)
                else:
                    weight = 5.
                self.assertTrue(edge['weight'] == weight)
                self.assertTrue(edge['raw_weight'] == weight)
                self.assertTrue(edge['type'] == -1)
        # check work activity edges
        for start in [3, 5, 7]:
            for delta, reward in zip([17, 19, 21, 23], [320., 360., 400., 440.]):
                edge = g.es[g.get_eid(5+start*num_nodes, 5+(start+delta)*num_nodes)]
                self.assertTrue(edge['weight'] == -reward + delta*shift)
                self.assertTrue(edge['raw_weight'] == -reward)
                self.assertTrue(edge['type'] == -1)
        # check mall activity edges
        self.assertTrue(-200. + 5*shift >= 0.)
        for i in range(11):
            edge = g.es[g.get_eid(2+(2*i+5)*num_nodes, 2+(2*i+10)*num_nodes)]
            self.assertTrue(edge['weight'] == -200. + 5*shift)
            self.assertTrue(edge['raw_weight'] == -200.)
            self.assertTrue(edge['type'] == 0)
        # check home edges
        for i in range(num_steps-1):
            edge = g.es[g.get_eid(i*num_nodes, (i+1)*num_nodes)]
            self.assertTrue(edge['weight'] == shift)
            self.assertTrue(edge['type'] == -1)


    def test_snap_activities_to_time_grid_get_shift(self):
        # test snapping of activities on time grid of 16 time steps
        # between 5am and 9pm 
        filepath_act = 'networks/SmallGrid_activities.txt'
        num_nodes = 6
        metadata = {'start_time': 5,
                    'end_time': 21,
                    'num_steps': 16,
                    'num_nodes': 6}
        out, shift = snap_activities_to_time_grid_get_shift(filepath_act, metadata)
        self.assertTrue(shift == 67)
        # check work activity edges
        for start in [1, 2, 3]:
            for delta, reward in zip([9, 10, 11, 12], [320., 360., 400., 440.]):
                edge = (5+start*num_nodes, 5+(start+delta)*num_nodes)
                self.assertTrue(out[edge] == [-1, reward, delta])
        # check mall activity edges
        self.assertTrue(-200. + 3*shift >= 0.)
        for i in range(11):
            edge = (2+(i+2)*num_nodes, 2+(i+5)*num_nodes)
            self.assertTrue(out[edge] == [0, 200., 3])


    def test_snap_activities_to_time_grid_get_shift_2(self):
        # test snapping of activities on time grid of 32 time steps
        # between 5am and 9pm
        filepath_act = 'networks/SmallGrid_activities.txt'
        num_nodes = 6
        metadata = {'start_time': 5,
                    'end_time': 21,
                    'num_steps': 32,
                    'num_nodes': 6}
        out, shift = snap_activities_to_time_grid_get_shift(filepath_act, metadata)
        self.assertTrue(shift == 40)
        # check work activity edges
        for start in [3, 5, 7]:
            for delta, reward in zip([17, 19, 21, 23], [320., 360., 400., 440.]):
                edge = (5+start*num_nodes, 5+(start+delta)*num_nodes)
                self.assertTrue(out[edge] == [-1, reward, delta])
        # check mall activity edges
        self.assertTrue(-200. + 5*shift >= 0.)
        for i in range(11):
            edge = (2+(2*i+5)*num_nodes, 2+(2*i+10)*num_nodes)
            self.assertTrue(out[edge] == [0, 200., 5])


    def test_txt_to_activities(self):
        filepath_act = 'networks/SmallGrid_activities_reduced.txt'
        num_nodes = 6
        metadata = {'start_time': 5,
            'end_time': 21,
            'num_steps': 16,
            'num_nodes': 6}
        out, shift = txt_to_activities(filepath_act, metadata)
        self.assertTrue(shift == 67)
        # check work activity edges
        for start in [1, 2, 3]:
            for delta, reward in zip([9, 10, 11, 12], [320., 360., 400., 440.]):
                edge = (5+start*num_nodes, 5+(start+delta)*num_nodes)
                self.assertTrue(out[edge] == [-1, reward, delta])
        # check mall activity edges
        self.assertTrue(-200. + 3*shift >= 0.)
        for i in range(11):
            edge = (2+(i+2)*num_nodes, 2+(i+5)*num_nodes)
            self.assertTrue(out[edge] == [0, 200., 3])


    def test_txt_to_activities_2(self):
        filepath_act = 'networks/SmallGrid_activities_reduced.txt'
        num_nodes = 6
        metadata = {'start_time': 5,
            'end_time': 21,
            'num_steps': 32,
            'num_nodes': 6}
        out, shift = txt_to_activities(filepath_act, metadata)
        self.assertTrue(shift == 40)
        # check work activity edges
        for start in [3, 5, 7]:
            for delta, reward in zip([17, 19, 21, 23], [320., 360., 400., 440.]):
                edge = (5+start*num_nodes, 5+(start+delta)*num_nodes)
                self.assertTrue(out[edge] == [-1, reward, delta])
        # check mall activity edges
        self.assertTrue(-200. + 5*shift >= 0.)
        for i in range(11):
            edge = (2+(2*i+5)*num_nodes, 2+(2*i+10)*num_nodes)
            self.assertTrue(out[edge] == [0, 200., 5])


    def test_all_times_combinations(self):
        times = all_times_combinations(2, 15, 8, 11)
        truth = [(2,10),(2,11),(2,12),(2,13),(3,11),(3,12),(3,13),(3,14),(4,12),
            (4,13),(4,14),(4,15),(5,13),(5,14),(5,15),(6,14),(6,15),(7,15)]
        self.assertTrue(times == truth)


if __name__ == '__main__':
    unittest.main()
