import unittest
from igraph import *
from pathfinding.pathfinding_extended import *

__author__ = 'jeromethai'


class TestPathfindingExtended(unittest.TestCase):

    def test_pathfinding_extended_1(self):
        # first test of pathfinding_extended
        # simple network:
        # (0)-10-0-(1)
        #  |        |
        #  1        2 
        #  |        |
        # (2)-11-3-(3)
        #  |        |
        #  4        5
        #  |        |
        # (4)-12-6-(5)
        #  |        |
        #  7        8
        #  |        |
        # (6)-13-9-(7) 
        # (i) is the id of the vertex
        # -i-j- are ids of edges, j being to right and i to left
        # weight edges 1, 4, 7 = 100
        # weight edges 2, 5, 8 = 80, 60, 40
        # weight edges 0, 3, 6, 9 = 10, 10, 10, 10
        # can only visit one edge from edges 2, 5, 8
        # hence edges 2, 5, 8 have type 0
        # other edges have type -1
        edges = [(0,1),(0,2),(1,3),(2,3),(2,4),(3,5),(4,5),(4,6),(5,7),(6,7),
                    (1,0),(3,2),(5,4),(7,6)]
        g = Graph(edges=edges, directed=True)
        g.es['weight'] = [10, 100, 80, 10, 100, 60, 10, 100, 40, 10, 10, 10, 10, 10]
        # edges of type -1 do not have any counter on them
        # edges of type >= 0 have a counter
        g.es['type'] = [-1, -1, 0, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1]

        def modifier(edge=None, a=None):
            # a modifier that takes an edge and an activity in argument
            if edge is None and a is None: 
                return 1 # return the number of types (edges 2, 5, 8 are types 0)
            w = edge['weight']
            u = edge.tuple[1]
            if edge['type'] == -1: return w, (u, a)
            if edge['type'] == 0 and a[0] == 0: return w, (u, (1,))
            if edge['type'] == 0 and a[0] == 1: return np.inf, -1

        out = dijkstra_extended(g, 0, [(6,(0,)), (6,(1,))], modifier)
        self.assertTrue(out[0] == [0, 2, 4, 6])
        self.assertTrue(out[1] == [0, 2, 4, 5, 7, 6])


    def test_pathfinding_extended_2(self):
        # second test for pathfinding_extended
        # in slice 1, activities of rewards 60 and 40 with type 0 and 1
        # in slice 2, activities of rewards 50 and 20 with type 0 and 1
        # activity of type 0 and 1 can be accomplished at most once
        # optimal is activity of type 0 is chosen first and then of type 1
        edges = [(0,1),(1,0),(0,2),(2,0),(1,2),(2,1),
                (3,4),(4,3),(3,5),(5,3),(4,5),(5,4),
                (6,7),(7,6),(6,8),(8,6),(7,8),(8,7),
                (0,3),(1,4),(2,5),(3,6),(4,7),(5,8)]
        g = Graph(edges=edges, directed=True)
        g.es['weight'] = [10.]*18 + [100., 60., 40., 100., 50., 20.]
        g.es['type'] = [-1]*18 + [-1, 0, 1, -1, 0, 1]

        def modifier(edge=None, a=None):
            if edge is None and a is None: return 2
            w = edge['weight']
            i = edge['type']
            u = edge.tuple[1]
            if i == -1: return w, (u, a)
            if i >= 0 and a[i] == 0: return w, (u, a[:i]+(1,)+a[i+1:])
            if i >= 0 and a[i] == 1: return np.inf, -1

        to = [(6,(0,0)), (6,(1,0)), (6,(0,1)), (6,(1,1))]
        out = dijkstra_extended(g, 0, to, modifier)
        self.assertTrue(out[0] == [0, 3, 6])
        self.assertTrue(out[1] == [0, 3, 4, 7, 6])
        self.assertTrue(out[2] == [0, 3, 5, 8, 6])
        self.assertTrue(out[3] == [0, 1, 4, 5, 8, 6])


    def test_pathfinding_extended_3(self):
        # third test for pathfinding_extended
        # similar network to test_pathfinding_extended_1(self)
        # activity edge (5,7) is replaced by (3,7) with cost 100
        # optimal if user takes this edge
        edges = [(0,1),(0,2),(1,3),(2,3),(2,4),(3,5),(4,5),(4,6),(3,7),(6,7),
                    (1,0),(3,2),(5,4),(7,6)]
        g = Graph(edges=edges, directed=True)
        g.es['weight'] = [10, 100, 80, 10, 100, 60, 10, 100, 100, 10, 10, 10, 10, 10]
        g.es['type'] = [-1, -1, 0, -1, -1, 0, -1, -1, 0, -1, -1, -1, -1, -1]

        def modifier(edge=None, a=None):
            # a modifier that takes an edge and an activity in argument
            if edge is None and a is None: 
                return 1 # edges 2, 5, 8 are same types 0
            w = edge['weight']
            u = edge.tuple[1]
            if edge['type'] == -1: return w, (u, a)
            if edge['type'] == 0 and a[0] == 0: return w, (u, (1,))
            if edge['type'] == 0 and a[0] == 1: return np.inf, -1

        out = dijkstra_extended(g, 0, [(6,(0,)), (6,(1,)), (6,(2,))], modifier)
        self.assertTrue(out[0] == [0, 2, 4, 6])
        self.assertTrue(out[1] == [0, 2, 3, 7, 6])
        self.assertTrue(out[2] == [])


    def test_pathfinding_extended_4(self):
        # fourth test for pathfinding extended
        # we have a network with following geometry
        # (0)--(1)--(2)
        #  |    |    |
        # (3)--(4)--(5)
        # multilpied by 16 time steps of one hour between 5am and 9pm
        # each slice represents travel times during [5am, 6am], [6am, 7am] ...
        # the home is at node 0
        # the mall is at node 2 and rewards 200 for two hours but only once
        # the mall opens at 8am and closes at 8pm
        # the work is at node 5 and rewards of 40/hour
        # with start time between 7am and 9am for 8 to 11 hours of work
        # note that user does not have time to go to work
        # note that travel times along path 0-3-4-5 are shorter
        # during both morning and evening peak hours
        # but user does not have time to go to mall before work
        # so user goes after to mall after work
        # on the return trip, the travel times are longer on path 0-1-2-5
        # but the detour is necessary to go to the mall

        # this graph was generated by:
        # filepath_net = 'networks/SmallGrid_net_times.txt'
        # filepath_act = 'networks/SmallGrid_activities.txt'
        # g = txt_to_supernetwork(filepath_net, filepath_act, 'SmallGrid')
        # g.write_pickle('SmallGrid.pkl')
        g = Graph.Read_Pickle('networks/SmallGrid.pkl')

        def modifier(edge=None, a=None):
            # a modifier that takes an edge and an activity in argument
            if edge is None and a is None:
                return 1 # only one "non-repeatable" type
            w = edge['weight']
            u = edge.tuple[1]
            if edge['type'] == -1: return w, (u, a)
            if edge['type'] == 0 and a[0] == 0: return w, (u, (1,))
            if edge['type'] == 0 and a[0] == 1: return np.inf, -1

        out = dijkstra_extended(g, 0, [(90,(0,)), (90,(1,)), (90,(2,))], modifier)
        # Scenario 1: does not visit mall
        # leaves home at 8am
        # goes to work following path 0-3-4-5 between 8am and 9am
        # arrives at work at 9am
        # stay at work for 11 hours until 8pm
        # goes back following 5-4-3-0 to back home at 9pm
        # Scenario 2: visits mall
        # leaves home at 6am
        # goes to work following path 0-3-4-5 between 6am and 7am
        # arriver at work at 7am
        # stay at work for 10 hours until 5pm
        # goes to mall at 2 at 6pm and stays for two hours until 8pm
        # goes back to home between 8pm and 9pm following path 2-1-0
        self.assertTrue(out[0] == [0, 6, 12, 18, 21, 22, 23, 95, 94, 93, 90])
        self.assertTrue(out[1] == [0, 6, 9, 10, 11, 77, 74, 92, 91, 90])
        self.assertTrue(out[2] == [])



if __name__ == '__main__':
    unittest.main()

