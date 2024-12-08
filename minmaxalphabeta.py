import copy
import time

class OthelloGame:
    def __init__(self):
        # Initialize an 8x8 board with empty spaces represented by '.'
        self.board = [["." for _ in range(8)] for _ in range(8)]
        self.current_player = "B"  # Start with Black by default
        self.difficulty = 4  # Set a default difficulty level
       
        self.static_weights = [
        [4, -3, 2, 2, 2, 2, -3, 4],
        [-3, -4, -1, -1, -1, -1, -4, -3],
        [2, -1, 1, 0, 0, 1, -1, 2],
        [2, -1, 0, 1, 1, 0, -1, 2],
        [2, -1, 0, 1, 1, 0, -1, 2],
        [2, -1, 1, 0, 0, 1, -1, 2],
        [-3, -4, -1, -1, -1, -1, -4, -3],
        [4, -3, 2, 2, 2, 2, -3, 4]
        ]
    
    def setup_initial_board(self, initial_disks):
        # Set up the initial board configuration with provided disks
        for x, y, color in initial_disks:
            self.board[x][y] = color


    def print_board(self):
        print("  " + " ".join(map(str, range(8))))
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(row))

    def is_valid_move(self, x, y, player):
        if self.board[x][y] != ".":
            return False
        opponent = "W" if player == "B" else "B"
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            if self.can_flip(x, y, dx, dy, player, opponent):
                return True
        return False

    def can_flip(self, x, y, dx, dy, player, opponent):
        x += dx
        y += dy
        has_opponent = False
        while 0 <= x < 8 and 0 <= y < 8:
            if self.board[x][y] == opponent:
                has_opponent = True
            elif self.board[x][y] == player:
                return has_opponent
            else:
                break
            x += dx
            y += dy
        return False

    def flip_pieces(self, x, y, player):
        opponent = "W" if player == "B" else "B"
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            if self.can_flip(x, y, dx, dy, player, opponent):
                nx, ny = x + dx, y + dy
                while self.board[nx][ny] == opponent:
                    self.board[nx][ny] = player
                    nx += dx
                    ny += dy

    def has_valid_moves(self, player):
        for x in range(8):
            for y in range(8):
                if self.is_valid_move(x, y, player):
                    return True
        return False

    def is_game_over(self):
        return not (self.has_valid_moves("B") or self.has_valid_moves("W"))

    def make_move(self, x, y, player):
        if self.is_valid_move(x, y, player):
            self.board[x][y] = player
            self.flip_pieces(x, y, player)
            return True
        return False

    def evaluate_board(self):
        black_score = sum(row.count("B") for row in self.board)
        white_score = sum(row.count("W") for row in self.board)
        return black_score - white_score
    
    def evaluate_static(self):
        """Use heuristic weights to evaluate the board for AI moves."""
        score = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == "B":
                    score += self.static_weights[x][y]  # Add weight for Black
                elif self.board[x][y] == "W":
                    score -= self.static_weights[x][y]  # Subtract weight for White
        return score

    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.is_game_over():
            return self.evaluate_static(), None  # Use heuristic here

        best_move = None
        if maximizing_player:
            max_eval = float("-inf")
            for x in range(8):
                for y in range(8):
                    if self.is_valid_move(x, y, "B"):
                        new_game = copy.deepcopy(self)
                        new_game.make_move(x, y, "B")
                        eval, _ = new_game.minimax(depth - 1, False)
                        if eval > max_eval:
                            max_eval = eval
                            best_move = (x, y)
            return max_eval, best_move
        else:
            min_eval = float("inf")
            for x in range(8):
                for y in range(8):
                    if self.is_valid_move(x, y, "W"):
                        new_game = copy.deepcopy(self)
                        new_game.make_move(x, y, "W")
                        eval, _ = new_game.minimax(depth - 1, True)
                        if eval < min_eval:
                            min_eval = eval
                            best_move = (x, y)
            return min_eval, best_move



    def alpha_beta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_game_over():
            return self.evaluate_static(), None  # Use heuristic here

        best_move = None
        if maximizing_player:
            max_eval = float("-inf")
            for x in range(8):
                for y in range(8):
                    if self.is_valid_move(x, y, "B"):
                        new_game = copy.deepcopy(self)
                        new_game.make_move(x, y, "B")
                        eval, _ = new_game.alpha_beta(depth - 1, alpha, beta, False)
                        if eval > max_eval:
                            max_eval = eval
                            best_move = (x, y)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval, best_move
        else:
            min_eval = float("inf")
            for x in range(8):
                for y in range(8):
                    if self.is_valid_move(x, y, "W"):
                        new_game = copy.deepcopy(self)
                        new_game.make_move(x, y, "W")
                        eval, _ = new_game.alpha_beta(depth - 1, alpha, beta, True)
                        if eval < min_eval:
                            min_eval = eval
                            best_move = (x, y)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval, best_move


    def get_ai_move(self, player):
        _, move = self.alpha_beta(self.difficulty, float("-inf"), float("inf"), player == "B")
        return move

    import time

    import time

    def play_game(self):
        turn_counter = 0
        move_counter = 0  # Track the number of moves
        max_turns = 100  # Set a reasonable limit to avoid infinite loops

        # Start measuring CPU implementation time
        start_time = time.process_time()

        while not self.is_game_over() and turn_counter < max_turns:
            self.print_board()
            print(f"Current Player: {self.current_player}")

            # Check if both players have no valid moves and end the game if so
            if not self.has_valid_moves("B") and not self.has_valid_moves("W"):
                print("Both players have no valid moves. Game over.")
                break

            if not self.has_valid_moves(self.current_player):
                print(f"{self.current_player} has no valid moves. Skipping turn.")
                self.current_player = "W" if self.current_player == "B" else "B"
                turn_counter += 1
                print()  # Add a blank line before the next turn
                continue

            if self.current_player == "B":
                move = self.get_ai_move("B")
            else:
                move = self.get_ai_move("W")

            if move:
                x, y = move
                print(f"{self.current_player} moves to: {chr(97 + y)}{x + 1}")
                self.make_move(x, y, self.current_player)
                self.current_player = "W" if self.current_player == "B" else "B"
                turn_counter += 1
                move_counter += 1  # Increment move counter
            else:
                print("No valid moves available.")
                turn_counter += 1

            print()  # Add a blank line before the next turn

        # Stop measuring CPU time
        end_time = time.process_time()

        if turn_counter >= max_turns:
            print("Game reached maximum turn limit. Ending game.")

        self.print_board()

        # Count the pieces for the final score
        black_count = sum(row.count("B") for row in self.board)
        white_count = sum(row.count("W") for row in self.board)

        # Print the final piece counts and declare the winner
        print(f"Final Score: Black (B) = {black_count}, White (W) = {white_count}")
        if black_count > white_count:
            print("Black wins!")
        elif white_count > black_count:
            print("White wins!")
        else:
            print("It's a tie!")

        # Print move count and CPU implementation time
        print(f"Total Moves Played: {move_counter}")
        print(f"CPU Implementation Time: {end_time - start_time:.2f} seconds")


