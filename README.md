# A-search-for-robots

Imagine in a 2-D space, starting from the starting point, the robot has to avoid the obstacles (which are rectangles) and reach the goal point.
A* search is implemented which the heuristic value is defined as the distance between the point and the goal.

For the input text file, the first line and the second line represents the start point and the goal point of the robot. The third line represents the number of the obstacles.
The rest of the lines represents the location of the obstacles. 
For example, 7 4 9 6 4 10 2 8 represents a rectangle with the points of (7,4),(9,6),(4,10) and (2,8).
If the text file is imported correctly, the program would print out all the points the robot went through along with the cumulative cost (which is the distance of the path)
