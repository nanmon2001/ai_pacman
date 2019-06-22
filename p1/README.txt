Name: Mon-Nan How
ID: E34148027

Description: 
For Q1 to Q4 search algorithms, the key is to manage the fringe. For each DFS, BFS, UCS, A* the fringe is constructed as a Stack, Queue, PriorityQueue, PriorityQueue. Another key to keep tract of the solution path is by constructing a Node class, to help trace the path and cost to each node, where a node is define as a state, path(the actions need to take from the start state to the node state) and cost (the cost required from the start state to the node state).

For Q5 the key is how to properly define the state for a specific problem (CornersProblem). The current postion matters and so as the flag (visited = 1, unvisited = 0) for the four corners. Therefore, I use a tuple to represent the state as a corordinate for position and a dicitionary for corners' flags, for example:
((x,y), {corner1:0, corner2:0, corner3:0, corner4:0}). 
When the four corners turned 1, means all corners were visited (goal state).

For Q6 the heuristic value design in the concept of thinking it as for "optimal" situations. So if there is no wall at all, there will be five conditions: (all distance mentioned bellow is manhantan distance)
1. All corners were visited: No need any cost at all, heuristic value = 0
2. One corner left to be visited: heuristic value is the distane between the current position and the left unvisited corner.
3. Two corners left unvisited: heuristic value is the distance between the two corners plus the distance to the nearest corner.
4. Three corners left unvisited: heuristic value is the shortest distance to connect the three corners plus the distance to the nearest corner.
5. Four corners left to be visited: heuristic value is the shortest distance to connect the four corners plus the distance to the nearest corner. 

For Q7, the concept of the heuristic method here is: base on the given state, calculate
the smallest manhattan distance need to travel between a group of food plus the distance from the
current position to the nearest food. The distance needed to travel between foods is at least "biggest x - smallest x" plus "biggest y - smallest y". Moreover,if there exist at least three x and y values, there must exist a imaginary rectangular on the manhattan path, this stituation at least need one more step cost. There is a an additional section in the code block that try to handle take the wall into consideration, but the issue is handled very ugly, where I don't want to explain....

For Q8, just follow the hint and fill the missing code.