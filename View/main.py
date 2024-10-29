import sys
import os
from copy import deepcopy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model.cfg import CFG
from Model.cnf import CNF
# from Model.cyk import cyk_algorithm

#Buiding CNF properties
terminals = {
    'he', 'she', 'cooks', 'drinks', 'eats', 'cuts',
    'in', 'with', 'cat', 'dog', 'beer', 'cake', 'juice',
    'meat', 'soup', 'fork', 'knife', 'oven', 'spoon',
    'a', 'the'
}
non_terminals = {'S', 'VP', 'NP', 'PP', 'V', 'P', 'N', 'Det'}
start_symbol = 'S'

# Build the CFG
cfg = CFG(terminals, non_terminals, start_symbol)

# Add the CFG rules
cfg.add_rule('S', ['NP', 'VP'])
cfg.add_rule('VP', ['VP', 'PP'])
cfg.add_rule('VP', ['V', 'NP'])
cfg.add_rule('VP', ['V'])
cfg.add_rule('NP', ['Det', 'N'])
cfg.add_rule('NP', ['he'])
cfg.add_rule('NP', ['she'])
cfg.add_rule('PP', ['P', 'NP'])
cfg.add_rule('V', ['cooks'])
cfg.add_rule('V', ['drinks'])
cfg.add_rule('V', ['eats'])
cfg.add_rule('V', ['cuts'])
cfg.add_rule('P', ['in'])
cfg.add_rule('P', ['with'])
cfg.add_rule('N', ['cat'])
cfg.add_rule('N', ['dog'])
cfg.add_rule('N', ['beer'])
cfg.add_rule('N', ['cake'])
cfg.add_rule('N', ['juice'])
cfg.add_rule('N', ['meat'])
cfg.add_rule('N', ['soup'])
cfg.add_rule('N', ['fork'])
cfg.add_rule('N', ['knife'])
cfg.add_rule('N', ['oven'])
cfg.add_rule('N', ['spoon'])
cfg.add_rule('Det', ['a'])
cfg.add_rule('Det', ['the'])

# Display the CFG
cfg.display()

# Create a CNF instance and copy the rules from the CFG
cnf = CNF(terminals, non_terminals, start_symbol)
cnf.rules = deepcopy(cfg.rules)

# Convert the CFG to CNF
cnf.to_cnf()

# Display the CNF grammar
print("\nGrammar in Chomsky Normal Form:")
cnf.display()

# Implement the CYK algorithm and parse sentences
sentences = [
    'he eats the cake',
    'she drinks a juice',
    'the dog eats a cake with a spoon',
    'he cuts the meat in the oven with a fork',
    'she cooks a soup with the knife',
    'he eats the cake in the oven with the spoon',
    'he eats the cake with the cake',  # Syntactically valid but semantically odd
    'she with eats', 
    'she eats a cake with a fork', #accepted
    'the fork eats the dog', #accepted
    'the cat the dog', #rejected
    'eats quicky she' #rejected
]

for sentence in sentences:
    print(f"\nParsing sentence: '{sentence}'")
    parse_trees = cnf.cyk_parse_with_tree(sentence)
    if parse_trees:
        print(f"The sentence '{sentence}' is accepted by the grammar.\n")
        print("Parse Trees:")
        cnf.print_parse_trees(parse_trees)
    else:
        print(f"The sentence '{sentence}' is rejected by the grammar.")