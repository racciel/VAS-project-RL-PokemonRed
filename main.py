from pyboy import PyBoy
from PokemonRedAgent import PokemonAgent
from MemoryManip import *

with PyBoy('./PokemonRed.gb') as pyboy:   
    while not pyboy.tick():
        agent = PokemonAgent()  
        num_pokemon = pyboy.get_memory_value(0xD163)
        num_attacks = num_moves(pyboy)
        agent.set_num_pokemon(num_pokemon)
        agent.set_num_attacks(num_attacks)
        print(f"Suma levela pokemona u party-ju: {party_lvl(pyboy)}")
        #print(f"Power: {pyboy.get_memory_value(selected_move_power)}")
        #print(f"Number of moves: {num_moves(pyboy)}")
        #print(f"Number of Pokemon: {pyboy.get_memory_value(0xD163)}")
        #print(f"Number of turns in battle: {pyboy.get_memory_value(0xCCD5)}")
        #print(f"Selected move: {pyboy.get_memory_value(0xCCDC)}")
        #print(f"Enemy level: {pyboy.get_memory_value(0xCFF3)}")  ## ovo se ne reseta na 0 nakon borbe
        #print(f"Battle turn: {pyboy.get_memory_value(0xFFF3)}")
        #print(f"Type of battle: {pyboy.get_memory_value(0xD057)}") # OVO RADI!
        
        #print(f"Tileset type: {pyboy.get_memory_value(0xB522)}")
        #print(f"Enemy pokemon intermal ID: {pyboy.get_memory_value(0xCFD8)}")
        
        print(f"Broj pokemona: {agent.num_pokemon}")
        print(f"Broj napada: {agent.num_attacks}")
        
        if pyboy.get_memory_value(0xD057) > 0:
            agent.set_battle_actions()
            print("Moguće akcije u borbi:", agent.get_actions())
        else:
            agent.set_overworld_actions()
            print("Moguće akcije u overworldu:", agent.get_actions())
        
pyboy.stop()