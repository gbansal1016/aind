assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)
row_unit = [cross(r, cols) for r in rows]
col_unit = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

diag_1 = []
diag_2 = []

for rs,cs in zip(('ABCDEFGHI'), ('123456789')):
    diag_1.append(rs + cs)

for rs,cs in zip(('ABCDEFGHI'), ('987654321')):
    diag_2.append(rs + cs)

diag_unit = [diag_1, diag_2]    
unitlist = row_unit + col_unit + square_units + diag_unit

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_dict = {}
    assert len(boxes)==81
    grid_dict = dict(zip(boxes, grid))
    #grid_dict.update( (k,'123456789') for (k,'.') in d )
    
    for key in grid_dict.keys():
        if (grid_dict[key]=="."):
            grid_dict[key]="123456789"

    return grid_dict


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    for key in values.keys():
        if(len(values[key])==1):
            cell = list(key)
            row_peers = cross(cell[0],cols)
            col_peers = cross(rows, cell[1])
            
            row_idx = rows.index(cell[0])
            col_idx = cols.index(cell[1])
            
            sq_peer_row = [cell[0]]
            sq_peer_col = [cell[1]]            

            if(row_idx %3 == 0):
                sq_peer_row.append(rows[row_idx+1])
                sq_peer_row.append(rows[row_idx+2])
            elif(row_idx%3  == 1):
                sq_peer_row.append(rows[row_idx+1])
                sq_peer_row.append(rows[row_idx-1])
            else:
                sq_peer_row.append(rows[row_idx-1]);
                sq_peer_row.append(rows[row_idx-2]);
    
            if(col_idx %3 == 0):
                sq_peer_col.append(cols[col_idx+1])
                sq_peer_col.append(cols[col_idx+2])
            elif(col_idx % 3 == 1):
                sq_peer_col.append(cols[col_idx+1])
                sq_peer_col.append(cols[col_idx-1])
            else:
                sq_peer_col.append(cols[col_idx-1])
                sq_peer_col.append(cols[col_idx-2])
            
            sq_peers = cross(sq_peer_row,sq_peer_col)
            
            diag_1_peers = []
            diag_2_peers = []
            if key in diag_1:
                diag_1_peers = diag_1
            
            if key in diag_2:
                diag_2_peers = diag_2
            
            peerlist = row_peers + col_peers + sq_peers + diag_1_peers + diag_2_peers
            val = values[key]

            peerlist = set(peerlist)
            peerlist.remove(key)

            for peer in peerlist:
                values[peer] = values[peer].replace(val,'')
                
    return values

def only_choice(values):
    for units in unitlist:
        for box in units:
            box_val = values[box]            

            if (len(box_val) > 1):            
                sq_copy = units.copy();
                sq_copy.remove(box)
                sq_val = [values[x] for x in sq_copy]
               
                for x in list(box_val):
                    match = [s for s in sq_val if x in s]
                    if (len(match) == 0):
                        values[box] = x
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for key in values.keys():
        box_val = values[key]
        if (len(box_val) != 2):
            continue
        
        peer_boxes = peers[key]
        
        twins = [ b for b in peer_boxes if values[b]==box_val ]
        if (not twins):
            continue
        
        for twin in twins:
            cells = []
            if twin[0]==key[0]:
                cells = [twin[0] + c for c in cols]
            else:
                cells = [ r + twin[1]  for r in rows]

            cells.remove(twin)
            cells.remove(key)
            for cell in cells:
                if len(values[cell])>2:
                    for v in box_val:
                        values[cell] = values[cell].replace(v,'')
                        
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        
        #values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    
    if all(len(values[s]) == 1 for s in boxes): 
        return values
    
    # Check how many boxes have a determined value
    vals, box = min((len(values[b]),b)  for b in boxes if len(values[b])>1 )
    
    for val in values[box]:
        new_sudoku = values.copy()
        new_sudoku[box] = val
        new_sudoku = search(new_sudoku)
        if new_sudoku:
            return new_sudoku

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    
    values = grid_values(grid)
    values = reduce_puzzle(values)
    return values
    
if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    solve(diag_sudoku_grid)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')