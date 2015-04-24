import unittest
from igraph import *
import sys
sys.path.append('../../')
from graph_utils.pathfinding import *
import numpy as np
import time


__author__ = 'jeromethai'


class TestPathfinding(unittest.TestCase):


    def test_pathfinding(self):
        # compare get_shortest_paths() from igraph with own implementation
        # https://pythonhosted.org/python-igraph/igraph.GraphBase-class.html#get_shortest_paths
        
        #g = Graph.Read_Pickle('networks/SiouxFalls_net.pkl')
        g = Graph.Read_Pickle('../../networks/ChicagoSketch_net.pkl')
        time_without_heap = 0.0
        for i in range(10):
            v = np.random.randint(933)
            output1 = g.get_shortest_paths(v, weights='weight')
            start = time.time()
            output2 = dijkstra(g, v, weights='weight')
            time_without_heap += time.time() - start
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
            start = time.time()
            output2 = dijkstra(g, v, weights='weight', to=[4,5,6])
            time_without_heap += time.time() - start
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
            start = time.time()
            output2 = dijkstra(g, v, weights='weight', output='epath')
            time_without_heap += time.time() - start
            for path1,path2 in zip(output1, output2):
                cost1 = sum([g.es[eid]['weight'] for eid in path1])
                cost2 = sum([g.es[eid]['weight'] for eid in path2])
                # check if shortest paths have some costs
                # remember that shortest paths are not unique
                self.assertTrue(cost1==cost2)

            output1 = g.get_shortest_paths(v, weights='weight', output='epath', to=[4,5,6])
            start = time.time()
            output2 = dijkstra(g, v, weights='weight', output='epath', to=[4,5,6])
            time_without_heap += time.time() - start
            for path1,path2 in zip(output1, output2):
                cost1 = sum([g.es[eid]['weight'] for eid in path1])
                cost2 = sum([g.es[eid]['weight'] for eid in path2])
                # check if shortest paths have some costs
                # remember that shortest paths are not unique
                self.assertTrue(cost1==cost2)

        print "time_without_heap", time_without_heap


    def test_pathfinding_with_heap(self):
        # compare get_shortest_paths() from igraph with own implementation
        # https://pythonhosted.org/python-igraph/igraph.GraphBase-class.html#get_shortest_paths
        
        #g = Graph.Read_Pickle('networks/SiouxFalls_net.pkl')
        g = Graph.Read_Pickle('../../networks/ChicagoSketch_net.pkl')
        time_with_heap = 0.0
        for i in range(10):
            v = np.random.randint(933)
            output1 = g.get_shortest_paths(v, weights='weight')
            start = time.time()
            output2 = dijkstra_with_heap(g, v, weights='weight')
            time_with_heap += time.time() - start
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
            start = time.time()
            output2 = dijkstra_with_heap(g, v, weights='weight', to=[4,5,6])
            time_with_heap += time.time() - start
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
            start = time.time()
            output2 = dijkstra_with_heap(g, v, weights='weight', output='epath')
            time_with_heap += time.time() - start
            for path1,path2 in zip(output1, output2):
                cost1 = sum([g.es[eid]['weight'] for eid in path1])
                cost2 = sum([g.es[eid]['weight'] for eid in path2])
                # check if shortest paths have some costs
                # remember that shortest paths are not unique
                self.assertTrue(cost1==cost2)

            output1 = g.get_shortest_paths(v, weights='weight', output='epath', to=[4,5,6])
            start = time.time()
            output2 = dijkstra_with_heap(g, v, weights='weight', output='epath', to=[4,5,6])
            time_with_heap += time.time() - start
            for path1,path2 in zip(output1, output2):
                cost1 = sum([g.es[eid]['weight'] for eid in path1])
                cost2 = sum([g.es[eid]['weight'] for eid in path2])
                # check if shortest paths have some costs
                # remember that shortest paths are not unique
                self.assertTrue(cost1==cost2)

        print "time_with_heap", time_with_heap


if __name__ == '__main__':
    unittest.main()
