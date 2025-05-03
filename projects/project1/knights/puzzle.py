from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."

knowledge0 = And(
    Or(AKnight, AKnave),  # A must be either a Knight or a Knave (but not both)
    Not(And(AKnight, AKnave)),  # A cannot be both a Knight and a Knave
    Implication(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),  # A must be either a Knight or a Knave (but not both)
    Not(And(AKnight, AKnave)),  # A cannot be both a Knight and a Knave
    Or(BKnight, BKnave),  # B must be either a Knight or a Knave (but not both)
    Not(And(BKnight, BKnave)),  # B cannot be both a Knight and a Knave
    
    Implication(AKnight, And(AKnave, BKnave)),  # If A is a Knight, A's statement is true: both A and B are Knaves
    Implication(AKnave, Not(And(AKnave, BKnave)))
    # If A is a Knave, A's statement is false: it cannot be true that both are Knaves
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),  # A must be either a Knight or a Knave (but not both)
    Not(And(AKnight, AKnave)),  # A cannot be both a Knight and a Knave
    Or(BKnight, BKnave),  # B must be either a Knight or a Knave (but not both)
    Not(And(BKnight, BKnave)),  # B cannot be both a Knight and a Knave

    # If A is a Knight, A's statement ("We are the same kind") is true: A and B are the same kind.
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),

    # If A is a Knave, A's statement ("We are the same kind") is false: A and B are not the same kind.
    Implication(AKnave, Or(And(AKnight, BKnave), And(AKnave, BKnight))),

    # If B is a Knight, B's statement ("We are of different kinds") is true: A and B are different kinds.
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),

    # If B is a Knave, B's statement ("We are of different kinds") is false: A and B are the same kind.
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),  # A must be either a Knight or a Knave (but not both)
    Not(And(AKnight, AKnave)),  # A cannot be both a Knight and a Knave
    Or(BKnight, BKnave),  # B must be either a Knight or a Knave (but not both)
    Not(And(BKnight, BKnave)),  # B cannot be both a Knight and a Knave
    Or(CKnight, CKnave),  # C must be either a Knight or a Knave (but not both)
    Not(And(CKnight, CKnave)),  # C cannot be both a Knight and a Knave

    # If A is a Knight, A's statement ("I am a Knight" or "I am a Knave") must be true.
    Implication(AKnight, Or(AKnight, AKnave)),

    # If A is a Knave, A's statement ("I am a Knight" or "I am a Knave") must be false.
    Implication(AKnave, Not(Or(AKnight, AKnave))),

    # If B is a Knight, B's statements ("A said 'I am a Knave'" and "C is a Knave") must be true.
    Implication(BKnight, And(
        Implication(AKnight, AKnave),  # If A is a Knight, then A said "I am a Knave".
        CKnave  # B's second statement: C is a Knave.
    )),

    # If B is a Knave, B's statements ("A said 'I am a Knave'" and "C is a Knave") must be false.
    Implication(BKnave, Not(And(
        Implication(AKnight, AKnave),
        CKnave
    ))),

    # If C is a Knight, C's statement ("A is a Knight") must be true.
    Implication(CKnight, AKnight),

    # If C is a Knave, C's statement ("A is a Knight") must be false.
    Implication(CKnave, Not(AKnight))
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
