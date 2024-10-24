from copy import deepcopy
from .cfg import CFG

class CNF(CFG):
    def __init__(self, terminals, non_terminals, start_symbol):
        super().__init__(terminals, non_terminals, start_symbol)

    def to_cnf(self):
        """
        Convert the CFG to Chomsky Normal Form (CNF).
        :return: A new CNF instance with the transformed rules.
        """
        # Step 1: Remove epsilon-productions
        self._remove_epsilon_productions()

        # Step 2: Remove unit productions
        self._remove_unit_productions()

        # Step 3: Convert to binary productions
        self._convert_to_binary()

        # Step 4: Ensure all terminal rules are in the correct form
        self._ensure_terminal_rules()

        # Return a new CNF object with the updated rules
        return self

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
        while True:
            new_nullable = nullable.copy()
            for nt, productions in deepcopy(self.rules).items():
                for prod in productions:
                    if any(symbol in nullable for symbol in prod):
                        # Add new production by removing nullable symbols
                        new_prod = [s for s in prod if s not in nullable]
                        if new_prod:
                            self.add_rule(nt, new_prod)

            if new_nullable == nullable:
                break

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
                self.rules[nt].extend([prod for prod in self.rules[target]])

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
                    # Create a new non-terminal
                    new_nt = f"X{counter}"
                    counter += 1
                    self.non_terminals.add(new_nt)

                    # Add the new rule
                    new_rules[new_nt] = [[prod[0], prod[1]]]

                    # Update the production
                    prod = [new_nt] + prod[2:]

                new_rules[nt].append(prod)

        self.rules = new_rules

    def _ensure_terminal_rules(self):
        """
        Ensure that all terminal rules are of the form A -> a.
        """
        new_rules = {}
        terminal_map = {}

        for nt, productions in deepcopy(self.rules).items():
            new_rules[nt] = []
            for prod in productions:
                if len(prod) == 2:
                    # If a production has a terminal and a non-terminal, separate the terminal
                    new_prod = []
                    for symbol in prod:
                        if symbol in self.terminals:
                            if symbol not in terminal_map:
                                new_nt = f"T_{symbol}"
                                self.non_terminals.add(new_nt)
                                terminal_map[symbol] = new_nt
                                new_rules[new_nt] = [[symbol]]
                            new_prod.append(terminal_map[symbol])
                        else:
                            new_prod.append(symbol)
                    new_rules[nt].append(new_prod)
                else:
                    new_rules[nt].append(prod)

        self.rules = new_rules
