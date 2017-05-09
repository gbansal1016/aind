# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Naked twin is a strategy to solve sudoku problem. The strategy works by identifying pairs from peers that can accept the same 2 digits as valid values. The strategy is implemented by iterating through all the cells that can accept only 2 digits as valid value in the box. The next step is to identify other cells from the list of peers that also has same 2 digits as valid values for the box. These other cells if found are called naked twins. The identification of naked twins constraints the digits that can be present in all other peers of these pairs. Essentialy the 2 digits are locked as possible values for the pair of naked twins. This implies that these 2 digits can be safely removed as possible digits from the all the common set of peers of the naked twins. The constraint on potential digits enforced by naked twin is propagated across all the common peers of the naked twins. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Diagonal sudoko enforces the constraint that the 2 long diagonals of the sudoku should contain all digits 1-9 at max once along the diagonal boxes and at the same time meet the constraint of the general sudoku. 

The solution of diagonal sudoku is an extension of the original sudoku. The solution is found by iteratively applying  the strategy of only_choice, eliminate and naked_twins until the solution is found or there is no feasible solution. 

To solve diagonal sudoku, the additional diagonal constraint is enforced by appending the cells along the diagonal to the unitlist. Only_choice strategy is then applied to the elements of unitlist by identifying the unique digit that is not present in any other cell of the unitlist.

The search algorithm is then used if the solution is not found after applying the only_choice, eliminate and naked_twins. The search algorithm subsitutes the digits in the unsolved boxes one at a time from the possible values of digits. After substituting the digit, the search algorith is recursively invoked. 

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

