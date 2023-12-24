from pyboy import PyBoy

"""
D163 - # Pokémon In Party
D164 - Pokémon 1
D165 - Pokémon 2
D166 - Pokémon 3
D167 - Pokémon 4
D168 - Pokémon 5
D169 - Pokémon 6
D16A - End of list
"""

#           1        2       3       4       5       6      
party_add = [0xD18C, 0xD1B8, 0xD1E4, 0xD210, 0xD23C, 0xD268]
selected_move_power = 0xCFD4
moves = [0xD01C, 0xD01D, 0xD01E, 0xD01F]
my_their_turn = 0xFFF3

    
def party_lvl(pb):
    """
    Returns a sum of party members levels
    """
    s = 0
    for a in party_add:
        s+=pb.get_memory_value(a)
    return s

def use_move(pb):
    """
    Well... The idea was to select a damaging move which has enough PP to be used.
    I wanted to put a heuristic rule for an agent to switch when there is no more
    damaging moves available on an active pokemon.
    """

    power = pb.get_memory_value(selected_move_power)
    #pp = 

def num_moves(pb):
    """
    Returns a number of moves available to the active pokemon in battle (max 4)
    """
    n = 0
    for m in moves:
        if(pb.get_memory_value(m)>0):
            n+=1
    return n