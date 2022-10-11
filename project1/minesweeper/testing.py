from minesweeper import Minesweeper, MinesweeperAI, Sentence

initial_cells = set()
initial_cells.add({"is_mine": False, "is_safe": False}, {"is_mine": True, "is_safe": False})

sentence = Sentence()