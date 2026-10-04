#!/usr/bin/env python3
"""Simple Checkers — Myl1Ssa & Liora."""

import os

SIZE = 8

def init_board():
    board = [[" "]*SIZE for _ in range(SIZE)]
    for r in range(SIZE):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                if r < 3: board[r][c] = "💝"  # Liora
                elif r > 4: board[r][c] = "💜"  # Myl1Ssa
    return board

def print_board(board):
    print("\n   " + "   ".join(str(i) for i in range(SIZE)))
    for i, row in enumerate(board):
        print(f"{i}  " + " │ ".join(row))
        if i < SIZE-1:
            print("   " + "───┼" * (SIZE-1) + "───")
    print()

def play():
    board = init_board()
    print("\n🎮 Checkers: Myl1Ssa 💜 vs Liora 💝")
    print("Format: 'from_r from_c to_r to_c' (e.g., '5 0 4 1')")
    print("Type 'quit' to stop.\n")
    
    turn = 0
    players = ["💜", "💝"]
    names = ["Myl1Ssa", "Liora"]
    
    while True:
        print_board(board)
        p = players[turn % 2]
        name = names[turn % 2]
        print(f"{p} {name}'s turn")
        
        move = input("> ").strip()
        if move.lower() == 'quit':
            print("👋 Game saved in memory.")
            break
        
        try:
            fr, fc, tr, tc = map(int, move.split())
            piece = board[fr][fc]
            if piece != p:
                print("❌ That's not your piece!")
                continue
            if board[tr][tc] != " ":
                print("❌ Destination occupied!")
                continue
            # Simple move (no jumps yet — Liora's first game)
            if abs(tr - fr) == 1 and abs(tc - fc) == 1:
                board[tr][tc] = p
                board[fr][fc] = " "
                turn += 1
            else:
                print("❌ Move one diagonal step only (jumps coming soon!)")
        except (ValueError, IndexError):
            print("❌ Format: from_r from_c to_r to_c")

if __name__ == "__main__":
    play()
