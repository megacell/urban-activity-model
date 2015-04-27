import unittest
from activity_engine.activity_engine import *

__author__ = "jeromethai"

# two optimal trajectories when does not visit the mall
optimal_0 = [(8, 9, [0,3,4,5]), (20, 21, [5,4,3,0])]
optimal_1 = [(8, 9, [0,3,4,5]), (20, 21, [5,4,1,0])]
# optimal trajectory when visits the mall
optimal_2 = [(6, 7, [0, 3, 4, 5]), (17, 18, [5, 2]), (20, 21, [2, 1, 0])]

class TestActivityEngine(unittest.TestCase):

    def test_activity_engine_1(self):
        # test on the small grid
        filepath_net = 'networks/SmallGrid_net_times.txt'
        filepath_act = 'networks/SmallGrid_activities.txt'
        activities, costs = activity_engine(filepath_net, filepath_act)
        for i, (start, end, traj) in enumerate(activities[(0,)]):
            self.assertTrue(start == optimal_0[i][0])
            self.assertTrue(end == optimal_0[i][1])
            self.assertTrue(traj == optimal_0[i][2] or traj == optimal_1[i][2])
        for i, (start, end, traj) in enumerate(activities[(1,)]):
            self.assertTrue(start == optimal_2[i][0])
            self.assertTrue(end == optimal_2[i][1])
            self.assertTrue(traj == optimal_2[i][2])
        self.assertTrue(costs[(0,)] == -395.0)
        self.assertTrue(costs[(1,)] == -554.0)


    def test_activity_engine_2(self):
        # test on the small grid without the mall activity
        filepath_net = 'networks/SmallGrid_net_times.txt'
        filepath_act = 'networks/SmallGrid_activities_0.txt'
        activities, costs = activity_engine(filepath_net, filepath_act)
        for i, (start, end, traj) in enumerate(activities[()]):
            self.assertTrue(start == optimal_0[i][0])
            self.assertTrue(end == optimal_0[i][1])
            self.assertTrue(traj == optimal_0[i][2] or traj == optimal_1[i][2])
        self.assertTrue(costs[()] == -395.0)


if __name__ == '__main__':
    unittest.main()