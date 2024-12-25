from Node import *
from DashboardLayout import *
import random

# MCTS function
# Steps of MCTS
# 1. Selection: Select the best child of the node
# 2. Expansion: Expand the node by adding a child
# 3. Simulation: Simulate the game from the child node
# 4. Backpropagation: Update the win and visit count of the nodes in the path
# The MCTS function takes the game and the number of iterations as input


def MCTS(game, iteration):
    # Initialize the root node with the current state of the game
    # The starting game state is the root node
    root = Node(game)

    # Perform MCTS iterations
    # The number of iterations is the number of times the MCTS algorithm is run
    # The more the number of iterations, the better the move
    # However, it also increases the time taken to make a move
    for i in range(iteration):
        
        node = root
        # Clone the game state, Do not change the original game state
        # That's why we clone the game state
        # We use Deepcopy to clone the game state
        state = game.clone()

        # Selection .........................................
        # Select the best child of the node
        # If the node is fully expanded and has children, then select the best child otherwise expand the node
        # I have already explained the is_fully_expanded function in the Node class
        while(node.is_fully_expanded and len(node.children) >0):
            node = node.get_best_child()
            state.apply_move(node.last_move)

        
        # Expansion .........................................
        # Expand the node by adding a child
        # If the node is not fully expanded, then expand the node
        if not node.is_fully_expanded():

            # Get the available moves from the current state
            available_moves = state.get_possible_moves()

            # See if children have already been there for the available moves
            # if yes, then ignore that move otherwise add that move in unvisited_moves
            unvisited_moves = [move for move in available_moves if not any(child.last_move == move for child in node.children)]

            # Select a random move from the unvisited moves
            move = random.choice(unvisited_moves)

            # Apply the move to the game state
            state.apply_move(move)

            # Create a child node with the new state
            child_node = Node(state, parent=node)

            # Update the last move of the child node
            child_node.last_move = move

            # Add the child node to the children of the parent node
            node.children.append(child_node)

            # Update the node to the child node
            node = child_node

        # Simulation
        # The game is simulated that is played randomly from the current state
        # Until the game is not over (either win or draw), the game is played randomly
        while(not state.is_terminal()[0]):

            # Get the available moves from the current state
            available_moves = state.get_possible_moves()

            # If there are no available moves, then break
            if(not available_moves): break

            # If current player is goat and goats are still to be placed on the board
            if(game.current_player == 'goat' and game.goats > 0):

                # Select a random move from the available moves
                move = random.choice(available_moves)

                # Apply the move to the game state
                state.apply_move(move)

            # If current player is goat and all goats are already placed on the board
            elif (game.current_player == 'goat'):
                goat_moves = {}

                # from the available moves, get the positions for each goat
                for move in available_moves:
                    src, dest = move 
                    if src not in goat_moves:
                        goat_moves[src] = []
                    goat_moves[src].append(dest)

                # Select a random goat from the available goats
                selected_goat = random.choice(list(goat_moves.keys()))
                # Get the valid moves for the selected goat
                valid_move = random.choice(goat_moves[selected_goat])
                # Apply the move to the game state
                state.apply_move(valid_move)
            else :
                # Select a random move from the available moves for tiger
                move = random.choice(available_moves)
                # Apply the move to the game state
                state.apply_move(move)


        # It is a terminal state, check if true, false
        # and player is the winner
        # print("State", state.is_terminal())
        check, player = state.is_terminal()
        # print("Check", state.is_terminal()[0])
        print("Player", state.is_terminal()[1])

        # Backpropagation
        # Update the win and visit count of the nodes in the path
        # If the player is the winner, then update the win count (+) of the nodes in the path
        # If the player is the loser, then update the win count (-) of the nodes in the path
        # If the game is a draw, then update the win count (+0.5) of the nodes in the
        while(node):
            node.visit += 1
            if player == 'tiger':
                node.win += 1
            elif player == 'goat':
                node.win -= 1
            else: 
                node.win += 0.5
            node = node.parent
    return root.get_best_child().last_move

