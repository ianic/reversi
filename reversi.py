import random

# The outside edge is marked ?, empty squares are ., black is @, and white is o.
# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', '*', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

def squares():
    """List all the valid squares on the board."""
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def initial_board():
    """Create a new board with the initial black and white positions filled."""
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # The middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

def print_board(board):
    """Get a string representation of the board."""
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, list(range(1, 9))))
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep

def is_valid(move):
    """Is move a square on the board?"""
    return move in squares()

def opponent(player):
    """Get player's opponent piece."""
    return BLACK if player is WHITE else WHITE

def find_bracket(square, player, board, direction):
    """
    Find a square that forms a bracket with `square` for `player` in the given
    `direction`.  Returns None if no such square exists.
    """
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    return None if board[bracket] in (OUTER, EMPTY) else bracket

def is_legal(move, player, board):
    """Is this a legal move for the player?"""
    if board[move] != EMPTY:
        return False
    for d in DIRECTIONS:
        if find_bracket(move, player, board, d):
            return True
    return False

def make_move(move, player, board):
    """Update the board to reflect the move by the specified player."""
    board[move] = player
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

def make_flips(move, player, board, direction):
    """Flip pieces in the given direction as a result of the move by player."""
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction

def legal_moves(player, board):
    """Get a list of all legal moves for player."""
    return [sq for sq in squares() if is_legal(sq, player, board)]

def any_legal_move(player, board):
    """Can player make any moves?"""
    return any(is_legal(sq, player, board) for sq in squares())

def play(black_strategy, white_strategy):
    """Play a game of Othello and return the final board and score."""
    board = initial_board()
    player = BLACK
    while player is not None:
        if player == BLACK:
            move = black_strategy(player, board)
        else:
            move = white_strategy(player, board)
        make_move(move, player, board)
        player = next_player(board, player)
        print(print_board(board))
    return board, score(BLACK, board)

def next_player(board, prev_player):
    """Which player should move next?  Returns None if no legal moves exist."""
    opp = opponent(prev_player)
    if any_legal_move(opp, board):
        return opp
    elif any_legal_move(prev_player, board):
        return prev_player
    return None

def score(player, board):
    """Compute player's score (number of player's pieces minus opponent's)."""
    mine, theirs = 0, 0
    opp = opponent(player)
    for sq in squares():
        piece = board[sq]
        if piece == player: mine += 1
        elif piece == opp: theirs += 1
    return mine - theirs

def computer(player, board):
    """A strategy that always chooses a random legal move."""
    return random.choice(legal_moves(player, board))

def human(player, board):
    print(print_board(board))
    #print('Your move?')
    while True:
        move = input('> ')
        if move and check(int(move), player, board):
            return int(move)
        elif move:
            print('Illegal move--try again.')

def check(move, player, board):
    return is_valid(move) and is_legal(move, player, board)

board, score = play(computer, computer)
print('Final score:', score)
print('%s wins!' % ('Black' if score > 0 else 'White'))
print(print_board(board))
