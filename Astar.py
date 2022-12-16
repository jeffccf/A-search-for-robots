def solution(inputtext):
    
    points = [] # Initialize a list of points
    obstacles = [] #Initialize a list of obstacles

    with open(inputtext,'r') as f: # Open the text file
        count = 0 # Count the current line of the text file
        for line in f.readlines():
            count += 1
            line.replace("\n","") # Ignore the "\n" character
            if count==1: # If it is the first line
                nums = line.split(" ") # Store the line into and array, split by space
                start = [int(nums[0]),int(nums[1])] # Store the starting point and change the data type to integer
                points.append(start) # Append the point to the list
            elif count==2: # If it is the second line
                nums = line.split(" ") # Store the line into and array, split by space
                goal = [int(nums[0]),int(nums[1])] # Store the goal and change the data type to integer
                points.append(goal) # Append the point to the list
            elif count==3: # If it is the third line
                num_of_obstacles=int(line) # store the number of obstacles
            else:
                nums = line.split(" ") # Store the line into and array, split by space
                nums = [[int(nums[2*i]),int(nums[2*i+1])] for i in range(len(nums)//2)] # Store the obstacles' coordinates and change the data type to integer
                for i in nums:
                    if i not in points:
                        points.append(i) # Append the points to the list
                obstacles.append(nums) # Append the obstacle to the list

    class nodes: # For each point, it belongs to this class
        def __init__(self,point): # Initialization of each point
            self.point = point # The coordinate of the point
            self.gvalue = None # The g-value of the point
            self.hvalue = None # The h-value of the point
            self.fvalue = None # The f-value of the point
            self.successors = [] # The neighbors of the point
            self.parent = None # The parent of the point

    def distance(point1,point2): # This function returns the distance between two points
        return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**(1/2)

    def determinant(x,y): # This function returns the determinant
        return x[0]*y[1]-x[1]*y[0]

    # This function returns whether a line segment passes a particular point
    def cross(p1,p2,point):
        x_cross = (p1[0]<=point[0] and point[0]<=p2[0]) or (p1[0]>=point[0] and point[0]>=p2[0])
        y_cross = (p1[1]<=point[1] and point[1]<=p2[1]) or (p1[1]>=point[1] and point[1]>=p2[1])
        return x_cross and y_cross

    # This function reutrns the intersection between two line segments, if no intersection, return None
    def intersect(p1,p2,p3,p4):
        x_dif = [p1[0]-p2[0],p3[0]-p4[0]]
        y_dif = [p1[1]-p2[1],p3[1]-p4[1]]
        det = determinant(x_dif,y_dif)
        if det==0: # Parrell or coincide, no block
            return None
        d = [determinant(p1,p2),determinant(p3,p4)]
        x = determinant(d,x_dif)/det # x-coordinate of the two lines (not segment)
        y = determinant(d,y_dif)/det # y-coordinate of the two lines (not segment)
        if cross(p1,p2,[x,y]) and cross(p3,p4,[x,y]): # Check if the intersection point lies in the line segments
            return [x,y]
        return None

    # This function returns whether two points are connected or they are blocked by obstacle(s)
    def connected(point1,point2,obstacles):
        for obstacle in obstacles: # Check all the obstacles
            if point1 in obstacle and point2 in obstacle:
                # If the points belongs to the same obstacle, check if they will be blocked by that particular obstacle
                return distance(point1,point2)==distance(obstacle[0],obstacle[1]) or distance(point1,point2)==distance(obstacle[1],obstacle[2])
            arr = [] # This array stores the intersect points between the two points and the obstacle
            for i in range(4): # Check the four sides of the obstacle
                cur = intersect(point1,point2,obstacle[i],obstacle[(i+1)%4])
                 # If there are intersection and it is not yet stored, append it to the array
                if cur and cur not in arr:
                    arr.append(cur)
            if len(arr)==2:
                #If there are two intersections between the obstacle and the line of point1 and point2, they are blocked
                if arr[0] in obstacle and arr[1] in obstacle and (distance(arr[0],arr[1])==distance(obstacle[0],obstacle[1]) or distance(arr[0],arr[1])==distance(obstacle[1],obstacle[2])):
                    # Unless they belong to the same obstacle
                    continue
                return False
        return True

    for i in range(len(points)): # Initialize the points, store their coordinates and hvalue
        points[i] = nodes(points[i])
        points[i].hvalue = distance(goal,points[i].point)

    # Initialize the values of starting point
    points[0].visited = True
    points[0].gvalue = 0
    points[0].fvalue = points[0].hvalue
    points[0].visited = True

    # For each pair of points, check if they are connected, if they are, store it in their "successor" list
    for i in range(len(points)-1):
        for j in range(i+1,len(points)):
            if connected(points[i].point,points[j].point,obstacles):
                points[i].successors.append(points[j])
                points[j].successors.append(points[i])

    frontier = [points[0]] # In the beginning, the only point in the frontier is the starting point
    visited = [] # The list that stores the visited points
    while frontier: # While the frontier is not empty
        frontier = sorted(frontier,key=lambda x:x.fvalue) # Sort the frontier array by the f-values
        cur = frontier.pop(0) # Pop the point with the lowest f-value as current point
        if cur.point==goal: # If the point is the goal, break
            break
        visited.append(cur) # Append current point to visited
        for successor in cur.successors: # For the neighbors in current point
            if successor in visited: # If the neightbor is already visited, ignore it
                continue
            if successor not in frontier or successor.gvalue>cur.gvalue+distance(cur.point,successor.point):
                # If it is not visited and not in frontier, or its new f-value is lower, update the three values and parent
                successor.gvalue = cur.gvalue+distance(cur.point,successor.point)
                successor.fvalue = successor.gvalue+successor.hvalue
                successor.parent = cur
            if successor not in frontier:
                # If it is not visited and not in frontier yet, add it to the frontier list
                frontier.append(successor)
    path = [] # This list stores the path
    cost = [] # This list stores the cost
    while cur:
        path = [cur.point]+path # Track the path
        cost = [cur.gvalue]+cost # Track the g-value of each point 
        cur = cur.parent # Track to the parent node
    print('Point ',' Cumulative Cost')
    for i in range(len(path)): # Print out the path and cost
        print(tuple(path[i]),cost[i])
        
        
if __name__ == '__main__':
    print("Simple dataset")
    solution("input1.txt")
    print("Difficult one")
    solution("input2.txt")
    print("My dataset")
    solution("input3.txt")