def main():
    # Create an instance of the game
    game = OthelloGame()

    # Set the difficulty level in the main function
    game.difficulty = 4  # Adjust the difficulty level as needed

    # Custom initial board configuration with more disks
    initial_disks = [
    (3, 3, "B"), (3, 4, "W"),  # First pair of disks
    (4, 3, "W"), (4, 4, "B")   # Second pair of disks
    ]
    print('Running initial_disks1:')
    '''
    initial_disks = [
    (2, 3, "B"), (2, 4, "W"),  # First row with two disks
    (3, 2, "W"), (3, 3, "B"),  # Second row with two disks
    (4, 4, "W"), (4, 5, "B"),  # Third row with two disks
    (5, 3, "B"), (5, 4, "W")   # Fourth row with two disks
    ]
    print('Running initial_disks2:')
    
    initial_disks = [
        (3, 3, "B"), (3, 4, "W"), (4, 3, "W"), (4, 4, "B"),
        (2, 2, "B"), (2, 3, "W"), (2, 4, "B"), (2, 5, "W"),
        (3, 2, "W"), (3, 5, "B"), (4, 2, "B"), (4, 5, "W"),
        (5, 2, "W"), (5, 3, "B"), (5, 4, "W"), (5, 5, "B")
    ]
    print('Running initial_disks3:')
    '''
    # Set up the initial board with the custom disks
    game.setup_initial_board(initial_disks)

    # Print the initial board configuration
    print("Initial board setup:")
    game.print_board()

    # Start the game
    game.play_game()

# Example of running the main function
if __name__ == "__main__":
    main()



