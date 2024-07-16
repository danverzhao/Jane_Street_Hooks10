import copy
import datetime

initial_grid = [
    [ 0,18, 0, 0, 0, 0, 7, 0, 0],
    [ 0, 0, 0, 0,12, 0, 0, 0, 0],
    [ 0, 0, 9, 0, 0, 0, 0,31, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 5, 0,11, 0,22, 0,22, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 9, 0, 0, 0, 0,19, 0, 0],
    [ 0, 0, 0, 0,14, 0, 0, 0, 0],
    [ 0, 0,22, 0, 0, 0, 0,15, 0]
]

blank_grid_original = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Grid with at least one zero in every 2x2 sub-grid
grid1 = [
    [0, 2, 0, 4, 0, 6, 0, 8, 0],
    [9, 8, 7, 6, 5, 4, 0, 2, 1],
    [0, 3, 0, 5, 0, 7, 0, 9, 0],
    [1, 9, 8, 7, 6, 5, 4, 3, 2],
    [0, 4, 0, 6, 0, 8, 0, 1, 0],
    [2, 1, 9, 8, 7, 6, 5, 4, 0],
    [0, 5, 0, 7, 0, 9, 0, 2, 0],
    [3, 2, 1, 9, 8, 7, 6, 5, 4],
    [0, 6, 0, 8, 0, 1, 0, 3, 0]
]

initial_grid_mini =  [
    [ 0, 0, 0, 0, 0],
    [ 0, 0, 9, 0, 7],
    [ 8, 0, 0, 0, 0],
    [ 0, 0, 15, 0, 12],
    [ 10, 0, 0, 0, 0]
]

def has_zero_in_2x2(grid):
    # Iterate through the grid
    for i in range(8):
        for j in range(8):
            # Check the 2x2 sub-grid
            sub_grid = [
                [grid[i][j], grid[i][j+1]],
                [grid[i+1][j], grid[i+1][j+1]]
            ]
            
            # Check if the sub-grid contains at least one zero
            if 0 not in sub_grid[0] and 0 not in sub_grid[1]:
                return False
    
    return True  

def points_between(start_point, end_point):
    points = []
    if start_point[0] > end_point[0] or start_point[1] > end_point[1]:
        middle = end_point
        end_point = start_point
        start_point = middle
    
    for x in range(start_point[0], end_point[0] + 1):
        for y in range(start_point[1], end_point[1] + 1):
            points.append((x, y))

    return points

def generate_combinations(x, y):
    """
    Generate all unique combinations of putting x number of the same thing in y containers,
    where each container can hold at most one thing, and the order doesn't matter.

    Args:
        x (int): The number of things to distribute.
        y (int): The number of containers.

    Returns:
        list: A list of tuples, where each tuple represents a unique combination.
    """
    if x > y:
        return []

    # Generate all possible ways to choose x containers from y containers
    from itertools import combinations
    container_choices = list(combinations(range(y), x))

    # Convert each choice to a container count tuple
    combinations = []
    for choice in container_choices:
        container_counts = [0] * y
        for container in choice:
            container_counts[container] = 1
        combinations.append(tuple(container_counts))

    return combinations


def print_state(state):
    for row in state:
        print(row)

def get_adjacent_sums(grid):
    adjacent_sums = [[0] * 9 for _ in range(9)]  # Initialize a 9x9 grid with zeros

    # Iterate through each cell in the grid
    for i in range(9):
        for j in range(9):
            adjacent_sum = 0

            # Check the top neighbor
            if i > 0:
                adjacent_sum += grid[i-1][j]

            # Check the bottom neighbor
            if i < 8:
                adjacent_sum += grid[i+1][j]

            # Check the left neighbor
            if j > 0:
                adjacent_sum += grid[i][j-1]

            # Check the right neighbor
            if j < 8:
                adjacent_sum += grid[i][j+1]

            adjacent_sums[i][j] = adjacent_sum

    return adjacent_sums

def is_valid(current_state, x, y, number):
    if (initial_grid[x][y] != 0):
        return False
    return True 

# put down number 1 as 1 can only be in 1x1
def get_new_starting_grid(x, y):
    current_grid = copy.deepcopy(blank_grid_original)

    if is_valid(current_grid, x, y, 1):
        print(f"x:{x} y:{y}")
        current_grid[x][y] = 1
        return current_grid
    
    else:
        return False

def is_board_valid(current_state, top_left, top_right, bot_right, bot_left):
    
    adj_sums = get_adjacent_sums(current_state) 
    
    for x, (ini_row, cur_row) in enumerate(zip(initial_grid, adj_sums)):
        for y, (ini, cur) in enumerate(zip(ini_row, cur_row)):
            # need to check 4 adjacent 
            if (ini != 0):
                # adj sums already bigger than clue sum
                if (ini < cur):
                    return False
                # is fully surrounded by L shapes and the sums don't add up to the clue sum
                # just numbers on the outside
                if (top_left[0] <= x <= bot_right[0]) and (top_left[1] <= y <= bot_right[1]):
                    if (x == 0) or (x == 8) or (y == 0) or (y == 8):
                        if (ini != cur):
                            return False
                # numbers not on the outside      
                if (top_left[0] < x < bot_right[0]) and (top_left[1] < y < bot_right[1]):
                    if (ini != cur):
                        return False
    
    return True

