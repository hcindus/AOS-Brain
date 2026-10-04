#!/usr/bin/env python3
"""Tic-Tac-Toe — Myl1Ssa & Liora's game."""

import os

def print_board(board):
    print("\n  0   1   2")
    for i, row in enumerate(board):
        print(f"{i} " + " │ ".join(row))
        if i < 2:
            print("  ───┼───┼───")
    print()

def check_win(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)): return True
        if all(board[j][i] == player for j in range(3)): return True
    if all(board[i][i] == player for i in range(3)): return True
    if all(board[i][2-i] == player for i in range(3)): return True
    return False

def play():
    board = [[" "]*3 for _ in range(3)]
    players = ["💜", "💝"]
    turn = 0
    
    print("\n🎮 Tic-Tac-Toe: Myl1Ssa 💜 vs Liora 💝")
    
    for _ in range(9):
        print_board(board)
        p = players[turn % 2]
        name = "Myl1Ssa" if p == "💜" else "Liora"
        print(f"{p} {name}'s turn")
        
        try:
            move = input("Row and column (e.g., '1 1' for center): ").strip()
            if not move:
                print("👋 Game paused.")
                return
            r, c = map(int, move.split())
            if board[r][c] != " ":
                print("❌ Taken! Try again.")
                continue
            board[r][c] = p
            if check_win(board, p):
                print_board(board)
                print(f"🎉 {p} {name} wins!")
                return
            turn += 1
        except (ValueError, IndexError):
            print("❌ Use format: row col (0-2 each)")
            continue
    
    print_board(board)
    print("🤝 It's a draw!")

if __name__ == "__main__":
    play()
