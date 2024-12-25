import math
# Node class for MCTS
# Each node has a state, parent, children, visit, win, and last_move
# Help to make the tree structure


class Node:
    def __init__(self, state, parent= None):
        # Initialize the node with the state and parent
        # state is the current state of the game means it is basically the board ( Baghchal class object)
        self.state = state
        # parent is the parent node of the current node
        self.parent = parent
        # children is the list of children of the current node
        self.children = []
        self.visit = 0
        self.win = 0
        # last_move is the move that led to the current state
        self.last_move = None
    

    # check if the node is fully expanded
    # what fully expanded means is that all the possible moves from the current state have been explored
    # If all the possible moves have been explored by the children of the node, then the node is fully expanded
    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_possible_moves())
    

    # Get the best child of the node from there siblings or from the children of the nodes
    def get_best_child(self, exploration_weight=1.41):

        # Basic formula for UCB1 is exploitation + exploration
        # exploitation is the win rate of the child
        # exploration is the square root of the log of the visit of the parent divided by the visit of the child
        best_child = None
        best_score = -float('inf')
        for child in self.children:
            if child.visit == 0:
                continue
            exploitation = child.win / child.visit  # Win rate
            exploration = exploration_weight * math.sqrt(
                math.log(self.visit) / child.visit
            )
            score = exploitation + exploration
            if score > best_score:
                best_score = score
                best_child = child
        return best_child
    
        
