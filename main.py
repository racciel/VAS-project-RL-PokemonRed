import random
from pyboy import PyBoy
from PokemonRedAgent import PokemonAgent
from MemoryManip import *

from colorama import Fore

with PyBoy('./PokemonRed.gb') as pyb: 
    base_tick_speed = 40
    rest = base_tick_speed
    agent = PokemonAgent() 
    btns = [0,1]   ## NULA GASI EMULATOR!!!! ZAPAMTI!
    while not pyb.tick():
        num_pokemon = pyb.get_memory_value(0xD163)
        num_attacks = num_moves(pyb)
        agent.set_num_pokemon(num_pokemon)
        agent.set_num_attacks(num_attacks)
        mode = pyb.get_memory_value(0xD057) # overworld = 0, in battle = anything else
        print(Fore.GREEN + f"Suma levela pokemona u party-ju: {party_lvl(pyb)}")
        
        print(f"Broj pokemona: {agent.num_pokemon}")
        print(f"Broj napada: {agent.num_attacks}")
        print(Fore.BLUE + f"Input(s): {pyb.get_input()}")
        
        if mode > 0:
            agent.set_battle_actions()
            print(Fore.GREEN + "Moguće akcije u borbi:", agent.get_actions())
        else:
            agent.set_overworld_actions()
            print(Fore.GREEN + "Moguće akcije u overworldu:", agent.get_actions()) 
        #print(Fore.YELLOW + str(rest))
        rest-=1
        if rest == 0:
            
            r = random.choice(list(agent.current_actions))
            #print(Fore.MAGENTA + f"{agent.current_actions[r]}")
            btns = agent.current_actions[r]
            agent.step(pyb, btns[0])
            
            rest = base_tick_speed
        elif rest == base_tick_speed/2:
            
            agent.step(pyb, btns[1])
                    
    
pyb.stop()