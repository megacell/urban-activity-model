import unittest
from igraph import *
from graph_utils.pathfinding_extended import *

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
        # weight edges 1, 4, 7 = 100
        # weight edges 2, 5, 8 = 80, 60, 40
        # weight edges 0, 3, 6, 9 = 10, 10, 10, 10
        # can only visti at one edge from edges 2, 5, 8
        edges = [(0,1),(0,2),(1,3),(2,3),(2,4),(3,5),(4,5),(4,6),(5,7),(6,7),
                    (1,0),(3,2),(5,4),(7,6)]
        g = Graph(edges=edges, directed=True)
        g.es['weight'] = [10, 100, 80, 10, 100, 60, 10, 100, 40, 10, 10, 10, 10, 10]
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

        out = dijkstra_extended(g, 0, [(6,(0,)), (6,(1,))], modifier)
        self.assertTrue(out[0] == [0, 2, 4, 6])
        self.assertTrue(out[1] == [0, 2, 4, 5, 7, 6])


    def test_pathfinding_extended_2(self):
        # second test for pathfinding_extended
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



if __name__ == '__main__':
    unittest.main()