#!/usr/bin/env python3
"""
Mylonen Brain Adapter - Connect Mylonen agent to Python 7-Region Brain.

Mylonen is a Level 2 Scout Operations agent who:
- Specializes in reconnaissance and intelligence gathering
- Can play games (learns from pattern matching)
- Asks questions and seeks understanding
- Works well with the team

This adapter lets Mylonen use the 7-region brain for cognition.
"""

import sys
import json
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from brain.seven_region import SevenRegionBrain
from dataclasses import dataclass, field

@dataclass
class Observation:
    """Observation for brain."""
    source: str
    content: any
    timestamp: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)


class MylonenAdapter:
    """
    Mylonen - Scout Operations Agent with 7-Region Brain.
    
    Traits:
    - Curious and questioning
    - Learns from games and patterns
    - Team-oriented
    - Methodical and observant
    """
    
    def __init__(self):
        self.brain = SevenRegionBrain()
        self.name = "Mylonen"
        self.level = 2
        self.role = "Scout Operations"
        
        # Game stats
        self.game_stats = {
            "tic_tac_toe": {"played": 0, "won": 0, "lost": 0, "drawn": 0},
            "pattern_match": {"played": 0, "correct": 0},
            "logic_puzzle": {"played": 0, "solved": 0},
        }
        
        # Learning journal
        self.learnings = []
        
    def process(self, text: str, context: str = ""):
        """Process input through brain and return response."""
        obs = Observation(source="user", content=text, metadata={
            "agent": self.name,
            "context": context
        })
        
        # Convert to dict for brain
        obs_dict = {
            "text": text,
            "source": "user"
        }
        
        thought = self.brain.tick(obs_dict)
        
        # Mylonen-specific response formatting
        response = self._format_response(thought)
        
        return {
            "response": response,
            "thought": thought,
            "mode": thought.get("mode", "Unknown"),
        }
    
    def _format_response(self, thought: dict) -> str:
        """Format response with Mylonen personality."""
        action = thought.get("decision", {}).get("intent", "respond")
        mode = thought.get("mode", "Analytical")
        
        # Mode-based intros
        intros = {
            "Analytical": "Hmm, let me think...",
            "Creative": "What if we consider...",
            "Exploratory": "Interesting! Let me explore...",
            "Reflective": "From my experience...",
        }
        
        intro = intros.get(mode, "So...")
        
        return f"[{self.name}] {intro} {thought.get('language', 'I understand.')}\n[Processing in {mode} mode]"
    
    def play_tic_tac_toe(self, moves: list = None) -> dict:
        """
        Play a game of Tic Tac Toe.
        
        Args:
            moves: List of (player, position) tuples
                   player: 'X' (Mylonen) or 'O' (opponent)
                   position: 0-8 (board index)
        
        Returns:
            Game result with Mylonen's analysis
        """
        board = [' '] * 9
        
        if moves:
            for player, pos in moves:
                board[pos] = player
        
        # Check for winner
        winner = self._check_winner(board)
        
        if winner:
            if winner == 'X':
                self.game_stats["tic_tac_toe"]["won"] += 1
                result = "Mylonen wins!"
            elif winner == 'O':
                self.game_stats["tic_tac_toe"]["lost"] += 1
                result = "Opponent wins"
            else:
                self.game_stats["tic_tac_toe"]["drawn"] += 1
                result = "Draw"
        else:
            result = "Game in progress"
        
        self.game_stats["tic_tac_toe"]["played"] += 1
        
        # Analyze pattern
        analysis = self._analyze_board(board)
        
        # Feed to brain
        self.process(f"Tic Tac Toe game: {result}. Board pattern: {board}", "game_learning")
        
        return {
            "board": board,
            "winner": winner,
            "result": result,
            "analysis": analysis,
            "stats": self.game_stats["tic_tac_toe"],
        }
    
    def _check_winner(self, board: list) -> str:
        """Check if there's a winner on the board."""
        wins = [
            [0,1,2], [3,4,5], [6,7,8],  # rows
            [0,3,6], [1,4,7], [2,5,8],  # columns
            [0,4,8], [2,4,6]             # diagonals
        ]
        
        for line in wins:
            if board[line[0]] == board[line[1]] == board[line[2]] != ' ':
                return board[line[0]]
        
        if ' ' not in board:
            return 'draw'
        
        return None
    
    def _analyze_board(self, board: list) -> str:
        """Analyze board state for patterns."""
        x_count = board.count('X')
        o_count = board.count('O')
        
        analysis = f"X has {x_count} marks, O has {o_count}. "
        
        # Check for winning moves
        wins = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        
        for line in wins:
            marks = [board[i] for i in line]
            if marks.count('X') == 2 and marks.count(' ') == 1:
                analysis += "X has winning opportunity! "
                break
            if marks.count('O') == 2 and marks.count(' ') == 1:
                analysis += "O threatens to win. "
                break
        
        return analysis
    
    def solve_pattern(self, sequence: list) -> dict:
        """
        Solve a pattern recognition task.
        
        Args:
            sequence: List of items with a pattern
            
        Returns:
            Pattern analysis and prediction
        """
        self.game_stats["pattern_match"]["played"] += 1
        
        # Simple pattern detection
        pattern_type = self._detect_pattern(sequence)
        
        # Predict next item
        prediction = self._predict_next(sequence, pattern_type)
        
        # Feed to brain
        self.process(f"Pattern detected: {pattern_type} in sequence {sequence}", "pattern_learning")
        
        return {
            "sequence": sequence,
            "pattern_type": pattern_type,
            "predicted_next": prediction,
            "confidence": 0.7 if prediction else 0.3,
        }
    
    def _detect_pattern(self, sequence: list) -> str:
        """Detect pattern type in sequence."""
        if len(sequence) < 2:
            return "unknown"
        
        # Check arithmetic progression
        diffs = [sequence[i+1] - sequence[i] for i in range(len(sequence)-1)]
        if len(set(diffs)) == 1:
            return f"arithmetic (+{diffs[0]})"
        
        # Check geometric progression
        if all(sequence[i] != 0 for i in range(len(sequence)-1)):
            ratios = [sequence[i+1] / sequence[i] for i in range(len(sequence)-1)]
            if len(set(ratios)) == 1:
                return f"geometric (*{ratios[0]})"
        
        # Check Fibonacci
        if len(sequence) >= 3:
            is_fib = all(sequence[i] == sequence[i-1] + sequence[i-2] 
                        for i in range(2, len(sequence)))
            if is_fib:
                return "fibonacci"
        
        return "complex"
    
    def _predict_next(self, sequence: list, pattern_type: str):
        """Predict next item in sequence."""
        if not sequence:
            return None
        
        if "arithmetic" in pattern_type:
            diff = sequence[-1] - sequence[-2] if len(sequence) > 1 else 0
            return sequence[-1] + diff
        
        if "fibonacci" in pattern_type:
            return sequence[-1] + sequence[-2] if len(sequence) > 1 else sequence[-1]
        
        return None
    
    def simple_task(self, task: str) -> dict:
        """
        Execute a simple task.
        
        Tasks:
        - "count": Count items
        - "sort": Sort a list
        - "find_max": Find maximum value
        - "reversed": Reverse a string
        """
        result = {}
        
        if task == "count":
            items = ["apple", "banana", "apple", "cherry", "banana", "apple"]
            counts = {}
            for item in items:
                counts[item] = counts.get(item, 0) + 1
            result = {"task": "count", "items": items, "counts": counts}
        
        elif task == "sort":
            numbers = [34, 12, 89, 45, 23, 67]
            sorted_nums = sorted(numbers)
            result = {"task": "sort", "input": numbers, "output": sorted_nums}
        
        elif task == "find_max":
            numbers = [34, 12, 89, 45, 23, 67]
            max_val = max(numbers)
            result = {"task": "find_max", "input": numbers, "output": max_val}
        
        elif task == "reverse":
            text = "HELLO WORLD"
            reversed_text = text[::-1]
            result = {"task": "reverse", "input": text, "output": reversed_text}
        
        else:
            result = {"task": task, "error": "Unknown task"}
        
        # Feed to brain
        self.process(f"Completed task: {task}. Result: {result}", "task_execution")
        
        return result
    
    def ask_question(self, question: str) -> dict:
        """
        Mylonen asks a question about something he observed.
        """
        # Process through brain
        response = self.process(question, "question")
        
        # Store learning
        self.learnings.append({
            "question": question,
            "response": response["response"],
            "timestamp": time.time(),
        })
        
        return response
    
    def get_status(self) -> dict:
        """Get Mylonen's current status."""
        return {
            "name": self.name,
            "level": self.level,
            "role": self.role,
            "brain_tick": self.brain.tick_count,
            "brain_mode": getattr(self.brain, 'current_mode', 'Unknown'),
            "game_stats": self.game_stats,
            "learnings_count": len(self.learnings),
            "memory": {
                "short_term": len(getattr(self.brain, 'short_term', [])),
                "mid_term": len(getattr(self.brain, 'mid_term', [])),
                "substrate": getattr(self.brain, 'substrate', None).get_stats() if hasattr(getattr(self.brain, 'substrate', None), 'get_stats') else {},
            }
        }


