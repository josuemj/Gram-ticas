from copy import deepcopy
from .cfg import CFG

class CNF(CFG):
    def __init__(self, terminals, non_terminals, start_symbol):
        super().__init__(terminals, non_terminals, start_symbol)

    def to_cnf(self):
        """
        Convert the CFG to Chomsky Normal Form (CNF).
        """
        # Step 1: Remove epsilon-productions
        self._remove_epsilon_productions()

        # Step 2: Remove unit productions
        self._remove_unit_productions()

        # Step 3: Convert to binary productions
        self._convert_to_binary()

        # Step 4: Ensure all terminal rules are in the correct form
        self._ensure_terminal_rules()

    def _remove_epsilon_productions(self):
        """
        Remove epsilon-productions from the CFG.
        """
        nullable = set()

        # Find nullable non-terminals
        for nt in self.rules:
            for prod in self.rules[nt]:
                if prod == ['epsilon']:
                    nullable.add(nt)

        # Remove epsilon-productions and add new productions for nullable symbols
        while nullable:
            nullable = set()
            for nt, productions in deepcopy(self.rules).items():
                for prod in productions:
                    if all(symbol in nullable for symbol in prod):
                        self.rules[nt].append(['epsilon'])
                    if any(symbol in nullable for symbol in prod):
                        new_prod = [s for s in prod if s not in nullable]
                        if new_prod and new_prod not in self.rules[nt]:
                            self.rules[nt].append(new_prod)
                        nullable.update([nt for nt in self.rules if ['epsilon'] in self.rules[nt]])

        # Remove original epsilon-productions
        for nt in self.rules:
            self.rules[nt] = [prod for prod in self.rules[nt] if prod != ['epsilon']]

    def _remove_unit_productions(self):
        """
        Remove unit productions from the CFG.
        """
        while True:
            unit_productions = [
                (nt, prod[0]) for nt in self.rules for prod in self.rules[nt]
                if len(prod) == 1 and prod[0] in self.non_terminals
            ]
            if not unit_productions:
                break

            for nt, target in unit_productions:
                self.rules[nt].remove([target])
                self.rules[nt].extend(
                    [prod for prod in self.rules[target] if prod != [target]]
                )

    def _convert_to_binary(self):
        """
        Convert productions to binary productions if needed.
        """
        new_rules = {}
        counter = 0

        for nt, productions in deepcopy(self.rules).items():
            new_rules[nt] = []
            for prod in productions:
                # If production has more than 2 symbols, convert to binary
                while len(prod) > 2:
                    new_nt = f"X{counter}"
                    counter += 1
                    self.non_terminals.add(new_nt)
                    new_rules[new_nt] = [[prod[0], prod[1]]]
                    prod = [new_nt] + prod[2:]
                new_rules[nt].append(prod)

        self.rules = new_rules

    def _ensure_terminal_rules(self):
        """
        Ensure that all terminal rules are of the form A -> a.
        """
        terminal_map = {}

        for nt, productions in deepcopy(self.rules).items():
            new_prods = []
            for prod in productions:
                if len(prod) == 2:
                    new_prod = []
                    for symbol in prod:
                        if symbol in self.terminals:
                            if symbol not in terminal_map:
                                new_nt = f"T_{symbol}"
                                terminal_map[symbol] = new_nt
                                self.non_terminals.add(new_nt)
                                self.rules[new_nt] = [[symbol]]
                            new_prod.append(terminal_map[symbol])
                        else:
                            new_prod.append(symbol)
                    new_prods.append(new_prod)
                else:
                    new_prods.append(prod)
            self.rules[nt] = new_prods
    
    def cyk_parse(self, sentence):
        """
        Parse a sentence using the CYK algorithm.
        :param sentence: The input sentence as a string.
        :return: True if the sentence can be derived from the grammar, False otherwise.
        """
        words = sentence.strip().split()
        n = len(words)
        if n == 0:
            return False  # Empty string not accepted unless the grammar can derive epsilon

        # Initialize the table
        T = [[set() for _ in range(n)] for _ in range(n)]

        # Fill in the diagonal of the table with productions that generate terminals
        for i in range(n):
            word = words[i]
            for nt in self.rules:
                for prod in self.rules[nt]:
                    if len(prod) == 1 and prod[0] == word:
                        T[i][i].add(nt)

        # Fill the table for substrings of length 2 to n
        for length in range(2, n + 1):  # Length of the span
            for i in range(n - length + 1):  # Start of the span
                j = i + length - 1  # End of the span
                for k in range(i, j):  # Split position
                    for B in T[i][k]:
                        for C in T[k + 1][j]:
                            for nt in self.rules:
                                for prod in self.rules[nt]:
                                    if len(prod) == 2 and prod[0] == B and prod[1] == C:
                                        T[i][j].add(nt)

        # Check if the start symbol is in the top-right cell of the table
        return self.start_symbol in T[0][n - 1]
