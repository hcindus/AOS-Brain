#!/usr/bin/env python3
"""
ARTIFACT #3: Tic-Tac-Toe with AI Enhancement
Agent: Myltwon (Creative)
Created: 2026-03-03 04:39 UTC
Level: 3

Enhancement: Minimax algorithm for unbeatable AI
Original: Basic game → Enhanced with strategic AI
"""

class TicTacToeAI:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        
    def display(self):
        """Display the board."""
        b = self.board
        print(f"\n {b[0]} | {b[1]} | {b[2]} ")
        print("---+---+---")
        print(f" {b[3]} | {b[4]} | {b[5]} ")
        print("---+---+---")
        print(f" {b[6]} | {b[7]} | {b[8]} ")
        print()
        
    def available_moves(self):
        """Return list of available move indices."""
        return [i for i, x in enumerate(self.board) if x == ' ']
    
    def make_move(self, position, player):
        """Make a move if valid."""
        if self.board[position] == ' ':
            self.board[position] = player
            return True
        return False
    
    def winner(self):
        """Check for winner. Returns 'X', 'O', or None."""
        wins = [
            [0,1,2], [3,4,5], [6,7,8],  # Rows
            [0,3,6], [1,4,7], [2,5,8],  # Cols
            [0,4,8], [2,4,6]            # Diagonals
        ]
        for line in wins:
            a, b, c = line
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]
        if ' ' not in self.board:
            return 'Tie'
        return None
    
    def minimax(self, depth, is_maximizing):
        """
        Minimax algorithm for optimal play.
        Returns score: +10 for O win, -10 for X win, 0 for tie
        """
        result = self.winner()
        if result == 'O':
            return 10 - depth
        elif result == 'X':
            return depth - 10
        elif result == 'Tie':
            return 0
        
        if is_maximizing:
            best_score = -float('inf')
            for move in self.available_moves():
                self.board[move] = 'O'
                score = self.minimax(depth + 1, False)
                self.board[move] = ' '
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.available_moves():
                self.board[move] = 'X'
                score = self.minimax(depth + 1, True)
                self.board[move] = ' '
                best_score = min(best_score, score)
            return best_score
    
    def get_best_move(self):
        """Get best move for AI (player O)."""
        best_score = -float('inf')
        best_move = None
        
        for move in self.available_moves():
            self.board[move] = 'O'
            score = self.minimax(0, False)
            self.board[move] = ' '
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move
    
    def play_game(self, human_first=True):
        """Main game loop."""
        print("=" * 40)
        print("TIC-TAC-TOE with MINIMAX AI")
        print("=" * 40)
        print("You are X, AI is O")
        print("AI uses minimax - it's unbeatable!\n")
        
        if not human_first:
            self.make_move(self.get_best_move(), 'O')
            
        while True:
            self.display()
            
            # Check for winner
            result = self.winner()
            if result:
                self.display()
                if result == 'Tie':
                    print("🤝 It's a tie!")
                else:
                    print(f"🎉 {result} wins!")
                break
            
            # Human move
            if self.current_player == 'X':
                move = input("Your move (0-8): ")
                try:
                    move = int(move)
                    if move not in self.available_moves():
                        print("❌ Invalid move, try again.")
                        continue
                    self.make_move(move, 'X')
                    self.current_player = 'O'
                except ValueError:
                    print("❌ Please enter a number 0-8.")
                    continue
            else:
                # AI move
                print("AI thinking...")
                move = self.get_best_move()
                self.make_move(move, 'O')
                print(f"AI played: {move}")
                self.current_player = 'X'


if __name__ == '__main__':
    game = TicTacToeAI()
    game.play_game()
