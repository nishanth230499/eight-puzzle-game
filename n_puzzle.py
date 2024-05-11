import heapq
import copy
import time

GRID_SIDE_LEN = 3 # Change this to 4 to solve 15 puzzle problem

# Function to take the difficulty level input from user and return the default puzzle state
def gen_default_puzzle_state():
    if GRID_SIDE_LEN == 3:
        puzzle_states = [
            [[1,2,3],[4,5,6],[7,8,0]],
            [[1,2,3],[4,5,6],[0,7,8]],
            [[1,2,3],[5,0,6],[4,7,8]],
            [[1,3,6],[5,0,2],[4,7,8]],
            [[1,3,6],[5,0,7],[4,8,2]],
            [[1,6,7],[5,0,3],[4,8,2]],
            [[7,1,2],[4,8,5],[6,3,0]],
            [[0,7,2],[4,6,1],[3,5,8]],
        ]
        diff = int(input("Enter the difficulty level in the range [0-7].\n"))
        if 0 <= diff <= 7:
            return puzzle_states[diff]
        else:
            raise Exception("Invalid Input!")

    # TODO: Add elif's to add default states for problem size other than 8 
    else:
        raise Exception("No default Puzzle States configured for {}.".format(GRID_SIDE_LEN*GRID_SIDE_LEN-1))

# Function to input the user defined puzzle state
def read_puzzle_state():
    print("Enter your initial puzzle state.\nUse a zero to represent the blank.\nEnter the numbers delimiting with a space.\nUse RET after completing a row")
    numbers_read = {}
    puzzle_state = []
    for i in range(GRID_SIDE_LEN):
        print("Enter row {}".format(i+1))
        row = list(map(int, input().split()))

        # Validate each row
        if len(row) != GRID_SIDE_LEN:
            raise Exception("A row should have length: {}.".format(GRID_SIDE_LEN))
        for num in row:
            if not 0 <= num < GRID_SIDE_LEN * GRID_SIDE_LEN:
                raise Exception("Numbers should be in the range [{}, {}].".format(0, GRID_SIDE_LEN * GRID_SIDE_LEN - 1))
            if num in numbers_read:
                raise Exception("Number {} already entered. Duplicates are not allowed".format(num))
            else:
                numbers_read[num] = True
        puzzle_state.append(row)
    return puzzle_state

# Function which checks whether the state is goal or not
def goal_test(puzzle_state):
    for i in range(GRID_SIDE_LEN):
        for j in range(GRID_SIDE_LEN):

            # Zero should be at the last
            if i == GRID_SIDE_LEN - 1 and j == GRID_SIDE_LEN - 1:
                if puzzle_state[i][j] != 0:
                    return False
            
            # Corresponding number should be present at the rest of the places
            else:
                if puzzle_state[i][j] != GRID_SIDE_LEN * i + j + 1:
                    return False
    return True

def expand_nodes(puzzle_state):
    # directions defines the increments and decrements of the row and column index
    directions = [
        [0, 1],
        [0, -1],
        [1, 0],
        [-1, 0]
    ]
    for i in range(GRID_SIDE_LEN):
        for j in range(GRID_SIDE_LEN):
            if puzzle_state[i][j] == 0:
                empty_space_x = i
                empty_space_y = j
    
    expanded_nodes = []
    for dx, dy in directions:
        x = empty_space_x + dx
        y = empty_space_y + dy
        if 0 <= x < GRID_SIDE_LEN and 0 <= y < GRID_SIDE_LEN:
            # For each move, deep copy the state and exchange blank with the corresponding tile
            node = copy.deepcopy(puzzle_state)
            node[empty_space_x][empty_space_y], node[x][y] = node[x][y], node[empty_space_x][empty_space_y]
            expanded_nodes.append(node)
    return expanded_nodes

# Function to convert a state to tuple so that we can easily check if it is visited or not
def node_to_tuple(node):
    arr = []
    for row in node:
        # Add all the numbers in the order and convert it to tuple
        arr.extend(row)
    return tuple(arr)

