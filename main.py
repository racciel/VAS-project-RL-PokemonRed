from pyboy import PyBoy
with PyBoy('./PokemonRed.gb') as pyboy:
    while not pyboy.tick():
        pass