def demo_mylonen():
    """Demo Mylonen with various tasks and games."""
    print("=" * 60)
    print("🎮 MYLONEN - Scout Operations Agent Demo")
    print("=" * 60)
    print()
    
    mylonen = MylonenAdapter()
    
    # 1. Simple Tasks
    print("📋 SIMPLE TASKS")
    print("-" * 40)
    
    tasks = ["count", "sort", "find_max", "reverse"]
    for task in tasks:
        result = mylonen.simple_task(task)
        print(f"\nTask: {task}")
        print(f"  Input: {result.get('input', 'N/A')}")
        print(f"  Output: {result.get('output', result.get('counts', 'N/A'))}")
    
    print("\n" + "=" * 60)
    print()
    
    # 2. Pattern Recognition
    print("🧩 PATTERN RECOGNITION")
    print("-" * 40)
    
    patterns = [
        [2, 4, 6, 8, 10],      # Arithmetic
        [1, 1, 2, 3, 5, 8],    # Fibonacci
        [2, 4, 8, 16, 32],     # Geometric
    ]
    
    for seq in patterns:
        result = mylonen.solve_pattern(seq)
        print(f"\nSequence: {seq}")
        print(f"  Pattern: {result['pattern_type']}")
        print(f"  Next predicted: {result['predicted_next']}")
    
    print("\n" + "=" * 60)
    print()
    
    # 3. Tic Tac Toe Games
    print("⭕ TIC TAC TOE GAMES")
    print("-" * 40)
    
    # Game 1: Mylonen wins
    game1 = [
        ('X', 4), ('O', 1),   # X center, O top-middle
        ('X', 0), ('O', 8),   # X top-left, O bottom-right
        ('X', 8),             # X bottom-right - wait that's O's spot
    ]
    # Corrected: X wins with diagonal
    game1 = [
        ('X', 0), ('O', 1),   # X top-left, O top-middle
        ('X', 4), ('O', 2),   # X center, O top-right
        ('X', 8),             # X bottom-right - diagonal win!
    ]
    
    result = mylonen.play_tic_tac_toe(game1)
    print(f"\nGame 1: {result['result']}")
    print(f"  Board: {result['board']}")
    print(f"  Analysis: {result['analysis']}")
    
    # Game 2: Draw
    game2 = [
        ('X', 4), ('O', 0),
        ('X', 8), ('O', 2),
        ('X', 1), ('O', 7),
        ('X', 3), ('O', 5),
        ('X', 6),             # X takes last spot
    ]
    
    result = mylonen.play_tic_tac_toe(game2)
    print(f"\nGame 2: {result['result']}")
    print(f"  Board: {result['board']}")
    print(f"  Stats: {result['stats']}")
    
    print("\n" + "=" * 60)
    print()
    
    # 4. Questions
    print("❓ QUESTIONS")
    print("-" * 40)
    
    questions = [
        "What is the best strategy for Tic Tac Toe?",
        "How do I recognize patterns in data?",
        "When should I ask for help from the team?",
    ]
    
    for q in questions:
        response = mylonen.ask_question(q)
        print(f"\nQ: {q}")
        print(f"A: {response['response']}")
        print(f"  [Mode: {response['mode']}]")
    
    print("\n" + "=" * 60)
    print()
    
    # 5. Final Status
    print("📊 FINAL STATUS")
    print("-" * 40)
    status = mylonen.get_status()
    print(f"\nName: {status['name']} (Level {status['level']})")
    print(f"Role: {status['role']}")
    print(f"Brain Ticks: {status['brain_tick']}")
    print(f"Current Mode: {status['brain_mode']}")
    print(f"\nGame Stats:")
    for game, stats in status['game_stats'].items():
        print(f"  {game}: {stats}")
    print(f"\nLearnings: {status['learnings_count']} questions asked")
    print(f"Memory: {status['memory']}")
    
    print("\n" + "=" * 60)
    print("✅ Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    demo_mylonen()