def compute_heuristic(node, algorithm):
    # Misplaced Heuristic
    if algorithm == 2:
        h = 0
        for i in range(GRID_SIDE_LEN):
            for j in range(GRID_SIDE_LEN):
                if i != GRID_SIDE_LEN - 1 or j != GRID_SIDE_LEN - 1: # Not checking for the last position
                    if node[i][j] != i * GRID_SIDE_LEN + j + 1: # If the position doesnot have the corresponding tile
                        h += 1
        return h
    
    # Manhattan Heuristic
    elif algorithm == 3:
        h = 0
        for i in range(GRID_SIDE_LEN):
            for j in range(GRID_SIDE_LEN):
                if node[i][j] != 0: # Not checking for the blank

                    # Computing the position of the tile in the goal state
                    goal_state_i = (node[i][j] - 1) // GRID_SIDE_LEN
                    goal_state_j = (node[i][j] - 1) % GRID_SIDE_LEN

                    # Incrementing the heuristic by the difference in indices
                    h += abs(goal_state_i - i)
                    h += abs(goal_state_j - j)
        return h
    else:
        return 0

# Function to print the intermediate nodes
def print_node(node):
    for i in range(GRID_SIDE_LEN):
        print("[", ", ".join(map(str, node[i])), "]")

# The Main Search Function
def search(inital_state, algorithm):
    nodes = [] # Initializing empty queue
    visited_nodes = set() # Set to track the visited nodes
    nodes_expanded = 0 # To track the number of nodes expanded
    max_queue_size = 0 # To track the maximum queue size
    start_time = time.time() # Start time of the algorithm
    h = compute_heuristic(inital_state, algorithm) # Compute heuristic for the initial state
    heapq.heappush(nodes, (h, 0, inital_state)) # Push the initial state onto the queue
    while len(nodes): # Until the queue is empty
        max_queue_size = max(max_queue_size, len(nodes)) # Check the queue size
        f, g, node = heapq.heappop(nodes) # Pop f(n), g(n) and the node having least f(n) from the queue
        if goal_test(node): # Check if the node is goal node or not
            # Print all the results
            print("Success! Goal State Found!")
            elapsed_time = time.time() - start_time
            print("Solution Depth: {}".format(g))
            print("Running Time: {0:.2f} ms".format(elapsed_time*1000))
            print("Nodes Expanded: {}".format(nodes_expanded))
            print("Max Queue Size: {}".format(max_queue_size))
            return node
        node_tuple = node_to_tuple(node)
        # Expand the node if it not visited
        if node_tuple not in visited_nodes:
            nodes_expanded += 1 # Increment the count tracking the number of nodes expanded
            visited_nodes.add(node_tuple) # Add it to visited
            # Print the current node. Comment the next 3 lines if you dont need lengthy intermediate nodes
            print("The best state to expand with a g(n) = {} and h(n) = {} is ...".format(g, f-g))
            print_node(node)
            print()

            # Expand the nodes
            expanded_nodes = expand_nodes(node)
            for expanded_node in expanded_nodes:
                if node_to_tuple(expanded_node) not in visited_nodes:
                    h = compute_heuristic(expanded_node, algorithm) # Computing the heuristics
                    heapq.heappush(nodes, (h + g + 1, g + 1, expanded_node)) # Pushing it to the queue
    
    # Print the results when the solution is not found
    print("Failure!")
    elapsed_time = time.time() - start_time
    print("Running Time: {0:.2f} ms".format(elapsed_time*1000))
    print("Nodes Expanded: {}".format(nodes_expanded))
    print("Max Queue Size: {}".format(max_queue_size))
        
def main():
    try:
        puzzle_mode = input("Welcome to my {}-Puzzle Solver.\nType '1' to enter the initial puzzle state, or type '2' to use the default state.\n".format(GRID_SIDE_LEN * GRID_SIDE_LEN - 1))
        if puzzle_mode == '2':
            puzzle_state = gen_default_puzzle_state()
        elif puzzle_mode == '1':
            puzzle_state = read_puzzle_state()
        else:
            print("Invalid Input!")
            return

        # For each heuristic, run the algorithm
        for i, algo in enumerate(["Uniform Cost Search", "A* with the misplaced tile heuristic", "A* with the Manhattan distance heuristic"]):
            print()
            print(algo)
            search(puzzle_state, i+1)
            

    except Exception as e:
        print(e)
        return
    

main()
