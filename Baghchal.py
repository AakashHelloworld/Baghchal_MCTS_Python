import numpy as np
from collections import Counter
import copy


# Class to represent the Baghchal game
class Baghchal:
    def __init__(self):
        # Initialize the 5x5 board
        self.board = np.full((5, 5), '.', dtype=object)

        # Initialize the tigers at the corners
        self.tigers = [(0, 0), (0, 4), (4, 0), (4, 4)
                       ]
        # Place the tigers on the board
        for x, y in self.tigers:
            self.board[x, y] = 'T'     

        self.goats = 20
        self.goats_on_board = 0
        self.current_player = 'goat'  
        self.captured_goats = 0

        # Track board states to check for draw conditions
        self.state_history = Counter() 
        # Track moves without progress 
        self.moves_since_progress = 0 


    # Function to print the board
    def print_board(self):
        # Print the board
        print("\n".join([" ".join(row) for row in self.board]))


    # Function to check if the tigers are blocked
    def are_tigers_blocked(self):
        for tiger in self.tigers:
            if self.get_adjacent_moves(*tiger, jump=True):
                return False
        return True

    # Function to clone the current state
    # This is used to simulate the effect of a move without changing the current state
    # Deep copy is used to avoid modifying the original state
    def clone(self):
        new_clone = Baghchal()
        new_clone.board = np.copy(self.board)  
        new_clone.tigers = copy.deepcopy(self.tigers)  
        new_clone.goats = self.goats
        new_clone.goats_on_board = self.goats_on_board
        new_clone.current_player = self.current_player
        new_clone.captured_goats = self.captured_goats
        new_clone.state_history = copy.deepcopy(self.state_history)
        new_clone.moves_since_progress = self.moves_since_progress
        return new_clone
    

    # Get valid moves for the current player
    # The moves are different for goats and tigers
    # Goats can place to empty cells or move to adjacent empty cells
    # Tigers can move to adjacent empty cells or jump over goats
    def get_possible_moves(self):
        moves = []
        # Get possible moves for the goat
        if self.current_player == 'goat':
            # If goats are not on board, place them on empty cells
            if self.goats > 0:
                moves = [(x, y) for x in range(5) for y in range(5) if self.board[x, y] == '.']
            # If goats are on board, move to adjacent empty cells
            else:
                moves = self.get_moves_for_goats()
        # Get possible moves for the tiger
        # Tigers can move to adjacent empty cells or jump over goats
        else:
            moves = self.get_moves_for_tigers()
        return moves
    


    # Get moves for goats if they all are on the board
    # Possible moves for goats are to move to adjacent empty cells
    def get_moves_for_goats(self):
        return [move for x in range(5) for y in range(5) if self.board[x, y] == 'G' for move in self.get_adjacent_moves(x, y)]


    # Get moves for tigers 
    # Possible moves for tigers are to move to adjacent empty cells or jump over goats
    def get_moves_for_tigers(self):
        return [move for x, y in self.tigers for move in self.get_adjacent_moves(x, y, jump=True)]


    # Provide valid adjacent moves for a position
    def get_adjacent_moves(self, x, y, jump=False):
        # Define directions for adjacent cells
        directions = []

        # check if the sum of x and y is odd or even
        # like (0,0) (1,1) (2,0) (2,2) and many more are even
        # and (0,1) (1,0) (1,2) (2,1) and many more are odd
        # for even we can move in 8 directions no need to check for diagonal
        # for odd we can move in 4 directions, no diagonal possible

        if (x + y) % 2 != 0:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        else:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]


        # list to store the possible moves
        moves = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check if the new position is within the board and empty
            # If it is in the board and empty, add it to the list of possible moves
            if 0 <= nx < 5 and 0 <= ny < 5 and self.board[nx, ny] == '.':
                moves.append(((x, y), (nx, ny)))
            # If jump is True, check for possible jumps
            elif jump:
                jump_x, jump_y = x + 2 * dx, y + 2 * dy
                if (
                    0 <= jump_x < 5
                    and 0 <= jump_y < 5
                    and self.board[nx, ny] == 'G'
                    and self.board[jump_x, jump_y] == '.'
                ):
                    moves.append(((x, y), (jump_x, jump_y)))
        return moves


    # Apply a move to the board
    # The move can be placing a goat or moving a goat or moving a tiger
    def apply_move(self, move):
        # Apply move for the goar
        if self.current_player == 'goat':
            # If all goats are not on board, place them on empty cells
            if self.goats > 0:  
                x, y = move
                self.board[x, y] = 'G'
                self.goats -= 1
                self.goats_on_board += 1
            # If all goats are on board, move them to adjacent empty cells
            # src are where goat initially were and dest are where goat is moving
            else: 
                (src_x, src_y), (dest_x, dest_y) = move
                # put goat on the destination and remove from source
                self.board[src_x, src_y] = '.'
                self.board[dest_x, dest_y] = 'G'
        # Apply move for the tiger
        else:
             # src are where goat initially were and dest are where goat is moving
            (src_x, src_y), (dest_x, dest_y) = move
            # remove tiger from source
            self.board[src_x, src_y] = '.'
            # check if tiger is jumping over goat
            if abs(src_x - dest_x) == 2 or abs(src_y - dest_y) == 2:
                #position of goat that is being jumped over
                mid_x, mid_y = (src_x + dest_x) // 2, (src_y + dest_y) // 2
                # remove goat
                self.board[mid_x, mid_y] = '.'
                # increment captured goats
                self.captured_goats += 1
                # decrement goats on board
                self.goats_on_board -= 1
            # put tiger on destination
            self.board[dest_x, dest_y] = 'T'
            # update tiger position
            self.tigers = [(x, y) if (x, y) != (src_x, src_y) else (dest_x, dest_y) for x, y in self.tigers]

        # Track board state after the move
        # Convert the board to a tuple of tuples to make it hashable
        # and use it as the key in the dictionary
        board_state = tuple(map(tuple, self.board))
        # Increment the count of the board state
        self.state_history[board_state] += 1

        # Reset progress counter if there's significant progress
        #if goats are captured or tigers are blocked
        if self.current_player == 'tiger' and self.captured_goats > 0:
            self.moves_since_progress = 0
        elif self.are_tigers_blocked():
            self.moves_since_progress = 0
        else:
            self.moves_since_progress += 1

        # Switch player
        self.current_player = 'goat' if self.current_player == 'tiger' else 'tiger'


    # function to check draw conditions
    # Check if the game has reached a terminal state
    def check_repetition_draw(self):
        # Check if any state has repeated 3 times
        for state, count in self.state_history.items():
            # Check if the board state has repeated 5 times
            if count >= 5:
                print("Draw due to repetitive moves!")
                return True
        return False

    #if no progress is made in 50 moves
    def check_no_progress_draw(self, limit=50):
        # Check for no progress in a certain number of moves
        if self.moves_since_progress >= limit:
            print("Draw due to no progress!")
            return True
        return False

    # Check if the game has reached a terminal state
    def is_terminal(self):
        # Check win conditions
        winner = "tiger" if self.current_player == "goat" else "goat"
        if self.captured_goats >= 5:
            return True, winner
        if self.are_tigers_blocked():
            return True, winner

        # Check draw conditions
        if (
            self.check_repetition_draw()
            or self.check_no_progress_draw()
        ):
            return True, None

        return False, None