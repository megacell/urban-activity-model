import unittest
from igraph import *
from pathfinding.pathfinding import *
import numpy as np

__author__ = 'jeromethai'


class TestPathfinding(unittest.TestCase):


    def test_pathfinding(self):
        # compare get_shortest_paths() from igraph with own implementation
        # https://pythonhosted.org/python-igraph/igraph.GraphBase-class.html#get_shortest_paths
        
        g = Graph.Read_Pickle('networks/SiouxFalls_net.pkl')
        
        for i in range(10):
            v = np.random.randint(25)
            output1 = g.get_shortest_paths(v, weights='weight')
            output2 = dijkstra(g, v, weights='weight')
            for path1,path2 in zip(output1, output2):
                cost1 = 0.0
                cost2 = 0.0
                for s,t in zip(path1[:-1], path1[1:]):
                    cost1 += g.es[g.get_eid(s,t)]['weight']
                for s,t in zip(path2[:-1], path2[1:]):
                    cost2 += g.es[g.get_eid(s,t)]['weight']
                # check if shortest paths have some costs
                # remember that shortest paths are not unique
                self.assertTrue(cost1==cost2)

            output1 = g.get_shortest_paths(v, weights='weight', to=[4,5,6])
            output2 = dijkstra(g, v, weights='weight', to=[4,5,6])
            for path1,path2 in zip(output1, output2):
                cost1 = 0.0
                cost2 = 0.0
                for s,t in zip(path1[:-1], path1[1:]):
                    cost1 += g.es[g.get_eid(s,t)]['weight']
                for s,t in zip(path2[:-1], path2[1:]):
                    cost2 += g.es[g.get_eid(s,t)]['weight']
                # check if shortest paths have some costs
                # remember that shortest paths are not unique
                self.assertTrue(cost1==cost2)

            output1 = g.get_shortest_paths(v, weights='weight', output='epath')
            output2 = dijkstra(g, v, weights='weight', output='epath')
            for path1,path2 in zip(output1, output2):
                cost1 = sum([g.es[eid]['weight'] for eid in path1])
                cost2 = sum([g.es[eid]['weight'] for eid in path2])
                # check if shortest paths have some costs
                # remember that shortest paths are not unique
                self.assertTrue(cost1==cost2)

            output1 = g.get_shortest_paths(v, weights='weight', output='epath', to=[4,5,6])
            output2 = dijkstra(g, v, weights='weight', output='epath', to=[4,5,6])
            for path1,path2 in zip(output1, output2):
                cost1 = sum([g.es[eid]['weight'] for eid in path1])
                cost2 = sum([g.es[eid]['weight'] for eid in path2])
                # check if shortest paths have some costs
                # remember that shortest paths are not unique
                self.assertTrue(cost1==cost2)


    def test_pathfinding_with_heap(self):
        # compare get_shortest_paths() from igraph with own implementation
        # https://pythonhosted.org/python-igraph/igraph.GraphBase-class.html#get_shortest_paths
        
        g = Graph.Read_Pickle('networks/SiouxFalls_net.pkl')
        
        for i in range(10):
            v = np.random.randint(25)
            output1 = g.get_shortest_paths(v, weights='weight')
            output2 = dijkstra_with_heap(g, v, weights='weight')
            for path1,path2 in zip(output1, output2):
                cost1 = 0.0
                cost2 = 0.0
                for s,t in zip(path1[:-1], path1[1:]):
                    cost1 += g.es[g.get_eid(s,t)]['weight']
                for s,t in zip(path2[:-1], path2[1:]):
                    cost2 += g.es[g.get_eid(s,t)]['weight']
                # check if shortest paths have some costs
                # remember that shortest paths are not unique
                self.assertTrue(cost1==cost2)

            output1 = g.get_shortest_paths(v, weights='weight', to=[4,5,6])
            output2 = dijkstra_with_heap(g, v, weights='weight', to=[4,5,6])
            for path1,path2 in zip(output1, output2):
                cost1 = 0.0
                cost2 = 0.0
                for s,t in zip(path1[:-1], path1[1:]):
                    cost1 += g.es[g.get_eid(s,t)]['weight']
                for s,t in zip(path2[:-1], path2[1:]):
                    cost2 += g.es[g.get_eid(s,t)]['weight']
                # check if shortest paths have some costs
                # remember that shortest paths are not unique
                self.assertTrue(cost1==cost2)

            output1 = g.get_shortest_paths(v, weights='weight', output='epath')
            output2 = dijkstra_with_heap(g, v, weights='weight', output='epath')
            for path1,path2 in zip(output1, output2):
                cost1 = sum([g.es[eid]['weight'] for eid in path1])
                cost2 = sum([g.es[eid]['weight'] for eid in path2])
                # check if shortest paths have some costs
                # remember that shortest paths are not unique
                self.assertTrue(cost1==cost2)

            output1 = g.get_shortest_paths(v, weights='weight', output='epath', to=[4,5,6])
            output2 = dijkstra_with_heap(g, v, weights='weight', output='epath', to=[4,5,6])
            for path1,path2 in zip(output1, output2):
                cost1 = sum([g.es[eid]['weight'] for eid in path1])
                cost2 = sum([g.es[eid]['weight'] for eid in path2])
                # check if shortest paths have some costs
                # remember that shortest paths are not unique
                self.assertTrue(cost1==cost2)

if __name__ == '__main__':
    unittest.main()