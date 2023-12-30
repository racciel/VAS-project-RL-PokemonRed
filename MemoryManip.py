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
    #return pb.get_memory_value(0xD755) == 196 # Brock's badge
    p, _, _ = get_x_y(pb)
    return p == 1 # Viridian City
    
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

def get_mode(pb):
    return pb.get_memory_value(0xD057)    

def total_items(pb):
    return pb.get_memory_value(0xD31D)

def get_badges(pb):
    return pb.get_memory_value(0xD356)

def num_pokemons(pb):
    return pb.get_memory_value(0xD163)

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

def get_died(pb):
    hps = hp_read(pb)
    dead = True
    for h in hps:
        if h[0] > 0 :
            dead = False    
    return dead

def hp_read(pb):
    hp_values = []
    for i in range(6):
        current_hp_address_high = 0xD16C + (i * 0x2D-1*i if i!=0 else 0)
        current_hp_address_low = 0xD16C + (i * 0x2D-1*i if i!=0 else 0)+0x1
        max_hp_address_high = 0xD18D + (i * 0x2D-1*i if i!=0 else 0)
        max_hp_address_low = 0xD18D + (i * 0x2D-1*i if i!=0 else 0)+0x1
        current_hp_low = pb.get_memory_value(current_hp_address_low)
        current_hp_high = pb.get_memory_value(current_hp_address_high)
        current = int((current_hp_high>>4)+current_hp_low)
        max_hp_low = pb.get_memory_value(max_hp_address_low)
        max_hp_high = pb.get_memory_value(max_hp_address_high)
        max_ = int((max_hp_high>>4)+max_hp_low)
        hp_values.append((current, max_))

    return hp_values

# player_pokemon_id, player_pokemon_level, player_pokemon_hp, enemy_pokemon_id, enemy_pokemon_level, enemy_pokemon_hp, battle_type, current_menu
def get_battle_state(pb):
    p_p_id = pb.get_memory_value(0xCFD9)
    p_p_level = pb.get_memory_value(0xD022)
    
    add_high = 0xD015
    add_low = 0xD016
    
    current_hp_high = pb.get_memory_value(add_high)
    current_hp_low = pb.get_memory_value(add_low)
    p_p_h = int((current_hp_high>>4)+current_hp_low)
    
    add_high = 0xD8C6
    add_low = 0xD8C7
    
    max_hp_high = pb.get_memory_value(add_high)
    max_hp_low = pb.get_memory_value(add_low)
    p_p_max_hp = int((max_hp_high>>4)+max_hp_low)
    
    p_per_hp = p_p_h / p_p_max_hp
    
    e_p_id = pb.get_memory_value(0xCFD8)
    e_p_lvl = pb.get_memory_value(0xCFF3)
    
    add_high = 0xCFE6
    add_low = 0xCFE7
    
    current_hp_high = pb.get_memory_value(add_high)
    current_hp_low = pb.get_memory_value(add_low)
    e_p_h = int((current_hp_high>>4)+current_hp_low)
    
    add_high = 0xCFF4
    add_low = 0xCFF5
    
    max_hp_high = pb.get_memory_value(add_high)
    max_hp_low = pb.get_memory_value(add_low)
    e_p_max_hp = int((max_hp_high>>4)+max_hp_low)
    
    e_per_hp = e_p_h / e_p_max_hp
    
    battle_type = get_mode(pb)
    current_menu = int(menu_option(pb))
    
    number_of_turns = pb.get_memory_value(0xCCD5)
    per_hp = percentage_party_hp(pb)
    
    if p_per_hp >=1/3:
        p_hp_state = 0
    elif p_per_hp >=2/3:
        p_hp_state = 1
    else:
        p_hp_state = 2
        
    if e_per_hp >=1/3:
        e_hp_state = 0
    elif e_per_hp >=2/3:
        e_hp_state = 1
    else:
        e_hp_state = 2
    
    #return (p_p_id, p_p_level, p_p_h, e_p_id, e_p_h, e_p_lvl, per_hp, battle_type, number_of_turns, current_menu)
    #return (p_p_id, p_p_level, p_p_h, e_p_id, e_p_h, e_p_lvl, battle_type, current_menu)
    #return (p_p_id, p_p_h, e_p_id, e_p_h, battle_type, current_menu)
    return (p_hp_state, e_hp_state, battle_type, current_menu)

def percentage_party_hp(pb):
    hps = hp_read(pb)
    s1 = 0
    s2 = 0
    for bar in hps:
        s1+=bar[0]
        s2+=bar[1]
    return s1/s2

def explore_mod(pb):
    d = {0: 0.5,   # Palletown
         12: 1.6,   # Route 1
         1: 2,    # Viridian City
         13: 2.6,  # Route 3 (we skip 2)
         50: 2.8,  # That thing between Viridian city and Viridian forest
         51: 3.4,  # Viridian forest
         47: 3.6,   # That thing between Viridian forest and Route 4
         13: 4,   # Route 4
         2: 5}    # Pewter city
    
    p, _, _ = get_x_y(pb)
    return d[p] if p in d else 0.05
    
    
def pokemon_owned(pb):
    
    ...