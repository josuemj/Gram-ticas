import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model.cfg import CFG

terminals = {
        'he', 'she', 'cooks', 'drinks', 'eats', 'cuts', 
        'in', 'with', 'cat', 'dog', 'beer', 'cake', 'juice', 
        'meat', 'soup', 'fork', 'knife', 'oven', 'spoon', 
        'a', 'the'
    }
non_terminals = {'S', 'VP', 'NP', 'PP', 'V', 'P', 'N', 'Det'}
start_symbol = 'S'

cfg = CFG(terminals, non_terminals, start_symbol)

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

cfg.display()