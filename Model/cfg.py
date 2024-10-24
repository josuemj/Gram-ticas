class CFG:
    def __init__(self, terminals, non_terminals, start_symbol):
        """
        Initialize the CFG with terminals, non-terminals, and a start symbol.
        """
        self.terminals = set(terminals)
        self.non_terminals = set(non_terminals)
        self.start_symbol = start_symbol
        self.rules = {}

    def add_rule(self, non_terminal, production):
        """
        Add a production rule to the grammar.
        :param non_terminal: The left side of the production (must be a non-terminal)
        :param production: The right side of the production (can be a list of symbols)
        """
        if non_terminal not in self.non_terminals:
            raise ValueError(f"{non_terminal} is not a non-terminal.")

        if non_terminal not in self.rules:
            self.rules[non_terminal] = []

        self.rules[non_terminal].append(production)

    def display(self):
        """
        Display the grammar in a readable format.
        """
        print("CFG:")
        print("Terminals:", self.terminals)
        print("Non-terminals:", self.non_terminals)
        print("Start Symbol:", self.start_symbol)
        print("Production Rules:")
        for nt, prods in self.rules.items():
            for prod in prods:
                print(f"  {nt} -> {' '.join(prod)}")

    def is_terminal(self, symbol):
        """
        Check if a symbol is a terminal.
        """
        return symbol in self.terminals

    def is_non_terminal(self, symbol):
        """
        Check if a symbol is a non-terminal.
        """
        return symbol in self.non_terminals

    def parse(self, string):
        """
        A simple recursive parsing method to check if a string can be derived from the start symbol.
        This is a brute-force method and not efficient for large strings or grammars.
        :param string: The input string to parse.
        :return: True if the string can be derived from the start symbol, False otherwise.
        """
        return self._derive([self.start_symbol], string.split())

    def _derive(self, symbols, string):
        """
        Recursively derive the string from the current list of symbols.
        :param symbols: The current list of symbols being derived.
        :param string: The target string as a list of symbols.
        :return: True if derivable, False otherwise.
        """
        # If the symbols and string are both empty, it's a match
        if not symbols and not string:
            return True
        
        # If symbols or string is empty, it's not a match
        if not symbols or not string:
            return False
        
        # Get the first symbol in the current derivation
        current_symbol = symbols[0]
        
        # If it's a terminal, it must match the string's first symbol
        if self.is_terminal(current_symbol):
            if current_symbol == string[0]:
                return self._derive(symbols[1:], string[1:])
            else:
                return False
        
        # If it's a non-terminal, try each production rule
        elif self.is_non_terminal(current_symbol):
            if current_symbol in self.rules:
                for production in self.rules[current_symbol]:
                    # Attempt to derive with the current production
                    if self._derive(production + symbols[1:], string):
                        return True
        
        # If no derivation was successful, return False
        return False
