from pyboy import PyBoy

#           1        2       3       4       5       6      
party_add = [0xD18C, 0xD1B8, 0xD1E4, 0xD210, 0xD23C, 0xD268]
selected_move_power = 0xCFD4

def party_lvl():
    s = 0
    for a in party_add:
        s+=pyboy.get_memory_value(a)
    return s

def use_move():
    power = pyboy.get_memory_value(selected_move_power)
    #pp = 


with PyBoy('./PokemonRed.gb') as pyboy:
    while not pyboy.tick():
        value = party_lvl()
        print(f"Suma levela pokemona u party-ju: {value}")
        value = pyboy.get_memory_value(selected_move_power)
        print(f"Power: {value}")

pyboy.stop()