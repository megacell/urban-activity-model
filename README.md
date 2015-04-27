# urban-activity-model
This project aims at modeling people's activities on the urban network.

Setup
-----
Python dependencies (once only):

	pip install python-igraph

Test igraph installation in your interpreter by typing:

	import igraph.test
	igraph.test.run_tests()

Activity model
-----

The activity model is described by two files, for example:

	networks/SmallGrid_activities.txt
	networks/SmallGrid_net_times.txt

SmallGrid_net_times.txt describes a directed network of geometry

	(0)--(1)--(2)
	 |    |    |
	(3)--(4)--(5)

multilpied by 16 time steps of one hour between 5am and 9pm
the weights are the travel times for each of the 16 time slices
which are (5am,6am], (6am,7am] and so on ...

SmallGrid_activities.txt describes the available activities
the activity located at Node gives Reward if done between Start time and End time
activities of type -1 can be done multiple times
activities of type 0 or more can only be done once

Activity engine
-----
Run activity engine on a small grid network:

	python activity_engine/activity_engine.py

Description of Activity engine
-----
The activity engine first converts the SmallGrid into a Supernetwork using

	from graph_utils.txt_to_supernetwork import txt_to_supernetwork

then it creates a modifier that sets the cost of an activity already done to +inf 
and solves using an extension of Dijkstra's algorithm
	
	from pathfinding.pathfinding_extended import dijkstra_extended

Example of a Supernetwork
-----
networks/SmallGrid_net_times.txt describes a network of geometry

	(0)--(1)--(2)
	 |    |    |
	(3)--(4)--(5)

multilpied by 16 time steps of one hour between 5am and 9pm
slice 0 has weights equal to the travel times during (5am, 6am]:

	(0)--(1)--(2)
	 |    |    |
	(3)--(4)--(5)

slice 1 has weights equal to the travel times during (6am, 7am]:

	(6)--(7)---(8)
	 |    |     |
	(9)--(10)--(11)

and so on ..., the slices are linked by activity edges in the time dimension

networks/SmallGrid_activities.txt describes the activities
staying at home is following path 0-6-12-...
staying at mall located at Node 2 between 8am amd 10am means taking edge
from vertex: Node + (start-1) * num_nodes = 2 + 2 * 6 = 14 
to vertex: Node + end * num_nodes = 2 + 5 * 6 = 32 where 
start-1=2 means activity starts sometime in time slice 2 (7am,8am]
end=5 means activity ends at 10am and driver is on the road at slice 5 (10am,11am]. 
An edge is of type -1 means that user can take edge any number of times while an edge is of type 0, 1, ... means user can only take it once. 
The modifier tracks activities of types 0, 1, ... which adds up to the complexity. 
Ff an activity can only be done once but has start times < end times, 
its type can be set up to -1 because the geometry of the resulting supernetwork 
implicitly restricts the edge to be taken at most once.
