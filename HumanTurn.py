from DashboardLayout import *
from MCTS import *
from Baghchal import *


game = Baghchal()

# Function to take human turn
def human_turn():

    # Play the game until it is not terminal
    while not game.is_terminal()[0]:
        print(f'Current Player: {game.current_player}')

        # Get the possible moves for the current player
        moves = game.get_possible_moves()
        # If there are no moves available, then break
        if not moves:
            print(f'No moves available for {game.current_player}')
            break
        # If it is the goat's turn and goats are still to be placed on the board
        if(game.current_player == 'goat' and game.goats >0):
            print("Place a goat in one of the avaiablea postions: ")
            display_board = game.board.copy()
            for i, (x, y) in enumerate(moves):
                display_board[x,y] = '  '
            print_board_with_layout(display_board)

            # Ask for input where to place the goat, and it should be in the available moves
            while True:
                try: 
                    move_index = int(input("Choose Index"))
                    if 0<=move_index< len(moves):
                        break
                    else:
                        print("Invalid Move")
                except ValueError:
                    print("Invalid input, enter again")  
            # Apply the move to the game state
            game.apply_move(moves[move_index])

        # If it is the goat's turn and all goats are already placed on the board
        elif game.current_player == 'goat':
            print("Choose a goat to move:")
            goat_moves ={}
            display_board = game.board.copy()
            for move in moves:
                src, dest = move
                if src not in goat_moves:
                    goat_moves[src] = []
                goat_moves[src].append(move)
                # Display goats with valid moves
            for i, (goat, move_list) in enumerate(goat_moves.items()):
                print(f"Goat {i}: {goat}", move_list)
                x, y = goat
                display_board[x, y] = str(i)

            print_board_with_layout(display_board)

            # Ask for goat selection
            while True:
                try:
                    goat_index = int(input("Choose a goat index (number on the board): "))
                    if 0 <= goat_index < len(goat_moves):
                        break
                    else:
                        print("Invalid goat index. Try again.")
                except ValueError:
                    print("Invalid input. Enter a number.")
            print(goat_moves.keys(), "goat moves keys")
            selected_goat = list(goat_moves.keys())[goat_index]
            valid_moves = goat_moves[selected_goat]
            display_board = game.board.copy()
            for i, (_, (dest_x, dest_y)) in enumerate(valid_moves):
                display_board[dest_x, dest_y] = i

            print("Available moves for the selected goat:")

            # Ask for move selection
            while True:
                try:
                    move_index = int(input("Choose a move index (number on the board): "))
                    if 0 <= move_index < len(valid_moves):
                        break
                    else:
                        print("Invalid move index. Try again.")
                except ValueError:
                    print("Invalid input. Enter a number.")
            # Apply the move to the game state
            game.apply_move(valid_moves[move_index])

  
        else:
            #  AI Turn
           move_from_ai = MCTS(game, 1000)
           game.apply_move(move_from_ai)    


if __name__ == "__main__":
    human_turn()
