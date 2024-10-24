import sys
import os
from copy import deepcopy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model.cfg import CFG
from Model.cnf import CNF

#Buiding CNF properties
terminals = {
        'he', 'she', 'cooks', 'drinks', 'eats', 'cuts', 
        'in', 'with', 'cat', 'dog', 'beer', 'cake', 'juice', 
        'meat', 'soup', 'fork', 'knife', 'oven', 'spoon', 
        'a', 'the'
    }
non_terminals = {'S', 'VP', 'NP', 'PP', 'V', 'P', 'N', 'Det'}
start_symbol = 'S'

#Building CFG
cfg = CFG(terminals, non_terminals, start_symbol)

#Adding CFG RULES
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

#Displaying CFG
cfg.display()

print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
cnf = CNF(cfg.terminals, cfg.non_terminals, cfg.start_symbol)
cnf.rules = deepcopy(cfg.rules)  # Copy the rules from CFG to CNF
cnf.to_cnf()
cnf.display()
