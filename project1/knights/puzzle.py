from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

knowledgeBase  = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    knowledgeBase,
    Biconditional(AKnight, And(AKnight, AKnave)), # If the sentence is true, then A is a Knight
    Biconditional(AKnave, Not(And(AKnight, AKnave))), # If the sentence is false, then A is a Knave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    knowledgeBase,
    Biconditional(AKnight, And(AKnave, BKnave)), # If the sentence is true, then A is a Knight
    Biconditional(AKnave, Not(And(AKnave, BKnave))), # If the sentence is false, then A is a Knave
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    knowledgeBase,
    Implication(AKnight, BKnight), # If A is a knight, then B MUST be a Knight
    Implication(AKnave, BKnight), # If A is a Knave, then B MUST be a Knight because A is lying
    Implication(BKnight, AKnave), # If B is a knight, then A MUST be a knave
    Implication(BKnave, AKnave) # If B is a Knave, then A MUST be a knave
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    knowledgeBase,
    Implication(And(BKnight, AKnight), AKnave), # If what B says is true, and A is a Knight, then A is a Knave
    Implication(And(BKnight, AKnave), AKnight),  # If what B says is true and A is a Knave, then A is a Knight
    # Since what B says is a contradiction, B must be a knave
    Biconditional(BKnight, CKnave), # If B is a knight, then C a knave
    Biconditional(BKnave, CKnight), # If B is a knave, then C a knight
    Biconditional(CKnight, AKnight), # If C is a knight, then B a knave
    Biconditional(CKnave, AKnave), # if C is a knave, then B a knight

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
