import unittest
from activity_engine.activity_engine import *

__author__ = "jeromethai"

# optimal trajectory when does not visit the mall
optimal_0 = [(8, 9, [0,3,4,5]), (20, 21, [5,4,3,0])]
# optimal trajectory when visits the mall
optimal_1 = [(6, 7, [0, 3, 4, 5]), (17, 18, [5, 2]), (20, 21, [2, 1, 0])]

class TestActivityEngine(unittest.TestCase):

    def test_activity_engine(self):
        filepath_net = 'networks/SmallGrid_net_times.txt'
        filepath_act = 'networks/SmallGrid_activities.txt'
        out = activity_engine(filepath_net, filepath_act)
        for i, (start, end, traj) in enumerate(out[(0,)]):
            self.assertTrue(start == optimal_0[i][0])
            self.assertTrue(end == optimal_0[i][1])
            self.assertTrue(traj == optimal_0[i][2])
        for i, (start, end, traj) in enumerate(out[(1,)]):
            self.assertTrue(start == optimal_1[i][0])
            self.assertTrue(end == optimal_1[i][1])
            self.assertTrue(traj == optimal_1[i][2])

if __name__ == '__main__':
    unittest.main()