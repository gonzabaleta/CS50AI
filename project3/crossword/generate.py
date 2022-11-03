import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Check that each domain is consistent with the variable's length
        for var in self.domains:
            possible_words = set()
            for word in self.domains[var]:
                # For each word in each var's domain, check that it's the same length as the variable requires
                if len(word) == var.length:
                    possible_words.add(word)
            # Update the domain so that only valid words remain
            self.domains[var] = possible_words

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Initialize variables
        overlap = self.crossword.overlaps[x, y]
        revised = False

        # If the two words don't overlap, skip to the next word
        if not overlap:
            return revised

        # Copy the domain of x
        possible_x = self.domains[x].copy()

        # For each word in x domain
        for x_word in self.domains[x]:
            # Initialize empty set of possible values in y domain that are consistent with overlap
            possible_y = set()

            # For each word in Y domain
            for y_word in self.domains[y]:
                # If the overlap is consistent and they aren't the same words, add y_word to the set
                if x_word[overlap[0]] == y_word[overlap[1]] and x_word != y_word:
                    possible_y.add(y_word)

            # If no possible values in Y for x, remove x from domain
            if not len(possible_y):
                possible_x.remove(x_word)
                revised = True

        self.domains[x] = possible_x
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # If no arcs privided, the arcs is the list of all the possible combination of variables
        if not arcs:
            arcs = list(self.crossword.overlaps.keys())
        queue = arcs

        # While the queue of arcs is not empty
        while len(queue) != 0:
            # Pick one arc
            x, y = queue.pop()
            # If the arc is revised (some values are removed from the domain of X) update the neighbors of X
            if self.revise(x, y):
                # If the domain of X is empty, then no solution
                if len(self.domains[x]) == 0:
                    return False
                else:
                    # Append to the queue all the neighbors of X
                    for neighbor in self.crossword.neighbors(x):
                        if neighbor == y:
                            continue
                        queue.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for v in self.crossword.variables:
            if v not in assignment.keys():
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for x in assignment:
            # Check that the word is of the correct length
            if x.length != len(assignment[x]):
                return False

            for y in assignment:
                if x == y:
                    continue
                # Check that the word is not repeated
                if assignment[x] == assignment[y]:
                    return False

                # Check that there are no conflicts between neighboring variables
                overlap = self.crossword.overlaps[x, y]
                if overlap:
                    if assignment[x][overlap[0]] != assignment[y][overlap[1]]:
                        return False

            # If all good, return true
            return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Dictionary of possible values
        # key: the value
        # value: the number of elements in the domain that this value rules out
        values = {}
        # Get all neighbors that haven't been assignmed yet
        neighbors = self.crossword.neighbors(var) - assignment.keys()

        for value in self.domains[var]:
            values[value] = 0
            for neighbor in neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                # Check all valus of the neighbor, and check if the value is consistent with the current value of var
                for value2 in self.domains[neighbor]:
                    if value[overlap[0]] != value2[overlap[1]]:
                        values[value] += 1

        # Sort the list of values
        values_list = [(key, value)
                       for key, value in values.items()]
        values_list.sort(key=lambda a: a[1])
        values_sorted_list = list()
        for val in values_list:
            values_sorted_list.append(val[0])

        return values_sorted_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # vars:
        # - key: a Variable
        # - value: the size of it's domain
        vars = dict()
        for v in self.crossword.variables:
            if v not in assignment.keys():
                vars[v] = len(self.domains[v])

        # get the lowest domain of all variables
        lowest_domain = min(vars.values())

        # Create a list of all the variables that have the lowest domain
        best_vars = list()
        for var in vars:
            if vars[var] == lowest_domain:
                best_vars.append(var)

        # If there's just one of those variables, then return that variable
        if len(best_vars) == 1:
            return best_vars[0]

        # Get the variable with the least amount of neighbors
        # neighbor_amount:
        # key: a Variable
        # value: the amount of neighbors of the variable
        neighbor_amount = {}
        for var in best_vars:
            amount_of_neighbors = len(self.crossword.neighbors(var))
            neighbor_amount[var] = amount_of_neighbors

        # Get the lowest number of neighbors of all variables
        lowest_neighbors = min(neighbor_amount.values())

        # Return the first variable with that amount of neighbors
        for var in neighbor_amount:
            if neighbor_amount[var] == lowest_neighbors:
                return var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If the assignment is complete, then return the assignment
        if self.assignment_complete(assignment):
            return assignment

        # Select best unassigned variable
        var = self.select_unassigned_variable(assignment)

        # Iterate over the ordered list of domain values
        for v in self.order_domain_values(var, assignment):
            # Create a copy of the assignment so we can test if it's consistent with the new assignment
            assignment_test = assignment.copy()
            assignment_test[var] = v

            # If consistent, then add the new assignment to the assignment and backtrack the result
            if self.consistent(assignment_test):
                assignment[var] = v
                result = self.backtrack(assignment)
                if result:
                    return result
                else:
                    assignment.pop(var)

        # If no more possibilities, then no solution
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
