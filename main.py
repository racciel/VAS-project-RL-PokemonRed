import random
from pyboy import PyBoy
from PokemonRedAgent import PokemonAgent
from MemoryManip import *

from colorama import Fore

#base_tick_speed = 20
#rest = base_tick_speed

ash = PokemonAgent()
ash.train(3)