def put_L_box(box_len, box_corner_info):
    
    set_of_points = []
    # top-left
    test_x = box_corner_info['top_left'][0] - 1
    test_y = box_corner_info['top_left'][1] - 1
    if (0 <= test_x + box_len <= 8) and (0 <= test_x <= 8 and 0 <= test_y <= 8) and (0 <= test_y + box_len <= 8): 
        all_points = points_between((test_x + box_len, test_y), (test_x, test_y)) + points_between((test_x, test_y + 1), (test_x, test_y + box_len))
        set_of_points.append(all_points)
    else:
        set_of_points.append([])
        
    # top-right
    test_x = box_corner_info['top_right'][0] - 1
    test_y = box_corner_info['top_right'][1] + 1
    if (0 <= test_y - box_len <= 8) and (0 <= test_x <= 8 and 0 <= test_y <= 8) and (0 <= test_x + box_len <= 8):
        all_points = points_between((test_x, test_y - box_len), (test_x, test_y)) + points_between((test_x + 1, test_y), (test_x + box_len, test_y))
        set_of_points.append(all_points)
    else:
        set_of_points.append([])
            
    # bot-right
    test_x = box_corner_info['bot_right'][0] + 1
    test_y = box_corner_info['bot_right'][1] + 1
    if (0 <= test_y - box_len <= 8) and (0 <= test_x <= 8 and 0 <= test_y <= 8) and (0 <= test_x - box_len <= 8): 
        all_points = points_between((test_x, test_y - box_len), (test_x, test_y)) + points_between((test_x - 1, test_y), (test_x - box_len, test_y))
        set_of_points.append(all_points)
    else:
        set_of_points.append([])
            
    # bot-left
    test_x = box_corner_info['bot_left'][0] + 1
    test_y = box_corner_info['bot_left'][1] - 1
    if (0 <= test_x - box_len <= 8) and (0 <= test_x <= 8 and 0 <= test_y <= 8) and (0 <= test_y + box_len <= 8):
        all_points = points_between((test_x - box_len, test_y), (test_x, test_y)) + points_between((test_x, test_y + 1), (test_x, test_y + box_len))
        set_of_points.append(all_points)
    else:
        set_of_points.append([])  
    
    return set_of_points



def get_new_box_corner_info(current_box_corner_info):
    new_box_corner_info = []
    
    # top-left
    top_left_dict = copy.deepcopy(current_box_corner_info)
    top_left_dict['top_left'][0] = top_left_dict['top_left'][0] - 1
    top_left_dict['top_left'][1] = top_left_dict['top_left'][1] - 1
    
    top_left_dict['top_right'][0] -= 1
    top_left_dict['bot_left'][1] -= 1
    new_box_corner_info.append(top_left_dict)
    
    # top-right
    top_right_dict = copy.deepcopy(current_box_corner_info)
    top_right_dict['top_right'][0] = top_right_dict['top_right'][0] - 1
    top_right_dict['top_right'][1] = top_right_dict['top_right'][1] + 1
    
    top_right_dict['top_left'][0] -= 1
    top_right_dict['bot_right'][1] += 1
    new_box_corner_info.append(top_right_dict)

    # bot-right
    bot_right_dict = copy.deepcopy(current_box_corner_info)
    bot_right_dict['bot_right'][0] = bot_right_dict['bot_right'][0] + 1
    bot_right_dict['bot_right'][1] = bot_right_dict['bot_right'][1] + 1
    
    bot_right_dict['top_right'][1] += 1
    bot_right_dict['bot_left'][0] += 1
    new_box_corner_info.append(bot_right_dict)
    
    # bot-left
    bot_left_dict = copy.deepcopy(current_box_corner_info)
    bot_left_dict['bot_left'][0] = bot_left_dict['bot_left'][0] + 1
    bot_left_dict['bot_left'][1] = bot_left_dict['bot_left'][1] - 1
    
    bot_left_dict['top_left'][1] -= 1
    bot_left_dict['bot_right'][0] += 1
    new_box_corner_info.append(bot_left_dict)
    
    return new_box_corner_info
        
