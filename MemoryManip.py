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

Prvi pokemon:
D173 - Move 1
D174 - Move 2
D175 - Move 3
D176 - Move 4




Pokemon1
D188 - PP Move 1
D189 - PP Move 2
D18A - PP Move 3
D18B - PP Move 4

CCDC - Player selected move


Meniji (value) iz menu_option(pb):
Fight - 193
PkMn - 199
Item - 233
Run - 239

Prvi napad - 169
Drgi napad - 189
Treci napad - 209
Cetvrti napad - 229
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

def menu_option(pb):
    """

    """
    return f"{pb.get_memory_value(0xCC30)}"

def use_move(pb, move_pool=None):
    return f"{pb.get_memory_value(0xD173)}"


def selected_move_power(pb):
    """

    """
    pokemon_types = [pb.get_memory_value(0xD019),pb.get_memory_value(0xD01A)]
    move_type = pb.get_memory_value(0xCFD5) ## 0 is normal btw
    move_power = pb.get_memory_value(0xCFD4)
    if move_type in pokemon_types:
        return move_power*1.5
    return move_power

def goal(pb):
    return pb.get_memory_value(0xD755) == 196 # mora biti 196 za pobjedu
    ...
    
def pos(pb):
    
    ...
    
def seen_pokes(pb):
    return [bin(pb.get_memory_value(i)).count('1') for i in range(0xD30A, 0xD31D)]

def n_pokemon(pb):
    return pb.get_memory_value(0xD163)

def get_money(pb):
    money_byte1 = pb.get_memory_value(0xD347)
    money_byte2 = pb.get_memory_value(0xD348)
    money_byte3 = pb.get_memory_value(0xD349)

    # Ukupna vrijednost novca
    full_money = int(f"{money_byte1 >> 4}{money_byte1 & 0xF}{money_byte2>>4}{money_byte2 & 0xF}{money_byte3>>4}{money_byte3 & 0xF}") ## THANKS GAMEFREAK
    ## https://www.youtube.com/watch?v=RhT2M35tQlc Same energy
    return full_money
    

def total_items(pb):
    return pb.get_memory_value(0xD31D)

def get_badges(pb):
    return pb.get_memory_value(0xD356)



    """
    D35E = Current Map Number

    D361 - 1 byte integer = Current Player Y-Position
    D362 - 1 byte integer = Current Player X-Position
    D363 = Current Player Y-Position (Current Block)
    D364 = Current Player X-Position (Current Block)
    """

def get_x_y(pb):
    place = pb.get_memory_value(0xD35E)
    x = pb.get_memory_value(0xD361)
    y = pb.get_memory_value(0xD362)
    
    return place, x, y