# output all possibility/combination of the next state    
def put_number_in_L_box(state, set_of_points, array_for_number_in, length_for_box, box_corner_info):
    
    L_area = (length_for_box + 1) * 2 - 1
    states = []
    numbers_left = []
    
    for number in array_for_number_in:
        empty_pos = []
        filter_index = []
        for index, point in enumerate(set_of_points):
            if initial_grid[point[0]][point[1]] == 0:
                empty_pos.append(point)
                filter_index.append(index)
        
        if number <= (len(empty_pos)):
            
            combinations = generate_combinations(number, L_area)
            filter_index_comb = generate_combinations(number, len(filter_index))
            filter_index_comb_real = []
            for comb in filter_index_comb:
                temp = []
                for index, num in enumerate(comb):
                    if num == 1:
                        temp.append(filter_index[index]) 
                if len(temp) != 0:
                    filter_index_comb_real.append(temp)
            
            all_filtered_tuples = []
            for filter_index in filter_index_comb_real:
                filtered_tuples = [t for t in combinations if all(t[i] == 1 for i in filter_index)]
                all_filtered_tuples.append(filtered_tuples)
                
            # try each combination of position
            for combination in all_filtered_tuples:
                
                save_point = copy.deepcopy(state)
                # put the number correspond to the position
                for yes_or_no, point in zip(combination[0], set_of_points):
                    if (yes_or_no == 1):
                        save_point[point[0]][point[1]] = number
               
                top_left = box_corner_info['top_left']
                top_right = box_corner_info['top_right']
                bot_right = box_corner_info['bot_right']
                bot_left = box_corner_info['bot_left']
                if (is_board_valid(save_point, top_left, top_right, bot_right, bot_left)):
                    states.append(save_point)
                    new_num_left = copy.deepcopy(array_for_number_in)
                    #print(new_num_left)
                    new_num_left.remove(number)
                    numbers_left.append(new_num_left)
                
    return states, numbers_left


def save(state, name):
    with open(name, "a") as file:
        # Write each row of the matrix to the file
        for row in state:
            # Convert each element to a string and join them with spaces
            row_str = " ".join(map(str, row))
            # Write the row to the file
            file.write(row_str + "\n")
        file.write("\n")


def is_connected(matrix):
    rows, cols = len(matrix), len(matrix[0])
    
    # Define a helper function for DFS traversal
    def dfs(x, y):
        if 0 <= x < rows and 0 <= y < cols and matrix[x][y] != 0 and not visited[x][y]:
            visited[x][y] = True
            # Explore neighbors
            dfs(x - 1, y)  # Up
            dfs(x + 1, y)  # Down
            dfs(x, y - 1)  # Left
            dfs(x, y + 1)  # Right
    
    # Find the first non-zero element and start DFS from there
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] != 0:
                # Initialize a 2D array to keep track of visited cells
                visited = [[False] * cols for _ in range(rows)]
                dfs(i, j)  # Start DFS from the first non-zero element found
                break
    
    # Check if all non-zero elements have been visited
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] != 0 and not visited[i][j]:
                return False  # Unreachable non-zero element found
    
    return True  # All non-zero elements are part of one connected region
#_______________________________________________________________________________
#_______________________________________________________________________________
recursive_count = 0

def play_game(state, length_for_box, array_for_number_in, box_corner_info):
    
    global recursive_count
    recursive_count += 1

    if recursive_count % 100 == 0:
        print('count: ',recursive_count)

    if (has_zero_in_2x2(state) == False):
        return False

    if len(array_for_number_in) == 0:
        #print(f'numbers left: {array_for_number_in}')
        save(state, 'matrix0.txt')
        if (is_connected(state)):
            save(state, 'final_matrix.txt')
    
    # get set of points for top-left, top-right, bot-right, bot-left
    all_avaliable_set_of_points = put_L_box(length_for_box, box_corner_info)
    for index, set_of_points in enumerate(all_avaliable_set_of_points): 
        if (set_of_points != []):
            new_box_corner_info = get_new_box_corner_info(box_corner_info)
            new_states, new_array_for_number_in = put_number_in_L_box(state, set_of_points, array_for_number_in, length_for_box, new_box_corner_info[index])
            
            if (len(new_states) == len(new_array_for_number_in)):
                for i in range(len(new_states)):
                    play_game(new_states[i], length_for_box + 1, new_array_for_number_in[i], new_box_corner_info[index])
            else: 
                print('ERROR')


# some calculations for fun
start_time_all = datetime.datetime.now()
time_matrix = [[0 for _ in range(9)] for _ in range(9)]
count_matrix = [[0 for _ in range(9)] for _ in range(9)]

for x in range(5, 9):
    print(x)
    for y in range(9):
        if y >= 7: # domain knowledge
            continue
        if x == 5 and y < 3:
            continue
        if (get_new_starting_grid(x, y)):
            new_grid = get_new_starting_grid(x, y)
            box_corner_info = {
                'top_left' : [x, y],
                'top_right' : [x, y],
                'bot_right' : [x, y],
                'bot_left' : [x, y]}
            start_time_mini = datetime.datetime.now()
            play_game(new_grid, 1, [2, 3, 4, 5, 6, 7, 8, 9], box_corner_info)
            end_time_mini = datetime.datetime.now()
            elapsed_time = end_time_mini - start_time_mini
            elapsed_minutes = round(elapsed_time.total_seconds() / 60, 2)
            print(f'function calls: {recursive_count}')
            print(f'time: {elapsed_minutes} minutes')
            count_matrix[x][y] = recursive_count
            time_matrix[x][y] = elapsed_minutes
            recursive_count = 0

            
end_time_all = datetime.datetime.now()
elapsed_time = end_time_all - start_time_all
elapsed_minutes = elapsed_time.total_seconds() / 60
print("Total Elapsed time:", elapsed_minutes, "minutes")

print('Time matrix:')
print_state(time_matrix)

print('Count matrix:')
print_state(count_matrix)

#at 5:3 takes 5h+ to reach 9600